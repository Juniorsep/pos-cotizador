# CRECE+ · Suite Comercial

Herramientas comerciales de **CRECE+** (POS / gestión comercial) para **Chile · Perú · Colombia**:
un **cotizador** de propuestas y un **benchmark** de mercado, unificados en una sola app con menú lateral.

🔗 **En vivo (GitHub Pages):** https://juniorsep.github.io/pos-cotizador/

---

## Qué incluye

| Herramienta | Descripción |
|---|---|
| **Cotizador** | Wizard de 6 pasos (país → cliente → sucursales → usuarios → volúmenes → cotización). Precios en **UF por país**, documentos electrónicos y adicionales (roles, SKU) alineados a mercado local. Exporta PDF/imagen. |
| **Benchmark** | Comparador de precios y funcionalidades vs. la competencia por país: escaleras de precio, banda de mercado, simulador, matriz funcional (21 features), documentos electrónicos, adicionales y **conclusión comercial** (diferenciador + discurso de venta consultiva/PNL). |

Ambas comparten la identidad visual (violeta/dorado, CRECE+).

---

## Estructura del repositorio

| Archivo | Rol |
|---|---|
| `index.html` | **Lo que sirve GitHub Pages** = copia de `crece-suite.html`. |
| `crece-suite.html` | Suite unificada: sidebar + cotizador y benchmark embebidos en iframes aislados (evita choques de CSS/JS). Archivo autocontenido. |
| `cotizador-dolpos.html` | Cotizador standalone. |
| `benchmark.html` | Benchmark standalone. |
| `build_suite.py` | Regenera `crece-suite.html` embebiendo los dos anteriores. Autoubicado (trabaja en su propia carpeta). |
| `deploy.sh` | Regenera la suite, actualiza `index.html`, hace commit y push en un paso. |
| `contexto-cotizador-dolpos.md` | Contexto del proyecto: estructura de precios, conversión de monedas, lógica del cotizador y **discurso comercial por país**. |
| `Benchmark 1.0.pages` | Documento fuente original (no se versiona; en `.gitignore`). |

> La suite **embebe** copias del cotizador y el benchmark. Si editas cualquiera de los dos, hay que **regenerar** la suite (ver abajo) para que el cambio se refleje.

---

## Publicar cambios

Editas `cotizador-dolpos.html` o `benchmark.html` y luego, desde la carpeta del proyecto:

```bash
./deploy.sh                       # mensaje de commit por defecto
./deploy.sh "Ajusta precios CO"   # con mensaje propio
```

El script: `build_suite.py` → `cp crece-suite.html index.html` → `git add/commit/push`.
En 1–3 minutos se actualiza la página (recarga con **Cmd+Shift+R**).

### Regenerar la suite manualmente
```bash
python3 build_suite.py
```

---

## Notas técnicas

- **Sin dependencias de build**: HTML/CSS/JS puro. Solo `build_suite.py` (Python 3 estándar) para ensamblar la suite.
- **Fuentes**: Inter + Space Grotesk (Google Fonts).
- **Multi-moneda**: UF → CLP / (USD →) PEN / (USD →) COP, con tasas editables por el ejecutivo en el paso 1.
- **Modelo de precios**: 1 empresa → varias sucursales → usuarios/caja por sucursal según plan. UF, documentos electrónicos y adicionales varían por país.
