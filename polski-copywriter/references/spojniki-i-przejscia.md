# Spójniki i przejścia — ludzie vs AI (pomiar na korpusie, 2026-09-07)

Częstość na 1000 słów. Korpus ludzki: polskie maile sprzedażowe (8,7 tys. słów, maile sprzedażowe), felieton i reportaż z Wolnych Lektur (2,3 mln słów, domena publiczna), 6 nagrań polskich copywriterów (55 tys. słów mówionych). AI: 21 tekstów Claude (sonnet, opus) bez skilli, 4,4 tys. słów. Pełna tabela: `workspace/korpus-polski/stats/connectives.md`.

## Wniosek główny
AI po polsku **nie mówi**. Brakuje mu spójników rozmowy, którymi człowiek klei myśli: **bo, więc, żeby, czyli, przecież, no, też, właśnie, jednak, zresztą**. Zamiast nich stawia kropkę i zaczyna nowe zdanie, albo bierze spójniki „pisane": **oraz, lecz, wreszcie, dziś, zamiast**.

| spójnik | ludzie (mail / mowa) | AI | co robić |
|---|---|---|---|
| **bo** | 2,5 / 5,9 | 0,7 | używaj; „bo" tłumaczy powód bez namaszczenia |
| **żeby** | 0,7 / 5,8 | 0,45 | cel: „żeby", nie „w celu", nie „aby" w co drugim zdaniu |
| **więc** | 0,9 / 4,6 | 0,2 | wniosek: „więc", nie „w związku z tym", nie „dlatego też" |
| **czyli** | 0,9 / 2,7 | 0,2 | wyjaśnienie: „czyli", nie „innymi słowy", nie „to znaczy, że" |
| **no** | 0,1 / 4,7 | 0 | w mowie i luźnym mailu: „No dobra, więc co jest w nim wyjątkowego?" |
| **też** | 0,35 / 6,5 | 0,7 | „też", nie „również", nie „także" (AI: również 0, także 0,45) |
| **właśnie** | 1,3 / 4,1 | 0,45 | podkreślenie: „to właśnie ten moment" |
| **przecież** | 0,1 / 0,2 | 0 | argument z oczywistości: „przecież wiesz" |
| **jednak** | 0,6 / 0,75 | 0 | kontrast bez „jednakże" |
| **że** | 11 / 18 | 4,7 | AI unika zdań podrzędnych z „że"; człowiek je lubi |
| **ale** | 2,2 / 7,9 | 1,35 | kontrast w środku zdania, nie nowe zdanie od „Jednak" |
| dziś | 0,46 / 0,13 | **3,2** | wyrzuć; „dziś" bez daty to pusty czas |
| zamiast | 0,23 / 0,11 | **1,6** | raz na tekst („Zaczniesz X zamiast Y" to celowy zabieg, nie nawyk) |
| oraz | 0,58 / 0,22 | **1,1** | „i" |
| lecz | 0 / 0,04 | 0,23 | „ale" |
| wreszcie | 0 / 0,09 | 0,45 | usuń |
| ponadto, dodatkowo, co więcej, jednakże, w rezultacie, podsumowując | 0 | rzadko u Claude, często u GPT | usuń zawsze |

## Jak przejść między akapitami po ludzku
1. **Powtórz ostatnie słowo poprzedniego akapitu** na początku następnego („…straconego czasu. Czas to jedyne, czego nie kupisz.").
2. **Pytanie**, na które odpowiada następny akapit („Dlaczego?" i odpowiedź bez „ponieważ": „Bo …").
3. **Konkret zamiast łącznika**: nowy akapit zaczyna się od liczby, daty, nazwiska, godziny.
4. **Kontrast jednym słowem**: „Ale.", „Tyle że…", „Tymczasem…".
5. **Zapowiedź w jednym zdaniu na końcu maila:** „Dowiesz się o nim więcej w następnym mailu."
6. **Bez „Podsumowując"**: tekst kończy się na ostatnim konkrecie albo na CTA.

## Test 300 słów
W 300 słowach copy ma być: ≥1 „bo", ≥1 „że", ≥1 „ale" w środku zdania, 0 „oraz", 0 „ponadto/dodatkowo", ≤1 „dziś", ≤1 „zamiast".
