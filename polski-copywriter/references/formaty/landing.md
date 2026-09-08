# Format: landing page / strona sprzedażowa / opt-in
**Szkielet landinga (12 elementów):** nad-nagłówek → nagłówek pozytywny → subline z bólem → obraz/dowód → problem w 3 scenach (bez teorii między nimi) → mechanizm → oferta (każdy element = 3 konkretne korzyści, nie feature'y) → DLA CIEBIE / NIE DLA CIEBIE (3+3) → kim jest mentor (max 4 akapity, ciągły tekst) → gwarancja z warunkiem → cena i termin → FAQ → CTA (powtórzone). Countdown ≤60 znaków.
**Sabri long-form / opt-in:** , `-opt-in-page`, `-headlines-bullets`; „BEZPŁATNY" zamiast „darmowy" w opt-in.
**DTC (advertorial, listicle):** edukacja, produkt raz i miękko na końcu, oznaczenie materiału komercyjnego.
**Pasmo:** `landing-plynny` dla marek premium (mediana 10–18 słów, ≤5% akapitów 1-słowowych, zero staccato); `generic` dla reszty. Bullety ≤70 znaków. Zero myślników. Kolumny równe.
**Kontrola:** `check_copy.py --format landing`: nad-nagłówek nad każdą sekcją H2, obecność obu list DLA/NIE DLA, brak „ZASADA #", bullety, EFSA jeśli rejestr suplementowy.

## List sprzedażowy long-form (format `list`, wzorzec: dwa polskie listy sprzedażowe, rozbiór w ciag-mysli.md)
**Pasmo `list-sprzedazowy` (zmierzone):** mediana 6–10 słów, ≥20% zdań ≤5 słów, ≤8% ≥20, ≥70% akapitów jednozdaniowych, pytania 3–9%, **liczebniki ≥30/1000** (zmierzone na wzorcach: 49 i 71), 0 myślników, otwieracze z przecinkiem 0.
**Szkielet 13 taktów i 12 zdań-mostów:** `references/ciag-mysli.md`. Zdania z adnotacją: `skladnia-i-rytm.md` §11.
**Oś:** dowód z groszami → diagnoza rynku (3–4 klęski osobno) → prawdziwy motyw → ostrzeżenie → metoda z przykładem z branży czytelnika → „to nie jest łatwe” ×4–6 → „Ale może być.” → fascinations → bonusy w zł → cena przez koszt alternatywy → „Wiem, co powiesz” → powód niskiej ceny → gwarancja w 3 zdaniach → stos → blok „Tak, [imię]!” → PS/PPS.
**Wyjątki formatu:** gęste pogrubienia, „Podsumowując” jako nagłówek stosu, proste cudzysłowy w cytatach nie są śladem (check_copy je wyłącza dla `--format list`).
**Kontrola:** `check_copy.py --format list --register <rejestr>`.
