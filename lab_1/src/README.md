# Katalog `src` do Labu 1

Ten katalog jest najmniejszą realną powierzchnią potrzebną do Labu 1.

Trzyma się zasady `simple-repo`:

- zachowuj obserwowalne zachowanie
- utrzymuj krótką drogę od wejścia do odpowiedzi
- unikaj abstrakcji bez realnego bieżącego odbiorcy

## Co zawiera katalog `src`

- `case_set.json`: wspólny reprezentatywny bank przypadków
- `versions/v0_raw_generation/system_prompt.txt`: zachowanie bazowe
- `versions/v1_task_contract/task_contract.txt`: widoczny plik kontraktu dla ulepszonej wersji
- `groq_client.py`: minimalna integracja z Groq
- `run.py`: uruchamianie jednej wersji albo porównania obu wersji, wraz z jawnymi sprawdzeniami dla wybranych przypadków

## Setup

Użyj Pythona 3.8+.

Edytuj `.env` w tym folderze:

```dotenv
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Skrypt automatycznie odczytuje `.env`.
`.env.example` jest dołączony jako zapisany szablon.

## Najszybsza ścieżka

```bash
make doctor
make compare
```

Jeśli chcesz tylko lokalne sprawdzenia, użyj:

```bash
make doctor-local
```

## Uruchomienie jednej wersji

```bash
make run-v0
make run-v1
```

To zapisze:

- `outputs/v0_raw_generation.md`
- `outputs/v1_task_contract.md`

## Uruchomienie porównania dla zadania

```bash
make compare
```

To zapisze:

- `outputs/v0_raw_generation.md`
- `outputs/v1_task_contract.md`
- `outputs/compare.md`

## Wymagana ograniczona zmiana

W ramach zadania edytuj tylko:

- `versions/v1_task_contract/task_contract.txt`

Następnie uruchom ponownie:

```bash
make compare
```

Celem jest sprawdzenie, czy bardzo mała zmiana naprawdę pomaga.

## Co student powinien sprawdzić

- zestaw przypadków
- pliki kontraktów dla obu wersji
- raport porównawczy w `outputs/compare.md`, razem z minimalnym zestawem jawnych sprawdzeń dla przypadku quizowego
- wynik konfiguracji z `make doctor`

## Zasada dotycząca sekretów

Nie commituj:

- `GROQ_API_KEY`
- `.env`
- wygenerowanych wyników, jeśli Twój sposób pracy nie zakłada ich zachowywania
