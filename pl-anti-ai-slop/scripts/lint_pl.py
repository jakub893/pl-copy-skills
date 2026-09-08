#!/usr/bin/env python3
"""Linter śladów AI dla polskiego i angielskiego.
Użycie: lint_pl.py PLIK|- [--lang auto|pl|en] [--register NAZWA] [--json] [--stats] [--threshold N] [--tells PLIK]
Wyjście: linia:kol [S3] id: "dopasowanie" -> poprawka. Kod wyjścia 1, gdy twardych trafień > threshold (domyślnie 0 przy --threshold, inaczej 0 zawsze)."""
import re, sys, json, pathlib, statistics
try:
    import yaml
except ImportError:
    print("brak PyYAML: pip3 install pyyaml", file=sys.stderr); sys.exit(2)

HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
TELLS_DEFAULT = SKILL / "references/tells.yaml"
REGISTER_DIRS = [SKILL / "references/registers", SKILL.parent / "polski-copywriter/references/registers"]
sys.path.insert(0, str(HERE))

def arg(name, default=None):
    if name in sys.argv:
        i = sys.argv.index(name)
        return sys.argv[i + 1] if i + 1 < len(sys.argv) else default
    return default

def load_register(name):
    if not name: return {}
    for d in REGISTER_DIRS:
        p = d / f"{name}.md"
        if p.exists():
            m = re.match(r"^---\n(.*?)\n---", p.read_text(encoding="utf-8"), re.S)
            return yaml.safe_load(m.group(1)) if m else {}
    print(f"uwaga: rejestr '{name}' nie znaleziony, używam generic", file=sys.stderr)
    return {}

def detect_lang(text):
    pl = len(re.findall(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]", text))
    return "pl" if pl / max(len(text), 1) > 0.004 else "en"

def sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s for s in re.split(r"(?<=[.!?…])\s+(?=[A-ZĄĆĘŁŃÓŚŹŻ0-9„\"“(\[])", text) if s.strip()]

def main():
    src = [a for a in sys.argv[1:] if not a.startswith("--") and (sys.argv[sys.argv.index(a) - 1] not in ("--lang", "--register", "--threshold", "--tells", "--format", "--exempt"))]
    if not src: print(__doc__); sys.exit(2)
    text = sys.stdin.read() if src[0] == "-" else pathlib.Path(src[0]).read_text(encoding="utf-8", errors="replace")
    if "--strip-notes" in sys.argv:  # odetnij notę „Do decyzji / Co sprawdzono" z końca dostawy
        text = re.split(r"\n(?:---\n)?\s*\*{0,2}(Do decyzji|Co sprawdzono|Nota|Uwagi)\*{0,2}\s*:?", text)[0]
    lang = arg("--lang", "auto"); lang = detect_lang(text) if lang == "auto" else lang
    reg_name = arg("--register"); reg = load_register(reg_name)
    tells = yaml.safe_load(pathlib.Path(arg("--tells", TELLS_DEFAULT)).read_text(encoding="utf-8")) or []
    exempt = set(reg.get("exempt_tells") or []) | set((arg("--exempt") or "").split(",")) - {""}
    lines = text.split("\n")
    line_starts = []; pos = 0
    for ln in lines: line_starts.append(pos); pos += len(ln) + 1
    def linecol(off):
        import bisect
        i = bisect.bisect_right(line_starts, off) - 1
        return i + 1, off - line_starts[i] + 1
    words = max(len(re.findall(r"\w+", text)), 1)
    hits = []
    for t in tells:
        if t.get("lang") not in (lang, "both"): continue
        if t["id"] in exempt or reg_name in (t.get("registers_exempt") or []): continue
        pat = t.get("pattern")
        if not pat: continue
        flags = re.M | re.U | (0 if t.get("case_sensitive") else re.I)
        try: rx = re.compile(pat, flags)
        except re.error as e: print(f"zły regex {t['id']}: {e}", file=sys.stderr); continue
        ms = list(rx.finditer(text))
        if not ms: continue
        cap = t.get("max_per_1000w")
        if cap is not None and 1000 * len(ms) / words <= cap: continue
        for m in ms:
            l, c = linecol(m.start())
            hits.append({"line": l, "col": c, "severity": int(t.get("severity", 2)), "id": t["id"], "match": m.group(0)[:60].replace("\n", " "), "fix": t.get("fix", ""), "category": t.get("category")})
    # kontrole strukturalne
    max_bul = int(reg.get("bullets_max_chars", 70))
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if re.match(r"^[-*•]\s", s) and len(s) > max_bul:
            hits.append({"line": i, "col": 1, "severity": 2, "id": "struct-bullet-za-dlugi", "match": s[:60], "fix": f"bullet max {max_bul} znaków: skróć albo rozbij", "category": "formatowanie"})
    max_sw = int(reg.get("max_sentence_words", 30))
    off = 0
    for par in re.split(r"\n\s*\n|\n(?=\s*[-*•]\s)|\n(?=\s*\d+[.)]\s)", text):
        for s in sentences(par):
            n = len(s.split())
            if n > max_sw:
                l, c = linecol(text.find(s[:40], off) if text.find(s[:40], off) >= 0 else off)
                hits.append({"line": l, "col": c, "severity": 2, "id": "struct-zdanie-za-dlugie", "match": s[:60], "fix": f"{n} słów; podziel na dwa (limit {max_sw})", "category": "skladnia"})
        off += len(par)
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip() and not p.strip().startswith("#")]
    if len(paras) >= 4 and sum(1 for p in paras if "**" in p) / len(paras) > 0.5:
        hits.append({"line": 1, "col": 1, "severity": 2, "id": "pl-formatowanie-kazdy-akapit-bold", "match": f"{sum(1 for p in paras if '**' in p)}/{len(paras)} akapitów z pogrubieniem", "fix": "pogrubienie tylko tam, gdzie oko ma się zatrzymać", "category": "formatowanie"})
    for w in (reg.get("banned_words") or []):
        for m in re.finditer(r"\b" + re.escape(w) + r"\w*", text, re.I):
            l, c = linecol(m.start()); hits.append({"line": l, "col": c, "severity": 3, "id": f"register-banned-{w}", "match": m.group(0), "fix": f"słowo zakazane w rejestrze {reg_name}", "category": "rejestr"})
    for pat in (reg.get("forbidden_patterns") or []):
        for m in re.finditer(pat, text, re.I | re.M):
            l, c = linecol(m.start()); hits.append({"line": l, "col": c, "severity": 3, "id": "register-forbidden-pattern", "match": m.group(0)[:60], "fix": f"wzorzec zakazany w rejestrze {reg_name}: {pat}", "category": "rejestr"})
    # deduplikacja: kilka śladów łapiących ten sam fragment -> zostaje najostrzejszy
    best = {}
    for h in hits:
        k = (h["line"], h["col"], h["match"][:25].lower())
        if k not in best or h["severity"] > best[k]["severity"]: best[k] = h
    hits = list(best.values())
    hits.sort(key=lambda h: (h["line"], h["col"]))
    summary = {"words": words, "lang": lang, "register": reg_name or "generic", "hard": sum(1 for h in hits if h["severity"] == 3), "warn": sum(1 for h in hits if h["severity"] == 2), "hint": sum(1 for h in hits if h["severity"] == 1), "hard_per_1k": round(1000 * sum(1 for h in hits if h["severity"] == 3) / words, 2)}
    stats = None
    if "--stats" in sys.argv:
        try:
            from stats import analyze
            stats = analyze(text)
            tp = SKILL / "references/targets.json"
            if tp.exists():
                bands = json.loads(tp.read_text()).get(reg_name or "generic") or json.loads(tp.read_text()).get("generic", {})
                stats["band_check"] = {k: (stats.get(k), v) for k, v in bands.items() if not (isinstance(v, list) and v[0] <= (stats.get(k) or 0) <= v[1])}
        except Exception as e:
            stats = {"error": str(e)}
    if "--json" in sys.argv:
        print(json.dumps({"summary": summary, "hits": hits, "stats": stats}, ensure_ascii=False, indent=1))
    else:
        for h in hits: print(f"{h['line']}:{h['col']} [S{h['severity']}] {h['id']}: \"{h['match']}\" -> {h['fix']}")
        print(f"\n{summary['words']} słów · {lang} · rejestr {summary['register']} · twarde {summary['hard']} · ostrzeżenia {summary['warn']} · wskazówki {summary['hint']} · twarde/1000 = {summary['hard_per_1k']}")
        if stats: print("stats:", json.dumps(stats, ensure_ascii=False))
    th = arg("--threshold")
    if th is not None and summary["hard"] > int(th): sys.exit(1)

if __name__ == "__main__":
    main()
