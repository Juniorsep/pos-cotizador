# Contexto de continuidad — Cotizador dolpos CRECE+
> Usar este documento como base al iniciar una nueva conversación con Claude para continuar el trabajo sobre pricing y cotizador.

---

## 1. Quién soy y qué estoy construyendo

Soy **Junior**, founder de **dolpos / CRECE+**, un SaaS de punto de venta (POS) orientado a retail en **Chile, Perú y Colombia**. La meta es llegar a **400 UF de MRR en 18 meses**.

El cotizador es una herramienta HTML standalone (sin backend, sin dependencias externas salvo html2canvas + jsPDF) que usan los comerciales para generar propuestas en tiempo real durante o después de una demo, exportarlas como PDF y adjuntarlas al correo de seguimiento.

---

## 2. Arquitectura del cotizador actual

### Archivo
`cotizador-dolpos.html` — HTML completo autocontenido, ~1.554 líneas.

### Flujo de pasos (wizard)
| Paso | Contenido |
|------|-----------|
| 1 | Selección de país (Chile / Perú / Colombia) + tasas de conversión editables |
| 2 | Nombre del cliente + número de empresas |
| 3 | Sucursales por empresa (stepper por empresa) |
| 4 | Usuarios por sucursal — 3 roles con stepper independiente por sucursal |
| 5 | Volúmenes de operación (SKU, boletas/mes, facturas/mes) |
| 6 | Cotización final con desglose, tabla por sucursal, compensación de usuarios, tarifas adicionales de referencia |

### Export
- **📄 Descargar PDF** — abre ventana nueva, usa html2canvas + jsPDF, genera PDF multipágina fiel al diseño visual
- **📷 Exportar imagen** — html2canvas directo, descarga PNG
- Botón PDF abre popup externo para escapar restricciones del iframe

---

## 3. Estructura de precios ACTUAL (en UF — base contractual)

> ⚠️ Esta es la estructura que se va a revisar con benchmark. Documentada aquí para tener la línea base.

### 3.1 Planes base (por sucursal / mes, valor neto)

| Plan | Cajas (Vendedores) | SKU | 🇨🇱 Chile UF | 🇵🇪 Perú / 🇨🇴 Colombia UF |
|------|-------------------|-----|-------------|-------------|
| Basic | 1 | 1.000 | 0,9 UF | 0,6 UF |
| Plus | 2 | 2.000 | 1,5 UF | 1,0 UF |
| Max | 3 | 5.000 | 2,0 UF | 1,5 UF |

> ⚠️ **Actualizado (Ago 2026):** el precio en UF ahora es **por país** (`PLAN_UF` en el código). Chile sostiene tarifas ~2× más altas que PE/CO (mediana de mercado ~1,7 UF vs ~0,9 UF), por eso su ladder es superior. Documentos electrónicos incluidos: ver sección 3.4.

- El plan es **el mismo para todas las sucursales** de un cliente.
- Precio es **por sucursal** — un cliente con 4 sucursales paga `plan.uf × 4`.

### 3.2 Roles de usuario y lógica de compensación

Cada plan incluye N "slots de Vendedor" (= cajas). Los **slots se compensan entre sucursales** (pool global):

```
slots_total = plan.cajas × total_sucursales
users_req   = suma de vendedores configurados en todas las sucursales
users_extra = max(0, users_req - slots_total)
costo_extra = users_extra × 0,3 UF
```

#### Roles y tarifas adicionales

| Rol | Incluido gratis | Tarifa adicional | Acceso |
|-----|----------------|-----------------|--------|
| Rol | Incluido gratis | Acceso |
|-----|----------------|--------|
| 👑 Administrador | 1 por empresa (no consume plan) | Reportería general · control total · sin venta |
| 🧑‍💼 Supervisor | 1 por sucursal | Venta + inventario + promociones + reportes sucursal |
| 🖥️ Vendedor (caja) | Según plan (1/2/3) | Solo venta · proformas · apertura/cierre de caja |

> ⚠️ **Tarifa adicional por país (Ago 2026, `ROLES_UF`)** — alineada a mercado local. En CRECE+ **cada usuario = una caja**, por eso el Vendedor se compara con el precio de CAJA del mercado (Siigo cobra una suscripción completa por caja; Loggro $43.990). Chile mantiene su tarifa (mercado UF alto); Perú y Colombia bajan.

| Rol adicional (UF/mes) | 🇨🇱 Chile | 🇵🇪 Perú | 🇨🇴 Colombia |
|---|---|---|---|
| Administrador | 0,40 | 0,19 | 0,19 |
| Supervisor | 0,50 | 0,30 | 0,25 |
| Vendedor (caja) | 0,30 | 0,30 | 0,25 |

### 3.3 SKU adicionales

- 🇨🇱 Chile / 🇵🇪 Perú: incluidos por plan **1.000 / 2.000 / 5.000**; bloque de 5.000 adicionales = **0,47 UF**.
- 🇨🇴 Colombia (el mercado da SKU ilimitado): incluidos **10.000 / 50.000 / ilimitado**; bloque de 5.000 = **0,17 UF** (solo aplica a Basic/Plus).

### 3.4 Facturación electrónica (DTE / facturas — no boletas)

> ⚠️ **Actualizado (Ago 2026)** según benchmark de mercado. Antes eran 50 DTE incluidos (flat, todos los países). Ahora los **documentos electrónicos incluidos son por país y plan** (por sucursal):

| Plan | 🇨🇱 Chile (facturas/DTE) | 🇵🇪 Perú (CPE) | 🇨🇴 Colombia (facturas DIAN) |
|------|------|------|------|
| Basic | 1.000 | 800 | 1.000 |
| Plus | 3.000 | 2.000 | 3.000 |
| Max | **Ilimitado** | **Ilimitado** | **Ilimitado** |

> El plan **Max incluye documentos electrónicos ilimitados (fair-use) en los 3 países**. Concepto transversal: ventas y recibos/comprobantes de venta siempre ilimitados; el tope aplica solo a documentos electrónicos (DTE).

**Fair-use del "ilimitado" (Colombia Max):** ~10.000 comprobantes/mes **por sucursal**, con **pool a nivel empresa** (se suman entre sucursales, igual que los slots de vendedor). Al superarlo aplica el cobro por excedente.

**Excedente** (se aplica sobre el cupo incluido `inc` de cada país/plan; misma curva para todos):

| Rango sobre el cupo | Costo mensual |
|--------------|--------------|
| Hasta `inc` | UF 0 (incluido) |
| `inc`+1 … `inc`+25 | UF 0,25 |
| `inc`+26 … `inc`+50 | UF 0,50 |
| `inc`+51 … `inc`+150 | UF 1,00 |
| `inc`+151 … `inc`+450 | UF 2,00 |
| Más de `inc`+450 | UF 0,0039 por documento adicional |

### 3.5 Boletas electrónicas adicionales

Las boletas incluidas dependen del plan (Basic 200, Plus 500, Max 1.000 por sucursal).

> ⚠️ En el código actual las boletas **solo alimentan la recomendación de plan** (`recommendPlan`); **no** generan un cargo por excedente en `calcCotizacion`. La tarifa "1 UF por cada 1.000 boletas" está documentada pero no implementada. Los recibos no electrónicos son ilimitados.

---

## 4. Conversión de monedas (tasas editables en el cotizador)

| País | Moneda base | Cadena de conversión | Impuesto |
|------|-------------|---------------------|----------|
| 🇨🇱 Chile | CLP | UF × uf_clp (default: 39.485) | IVA 19% |
| 🇵🇪 Perú | PEN | UF × uf_usd (42) × usd_pen (3,72) | IGV 18% |
| 🇨🇴 Colombia | COP | UF × uf_usd (42) × usd_cop (4.200) | IVA 19% |

Las tasas son **editables por el ejecutivo** en el paso 1 y también en la vista de resultado final (sin tener que volver atrás).

---

## 5. Lógica del cotizador paso a paso (resumen técnico)

```javascript
// Recomendación de plan
function recommendPlan(maxVendedoresPorSuc, sku, boletas):
  if maxVend <= 1 && sku <= 1000 && boletas <= 200 → 'basic'
  if maxVend <= 2 && sku <= 2000 && boletas <= 500 → 'plus'
  else → 'max'

// Cálculo total
ufPlan         = plan.uf × totalSucursales
ufVendExtra    = vendExtra × 0.3
ufAdminExtra   = totalAdminExtra × 0.4
ufSupExtra     = totalSupExtra × 0.5
ufFacturacion  = calcFacturacionExtra(facturas) × totalSucursales
ufNeto         = ufPlan + ufVendExtra + ufAdminExtra + ufSupExtra + ufFacturacion
ufConIva       = ufNeto × (1 + pais.impuesto)
```

---

## 6. Constantes de referencia del negocio

- **Ticket promedio Chile**: ~1,25 UF × sucursales
- **Ticket promedio Perú**: USD 25–35 × sucursales (→ UF via USD)
- **Ticket promedio Colombia**: COP 80.000–100.000 × sucursales (→ UF via USD)
- **Competidores directos**: Siigo, Alegra, Keyfacil, Bsale, Defontana
- **Barrera de precio** en Perú y Colombia vs. competidores locales (~USD 20 Alegra, COP 50k Siigo)
- **Argumento de reencuadre**: USD 30/suc = USD 1/día por caja

---

## 7. Benchmarks de SaaS SMB usados en la estrategia

| Métrica | Valor | Fuente |
|---------|-------|--------|
| Churn mensual SMB | 3–5% | Optifai 2026 N=939 |
| Demo-to-close | 30–38% | Optifai 2026 |
| Churn primeros 90 días | 43% del total | UserMotion 2024 N=1000 |
| Churn best-in-class | 3,5% anual | Recurly 2025 |
| Form fill → demo agendada | 66,7% | Chili Piper 2025 |
| Churn mensual típico SMB | 2–4% | Livmo 2026 |

---

## 8. Contexto de pricing para el benchmark nuevo

### Lo que quiero revisar en la siguiente conversación

Aplicar benchmark de mercado para redefinir la estructura de precios del cotizador. Las preguntas clave que quiero responder:

1. **¿Los planes base (0,6 / 1,0 / 1,5 UF) son competitivos vs. el mercado SaaS POS LATAM?**
2. **¿La diferenciación de precio por rol (0,3 / 0,4 / 0,5 UF) es estándar o hay otra lógica más aceptada?**
3. **¿El precio por SKU (0,47 UF/5k) tiene referentes en el mercado?**
4. **¿Hay una estructura de precios (por transacción, por GMV, flat rate, etc.) más adecuada para el segmento retail LATAM?**
5. **Una vez definida la nueva estructura, actualizar las constantes de precio en el cotizador HTML.**

### Competidores a benchmarkear (mínimo)
- **Bsale** (Chile) — modelo freemium, precio por plan
- **Siigo** (Colombia/Perú) — precio mensual por usuario
- **Alegra** (Colombia/Perú) — precio por empresa + módulos
- **Keyfacil** (Chile) — precio por caja/sucursal
- **Defontana** (Chile) — ERP con POS integrado
- **Poster POS**, **Loyverse**, **Square** — referencias internacionales

---

## 9. Archivos existentes en este proyecto

| Archivo | Descripción |
|---------|-------------|
| `cotizador-dolpos.html` | Cotizador interactivo multi-país (el que se va a actualizar con nuevos precios) |
| `dolpos-tracker.html` | App de seguimiento estratégico 18 meses (pipeline, métricas, plan de acción) |
| `capacitacion-comercial-dolpos.html` | Plan de capacitación 4 semanas para comercial nuevo Perú+Colombia |
| `contexto-cotizador-dolpos.md` | Este archivo — contexto de continuidad |

---

## 10. Instrucciones para Claude en la nueva conversación

```
Tengo un proyecto de pricing para un SaaS POS llamado dolpos / CRECE+,
operando en Chile, Perú y Colombia. Tengo un cotizador en HTML con la
estructura de precios actual documentada en el archivo de contexto adjunto.

Quiero hacer un benchmark de precios contra los principales competidores
(Bsale, Siigo, Alegra, Keyfacil, Defontana, Square, Loyverse) para:
1. Validar si la estructura actual es competitiva
2. Proponer una nueva estructura de precios basada en datos reales
3. Actualizar las constantes de precio en el cotizador HTML

El contexto completo del proyecto está en el documento adjunto.
Las constantes que se deben actualizar en el código están claramente
marcadas en la sección "Estructura de precios actual".
```

---

## 11. Referencia rápida: constantes a modificar en el cotizador

Cuando se defina el nuevo pricing, estos son los únicos valores a cambiar en `cotizador-dolpos.html`:

```javascript
// LÍNEA ~651 — Planes base
const PLANES = {
  basic: { uf: 0.6,  cajas: 1, sku: 1000,  boletas: 200  },
  plus:  { uf: 1.0,  cajas: 2, sku: 2000,  boletas: 500  },
  max:   { uf: 1.5,  cajas: 3, sku: 5000,  boletas: 1000 },
};

// LÍNEA ~601 — Tarifas adicionales por rol
const ROLES = {
  admin: { ufExtra: 0.4 },   // Administrador adicional
  sup:   { ufExtra: 0.5 },   // Supervisor adicional
  vend:  { ufExtra: 0.3 },   // Vendedor adicional
};

// LÍNEA ~1443 — SKU adicionales
const UF_POR_BLOQUE_SKU = 0.47;
const SKU_POR_BLOQUE    = 5000;

// DOCUMENTOS ELECTRÓNICOS incluidos — por país y plan (Ago 2026)
const DTE_INCLUIDOS = {
  cl: { basic: 1000, plus: 3000, max: Infinity },
  pe: { basic: 800,  plus: 2000, max: Infinity },
  co: { basic: 1000, plus: 3000, max: Infinity }, // Max ilimitado (fair-use) en los 3
};
const DTE_FAIRUSE_POR_SUC = 10000; // fair-use por sucursal, pool a nivel empresa

// Precio en UF por país y plan (Chile > PE/CO)
const PLAN_UF = {
  cl: { basic: 0.9, plus: 1.5, max: 2.0 },
  pe: { basic: 0.6, plus: 1.0, max: 1.5 },
  co: { basic: 0.6, plus: 1.0, max: 1.5 },
};
// planUF(paisKey, planKey) → usado en ufPlan y en el precio de sucursal adicional.

// Adicionales (roles) en UF por país
const ROLES_UF = {
  cl: { admin: 0.40, sup: 0.50, vend: 0.30 },
  pe: { admin: 0.19, sup: 0.30, vend: 0.30 },
  co: { admin: 0.19, sup: 0.25, vend: 0.25 },
};
// roleUF(paisKey, role) → usado en ufVendExtra/ufAdminExtra/ufSupExtra, tabla por sucursal y render de roles.

// SKU incluidos por país/plan (solo Colombia difiere; resto usa PLANES[x].sku)
const SKU_INCLUIDOS = { co: { basic: 10000, plus: 50000, max: Infinity } };
// Bloque de 5.000 SKU adicionales en UF por país
const SKU_BLOQUE_UF = { cl: 0.47, pe: 0.47, co: 0.17 };
// skuIncl(paisKey, planKey) y skuBloqueUF(paisKey) → usados en el render de SKU y en recommendPlan.

// calcFacturacionExtra(dte, planKey, paisKey):
//   inc = DTE_INCLUIDOS[paisKey][planKey]
//   si inc === Infinity → 0 (sin cargo; fair-use)
//   ex = max(0, dte - inc); curva de excedente:
//     ex<=25:0.25 · ex<=50:0.5 · ex<=150:1.0 · ex<=450:2.0 · resto: ex*0.0039
// La tabla DTE de referencia (render) se genera dinámicamente a partir de inc.

// Boletas adicionales
// NOTA: en el código actual las boletas SOLO alimentan recommendPlan (umbral 200/500/1000);
// no se cobra excedente de boletas en calcCotizacion. Los "recibos" son ilimitados.
```

---

## 12. Conclusiones & discurso comercial por país (benchmark)

> Base para el discurso de venta. Fundamentos: precio neto, cobertura funcional (21 features), documentos electrónicos y adicionales del benchmark. Técnicas: **venta consultiva + PNL**. Modelo real: **1 empresa → varias sucursales → usuarios/caja por sucursal según plan** (multi-empresa = contrato separado por empresa). El diferenciador estructural es el **manejo multi-sucursal con pool de cajas** (los cupos de vendedor se compensan entre sucursales).

### 🇨🇱 Chile — "La plataforma más completa del mercado, a precio de valor"
- **¿Por qué contratar? (resumen ejecutivo):** obtiene la **cobertura funcional #1 (16/21… 15 tras ajuste multi-empresa)** a precio de valor (Plus ≈ mediana; Max $78.970 vs Bsale Full $114.507), con **reportería con IA** y operación 100% móvil sin instalar, y crece en sucursales sin que el costo lo penalice.
- **Diferenciador:** #1 en cobertura a precio de valor, hecho para crecer en sucursales sin fricción.
- **Ventajas:** multi-sucursal con pool de cajas (Bsale/RelBase/Facto no lo modelan) · reportería con IA (casi único, solo Bicom se acerca) · 100% responsive + app nativa · precio transparente vs Bicom (cotiza caso a caso).
- **Discurso:**
  - *Descubrimiento:* "¿Cuántas horas al mes se van armando reportes? ¿Cuántas cajas necesitas abrir en peak sin trabarte?"
  - *Reencuadre:* "El Max cuesta menos que 2 UF/día por caja — y trae IA que otros cobran aparte o no tienen."
  - *Contraste:* "Bsale Full $114.507 vs CRECE+ Max $78.970, con IA y más control. Más, por menos."
  - *Future pacing:* "Imagina cerrar el mes con tus 3 reportes de IA listos, desde el celular, sin depender del contador."

### 🇵🇪 Perú — "Más completo, por la mitad del ticket de entrada"
- **¿Por qué contratar?** paga el **ticket de entrada más bajo (Basic S/94, ~la mitad de Bsale neto S/160)** y aun así obtiene **IA, crédito a clientes y control multi-sucursal** que ni los caros publicitan.
- **Diferenciador:** entrada imbatible con features premium que el mercado local no incluye (IA, CxC, listas de precio) + crecimiento multi-sucursal con pool de cajas.
- **Ventajas:** precio bajo + valor alto (baratos = limitados; completos no publicitan IA/CxC) · CxC y listas de precio de base · IA incluida (inédito en Perú) · escala sin castigo (usuario=caja compensado); Max con DTE ilimitados.
- **Discurso:**
  - *Descubrimiento:* "¿Le vendes al crédito? ¿Cómo lo controlas? ¿Manejas precios distintos por cliente o canal?"
  - *Reencuadre:* "Por menos que un café al día por caja: facturación SUNAT + IA + crédito a clientes."
  - *Contraste:* "Bsale Básico S/160 vs CRECE+ Basic S/94, con más control."
  - *Future pacing:* "En tu próxima temporada alta sumas cajas el día que las necesitas y las bajas después, sin renegociar el plan."

### 🇨🇴 Colombia — "Cumplimiento DIAN y valor, sin el castigo del 'por caja'"
- **¿Por qué contratar?** **cumple con la DIAN a precio de valor** y crece por sucursales/cajas **sin el sobrecosto del 'por caja' de Siigo** ni los saltos de Defontana — con IA y crédito a clientes de base.
- **Diferenciador:** POS + cumplimiento DIAN a precio de valor, con modelo por sucursal y pool de usuarios (más flexible que el 'por caja' de Siigo).
- **Ventajas:** sin castigo 'por caja' (Siigo = suscripción completa por caja; CRECE+ caja adicional $44.100 compartida entre sucursales) · SKU ilimitado en Plus/Max + IA + CxC + listas de precio · vs Vendty: más fuerte en retail · vs Defontana: sin el salto Starter→Pro +300%.
- **Discurso:**
  - *Descubrimiento:* "¿Cuántos puntos de venta o cajas manejas? ¿Cómo te cobran hoy los documentos electrónicos?"
  - *Reencuadre vs Siigo:* "Con Siigo cada caja nueva = otra suscripción completa. Con CRECE+ sumas cajas por $44.100 — tu crecimiento no te penaliza."
  - *Contraste:* "Defontana salta de $100.000 a $400.000 entre planes; CRECE+ escala parejo."
  - *Future pacing:* "Visualiza abrir tu segundo punto el próximo trimestre: la plataforma ya lo soporta y el costo es predecible."

**Hilo conductor (3 países):** ventas y recibos ilimitados (solo los documentos electrónicos tienen tope) · reportería con IA · crédito a clientes + listas de precio · modelo por sucursal / usuario=caja con pool → **"más valor y crecimiento sin penalización, a precio justo por país"**.

---

*Documento generado el 7 de septiembre de 2026 · Conclusiones comerciales agregadas el 8 de septiembre de 2026 — dolpos CRECE+ · Junior*
