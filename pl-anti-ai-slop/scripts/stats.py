#!/usr/bin/env python3
"""Statystyki rytmu i składni tekstu (PL/EN). Użycie: stats.py PLIK... [--json] [--dir KATALOG]
Zwraca per plik: zdania, słowa/zdanie (śr., mediana, odch.), burstiness, udział zdań <=5 i >=20 słów,
akapity, % akapitów 1-słowowych, pytania, wykrzykniki, myślniki, spójniki/1000 słów, imiesłowy, strona bierna,
otwieracze z przecinkiem, tricolony, 'nie tylko', liczebniki/1000, nazwy własne/1000."""
import re, sys, json, statistics, pathlib

CONNECTIVES_PL = ["dodatkowo", "ponadto", "co więcej", "warto zauważyć", "należy podkreślić", "podsumowując",
                  "w rezultacie", "w związku z tym", "jednakże", "niemniej jednak", "z kolei", "natomiast",
                  "w efekcie", "co istotne", "co ważne", "przede wszystkim", "ostatecznie", "w konsekwencji",
                  "warto", "dlatego", "bo", "ale", "więc", "a", "i", "że", "bo", "jednak", "choć", "przecież"]
OPENERS_COMMA = r"^(Dodatkowo|Ponadto|Co więcej|Jednakże|Niemniej jednak|W rezultacie|W efekcie|Podsumowując|Ostatecznie|Warto zauważyć, że|Należy podkreślić, że|W konsekwencji|Co istotne|Co ważne|Przede wszystkim|Furthermore|Moreover|Additionally|However|In conclusion|Ultimately),"
IMIESLOW = r"\b\w+(ąc|łszy|wszy)\b"
PASSIVE_PL = r"\b(zosta[łlć]\w*|jest|są|był\w*|będzie|będą)\s+\w+(any|ana|ane|ani|ony|ona|one|eni|ty|ta|te|ci)\b"
PASSIVE_EN = r"\b(is|are|was|were|been|being|be)\s+\w+(ed|en)\b"
SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+(?=[A-ZĄĆĘŁŃÓŚŹŻ0-9„\"“(\[])")

def sentences(par):
    par = re.sub(r"\s+", " ", par.strip())
    return [s for s in SENT_SPLIT.split(par) if len(s.split()) >= 1]

def analyze(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)  # markdown linki
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip() and not p.strip().startswith("#")]
    sents = [s for p in paras for s in sentences(p)]
    wl = [len(s.split()) for s in sents] or [0]
    words = sum(wl) or 1
    mean = statistics.mean(wl); sd = statistics.pstdev(wl) if len(wl) > 1 else 0.0
    pl_words = [len(p.split()) for p in paras] or [0]
    low = text.lower()
    conn = sum(len(re.findall(r"\b" + re.escape(c) + r"\b", low)) for c in CONNECTIVES_PL if len(c) > 2)
    tric = len(re.findall(r"\b\w+, \w+ (i|oraz|and) \w+\b", low))
    tokens = re.findall(r"\b\w+\b", text)
    proper = 0
    for p in paras:
        for s in sentences(p):
            ws = s.split()
            proper += sum(1 for w in ws[1:] if w[:1].isupper() and w.strip("„\"“”(").isalpha())
    return {
        "words": words, "sentences": len(sents), "paragraphs": len(paras),
        "wps_mean": round(mean, 2), "wps_median": statistics.median(wl), "wps_sd": round(sd, 2),
        "burstiness": round(sd / mean, 3) if mean else 0,
        "pct_le5": round(100 * sum(1 for x in wl if x <= 5) / len(wl), 1),
        "pct_ge20": round(100 * sum(1 for x in wl if x >= 20) / len(wl), 1),
        "max_sentence": max(wl),
        "wpp_mean": round(statistics.mean(pl_words), 2),
        "pct_par_1word": round(100 * sum(1 for x in pl_words if x == 1) / len(pl_words), 1),
        "pct_par_1sentence": round(100 * sum(1 for p in paras if len(sentences(p)) == 1) / len(paras), 1) if paras else 0,
        "pct_questions": round(100 * sum(1 for s in sents if s.rstrip().endswith("?")) / len(sents), 1) if sents else 0,
        "pct_exclam": round(100 * sum(1 for s in sents if s.rstrip().endswith("!")) / len(sents), 1) if sents else 0,
        "em_dash": text.count("—"), "en_dash_spaced": len(re.findall(r"\s–\s", text)),
        "hyphen_spaced": len(re.findall(r"\s-\s", text)),
        "connectives_per_1k": round(1000 * conn / words, 1),
        "openers_comma_per_1k": round(1000 * len(re.findall(OPENERS_COMMA, text, re.M)) / words, 2),
        "imieslow_per_1k": round(1000 * len(re.findall(IMIESLOW, low)) / words, 1),
        "passive_per_1k": round(1000 * (len(re.findall(PASSIVE_PL, low)) + len(re.findall(PASSIVE_EN, low))) / words, 1),
        "tricolon_per_1k": round(1000 * tric / words, 2),
        "nie_tylko_per_1k": round(1000 * len(re.findall(r"nie tylko", low)) / words, 2),
        "numerals_per_1k": round(1000 * len(re.findall(r"\b\d[\d.,%]*\b", text)) / words, 1),
        "proper_per_1k": round(1000 * proper / words, 1),
        "bold_pars_pct": round(100 * sum(1 for p in paras if "**" in p) / len(paras), 1) if paras else 0,
        "bullets_gt70": sum(1 for ln in text.splitlines() if re.match(r"^\s*[-*•]\s", ln) and len(ln.strip()) > 70),
    }

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    files = []
    for a in args:
        p = pathlib.Path(a)
        files += sorted(p.rglob("*.txt")) + sorted(p.rglob("*.md")) if p.is_dir() else [p]
    out = {}
    for f in files:
        try: out[str(f)] = analyze(f.read_text(encoding="utf-8", errors="replace"))
        except Exception as e: out[str(f)] = {"error": str(e)}
    if as_json: print(json.dumps(out, ensure_ascii=False, indent=1)); return
    keys = ["words","wps_median","wps_mean","burstiness","pct_le5","pct_ge20","pct_par_1sentence","em_dash","openers_comma_per_1k","imieslow_per_1k","passive_per_1k","tricolon_per_1k","numerals_per_1k"]
    print("\t".join(["file"] + keys))
    for f, r in out.items():
        print("\t".join([pathlib.Path(f).name] + [str(r.get(k, "")) for k in keys]))

if __name__ == "__main__":
    main()
