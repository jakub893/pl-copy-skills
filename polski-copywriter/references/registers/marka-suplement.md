---
name: marka-suplement
adresat: Ty / bezosobowo (mieszana demografia)
plec: neutralna
band: generic
max_sentence_words: 22
bullets_max_chars: 70
exempt_tells: []
forbidden_patterns: ['\b(leczy|wyleczy|uleczy|zwalcza|gwarantuje|zapobiega|obni[żz]a|likwiduje|usuwa)\b', 'czujesz różnicę']
required_verbs: [wpływa, pomaga, wspiera]
---
# Rejestr marka-suplement — przykład rejestru z twardym compliance (EFSA)

Rejestr pokazuje, jak wpiąć wymogi regulacyjne w linter. Podmień pod własną kategorię.

**EFSA (twarde):** o działaniu wyłącznie czasownikami **wpływa / pomaga / wspiera**. Zakaz obietnic zdrowotnych: „leczy", „zwalcza", „gwarantuje", „pożegnaj zmęczenie", „czujesz różnicę". W trzech kolumnach korzyści użyj wszystkich trzech czasowników.

`forbidden_patterns` i `required_verbs` we frontmatterze sprawiają, że `check_copy.py` zwraca twardy błąd, gdy w copy pada obietnica lecznicza albo brakuje czasowników dopuszczonych.

**Copy reklamowe:** zero em-dash i en-dash w renderowanym tekście. Edukacja przed sprzedażą, produkt jako wniosek, nie jako krzyk.

Zdania wzorcowe:
1. selen pomaga zachować zdrowe włosy i paznokcie.
2. Cynk wpływa na prawidłową pracę układu odpornościowego.
3. Kilka kropli do szklanki wody rano.
