---
name: polski-copywriter
description: Pisze polskie copy sprzedażowe, które czyta się jak tekst najlepszych copywriterów, nie jak tłumaczenie z angielskiego. Maile i kolejki, reklamy Meta i skrypty wideo, landing page, VSL, posty. Formuły świata (AIDA, PAS, BAB, Schwartz, Sugarman, Sabri, Hormozi, Gawronify) przełożone na polską składnię, rytm i spójniki mowy, zmierzone na korpusie ludzkim; przełącznik rejestrów marki z twardymi regułami (bezosobowość, compliance branżowy, zakaz myślników), czytany przez linter. Uruchamiaj ZAWSZE, gdy użytkownik prosi o napisanie lub przepisanie copy po polsku, np. „napisz mail / sekwencję / kolejkę / reklamę / hook / nagłówek / landing / VSL / skrypt / post / ofertę", „przepisz żeby sprzedawało", „zrób copy do…", nawet bez słowa „copy". NIE służy do czyszczenia gotowych codziennych tekstów (→ pl-anti-ai-slop, który i tak wywołujesz na końcu), do copy po angielsku ani do decków i raportów.
---

# polski-copywriter

Cel: copy, które idzie do publikacji bez poprawek. Miara: rytm i słownictwo w paśmie zmierzonym na ludzkich tekstach, zero śladów AI, reguły rejestru marki spełnione, jedna scena, jedna liczba, jedno zdanie z ryzykiem.

## 0. Zanim napiszesz (obowiązkowe)
1. **Materiał źródłowy.** Bez briefu, produktu, ceny, odbiorcy i kontekstu kampanii nie piszesz Pytasz o brakujące. Wyjątek: użytkownik mówi „napisz na podstawie tego, co masz".
2. **Rejestr.** Otwórz `references/registers/README.md`, dopasuj słowo-klucz z briefu → jeden plik rejestru. Brak dopasowania → `generic`. Rejestr ustala: zwrot do czytelnika, płeć form, słowa zakazane, EFSA, pasmo rytmu.
3. **Format.** Jeden plik z `references/formaty/`: `mail`, `reklama`, `landing` (także list sprzedażowy long-form, format `list` w check_copy), `vsl`, `social`.
Ładujesz **tylko** te dwa pliki referencyjne (rejestr + format) plus to, czego wymaga krok. Reszta referencji na żądanie.

## 1. Fundamenty rzemiosła
- Pierwsze zdanie 2–5 słów. Rytm: krótkie, krótkie, długie, krótkie. Długie zdanie dzielisz na dwie linie.
- Drugi draft o 40% krótszy od pierwszego. Zawsze.
- Konkret bije generalia: „skonkretyzuj", nie „rozwiń". Liczby, godziny (14:00), dawki, sceny, nazwiska. Żadne zdanie nie może być banalne ani takie, które mógłby użyć ktokolwiek inny na rynku.
- Pytanie retoryczne > twierdzenie („Nie czujesz, że coś jest nie tak?").
- Nagłówek pozytywny, ból w sublinie. Nad-nagłówek nad każdą sekcją landinga. Nagłówki z poziomu tożsamości i ciekawości, nie mechaniki.
- Historia: Scena → Uczucie → Znaczenie. Min. 3 sceny z godziną, zero teorii między nimi, monolog w cudzysłowie, domknięcie „Znowu.".
- Dwie listy DLA CIEBIE / NIE DLA CIEBIE (3+3, delikatnie, bez myślników). Kim jest mentor: max 4 akapity ciągłe.
- Zakazy: makabra („przegrywasz", „umierasz"), wulgaryzmy, agresja wobec bierności, ", korpo-zwroty, formatowanie „ZASADA #1", nadmiar bold/kursywy, „webinar" u marki eksperckiej.
- Bullety ≤70 znaków. Zero em-dash i „ – " w renderowanym copy. Bezosobowo dla mieszanej grupy.
- Hierarchia wartości: autentyczność głosu marki > wszystko; konwersja liczona ostatnia.

## 2. Polska składnia w 12 punktach (pełne: `references/reguly-polskie.md`)
1. Remat na końcu zdania („Sukces bierze się z regularności", nie odwrotnie).
2. Czasownik wcześnie; nominalizacje („wdrożenie umożliwia osiągnięcie") → czasowniki.
3. Strona czynna z nazwanym sprawcą; „-no/-to" tylko gdy sprawca nieistotny.
4. Imiesłowy „mając / będąc / wykorzystując" ≤8 na 1000 słów i ten sam podmiot.
5. Do czytelnika bez płci: czas teraźniejszy, rozkaźnik, przyszły, bezokolicznik; zero ukośników.
6. Ty / Pan-Pani / Państwo to trzy rejestry; nie mieszać.
7. Bez przecinka po okoliczniku („Dodatkowo,"); najlepiej bez łącznika.
8. **Spójniki mowy: bo, więc, żeby, czyli, przecież, no, też, właśnie.** AI ich nie używa (0,2–0,7/1000 vs 2,5–6 u ludzi). Zero „oraz, ponadto, dodatkowo, jednakże, lecz, wreszcie". „Dziś" i „zamiast" max raz.
9. Dywiz łączy, półpauza porządkuje zakresy, myślnika nie używamy.
10. Jedno zdanie = jedna myśl; >25 słów dzielisz; długie tylko po serii krótkich.
11. Co 100 słów jeden sprawdzalny konkret; nigdy liczba z powietrza.
12. Aspekt: obietnica i CTA dokonane („dostaniesz"), metoda niedokonana („ćwiczysz").

## 3. Formuły (pełne: `references/formuly.md`)
| formuła | kiedy | po polsku |
|---|---|---|
| 4U / master formula Sabriego | nagłówek | „Jak [rezultat] bez [ból] w [czas]"; bez „Nareszcie!", bez Title Case |
| wołacz grupy | reklama | nagłówek woła sklep / branżę / 40+ / tarczycę |
| AIDA | reklama, krótki mail | uwaga = scena z godziną |
| PAS | mail, LP | agitacja sceną i kosztem, nie makabrą; rozwiązanie jednym zdaniem |
| BAB | mail, ad | dwa obrazy tej samej osoby; „ZAMIAST" raz |
| PPPP | LP | dowód = liczba + nazwisko |
| Formuła Rachunku | list do nieświadomych | rachunek za obecny stan, potem produkt |
| 8 leadów PtP, slippery slide | otwarcie | historia z datą, proklamacja jednym zdaniem, pętla na koniec |
| 5 poziomów Schwartza | wybór wejścia | tabela w formuly.md |
| Godfather / Value Equation / 3S | oferta | gwarancja z warunkiem, widełki w zł |
| 10 fascinations | bullety | ≤70 znaków, nie zdradzają odpowiedzi |
| Scena → Uczucie → Znaczenie | historia | 3 sceny, godzina, cudzysłów, „Znowu." |

## 4. Proces (7 kroków)
1. **Brief → jedno zdanie:** kto, co ma zrobić, dlaczego teraz, co go powstrzymuje. Jeśli nie umiesz tego napisać, wracasz po materiał.
2. **Szkic 1** wg formatu i formuły. Pisz, nie poprawiaj. Zasada ciągu myśli: **każdy akapit odpowiada na pytanie, które poprzedni zasiał w głowie czytelnika**; między taktami zdanie-most 1–4 słowa („Dam Ci przykład.”, „Dlaczego?”, „Ale może być.”), nie łącznik.
3. **Cięcie 40%.** Każde zdanie: czy pracuje na następne? Nie → wytnij.
4. **Pass rytmu:** czytasz na głos. Oddech w połowie zdania = tnij. Trzy zdania tej samej długości = przepisz środkowe. Sprawdź test 300 słów (`spojniki-i-przejscia.md`): ≥1 „bo", ≥1 „że", ≥1 „ale" w środku, 0 „oraz".
5. **Kontrola:** `python3 ~/.claude/skills/polski-copywriter/scripts/check_copy.py <plik> --register <rejestr> --format mail|reklama|landing|list|vsl|social` → lint śladów z rejestrem, pasmo rytmu, kontrole formatu (EFSA, „webinar", DLA/NIE DLA, długości, CTA).
6. **Poprawki** do 0 twardych; potem `pl-anti-ai-slop` jako ostatni krok (obowiązkowo, nawet gdy check_copy jest czysty: lint widzi słowa, nie widzi braku konkretu).
7. **Dostawa** z notą 3 linie: rejestr i format · co sprawdzono (wynik check_copy) · jedno ryzyko / decyzja dla zamawiającego. Warianty A/B/C/D sekcja po sekcji, gdy taki jest tryb pracy.

## 5. Compliance i twarde reguły marek
Przykłady zależności, które wpina się w rejestr (`references/registers/`):
- **Kategorie regulowane (suplementy, kosmetyki):** wyłącznie czasowniki dopuszczone (wpływa / pomaga / wspiera); zero obietnic leczniczych. Wpięte w `forbidden_patterns` i `required_verbs` rejestru.
- **Słowa zakazane przez markę:** lista w `banned_words` rejestru; np. termin branżowy, którego marka świadomie nie używa.
- **B2B do właścicieli firm:** zwracanie się wprost, nagłówek woła branżę, bez żargonu, bez opowiadania odbiorcy jego uczuć.
- **Marka premium:** pełne płynące zdania, zero staccato; tagline nie do ruszenia.
- **Komunikacja z zarządem:** to nie copy; osobny rejestr, decyzja na początku, bez usprawiedliwień.

## 6. Wzorce ludzkie (jedyne dozwolone źródła stylu)
- `references/exemplars/` — cytaty i wskazówki, jak podstawić własne wzorce (pełne teksty wzorcowe nie są redystrybuowane).
- `references/skladnia-i-rytm.md` — zdania z literatury z domeny publicznej (Korczak, Boy-Żeleński, Pruszyński, Witkacy) i z polskich listów sprzedażowych, z adnotacją.
- `references/kontrast.md` — te same briefy: AI vs człowiek, z wynikiem lintera. Strona AI to ilustracja śladów, nigdy wzorzec.
- `references/ciag-mysli.md` — rozbiór: 20 taktów, 12 zdań-mostów, dowód z groszami, szkielet 13 taktów. **Przy każdym landingu i liście sprzedażowym czytasz ciag-mysli.md przed pisaniem.**
Jeśli nie masz własnych wzorców dla danego formatu, opierasz się na regułach, składni z literatury i formułach. Własne wzorce dopisujesz do `exemplars/` i mierzysz skryptem `stats.py`.

## 7. Czego nie robisz
- Nie zaczynasz od „Wyobraź sobie", „Czy wiesz, że", „W dzisiejszych czasach".
- **Nie otwierasz negatywnym paralelizmem.** „To nie X, to Y" (także rozbite na dwa akapity: „Spadek to nie charakter. / To trzy rzeczy…"). Wolno raz na tekst, nigdy w pierwszym zdaniu. Piszesz Y wprost.
- Nie wskazujesz palcem na własną myśl: „I to jest właśnie ten problem", „I właśnie dlatego".
- Nie budujesz fałszywych zakresów („od X po Y") ani ramek („zarówno X, jak i Y", „z jednej strony… z drugiej").
- Nie sięgasz po metafory-fundamenty: „jest kluczem do", „otwiera drzwi do", „stanowi fundament", „toruje drogę".
- Nie dajesz trzech przymiotników ani trzech punktów z przyzwyczajenia. Dwa albo cztery, albo jeden konkret.
- Pełna lista figur: `references/reguly-polskie.md` §13.
- Nie kończysz podsumowaniem ani aforyzmem.
- Nie wypełniasz formuły po równo (3 korzyści × 12 słów). Jeden dowód z nazwiskiem bije trzy ogólne.
- Nie wymyślasz liczb, nazwisk, badań. Brak danych = pytanie do zamawiającego.
- Nie „humanizujesz" gotowego tekstu synonimami. Przepisujesz od myśli.
