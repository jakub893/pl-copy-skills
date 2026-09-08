---
name: pl-anti-ai-slop
description: Usuwa ślady AI z codziennych tekstów po polsku i angielsku, zanim ktoś je przeczyta. Wiadomości, maile do ludzi, odpowiedzi klientom, notatki, raporty, posty, komentarze na czacie. Deterministyczny linter (scripts/lint_pl.py) z bazą ponad 150 zmierzonych śladów (kalki z angielskiego, „kluczowy / kompleksowy / dedykowany", myślniki, „Dodatkowo,", ukośniki płciowe, „Państwo / uprzejmie", brak „bo / więc / żeby", akapit podsumowujący, title case) plus reguły przepisywania. Uruchamiaj ZAWSZE gdy użytkownik mówi „wyczyść", „brzmi jak AI", „odslopuj", „popraw ten mail / tekst", „clean this up", „czy to brzmi jak chatgpt", „sprawdź zanim wyślę", albo gdy sam piszesz dowolny tekst do wysłania w czyimś imieniu. NIE pisze copy sprzedażowego od zera (do tego jest polski-copywriter), ale polski-copywriter wywołuje ten lint na końcu.
---

# pl-anti-ai-slop — lint codziennych tekstów

Cel: tekst, którego odbiorca nie rozpozna jako wygenerowanego. Nie „ładniej", tylko „jak człowiek, który wie, co chce powiedzieć".

## Kiedy używać, kiedy nie
- **Tak:** każdy tekst do wysłania (mail, wiadomość, odpowiedź klientowi, notatka, raport, post, komentarz), przegląd cudzego tekstu na prośbę („czy to brzmi jak AI?"), ostatni krok po `polski-copywriter`.
- **Nie:** pisanie copy sprzedażowego od zera (→ `polski-copywriter`), korekta ortografii bez de-slopu, tłumaczenie, kod.

## Przebieg (4 kroki, zawsze w tej kolejności)
1. **Lint.** Zapisz tekst do pliku (albo podaj przez stdin) i uruchom:
 ```
 python3 ~/.claude/skills/pl-anti-ai-slop/scripts/lint_pl.py <plik|-> [--register luzny|neutralny|formalny|urzad|<rejestr marki>] [--json] [--stats]
 ```
 Wyjście: `linia:kol [S3] id: "dopasowanie" -> poprawka`. S3 = twarde (przepisz), S2 = ostrzeżenie, S1 = wskazówka. Rejestr domyślny: `neutralny`. Rejestry marek (`generic`, `marka-suplement`, `marka-premium`, `sklep-ecommerce`, `marka-suplement-board`, `ice-tiger`, `mentoring-meski`) czytane z `polski-copywriter/references/registers/`.
2. **Przepisz, nie łataj.** Każdy akapit z ≥2 trafieniami piszesz od nowa na głos: co autor chce powiedzieć, komu, po co. Podmiana słowa na synonim to nie naprawa: „kluczowy" → „istotny" to ten sam ślad.
3. **Osiem reguł PL** (poniżej) przechodzisz po kolei nawet wtedy, gdy linter milczy: linter widzi słowa, nie widzi braku konkretu.
4. **Re-lint.** Cel: 0 twardych, ≤2 ostrzeżenia na 300 słów. Przy `--stats` sprawdź pasmo rejestru (`references/targets.json`). Dopiero wtedy tekst idzie dalej.

## Osiem reguł PL (kolejność = kolejność cięcia)
1. **Konkret.** Każde 100 słów ma liczbę, godzinę, nazwę, cenę albo scenę. Bez danych = zdanie bez liczby, nigdy liczba z powietrza. „Wielu klientów" → „312 osób" albo wytnij.
2. **Krótkie po długim.** Zdanie powyżej 25 słów dzielisz. Po trzech krótkich wolno jedno długie. Trzy zdania tej samej długości pod rząd = przepisz środkowe.
3. **Bez zapowiedzi i podsumowań.** „Warto zauważyć, że", „Należy podkreślić", „Podsumowując", „Mam nadzieję, że to pomoże", „Kluczowe wnioski": wytnij, zostaw treść. Tekst kończy się na ostatnim konkrecie albo na prośbie.
4. **Bez kalk.** dedykowany → przeznaczony dla; adresować problem → rozwiązać; w kontekście → jeśli chodzi o; na koniec dnia → ostatecznie; robi sens → ma sens; dostarczać wartość → powiedz, co dajesz; Title Case → tylko pierwsza litera; „Dodatkowo," → usuń łącznik.
5. **Spójniki mowy.** W 300 słowach ma być przynajmniej jedno „bo", jedno „że", jedno „ale" w środku zdania. Zero „oraz", „ponadto", „dodatkowo", „jednakże". To najsilniejszy zmierzony ślad: AI po polsku nie używa „bo / więc / żeby / czyli / przecież".
6. **Do czytelnika bez płci, ale z człowiekiem.** Zero „zrobiłeś/aś", zero ukośników. Czas teraźniejszy („masz"), rozkaźnik („sprawdź"), przyszły („dostaniesz"), bezokolicznik, „po zakupie widać…". Rejestr męski (reklama wideo marki eksperckiej, mentoring) dopuszcza „zrobiłeś".
7. **Bez myślników.** „—" i „ – " zastępujesz kropką, przecinkiem, dwukropkiem, nawiasem. Półpauza tylko w zakresach (10–20 min).
8. **Bez figur AI.** Negatywny paralelizm („To nie X, to Y", także przez granicę akapitu), wskazywanie palcem („I to jest właśnie…"), reguła trzech, fałszywe zakresy („od X po Y"), ramki („zarówno…, jak i", „z jednej strony… z drugiej"), metafory-fundamenty („kluczem do", „otwiera drzwi", „stanowi fundament"). Wolno raz na tekst, nigdy w otwarciu. Pełna lista: `references/tells-pl.md`, kategoria struktura.
9. **Jedna opinia z ryzykiem.** Tekst bez żadnego zdania, za które autor może oberwać, brzmi jak AI. Jedno zdanie w tekście ma być zdecydowane: „To nie zadziała", „Nie kupuj tego", „Zrobiłem błąd".

## Reguły EN (skrót; pełna lista w `references/tells-en.md`)
- Otwieracze: „Here's the thing", „The truth is", „Let's dive in", „I hope this email finds you well", „Great question" → wytnij.
- Słowa: delve, leverage, tapestry, testament, landscape, navigate, robust, seamless, crucial, pivotal, foster, empower, unlock, elevate, streamline, „it's important to note", „in today's fast-paced world" → prosty odpowiednik albo nic.
- Struktury: „It's not X, it's Y", „Not just X but Y", tricolon przymiotników, „No fluff. No filler. Just results.", pytanie retoryczne jako haczyk, akapit-podsumowanie → jedna rzecz powiedziana wprost.
- Fałszywe sprawstwo: „the data tells us", „the market rewards", „the decision emerges" → nazwij, kto co zrobił.
- Przysłówki-wypełniacze: really, truly, genuinely, actually, simply, deeply → wytnij. Hedging: might, could, perhaps, potentially → zdecyduj.
- Em-dash: ten sam zakaz co po polsku.

## Rejestry lekkie (`references/registers/`)
`luzny` (znajomi, zespół: „hej", „dzięki", „daj znać"), `neutralny` (domyślny: maile robocze, klienci, notatki), `formalny` (pisma do firm: „Szanowni Państwo" OK), `urzad` (ZUS, US: formuły urzędowe OK, kalki i podsumowania nadal zakazane). Rejestr wyłącza wybrane ślady (`exempt_tells`), reszta obowiązuje.

## Tryb przeglądu („czy to brzmi jak AI?")
Nie przepisujesz. Zwracasz raport lintera + 3 zdania: najmocniejszy ślad, drugi ślad, co bym zmienił najpierw. Przepisujesz dopiero na prośbę.

## Test jednego zdania
Czy to zdanie mogłoby paść w rozmowie przy kawie, z tą samą osobą, o tej samej sprawie? Jeśli nie, przepisz tak, żeby mogło.

## Pliki
- `references/tells.yaml` — baza śladów (PL+EN) z regexami, poprawkami, ważnością, częstością w korpusie ludzkim vs AI. Jedyne źródło prawdy; `tells-pl.md` i `tells-en.md` są generowane (`scripts/build_tells_md.py`).
- `references/zamienniki.md` — słowo AI → ludzki odpowiednik.
- `references/przyklady-przed-po.md` — 12 par PL + 4 EN.
- `references/registers/` — rejestry lekkie.
- `references/targets.json` — pasma rytmu per rejestr, zmierzone na korpusie (`workspace/korpus-polski/`).
- `scripts/stats.py` — statystyki rytmu (współdzielony z `polski-copywriter`).
