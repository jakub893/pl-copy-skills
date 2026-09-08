#!/usr/bin/env python3
"""Generuje references/tells-pl.md, tells-en.md i zamienniki.md z tells.yaml (jedyne źródło prawdy)."""
import yaml, pathlib, collections
R = pathlib.Path(__file__).resolve().parent.parent / "references"
tells = yaml.safe_load((R / "tells.yaml").read_text(encoding="utf-8"))
CAT = {"leksyka": "Leksyka (słowa nadużywane)", "kalka": "Kalki z angielskiego", "skladnia": "Składnia", "interpunkcja": "Interpunkcja",
 "struktura": "Struktura i retoryka", "ton": "Ton (pochlebstwa, hedging)", "formatowanie": "Formatowanie", "zwrot-do-czytelnika": "Zwrot do czytelnika"}
for lang, fname, title in (("pl", "tells-pl.md", "Ślady AI po polsku"), ("en", "tells-en.md", "AI tells in English")):
 items = [t for t in tells if t.get("lang") == lang]
 by = collections.defaultdict(list)
 for t in items: by[t.get("category", "inne")].append(t)
 out = [f"# {title} — {len(items)} śladów (generowane z tells.yaml, nie edytować ręcznie)\n",
 "Kolumny: S = ważność (3 twarde, 2 ostrzeżenie, 1 wskazówka); AI/1k i ludzie/1k = częstość na 1000 słów w próbkach AI vs korpusie ludzkim (polskie maile sprzedażowe, felieton, reportaż, blogi); ratio = AI/ludzie (99 = u ludzi 0).\n",
 "## Spis\n" + "\n".join(f"- {CAT.get(c, c)} ({len(v)})" for c, v in sorted(by.items(), key=lambda x: -len(x[1]))) + "\n"]
 for c, v in sorted(by.items(), key=lambda x: -len(x[1])):
 out.append(f"\n## {CAT.get(c, c)}\n\n| S | id | przykład | poprawka | AI/1k | ludzie/1k | ratio |\n|---|---|---|---|---|---|---|")
 for t in sorted(v, key=lambda t: (-int(t.get("severity", 2)), t["id"])):
 ex = str(t.get("example", "")).replace("|", "/").replace("\n", " ")[:90]; fx = str(t.get("fix", "")).replace("|", "/").replace("\n", " ")[:110]
 out.append(f"| {t.get('severity', 2)} | `{t['id']}` | {ex} | {fx} | {t.get('freq_ai_per_1k', '')} | {t.get('freq_human_per_1k', '')} | {t.get('corpus_ratio', '')} |")
 (R / fname).write_text("\n".join(out) + "\n", encoding="utf-8")
# zamienniki: leksyka + kalka PL z polem fix
z = ["# Zamienniki — słowo AI → ludzki polski (generowane z tells.yaml)\n", "| zamiast | użyj |\n|---|---|"]
for t in sorted([t for t in tells if t.get("lang") == "pl" and t.get("category") in ("leksyka", "kalka", "ton") and t.get("fix")], key=lambda t: t["id"]):
 z.append(f"| {str(t.get('example','')).replace('|','/')[:70]} | {str(t['fix']).replace('|','/')[:120]} |")
(R / "zamienniki.md").write_text("\n".join(z) + "\n", encoding="utf-8")
print({l: sum(1 for t in tells if t.get("lang") == l) for l in ("pl", "en")}, "-> tells-pl.md, tells-en.md, zamienniki.md")
