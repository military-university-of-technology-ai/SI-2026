# Meta Lecture 1: Od surowej generacji do systemów opartych na LLM-ie

## 1. Punkt wyjścia

- LLM potrafi generować płynny tekst.
- To jednak nie wystarcza, aby zbudować system oparty na LLM-ie.
- Kurs dotyczy przejścia od surowej generacji do systemu, w którym działają jawne mechanizmy kontroli.

## 2. Główna idea

- **System oparty na LLM-ie = surowa generacja + warstwy kontroli**
- Główne warstwy:
  - kontrakt zadania
  - kontekst
  - weryfikacja
  - uprawnienia i granice
  - stan i przepływ pracy

Kluczowa teza: surowa generacja staje się częścią systemu dopiero wtedy, gdy zostaje ograniczona i uzupełniona przez warstwy kontroli.

## 3. Czym jest surowa generacja

- pojedyncze wywołanie modelu
- wejście -> płynna odpowiedź
- model potrafi:
  - kontynuować tekst
  - streszczać
  - odpowiadać na pytania
  - naśladować strukturę odpowiedzi

Warto zauważyć: model potrafi dużo, ale to nadal nie jest jeszcze pełny system AI.

## 4. Ograniczenia surowej generacji

- Płynność nie oznacza:
  - poprawności
  - niezawodności
  - kontroli
- Model może:
  - brzmieć poprawnie i być błędny
  - pominąć instrukcję
  - zignorować kontekst
  - wygenerować zły format
  - zasugerować niewykonaną akcję

Kluczowa obserwacja: właśnie na tym poziomie najczęściej pojawiają się pierwsze błędne intuicje o możliwościach modelu.

## 5. Model i system

- Model generuje tekst.
- System wokół modelu określa:
  - prompt
  - kontekst
  - format wyjścia
  - sprawdzenia
  - dozwolone działania
  - stan między krokami

## 6. Chatbot a komponent systemowy

- W bezpośrednim użyciu chatbota człowiek nadal:
  - interpretuje wynik
  - sprawdza źródła
  - zatrzymuje błędne użycie
- W systemie te zabezpieczenia trzeba odtworzyć jawnie.
- Wynik może zostać użyty dalej, zanim człowiek go oceni.

Kluczowe przejście: od intuicji „chatbot odpowiada” do myślenia „system musi to kontrolować”.

## 7. Granice promptowania

- Lepszy prompt może poprawić formę odpowiedzi.
- Nie zastąpi jednak:
  - brakujących informacji
  - zewnętrznej kontroli poprawności
  - granic działania
  - sterowania przepływem pracy

## 8. Mapa warstw kontroli

- Kontrakt zadania: co system ma zrobić
- Kontekst: jakie informacje system dostaje
- Weryfikacja: jak sprawdzamy wynik
- Uprawnienia i granice: co systemowi wolno
- Stan i przepływ pracy: jak utrzymujemy spójność między krokami
- Całość systemu: jak te warstwy działają razem

## 9. Kontrakt zadania

- precyzuje, co system ma zrobić
- określa ograniczenia i format
- wskazuje, co zrobić przy niejednoznaczności

Przykład:

- odpowiedź w 3 punktach
- bez kodu
- zaznaczenie, gdy źródło jest niewystarczające

Kluczowa teza: kontrakt zadania porządkuje oczekiwanie wobec systemu, ale nie gwarantuje poprawności.

## 10. Kontekst

- dostarcza informacje potrzebne do zadania
- ogranicza zgadywanie
- może obejmować:
  - dokumenty
  - pliki
  - wcześniejszy stan rozmowy
  - materiał dowodowy

## 11. Weryfikacja

- sprawdza, czy wynik spełnia warunki akceptacji
- może obejmować:
  - walidatory
  - testy
  - sprawdzenie schematu
  - sprawdzenie zgodności ze źródłem

Kluczowa teza:

- wiarygodny wynik nadal może być błędny

## 12. Uprawnienia i granice

- oddziela to, co model może wygenerować, od tego, co może wykonać
- przykładowe pytania:
  - czy system może użyć narzędzia?
  - czy może wykonać akcję?
  - czy musi uzyskać zgodę?

Kluczowa teza:

- możliwość techniczna nie jest tym samym co uprawnienie

## 13. Stan i przepływ pracy

- utrzymuje spójność działania między krokami
- obejmuje:
  - postęp zadania
  - pamięć roboczą
  - ważne decyzje
  - aktualną wersję artefaktu

Kluczowa teza:

- systemy wieloetapowe zawodzą inaczej niż pojedyncze prompty

## 14. Ograniczenia warstw

- lepszy prompt nie zastępuje brakującej wiedzy
- sam kontekst nie gwarantuje poprawnego użycia danych
- weryfikacja nie tworzy poprawnej odpowiedzi
- dostęp do narzędzi nie czyni wyniku automatycznie godnym zaufania

Kluczowa teza: żadna pojedyncza technika nie rozwiązuje całego problemu.

## 15. Podsumowanie

- Chatbot to za mało, by mówić o systemie AI.
- System oparty na LLM-ie wymaga jawnych warstw kontroli.
- Kurs pokazuje, jak te warstwy rozumieć i łączyć.
