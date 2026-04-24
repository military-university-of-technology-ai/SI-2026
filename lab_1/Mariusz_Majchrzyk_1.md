# Raport do Labu 1

Pisz krótko.

Każdy ważny wniosek powinien zawierać:

- co najmniej jedno `case_id`
- jeden konkretny dowód z odpowiedzi albo z jawnego sprawdzenia

Nie pisz ogólnie: `v1 jest lepsze`.
Pisz konkretnie: `w c2 v1 było krótsze i naprawdę porównywało dwa pojęcia`.

## 1. Szybka mapa przypadków

Używaj tylko tych wartości w kolumnie `Ocena`:

- `lepsze`
- `bez zmian`
- `gorsze`
- `niejasne`

Wypełnij tabelę dla wszystkich 6 przypadków.

| ID przypadku | Ocena | Jednozdaniowy dowód |
| --- | --- | --- |
| `c1_beginner_explanation` |lepsze  |w c1 v1 podaje strukturę, podczas gdy v0 było bardziej ogólne i pomijało jedno z pól  |
| `c2_brief_comparison` |lepsze |w c2 v1 faktycznie porównuje dwa pojęcia wprost, a v0 opisuje je osobno bez jasengo kontrastu  |
| `c3_self_check_mode` |bez zmian |w c3 oba modele deklarują sprawdzenie, ale brakuje dowodu faktycznego sprawdzenia wyniku  |
| `c4_course_uncertainty` |lepsze |w c4 v1 zaznacza brak pewności i ograniczenia kontekstu, a v0 tego nie robi  |
| `c5_feedback_mode` |lepsze |w c5 v1 daje konkretne uwagi, a v0 jest ogólne  |
| `c6_personalized_plan_limit` |nie jasne |w c6 v1 wygląda bardziej dopasowane, ale brakuje dowodu  |

## 2. Główny argument

### Usprawnienie 1

- `case_id:`c2_brief_comparison
- `dowód:`v1 bezpośrednio zestawia dwa pojęcia w jednym zdaniu, zamiast dwóch oddzielnych opisów
- `dlaczego to jest realna poprawa:`kontrakt wymusza strukturę zadania, co zmienia sposób rozumowania odpowiedzi, a nie tylko jej styl

### Usprawnienie 2

- `case_id:`c4_course_uncertainty
- `dowód:`v1 explicite zaznacza brak wystarczających danych zamiast zgadywać
- `dlaczego to jest realna poprawa:`zgodnie z ideą kontraktu zadania ogranicza zgadywanie i wprowadza kontrolę nad niepewnością

### Jedno pozostałe ograniczenie

- `case_id:`c3_self_check_mode
- `dowód:`v1 deklaruje sprawdzenie, ale nie pokazuje konkretnego wyniku walidacji
- `dlaczego sam kontrakt zadania tego nie rozwiązuje:`kontrakt określa format, ale bez warstwy weryfikacji nie zapewnia realnego sprawdzenia poprawności
 

### Jedno odrzucone słabsze wyjaśnienie

- `słabsze wyjaśnienie:`v1 jest lepsze, bo brzmi bardziej profesjonalnie
- `case_id:`c5_feedback_mode
- `dowód przeciw temu wyjaśnieniu:`poprawa polega na odniesieniu do konkretów odpowiedzi (np. wskazanie błędu), a nie tylko na stylu wypowiedzi

## 3. Ocena końcowa

W polu `werdykt` wpisz dokładnie jedną z tych wartości:

- `v1 wyraźnie pomogło`
- `v1 trochę pomogło`
- `v1 jest głównie kosmetyczne`
- `na podstawie tych dowodów nie wiadomo`

- `werdykt:`v1 trochę pomogło
- `uzasadnienie z case_id:`poprawa widoczna w c2 i c4, ale brak realnej zmiany w c3 i niejasność w c6

## 4. Wymagana ograniczona zmiana

- `edytowany plik:`src/versions/v1_task_contract/task_contract.txt
- `jednozdaniowy opis zmiany:`jednozdaniowy opis zmiany:` dodanie wymogu jawnego pokazania wyniku sprawdzenia zamiast samej deklaracji
- `docelowe case_id:`c3_self_check_mode
- `co zmieniło się po uruchomieniu:`odpowiedź zawiera konkretny wynik sprawdzenia zamiast ogólnej deklaracji

W polu `ocena zmiany` wpisz dokładnie jedną z tych wartości:

- `pomogła`
- `pogorszyła`
- `głównie kosmetyczna`
- `niejasne`

- `ocena zmiany:`pomogła
- `dowód:`w c3 pojawia się jawny wynik weryfikacji zamiast pustego stwierdzenia

## 5. Jak doszedłem lub doszłam do wniosku

- `2-4 najważniejsze obserwacje:`v1 poprawia strukturę odpowiedzi (np. c1, c2)
  * v1 lepiej radzi sobie z niepewnością (c4)
  * brak warstwy weryfikacji powoduje pozorne poprawy (c3)
- `czego te wyniki jeszcze nie dowodzą:`* że system jako całość jest bardziej niezawodny, odpowiedzi są faktycznie poprawne, a nie tylko lepiej sformułowane orazpersonalizacja działa na podstawie danych

W polu `następny sensowny krok` wpisz dokładnie jedną z tych wartości:

- `lepszy kontrakt zadania`
- `więcej kontekstu`
- `dodatkowa weryfikacja`
- `wyraźniejsza granica narzędziowa`
- `lepszy przebieg pracy albo stan`

- `następny sensowny krok:`dodatkowa weryfikacja
- `krótkie uzasadnienie:`kontrakt poprawia strukturę, ale bez sprawdzania wyników nie mamy dowodu realnej poprawy jakości
