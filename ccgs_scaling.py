import os, json, re, math
from PyPDF2 import PdfReader

PDFS = {
    "2023": "atar-frequency-dist-2023.pdf",
    "2024": "atar-frequency-dist-2024.pdf",
    "2025": "atar-frequency-dist-2025.pdf",
}
CACHE_PATH = "atar_cumperc_cache.json"

# (x_percent_of_state_top, y_fraction_top_from_distribution)
CCGS_POINTS = [
    (0.05, 0.0081757271),
    (0.10, 0.0167597765),
    (1.00, 0.1259952857),
    (2.00, 0.2236028880),
    (5.00, 0.3838322909),
    (8.00, 0.5),
]

def _is_step(val, step, eps=1e-9):
    return abs(round(val/step)*step - val) < eps

def parse_pdf_to_atar_cumperc(pdf_path):
    reader = PdfReader(pdf_path)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)

    # grab ints + floats (two decimals)
    tokens = re.findall(r"\d+\.\d{2}|\d+", text)
    parsed = []
    for t in tokens:
        if "." in t:
            parsed.append(float(t))
        else:
            parsed.append(int(t))

    mapping = {}
    i = 0
    n = len(parsed)

    while i + 3 < n:
        a, b, c, d = parsed[i], parsed[i+1], parsed[i+2], parsed[i+3]

        if isinstance(a, float) and isinstance(d, float) and isinstance(b, int) and isinstance(c, int):
            atar = a
            rel = b
            cumf = c
            cump = d

            ok = (
                0.00 <= atar <= 99.95 and _is_step(atar, 0.05) and
                0 <= rel <= 500 and 0 <= cumf <= 200000 and
                0.00 <= cump <= 100.00
            )

            if ok:
                # keep the smallest cumulative % found for that ATAR (should be identical anyway)
                if atar not in mapping or cump < mapping[atar]:
                    mapping[atar] = float(cump)
                i += 4
                continue

        i += 1

    if not mapping:
        raise RuntimeError(f"Failed to parse any ATAR rows from: {pdf_path}")

    return mapping

def load_or_build_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)

    cache = {}
    for year, path in PDFS.items():
        m = parse_pdf_to_atar_cumperc(path)
        cache[year] = {f"{k:.2f}": v for k, v in m.items()}

    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)

    return cache

def cumperc_for_atar(atar, year_map):
    # year_map: dict str->float (ATAR->cum%)
    keys = sorted(float(k) for k in year_map.keys())
    if atar <= keys[0]:
        return year_map[f"{keys[0]:.2f}"]
    if atar >= keys[-1]:
        return year_map[f"{keys[-1]:.2f}"]

    # exact
    k = f"{atar:.2f}"
    if k in year_map:
        return year_map[k]

    # bracket + interpolate
    for lo, hi in zip(keys, keys[1:]):
        if lo <= atar <= hi:
            y1 = year_map[f"{lo:.2f}"]
            y2 = year_map[f"{hi:.2f}"]
            if hi == lo:
                return y1
            return y1 + (atar - lo) * (y2 - y1) / (hi - lo)

    # should never hit
    return year_map[f"{keys[-1]:.2f}"]

def invert_piecewise_linear(y, pts):
    # pts: list of (x, y) with y increasing
    pts = sorted(pts, key=lambda t: t[1])
    ys = [p[1] for p in pts]

    if y <= ys[0]:
        (x1, y1), (x2, y2) = pts[0], pts[1]
        return x1 + (y - y1) * (x2 - x1) / (y2 - y1)
    if y >= ys[-1]:
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        return x1 + (y - y1) * (x2 - x1) / (y2 - y1)

    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if y1 <= y <= y2:
            if y2 == y1:
                return x1
            return x1 + (y - y1) * (x2 - x1) / (y2 - y1)

    return pts[-1][0]

def ccgs_scaled_atar(raw_atar, cache):
    # 1) raw ATAR -> mean top fraction across 3 years
    cumps = []
    for year in ("2023", "2024", "2025"):
        cumps.append(cumperc_for_atar(raw_atar, cache[year]))
    mean_cumperc = sum(cumps) / len(cumps)          # in %
    mean_top_fraction = mean_cumperc / 100.0        # in [0,1]

    # 2) mean top fraction -> x (top % of state) via inverse of CCGS curve
    x_top_percent = invert_piecewise_linear(mean_top_fraction, CCGS_POINTS)

    # 3) convert top% -> ATAR
    scaled_atar = 100.0 - x_top_percent

    # clamp
    scaled_atar = max(0.0, min(99.95, scaled_atar))
    return scaled_atar, mean_cumperc, mean_top_fraction, x_top_percent

def main():
    cache = load_or_build_cache()
    while True:
        s = input("Enter unscaled ATAR (blank to quit): ").strip()
        if not s:
            break
        raw = float(s)
        scaled, mean_cumperc, mean_top_frac, x_top_pct = ccgs_scaled_atar(raw, cache)
        print(f"CCGS scaled ATAR = {scaled:.4f}")

if __name__ == "__main__":
    main()
