# Rejestry — przełącznik marki

Jeden rejestr na zadanie. Wybór po słowie-kluczu z briefu. Brak dopasowania → `generic`.

W repozytorium są trzy rejestry przykładowe. Prawdziwe rejestry marek (z cenami, progami, nazwiskami i regułami compliance) trzymaj lokalnie, poza repo.

| Kiedy | Rejestr | Adresat | Rytm |
|---|---|---|---|
| brak dopasowania, mieszana grupa | `generic` | bezosobowo | 12–15 słów, bullety ≤70 |
| usługa dla właścicieli sklepów (B2B) | `sklep-ecommerce` | Ty wprost | nagłówek woła branżę, bez żargonu |
| suplement, kosmetyk, kategoria regulowana | `marka-suplement` | Ty / bezosobowo | tylko czasowniki dopuszczone (EFSA) |

## Jak dodać własny rejestr
Utwórz `registers/<nazwa>.md` z frontmatterem YAML. `lint_pl.py --register <nazwa>` i `check_copy.py --register <nazwa>` czytają go automatycznie.

```yaml
---
name: moja-marka
adresat: Ty wprost | bezosobowo | Pan/Pani
plec: neutralna | męska
band: generic | mail-sprzedazowy | landing-plynny | codzienny | list-sprzedazowy
max_sentence_words: 22
bullets_max_chars: 70
exempt_tells: [pl-zwrot-do-czytelnika-czas-przeszly-plciowy]   # ślady wyłączone w tym rejestrze
banned_words: [żargon, którego, marka, nie, używa]
forbidden_patterns: ['\bleczy\b']                              # twardy błąd przy trafieniu
required_verbs: [wpływa, pomaga, wspiera]                      # ostrzeżenie, gdy żadnego nie ma
---
```
Pod frontmatterem: głos marki w kilku zdaniach, twarde reguły, 3–5 zdań wzorcowych.
