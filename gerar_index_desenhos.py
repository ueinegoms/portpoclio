#!/usr/bin/env python3
"""
Escaneia a pasta ./desenhos e injeta a lista de imagens direto no index.html
como window.DESENHOS_INDEX — compatível com file://, sem precisar de servidor.

Uso:
    python gerar_index_desenhos.py

Rode sempre que adicionar ou remover imagens da pasta.
"""

import json
import re
import sys
from pathlib import Path

PASTA      = Path(__file__).parent / "desenhos"
INDEX_HTML = Path(__file__).parent / "index.html"
EXTENSOES  = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

MARKER_START = "/* __DESENHOS_INDEX_START__ */"
MARKER_END   = "/* __DESENHOS_INDEX_END__ */"

def main():
    if not PASTA.exists():
        print(f"[erro] Pasta '{PASTA}' não encontrada.")
        sys.exit(1)

    if not INDEX_HTML.exists():
        print(f"[erro] '{INDEX_HTML}' não encontrado.")
        sys.exit(1)

    arquivos = sorted(
        f.name for f in PASTA.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSOES
    )

    if not arquivos:
        print(f"[aviso] Nenhuma imagem encontrada em '{PASTA}'.")

    # Bloco que será injetado no HTML
    lista_json = json.dumps(arquivos, ensure_ascii=False)
    bloco = f"{MARKER_START}\nwindow.DESENHOS_INDEX = {lista_json};\n{MARKER_END}"

    html = INDEX_HTML.read_text(encoding="utf-8")

    # Se os markers já existem, substitui só o conteúdo entre eles
    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        re.DOTALL
    )

    if pattern.search(html):
        novo_html = pattern.sub(bloco, html)
    else:
        # Primeira vez: injeta antes do fechamento do </head>
        if "</head>" not in html:
            print("[erro] Não encontrei </head> no index.html.")
            sys.exit(1)
        novo_html = html.replace(
            "</head>",
            f"<script>\n{bloco}\n</script>\n</head>"
        )

    INDEX_HTML.write_text(novo_html, encoding="utf-8")

    print(f"[ok] {len(arquivos)} imagem(ns) injetada(s) no index.html")
    for nome in arquivos:
        print(f"     • {nome}")

if __name__ == "__main__":
    main()
