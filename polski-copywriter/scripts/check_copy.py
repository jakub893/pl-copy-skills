#!/usr/bin/env python3
"""Kontrola copy: lint śladów z rejestrem + pasmo rytmu + kontrole formatu.
Użycie: check_copy.py PLIK --register NAZWA --format mail|reklama|landing|list|vsl|social [--json]
Kod wyjścia 1 gdy są twarde błędy."""
import sys, json, re, pathlib, subprocess
HERE = pathlib.Path(__file__).resolve().parent
SLOP = HERE.parent.parent / "pl-anti-ai-slop/scripts"
sys.path.insert(0, str(SLOP))
import yaml
from stats import analyze
def arg(n, d=None):
    return sys.argv[sys.argv.index(n) + 1] if n in sys.argv and sys.argv.index(n) + 1 < len(sys.argv) else d
path = next((a for a in sys.argv[1:] if not a.startswith("--") and sys.argv[sys.argv.index(a) - 1] not in ("--register", "--format")), None)
if not path: print(__doc__); sys.exit(2)
reg = arg("--register", "generic"); fmt = arg("--format", "mail")
text = pathlib.Path(path).read_text(encoding="utf-8")
regp = HERE.parent / "references/registers" / f"{reg}.md"
rmeta = yaml.safe_load(re.match(r"^---\n(.*?)\n---", regp.read_text(), re.S).group(1)) if regp.exists() else {}
# list sprzedażowy i landing mają prawo do pogrubień i nagłówka „Podsumowując” nad stosem oferty
FMT_EXEMPT = {"landing": "pl-formatowanie-nadmiar-pogrubien,pl-formatowanie-nadmierne-pogrubienia,pl-formatowanie-cudzyslowy-proste,pl-leksyka-podsumowujac,pl-struktura-akapit-podsumowujacy",
              "list": "pl-formatowanie-nadmiar-pogrubien,pl-formatowanie-nadmierne-pogrubienia,pl-formatowanie-cudzyslowy-proste,pl-leksyka-podsumowujac,pl-struktura-akapit-podsumowujacy"}
lint = json.loads(subprocess.run([sys.executable, str(SLOP / "lint_pl.py"), path, "--register", reg, "--json"] + (["--exempt", FMT_EXEMPT[fmt]] if fmt in FMT_EXEMPT else []), capture_output=True, text=True).stdout)
st = analyze(text)
issues = []
def hard(msg): issues.append({"severity": 3, "msg": msg})
def warn(msg): issues.append({"severity": 2, "msg": msg})
# pasmo
# długość zdania to sprawa marki (rejestr), wariancja rytmu to sprawa medium (format)
FMT_BAND = {"social": "codzienny", "vsl": "codzienny", "list": "list-sprzedazowy"}
band = rmeta.get("band", "generic")
_all = json.loads((SLOP.parent / "references/targets.json").read_text())
targets = dict(_all.get(band, {}))
if fmt == "list":
    band = "list-sprzedazowy"; targets = dict(_all.get(band, {}))
elif fmt in FMT_BAND:
    for k in ("burstiness", "pct_par_1sentence", "pct_le5"):
        if k in _all.get(FMT_BAND[fmt], {}): targets[k] = _all[FMT_BAND[fmt]][k]
for k, (lo, hi) in targets.items():
    v = st.get(k)
    if v is not None and not (lo <= v <= hi): warn(f"pasmo {band}: {k}={v} poza [{lo}, {hi}]")
# format
low = text.lower()
first = re.sub(r"^\s*(temat:.*\n)?", "", text, flags=re.I).strip().split("\n")[0]
first_words = len(re.findall(r"\w+", first.split(".")[0]))
if fmt in ("mail", "reklama", "vsl") and first_words > 6: warn(f"pierwsze zdanie ma {first_words} słów (2–5)")
if fmt == "mail":
    m = re.search(r"^temat:\s*(.+)$", text, re.I | re.M)
    if m and len(m.group(1).split()) > 8: warn("temat maila dłuższy niż 8 słów")
    ctas = len(re.findall(r"\[(link|tutaj|kliknij)[^\]]*\]|https?://|\bkliknij\b|\bzapisz się\b|\bzarezerwuj\b|\bkup\b|\bzamów\b", low))
    if ctas == 0: warn("brak CTA"); 
    if ctas > 3: warn(f"{ctas} wezwań do działania (jedno CTA na mail)")
if fmt in ("landing", "list"):
    h2 = re.findall(r"^##\s+.+$", text, re.M)
    if h2 and not re.search(r"^\*[^*\n]{3,40}\*\s*$|^#{3,6}\s.+\n+^##\s", text, re.M): warn("brak nad-nagłówków (etykieta 3–6 słów nad sekcją)")
    if "dla ciebie" in low and "nie dla ciebie" not in low: warn("jest DLA CIEBIE, brak NIE DLA CIEBIE (zawsze obie listy 3+3)")
    if re.search(r"zasada\s*#\s*\d", low): hard("formatowanie „ZASADA #1” zakazane")
if fmt == "vsl":
    scenes = len(re.findall(r"\b\d{1,2}[:.]\d{2}\b|\bo (siódmej|ósmej|dziewiątej|szóstej|dziesiątej|jedenastej|czternastej|piętnastej|szesnastej|osiemnastej|dwudziestej)\b", low))
    if scenes < 3: warn(f"{scenes} scen z godziną (minimum 3)")
    if st["pct_questions"] < 3: warn("mniej niż 3% pytań (mowa potrzebuje pytań)")
for rv in rmeta.get("required_verbs") or []:
    pass
if rmeta.get("required_verbs"):
    claims = re.findall(r"\b(wp[łl]ywa\w*|pomaga\w*|wspiera\w*)\b", low)
    if not claims: warn(f"rejestr {reg}: brak czasowników EFSA (wpływa/pomaga/wspiera) przy korzyściach")
for ph in rmeta.get("required_phrases") or []:
    if ph.lower() not in low: hard(f"rejestr {reg}: brak wymaganej frazy „{ph}”")
# test 300 słów spójników
w = st["words"]
if w >= 300:
    for c, mn in (("bo", 1), ("że", 1)):
        if len(re.findall(r"(?<!\w)" + c + r"(?!\w)", low)) < mn: warn(f"test spójników: brak „{c}” w {w} słowach (AI-owy brak mowy)")
    if re.search(r"(?<!\w)oraz(?!\w)", low): warn("„oraz” → „i”")
hard_n = lint["summary"]["hard"] + sum(1 for i in issues if i["severity"] == 3)
out = {"register": reg, "format": fmt, "lint": lint["summary"], "lint_hits": lint["hits"], "format_issues": issues, "stats": {k: st[k] for k in ("words", "wps_median", "burstiness", "pct_le5", "pct_ge20", "pct_par_1sentence", "pct_questions", "numerals_per_1k", "em_dash")}, "hard_total": hard_n}
if "--json" in sys.argv: print(json.dumps(out, ensure_ascii=False, indent=1))
else:
    for h in lint["hits"]: print(f"{h['line']}:{h['col']} [S{h['severity']}] {h['id']}: \"{h['match']}\" -> {h['fix']}")
    for i in issues: print(f"[S{i['severity']}] {i['msg']}")
    print(f"\n{reg}/{fmt} · {w} słów · mediana {st['wps_median']} · burst {st['burstiness']} · ≤5 {st['pct_le5']}% · 1zd {st['pct_par_1sentence']}% · liczby {st['numerals_per_1k']}/1k · TWARDE {hard_n} · ostrzeżenia {lint['summary']['warn'] + sum(1 for i in issues if i['severity']==2)}")
sys.exit(1 if hard_n else 0)
