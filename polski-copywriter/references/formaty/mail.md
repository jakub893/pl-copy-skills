# Format: mail sprzedażowy / kolejka
**Pasmo (targets.json `mail-sprzedazowy`, zmierzone na polskich mailach sprzedażowych):** mediana 6–11 słów/zdanie, ≥22% zdań ≤5 słów, ≤10% zdań ≥20 słów, ≥70% akapitów jednozdaniowych, 0 myślników, 0 „Dodatkowo,", strona bierna ≤2/1000.
**Szkielet:** temat (2–6 słów, bez wersalików, bez „[Imię], …" jeśli brak personalizacji) → pierwsze zdanie 2–5 słów → scena/historia/rachunek → mechanizm w 1–2 zdaniach → dowód (liczba, nazwisko) → jedno CTA → podpis → PS (opcjonalnie: druga pętla).
**Kolejka:** każdy mail otwiera pętlę na następny („Jutro dostaniesz odpowiedź"). Podgrzewacz → historia → zaproszenie → sprzedaż z terminem → wartość → deadline. 5 alternatywnych tematów do każdego maila .
**Rejestr decyduje o „Ty":** rejestr marki.
**Kontrola:** `check_copy.py --format mail --register X`: temat ≤ 8 słów, 1 CTA, pasmo, lint.
