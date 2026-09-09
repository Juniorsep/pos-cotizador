#!/usr/bin/env python3
"""
Reconstruye la suite comercial CRECE+ (crece-suite.html) embebiendo el
cotizador y el benchmark en iframes aislados (sin conflictos de CSS/JS).

Uso:  python3 build_suite.py
Trabaja SIEMPRE dentro de la carpeta donde está este script, así que basta
con tenerlo junto a cotizador-dolpos.html y benchmark.html.
"""
import pathlib

BASE = pathlib.Path(__file__).resolve().parent
COT_FILE   = BASE / "cotizador-dolpos.html"
BENCH_FILE = BASE / "benchmark.html"
OUT_FILE   = BASE / "crece-suite.html"


def esc(s: str) -> str:
    """Escapa para usarse dentro de srcdoc=\"...\" (atributo con comillas dobles)."""
    return s.replace("&", "&amp;").replace('"', "&quot;")


def main() -> None:
    for f in (COT_FILE, BENCH_FILE):
        if not f.exists():
            raise SystemExit(f"No se encontró {f.name} en {BASE}")

    cot = COT_FILE.read_text(encoding="utf-8")
    bench = BENCH_FILE.read_text(encoding="utf-8")

    shell = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CRECE+ Suite Comercial</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&display=swap">
<style>
  :root{{--p900:#130326;--p800:#1e0540;--p700:#3b0764;--p600:#6b21a8;--p500:#9333ea;--p400:#c084fc;--gold:#f5c518;--gold2:#fbbf24}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{height:100%}}
  body{{font-family:'Inter',system-ui,sans-serif;display:flex;height:100vh;overflow:hidden;background:var(--p900);color:#fff}}
  .side{{width:216px;flex:none;background:linear-gradient(180deg,var(--p900),#1a043a 60%,#24074a);
    border-right:1px solid rgba(255,255,255,.08);display:flex;flex-direction:column;padding:22px 14px}}
  .brand{{font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:22px;color:#fff;
    background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:12px;
    padding:12px 14px;text-align:center;letter-spacing:-.01em;margin-bottom:8px}}
  .brand sup{{color:var(--gold2);font-size:13px}}
  .side .subt{{font-size:11px;color:rgba(255,255,255,.4);text-align:center;letter-spacing:.14em;
    text-transform:uppercase;margin-bottom:22px}}
  nav{{display:flex;flex-direction:column;gap:6px}}
  .nav-item{{display:flex;align-items:center;gap:11px;font-family:'Inter',sans-serif;font-weight:600;font-size:14.5px;
    color:rgba(255,255,255,.7);background:transparent;border:0;border-radius:10px;padding:12px 14px;cursor:pointer;
    text-align:left;transition:.15s;width:100%}}
  .nav-item .ic{{font-size:17px;line-height:1}}
  .nav-item:hover{{background:rgba(255,255,255,.06);color:#fff}}
  .nav-item.active{{background:var(--gold);color:var(--p900)}}
  .side-foot{{margin-top:auto;font-size:11px;color:rgba(255,255,255,.35);text-align:center;line-height:1.5}}
  .stage{{flex:1;position:relative;background:var(--p900)}}
  .stage iframe{{position:absolute;inset:0;width:100%;height:100%;border:0;background:var(--p900)}}
  .stage iframe[hidden]{{display:none}}
  @media(max-width:760px){{
    body{{flex-direction:column}}
    .side{{width:100%;flex-direction:row;align-items:center;padding:10px 12px;overflow-x:auto}}
    .brand{{margin:0 10px 0 0;padding:8px 12px;font-size:17px}}
    .side .subt{{display:none}} nav{{flex-direction:row;gap:6px}} .side-foot{{display:none}}
    .nav-item{{padding:9px 12px;white-space:nowrap}}
  }}
</style>
</head>
<body>
  <aside class="side">
    <div class="brand">CRECE<sup>+</sup></div>
    <div class="subt">Suite comercial</div>
    <nav>
      <button class="nav-item active" data-t="cot"><span class="ic">&#129518;</span> Cotizador</button>
      <button class="nav-item" data-t="bench"><span class="ic">&#128202;</span> Benchmark</button>
    </nav>
    <div class="side-foot">CRECE+<br>Chile &middot; Per&uacute; &middot; Colombia</div>
  </aside>
  <main class="stage">
    <iframe id="f-cot" title="Cotizador" srcdoc="{esc(cot)}"></iframe>
    <iframe id="f-bench" title="Benchmark" hidden srcdoc="{esc(bench)}"></iframe>
  </main>
  <script>
    const items=document.querySelectorAll('.nav-item');
    const fCot=document.getElementById('f-cot'), fBench=document.getElementById('f-bench');
    items.forEach(b=>b.addEventListener('click',()=>{{
      items.forEach(x=>x.classList.toggle('active',x===b));
      const t=b.dataset.t;
      fCot.hidden = t!=='cot';
      fBench.hidden = t!=='bench';
    }}));
  </script>
</body>
</html>
"""
    OUT_FILE.write_text(shell, encoding="utf-8")
    print(f"OK -> {OUT_FILE}  ({len(shell):,} bytes)")


if __name__ == "__main__":
    main()
