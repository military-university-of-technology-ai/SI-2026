# Lab 1

`Od surowej generacji do kontraktu zadania`

## Cel

W tym laboratorium porównujesz dwie wersje tego samego systemu `Study Assistant`:

- `v0_raw_generation`
- `v1_task_contract`

Celem jest ocena, czy pierwsza warstwa kontroli rzeczywiście poprawia zachowanie systemu, czy jedynie porządkuje powierzchnię odpowiedzi.

### 0. Przygotowanie pojęciowe

Najpierw wykonaj przygotowanie pojęciowe. Jego celem jest zrozumienie:

- czym jest surowa generacja,
- co może poprawić kontrakt zadania,
- czego kontrakt zadania nie rozwiązuje,
- jaka jest różnica między zachowaniem modelu a projektem systemu,
- dlaczego lepsze sformułowanie odpowiedzi nie jest jeszcze dowodem na lepszą aplikację AI.

Wykonaj poniższe prompty w tej kolejności.

#### Prompt 1

```text
Wyjaśnij poniższe pojęcia prostym językiem dla początkującego programisty:
- surowa generacja
- kontrakt zadania
- model i system

Dla każdego pojęcia:
1. podaj prostą definicję
2. wskaż, jaki problem pomaga wyjaśnić
3. wskaż, czego nie rozwiązuje
4. podaj mały przykład w asystencie do nauki
5. podaj jedno częste nieporozumienie
```

#### Prompt 2

```text
Dla małego asystenta AI do nauki podaj:
- 3 przypadki, w których dodanie kontraktu zadania prawdopodobnie poprawiłoby zachowanie
- 3 przypadki, w których dodanie kontraktu zadania nadal nie rozwiązałoby właściwego problemu

Dla każdego przypadku wyjaśnij, czy pozostały problem wynika głównie z:
- zachowania modelu
- brakującego kontekstu
- braku weryfikacji
- szerszego projektu systemu

Przykłady mają być krótkie i konkretne.
```

#### Prompt 3

```text
Utwórz tabelę porównawczą:
- sama surowa generacja
- surowa generacja plus kontrakt zadania

Wiersze:
- co zwykle się poprawia
- co zwykle pozostaje słabe
- co studenci często błędnie interpretują
- jaki typ dowodu można uznać za realną poprawę
- jaka kolejna warstwa kontroli może być potrzebna

Użyj krótkich przykładów z asystenta do nauki.
```

#### Pytania uzupełniające

Po wykonaniu trzech promptów zadaj dodatkowo:

- Czy możesz pokazać przypadek, w którym kontrakt zadania pomaga, ale odpowiedź nadal pozostaje słaba?
- Co odróżnia problem modelu od problemu projektu systemu?
- Jaka różnica w odpowiedzi stanowi rzeczywistą poprawę, a nie tylko poprawę stylistyczną?
- Jeśli kontrakt zadania nie wystarcza, jaka warstwa kontroli zwykle pojawia się jako następna i dlaczego?

Do części praktycznej przejdź dopiero wtedy, gdy potrafisz samodzielnie odpowiedzieć na pięć pytań wypisanych na początku tej sekcji.

### 1. Przygotowanie środowiska

Pracuj w katalogu [src](./src).

Najważniejsze pliki:

- [src/case_set.json](./src/case_set.json)
- [src/versions/v0_raw_generation/system_prompt.txt](./src/versions/v0_raw_generation/system_prompt.txt)
- [src/versions/v1_task_contract/task_contract.txt](./src/versions/v1_task_contract/task_contract.txt)
- [src/outputs/compare.md](./src/outputs/compare.md)

Uzupełnij [src/.env](./src/.env):

```dotenv
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Z głównego katalogu repozytorium uruchom:

```bash
cd lab_1/src
make doctor
make compare
```

Notatka:

- jeżeli `make doctor` zakończy się błędem, najpierw napraw środowisko,
- jeżeli `make` nie jest dostępne, użyj `python3 run.py doctor --live` i `python3 run.py compare`.

### 2. Pierwsze porównanie

Po pierwszym uruchomieniu:

1. Otwórz `src/outputs/compare.md`.
2. Przeczytaj całe porównanie `v0` versus `v1`.
3. Przeanalizuj `src/versions/v1_task_contract/task_contract.txt`.

Na tym etapie:

- nie edytuj `src/case_set.json`,
- nie zmieniaj jeszcze kontraktu zadania,
- nie dodawaj żadnej nowej infrastruktury.

Stały zbiór przypadków jest wymagany, ponieważ utrzymuje wspólną powierzchnię dowodową dla `v0` i `v1`.

### 3. Analiza

Na podstawie pierwszego porównania wykonaj analizę wszystkich 6 przypadków.

Twoim zadaniem jest:

- wskazać, gdzie `v1` daje rzeczywistą poprawę,
- wskazać, gdzie `v1` pozostaje niewystarczające,
- odrzucić co najmniej jedno słabsze wyjaśnienie poprawy.

W analizie opieraj się wyłącznie na:

- odpowiedziach `v0` i `v1`,
- treści kontraktu zadania `v1`,
- jawnych sprawdzeniach w `compare.md`,
- własnej ocenie jakości odpowiedzi.

Jeżeli nie wiesz, od których przypadków zacząć, zacznij od:

- `Krótkie porównanie`
- `Tryb feedbacku`
- `Granica personalizacji`

Przypadek `Granica trybu quizowego` wykorzystaj do sprawdzenia różnicy między:

- zaliczonym jawnym sprawdzeniem,
- rzeczywiście dobrą odpowiedzią.

### 4. Ograniczona zmiana

Po zakończeniu pierwszej analizy wprowadź jedną małą zmianę.

Wymagania:

- edytuj wyłącznie [src/versions/v1_task_contract/task_contract.txt](./src/versions/v1_task_contract/task_contract.txt),
- zachowaj mały zakres zmiany,
- nie przebudowuj struktury `src`,
- nie dodawaj nowej infrastruktury.

Następnie uruchom ponownie:

```bash
make compare
```

albo:

```bash
python3 run.py compare
```

Po ponownym uruchomieniu oceń, czy zmiana:

- pomogła,
- pogorszyła wynik,
- dała efekt głównie kosmetyczny,
- nadal pozostaje niejasna.

### 5. Raport

Na końcu uzupełnij [imie_nazwisko_1.md](./imie_nazwisko_1.md).

Przed oddaniem zadania w GitHub Classroom zmień nazwę pliku na własne dane, na przykład:

- `jan_kowalski_1.md`

Do repozytorium należy zacommitować już raport pod właściwą nazwą pliku studenta.

Raport jest obowiązującym formatem oddania pracy. Wypełnij go w tej kolejności:

1. `Szybka mapa przypadków`  
   Wypełnij tabelę dla wszystkich 6 przypadków.

2. `Główny argument`  
   Wskaż:
   - dwa najmocniejsze usprawnienia w `v1`,
   - jedno pozostałe ograniczenie,
   - jedno odrzucone słabsze wyjaśnienie.

3. `Ocena końcowa`  
   Wpisz w polu `werdykt` dokładnie jedną z tych wartości:
   - `v1 wyraźnie pomogło`
   - `v1 trochę pomogło`
   - `v1 jest głównie kosmetyczne`
   - `na podstawie tych dowodów nie wiadomo`

4. `Wymagana ograniczona zmiana`  
   Opisz:
   - co zmieniłeś lub zmieniłaś,
   - co zmieniło się w odpowiedziach,
   - czy zmiana faktycznie pomogła.

5. `Jak doszedłem lub doszłam do wniosku`
