# polski-copywriter + pl-anti-ai-slop

Dwa skille dla Claude Code do pisania po polsku: jeden pisze copy sprzedażowe, drugi czyści codzienne teksty ze śladów AI. Oba mają deterministyczny linter, bazę zmierzonych śladów i pasma rytmu wyliczone z korpusu ludzkiej polszczyzny.

Powstały, bo typowe „anti-AI" skille są napisane po angielsku i wykrywają angielskie ślady (`delve`, `tapestry`, em-dash). Po polsku problem wygląda inaczej.

## Co się okazało po zmierzeniu

Korpus: 220 książek z Wolnych Lektur (felieton, reportaż, proza), 60 wpisów blogowych sprzed 2022, 6 nagrań polskich copywriterów (55 tys. słów mówionych), polskie maile i listy sprzedażowe. Klasa negatywna: 71 tekstów wygenerowanych przez modele bez żadnych instrukcji stylu.

**Najsilniejszy ślad AI po polsku to nie słownictwo, tylko brak spójników mowy.**

| spójnik | ludzie (mail / mowa) | AI |
|---|---|---|
| bo | 2,5 / 5,9 | 0,7 |
| żeby | 0,7 / 5,8 | 0,45 |
| więc | 0,9 / 4,6 | 0,2 |
| czyli | 0,9 / 2,7 | 0,2 |
| że | 11 / 18 | 4,7 |

Częstość na 1000 słów. Model zamiast nich stawia kropkę albo sięga po spójniki pisane: „dziś" (10 razy częściej niż ludzie), „zamiast" (9 razy), „oraz" (3 razy).

Druga rzecz: **gęstość konkretu**. Polski list sprzedażowy pisany przez człowieka ma 49 do 71 liczebników na 1000 słów. Teksty modelu bez danych: 22, i są to głównie liczby z listy punktowanej.

Trzecia: **em-dash nie jest uniwersalnym śladem**. W polskiej literaturze XIX wieku jest wszędzie (dialogi). Jako ślad działa dopiero w krótkim tekście użytkowym, gdzie człowiek stawia przecinek albo kropkę.

## Co jest w środku

### `pl-anti-ai-slop`: lint codziennych tekstów
- `scripts/lint_pl.py`: linter: 528 śladów (307 polskich, 219 angielskich, 2 wspólne; 57 twardych) z regexami odpornymi na fleksję, poprawką i zmierzoną częstością w korpusie ludzkim kontra AI. Wyjście: `linia:kolumna [S3] id: "dopasowanie" -> poprawka`.
- `scripts/stats.py`: rytm i składnia: mediana i odchylenie długości zdania, burstiness, udział zdań krótkich, akapity jednozdaniowe, imiesłowy, strona bierna, tricolony, liczebniki.
- `references/tells.yaml`: jedyne źródło prawdy. `tells-pl.md`, `tells-en.md` i `zamienniki.md` generuje `build_tells_md.py`.
- Cztery rejestry lekkie: luźny, neutralny, formalny, urząd.

### `polski-copywriter`: rzemiosło copy
- Dwanaście reguł polskiej składni (szyk i remat, nominalizacje, imiesłowy, zwrot do czytelnika bez płci, przecinek po okoliczniku, aspekt).
- Osiem figur, po których widać AI: negatywny paralelizm („To nie X, to Y", także rozbity na dwa akapity), wskazywanie palcem na własną myśl, reguła trzech, fałszywe zakresy, ramki „zarówno, jak i", metafory-fundamenty.
- Formuły świata (AIDA, PAS, BAB, Schwartz, Sugarman, Hormozi) z adaptacją do polskiej składni.
- `references/ciag-mysli.md`: rozbiór polskiego listu sprzedażowego: 20 taktów, 12 zdań-mostów, reguła dowodu, rytm w liczbach, szkielet do wypełnienia.
- `scripts/check_copy.py`: kontrola formatu i rejestru: pasmo rytmu, długość bulletów, wymagane i zakazane frazy, compliance branżowy.
- Przełącznik rejestrów marki: `--register <nazwa>` czyta frontmatter YAML z `references/registers/`.

## Instalacja

```bash
git clone https://github.com/jakub893/pl-copy-skills.git
cp -r pl-copy-skills/polski-copywriter pl-copy-skills/pl-anti-ai-slop ~/.claude/skills/
pip3 install pyyaml
```

Sprawdzenie:
```bash
echo 'W dzisiejszych czasach kluczowe jest kompleksowe podejście. Dodatkowo, warto zauważyć, że synergia — to podstawa.' \
  | python3 ~/.claude/skills/pl-anti-ai-slop/scripts/lint_pl.py -
```

## Użycie

```bash
# lint tekstu przed wysłaniem
python3 ~/.claude/skills/pl-anti-ai-slop/scripts/lint_pl.py mail.md --register neutralny

# lint ze statystykami rytmu i sprawdzeniem pasma
python3 ~/.claude/skills/pl-anti-ai-slop/scripts/lint_pl.py post.md --stats --json

# kontrola copy: rejestr marki + format
python3 ~/.claude/skills/polski-copywriter/scripts/check_copy.py list.md --register sklep-ecommerce --format list
```

Formaty: `mail`, `reklama`, `landing`, `list`, `vsl`, `social`. Pasma rytmu w `references/targets.json`.

W Claude Code skille odpalają się same: `pl-anti-ai-slop` na „wyczyść", „brzmi jak AI", „popraw ten mail"; `polski-copywriter` na „napisz mail", „zrób reklamę", „przepisz landing".

## Kalibracja

Linter strojono tak, żeby milczał na tekstach ludzkich i krzyczał na modelowych. Twarde trafienia na 1000 słów:

| korpus | twarde/1000 |
|---|---|
| polskie maile sprzedażowe (ludzie) | 0,23 |
| mowa polskich copywriterów | 0,51 |
| teksty modelu po polsku | 11,4 |
| teksty modelu po angielsku | 12,6 |

Ślad, który trafiał w ludzi częściej niż trzy razy, dostawał limit częstości albo niższą wagę. Stąd konstrukcje w rodzaju „To nie X, to Y" nie są zakazane, tylko limitowane: człowiek używa ich raz na tekst, model co akapit.

Benchmark na 20 zadaniach (z skillem kontra bez, ten sam model):

| skill | twarde trafienia z / bez | em-dashe z / bez |
|---|---|---|
| polski-copywriter | 0,0 / 9,3 | 0,1 / 8,3 |
| pl-anti-ai-slop | 0,0 / 1,4 | 0,4 / 1,2 |

## Jak dodać własny rejestr marki

Rejestry w repozytorium są przykładowe. Prawdziwe (z cenami, progami, nazwiskami, compliance) trzymaj lokalnie, poza gitem. Schemat frontmattera opisuje `polski-copywriter/references/registers/README.md`.

## Materiały źródłowe

Wzorce, na których mierzono rytm, nie wchodzą do repozytorium, bo są cudzą własnością. Zostają: rozbiór struktury, pomiary i krótkie cytaty w granicach prawa cytatu (`references/exemplars/`). Cytaty z literatury pochodzą z Wolnych Lektur (domena publiczna).

Jeśli budujesz swoją wersję: podstaw teksty, do których masz prawa, i zmierz je przez `stats.py`. Wartość bierze się z pomiaru własnych wzorców.

## Licencja

MIT dla kodu i opracowań. Cytowane fragmenty cudzych tekstów pozostają własnością ich autorów.
