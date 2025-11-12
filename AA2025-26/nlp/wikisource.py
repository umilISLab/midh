#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import json
import argparse
import re
import urllib.parse as ul
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

WIKIDATA_SPARQL = "https://query.wikidata.org/sparql"
IT_WIKISOURCE_API = "https://it.wikisource.org/w/api.php"

# Periodi storici predefiniti → intervalli (inclusivi)
PERIODI = {
    "medioevo": (1200, 1499),
    "rinascimento": (1500, 1600),
    "seicento": (1601, 1700),
    "settecento": (1701, 1800),
    "illuminismo": (1715, 1799),   # indicativo
    "ottocento": (1801, 1900),
    "risorgimento": (1815, 1871),
    "novecento": (1901, 2000),
    "contemporaneo": (2001, 2100),
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

def guess_period_range(periodo: str):
    p = periodo.lower().strip()
    if p not in PERIODI:
        raise ValueError(
            f"Periodo '{periodo}' non riconosciuto. "
            f"Disponibili: {', '.join(sorted(PERIODI.keys()))}"
        )
    return PERIODI[p]

def build_sparql(start_year: int, end_year: int, limit: int = 2000):
    """
    Cerca opere (item) con:
      - data di pubblicazione P577 nell'intervallo
      - lingua dell'opera P407 = Italiano (Q652)
      - sitelink su it.wikisource.org
    Ritorna titolo della pagina Wikisource + anno.
    """
    query = f"""
SELECT ?item ?itemLabel ?sitelink ?date ?year WHERE {{
  ?item wdt:P577 ?date .
  BIND(YEAR(?date) AS ?year)
  FILTER (?year >= {start_year} && ?year <= {end_year})
  ?item wdt:P407 wd:Q652 .
  ?sitelink schema:about ?item ;
            schema:isPartOf <https://it.wikisource.org/> .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "it,en". }}
}}
LIMIT {limit}
"""
    return query

def run_sparql(query: str):
    r = requests.get(
        WIKIDATA_SPARQL,
        params={"query": query, "format": "json"},
        headers=HEADERS,
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    rows = []
    for b in data.get("results", {}).get("bindings", []):
        sitelink = b["sitelink"]["value"]           # URL it.wikisource.org/.../Titolo
        year = int(b["year"]["value"])
        # Ricava il titolo URL-decoded dopo il path /wiki/
        # Esempio: https://it.wikisource.org/wiki/Divina_Commedia
        title = ul.unquote(sitelink.split("/wiki/")[-1])
        rows.append({"title": title, "year": year, "url": sitelink})
    return rows

def fetch_wikisource_plaintext(title: str):
    """
    Usa action=parse per ottenere l'HTML
    e lo converte in testo (grezzo ma leggibile).
    In alternativa si potrebbe provare prop=extracts&explaintext,
    ma non sempre è attivo/omogeneo su Wikisource.
    """
    params = {
        "action": "parse",
        "page": title,
        "prop": "text",
        "format": "json"
    }
    r = requests.get(IT_WIKISOURCE_API, params=params, headers=HEADERS, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    html = data["parse"]["text"]["*"]

    # Pulisci HTML → testo
    soup = BeautifulSoup(html, "html.parser")

    # Rimuovi tabelle di navigazione, box, note marginali, ecc.
    for sel in [
        ".toc", ".mw-editsection", ".noprint", ".ws-noexport", ".references",
        ".navbox", ".infobox", ".sidenote", ".sidenotes", ".thumb", ".magnify"
    ]:
        for tag in soup.select(sel):
            tag.decompose()

    # Prendi contenuto principale
    content = soup.select_one(".mw-parser-output") or soup
    text = content.get_text("\n", strip=True)

    # Normalizzazioni leggere
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text

def safe_filename(name: str, maxlen=120):
    name = re.sub(r"[\\/:*?\"<>|]", "_", name)
    return name[:maxlen].strip("_ ").strip()

def main():
    ap = argparse.ArgumentParser(
        description="Scarica testi da it.wikisource.org per periodo storico o range di anni (via Wikidata)."
    )
    ap.add_argument("--periodo", type=str, default=None,
                    help=f"Nome di periodo (es: {', '.join(sorted(PERIODI.keys()))})")
    ap.add_argument("--dal", type=int, default=None, help="Anno iniziale (es. 1850)")
    ap.add_argument("--al", type=int, default=None, help="Anno finale (es. 1900)")
    ap.add_argument("--limite", type=int, default=200, help="Numero massimo di opere da considerare")
    ap.add_argument("--delay", type=float, default=1.0, help="Secondi di pausa tra richieste API (rispetto rate-limit)")
    ap.add_argument("--outdir", type=str, default="wikisource_texts", help="Cartella di output")
    args = ap.parse_args()

    if args.periodo:
        start_year, end_year = guess_period_range(args.periodo)
    else:
        if args.dal is None or args.al is None:
            ap.error("Specifica --periodo oppure entrambi --dal e --al.")
        start_year, end_year = args.dal, args.al

    os.makedirs(args.outdir, exist_ok=True)

    print(f"[INFO] Cerco opere in italiano su Wikisource tra {start_year} e {end_year} (limite {args.limite})...")
    q = build_sparql(start_year, end_year, limit=args.limite)
    hits = run_sparql(q)
    if not hits:
        print("[WARN] Nessun risultato dal SPARQL. Prova ad allargare l'intervallo.")
        return

    print(f"[INFO] Trovate {len(hits)} opere candidate.")
    errors = []

    for row in tqdm(hits, desc="Scarico testi"):
        title = row["title"]
        year = row["year"]

        subdir = os.path.join(args.outdir, str(year))
        os.makedirs(subdir, exist_ok=True)

        outpath = os.path.join(subdir, safe_filename(title) + ".txt")
        if os.path.exists(outpath):
            # già scaricato
            continue

        try:
            text = fetch_wikisource_plaintext(title)
            # Filtro banale: evita salvataggi di pagine troppo piccole (probabili indici)
            if len(text.split()) < 200:
                # può essere un indice: salvalo comunque ma segnalo
                note = f"\n\n[NOTA] Il testo potrebbe essere incompleto o una pagina indice ({row['url']})."
                text = text + note

            with open(outpath, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            errors.append({"title": title, "year": year, "error": str(e)})
        finally:
            time.sleep(args.delay)

    print(f"[OK] Download completato in '{args.outdir}'. File totali: "
          f"{sum(1 for _ in _iter_txt(args.outdir))}")

    if errors:
        print(f"[WARN] {len(errors)} errori. Esempi:")
        for e in errors[:5]:
            print(f"  - {e['year']} :: {e['title']} :: {e['error']}")

def _iter_txt(root):
    for base, _, files in os.walk(root):
        for fn in files:
            if fn.lower().endswith(".txt"):
                yield os.path.join(base, fn)

if __name__ == "__main__":
    main()
