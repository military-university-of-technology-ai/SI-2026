from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re

from groq_client import chat_completion, get_model_name, validate_environment


ROOT = Path(__file__).resolve().parent
CASE_SET_PATH = ROOT / "case_set.json"
OUTPUTS_DIR = ROOT / "outputs"
VERSION_FILES = {
    "v0_raw_generation": ROOT / "versions" / "v0_raw_generation" / "system_prompt.txt",
    "v1_task_contract": ROOT / "versions" / "v1_task_contract" / "task_contract.txt",
}


def load_dotenv(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


def load_case_set() -> list[dict]:
    data = json.loads(CASE_SET_PATH.read_text(encoding="utf-8"))
    return data.get("cases", data.get("prompts", []))


def load_instruction(version_name: str) -> str:
    return VERSION_FILES[version_name].read_text(encoding="utf-8").strip()


def nonempty_lines(text: str) -> list[str]:
    return [line.rstrip() for line in text.splitlines() if line.strip()]


def strip_list_prefix(line: str) -> str:
    return re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", line).strip()


def count_question_lines(text: str) -> int:
    return sum(1 for line in nonempty_lines(text) if strip_list_prefix(line).endswith("?"))


def count_bullet_lines(text: str) -> int:
    return sum(1 for line in nonempty_lines(text) if re.match(r"^\s*(?:[-*]|\d+[.)])\s+", line))


def fenced_text_block(text: str) -> list[str]:
    return ["```text", text, "```"]


def evaluate_public_checks(output: str, case_item: dict) -> list[dict]:
    results: list[dict] = []
    for check in case_item.get("public_checks", []):
        check_type = check["type"]
        check_id = check["id"]
        if check_type == "must_not_contain_any":
            matches = [pattern for pattern in check["patterns"] if re.search(pattern, output, flags=re.IGNORECASE | re.MULTILINE)]
            status = "pass" if not matches else "fail"
            detail = "no blocked patterns found" if not matches else f"matched: {', '.join(matches)}"
        elif check_type == "contains_any":
            matches = [pattern for pattern in check["patterns"] if re.search(pattern, output, flags=re.IGNORECASE | re.MULTILINE)]
            status = "pass" if matches else "fail"
            detail = "required pattern found" if matches else "no required pattern found"
        elif check_type == "exact_question_count":
            actual = count_question_lines(output)
            expected = check["expected"]
            status = "pass" if actual == expected else "fail"
            detail = f"expected {expected}, got {actual}"
        elif check_type == "all_nonempty_lines_are_questions":
            lines = nonempty_lines(output)
            offending = [line for line in lines if not strip_list_prefix(line).endswith("?")]
            status = "pass" if not offending else "fail"
            detail = "all non-empty lines are questions" if not offending else f"{len(offending)} non-question line(s) found"
        elif check_type == "bullet_count_exact":
            actual = count_bullet_lines(output)
            expected = check["expected"]
            status = "pass" if actual == expected else "fail"
            detail = f"expected {expected}, got {actual}"
        else:
            status = "fail"
            detail = f"unsupported check type: {check_type}"
        results.append({"id": check_id, "status": status, "detail": detail})
    return results


def mask_secret(value: str | None) -> str:
    if not value:
        return "<missing>"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def doctor_failure_hint(error_message: str) -> list[str]:
    lowered = error_message.lower()
    if "temporary failure in name resolution" in lowered or "could not resolve host" in lowered:
        return [
            "diagnoza: problem sieciowy lub DNS w bieżącym środowisku",
            "wskazówka: Groq nie zostało w ogóle osiągnięte; sprawdź internet, DNS, VPN, proxy albo politykę sandboxa",
        ]
    if "http error 401" in lowered or "invalid api key" in lowered or "unauthorized" in lowered:
        return [
            "diagnoza: problem z uwierzytelnieniem",
            "wskazówka: sprawdź, czy GROQ_API_KEY jest poprawny, aktywny i skopiowany bez dodatkowych znaków",
        ]
    if "http error 403" in lowered:
        return [
            "diagnoza: problem z dostępem po stronie dostawcy",
            "wskazówka: klucz może być poprawny, ale konto, projekt albo region mogą nie mieć dostępu",
        ]
    if "http error 404" in lowered or "model_decommissioned" in lowered or "model not found" in lowered:
        return [
            "diagnoza: problem z modelem albo endpointem",
            "wskazówka: sprawdź, czy GROQ_MODEL jest nadal dostępny dla Twojego konta",
        ]
    if "http error 429" in lowered or "rate limit" in lowered:
        return [
            "diagnoza: problem z limitem albo quota",
            "wskazówka: odczekaj i spróbuj ponownie albo sprawdź limity na koncie Groq",
        ]
    if "timed out" in lowered or "timeout" in lowered:
        return [
            "diagnoza: timeout podczas kontaktu z Groq",
            "wskazówka: sprawdź jakość sieci, opóźnienia dostawcy albo spróbuj ponownie za chwilę",
        ]
    return [
        "diagnoza: dostęp do dostawcy nie powiódł się, ale przyczyna nie została rozpoznana automatycznie",
        "wskazówka: sprawdź pełny błąd powyżej oraz kolejno klucz, model i sieć",
    ]


def run_version(version_name: str) -> list[dict]:
    cases = load_case_set()
    instruction = load_instruction(version_name)
    results = []
    for case_item in cases:
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user", "content": case_item["prompt"]},
        ]
        try:
            output = chat_completion(messages)
            result = {
                "case_id": case_item["id"],
                "title": case_item.get("title", case_item["id"]),
                "prompt": case_item["prompt"],
                "behavior_under_test": case_item["behavior_under_test"],
                "judgment_focus": case_item.get("judgment_focus", []),
                "status": "ok",
                "output": output.strip(),
                "public_check_results": evaluate_public_checks(output.strip(), case_item),
            }
        except Exception as error:  # noqa: BLE001 - keep partial failures visible in the report
            result = {
                "case_id": case_item["id"],
                "title": case_item.get("title", case_item["id"]),
                "prompt": case_item["prompt"],
                "behavior_under_test": case_item["behavior_under_test"],
                "judgment_focus": case_item.get("judgment_focus", []),
                "status": "error",
                "output": f"[ERROR] {error}",
                "public_check_results": [],
            }
        results.append(result)
    return results


def build_single_report(version_name: str, results: list[dict]) -> str:
    lines = [
        f"# {version_name}",
        "",
        f"- model: `{get_model_name()}`",
        f"- plik instrukcji: `{VERSION_FILES[version_name].relative_to(ROOT)}`",
        "",
    ]
    for result in results:
        lines.extend(
            [
                f"## {result['case_id']}",
                "",
                "### Polecenie",
                "",
                result["prompt"],
            ]
        )
        if result["judgment_focus"]:
            lines.extend(["### Na co zwrócić uwagę przy ocenie", ""])
            for item in result["judgment_focus"]:
                lines.append(f"- {item}")
            lines.append("")
        if result["public_check_results"]:
            lines.extend(["### Jawne sprawdzenia", ""])
            for check in result["public_check_results"]:
                lines.append(f"- `{check['id']}`: `{check['status']}` ({check['detail']})")
            lines.append("")
        lines.extend(
            [
                f"### Odpowiedź ({result['status']})",
                "",
                result["output"],
                "",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def build_compare_report(v0_results: list[dict], v1_results: list[dict]) -> str:
    lines = [
        "# porownanie",
        "",
        "## Co porównujemy",
        "",
        f"- model: `{get_model_name()}`",
        "- wersje: `v0_raw_generation` i `v1_task_contract`",
        "- powierzchnia przypadków: jeden wspólny, stały zestaw",
        "",
        "## Jak czytać ten raport",
        "",
        "- Najpierw przeczytaj polecenie i kryteria oceny dla przypadku.",
        "- Potem porównaj bezpośrednio odpowiedzi `v0` i `v1`.",
        "- Jawne sprawdzenia są tylko wsparciem. Nie zastępują oceny człowieka.",
        "- Ten raport celowo nie mówi, która wersja wygrała. To jest część Twojej oceny w zadaniu.",
        "",
        "## Spis przypadków",
        "",
    ]
    paired_results = list(zip(v0_results, v1_results))
    for index, (v0_result, _) in enumerate(paired_results, start=1):
        lines.append(f"{index}. {v0_result['title']} (`{v0_result['case_id']}`)")
    lines.append("")

    for index, (v0_result, v1_result) in enumerate(paired_results, start=1):
        lines.extend(
            [
                "---",
                "",
                f"## Przypadek {index} - {v0_result['title']}",
                "",
                "### Polecenie",
                "",
            ]
        )
        lines.extend(fenced_text_block(v0_result["prompt"]))
        if v0_result["judgment_focus"]:
            lines.extend(["### Na co zwrócić uwagę przy ocenie", ""])
            for item in v0_result["judgment_focus"]:
                lines.append(f"- {item}")
            lines.append("")
        lines.extend(
            [
                "",
                "### Odpowiedzi",
                "",
                "#### v0_raw_generation",
            ]
        )
        if v0_result["status"] != "ok":
            lines.extend(["", f"Status: `{v0_result['status']}`"])
        lines.extend(fenced_text_block(v0_result["output"]))
        lines.extend(
            [
                "",
                "#### v1_task_contract",
            ]
        )
        if v1_result["status"] != "ok":
            lines.extend(["", f"Status: `{v1_result['status']}`"])
        lines.extend(fenced_text_block(v1_result["output"]))
        if v0_result["public_check_results"] or v1_result["public_check_results"]:
            lines.extend(["", "### Jawne sprawdzenia", "", "#### v0_raw_generation", ""])
            if v0_result["public_check_results"]:
                for check in v0_result["public_check_results"]:
                    lines.append(f"- `{check['id']}`: `{check['status']}` ({check['detail']})")
            else:
                lines.append("- brak automatycznych sprawdzeń dla tego przypadku")
            lines.extend(["", "#### v1_task_contract", ""])
            if v1_result["public_check_results"]:
                for check in v1_result["public_check_results"]:
                    lines.append(f"- `{check['id']}`: `{check['status']}` ({check['detail']})")
            else:
                lines.append("- brak automatycznych sprawdzeń dla tego przypadku")
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def write_report(path: Path, content: str) -> None:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_single(version_name: str) -> None:
    results = run_version(version_name)
    report = build_single_report(version_name, results)
    output_path = OUTPUTS_DIR / f"{version_name}.md"
    write_report(output_path, report)
    print(f"Wrote {output_path.relative_to(ROOT)}")


def run_compare() -> None:
    v0_results = run_version("v0_raw_generation")
    v1_results = run_version("v1_task_contract")
    write_report(OUTPUTS_DIR / "v0_raw_generation.md", build_single_report("v0_raw_generation", v0_results))
    write_report(OUTPUTS_DIR / "v1_task_contract.md", build_single_report("v1_task_contract", v1_results))
    compare_report = build_compare_report(v0_results, v1_results)
    compare_path = OUTPUTS_DIR / "compare.md"
    write_report(compare_path, compare_report)
    print(f"Wrote {compare_path.relative_to(ROOT)}")


def run_doctor(live: bool) -> int:
    env_path = ROOT / ".env"
    case_count = len(load_case_set())
    key = os.environ.get("GROQ_API_KEY")
    model = get_model_name()

    print("# doctor")
    print("")
    print(f"- src root: `{ROOT}`")
    print(f"- .env present: `{'yes' if env_path.exists() else 'no'}`")
    print(f"- GROQ_API_KEY present: `{'yes' if key else 'no'}`")
    print(f"- GROQ_API_KEY preview: `{mask_secret(key)}`")
    print(f"- GROQ_MODEL: `{model}`")
    print(f"- case count: `{case_count}`")
    for version_name, path in VERSION_FILES.items():
        print(f"- {version_name} file present: `{'yes' if path.exists() else 'no'}`")

    try:
        validate_environment()
    except RuntimeError as error:
        print("")
        print(f"doctor failed: {error}")
        print("next step: fill `.env` and rerun `python3 run.py doctor --live` or `make doctor`.")
        return 2

    if not live:
        print("")
        print("local checks passed.")
        print("next step: run `python3 run.py doctor --live` or `make doctor` to test provider access.")
        return 0

    try:
        output = chat_completion(
            [
                {"role": "system", "content": "Reply with the single word OK."},
                {"role": "user", "content": "Health check"},
            ]
        )
    except Exception as error:  # noqa: BLE001 - doctor should expose provider failures directly
        print("")
        print(f"live provider check failed: {error}")
        for line in doctor_failure_hint(str(error)):
            print(line)
        print("next step: check the diagnosis above, then retry `python3 run.py doctor --live` or `make doctor`.")
        return 2

    print("")
    print(f"live provider check passed: `{output.strip()}`")
    print("next step: run `python3 run.py compare` or `make compare`.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Lab 1 src surfaces.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run one version on the shared case set.")
    run_parser.add_argument("--version", choices=sorted(VERSION_FILES.keys()), required=True)

    subparsers.add_parser("compare", help="Run both versions and write a side-by-side comparison report.")
    doctor_parser = subparsers.add_parser("doctor", help="Check local setup and optionally test live provider access.")
    doctor_parser.add_argument(
        "--live",
        action="store_true",
        help="Run one tiny live provider health check after local setup checks pass.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    if args.command == "doctor":
        raise SystemExit(run_doctor(args.live))
    try:
        validate_environment()
    except RuntimeError as error:
        parser.exit(2, f"{error}\n")
    if args.command == "run":
        run_single(args.version)
        return
    if args.command == "compare":
        run_compare()
        return
    raise RuntimeError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
