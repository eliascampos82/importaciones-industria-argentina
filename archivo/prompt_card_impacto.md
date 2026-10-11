# Prompt: tarjetas de impacto (formato afiche)

Especificación completa y reutilizable del formato de tarjeta «de impacto» para mostrar cifras clave en dashboards, informes o presentaciones.
No trae contenido: define **cada parte de la tarjeta, sus medidas, colores, tipografías, la grilla donde se ubican y las reglas** a las que se llegó después de muchas iteraciones.

Al final hay un **prompt listo para copiar y pegar** (sección 12) y una **plantilla HTML/CSS de referencia** (sección 13).

---

## 1. Idea en una frase

Cada tarjeta es un **afiche**: una cifra gigante que se lee de un golpe, debajo una frase corta en mayúsculas que dice **qué significa** esa cifra,
y abajo, chico, el detalle exacto y la fuente. **Impacto visual sobre una base formal y profesional.**

Jerarquía de lectura, siempre en este orden:

```
1. CIFRA            (lo primero que ve el ojo)
2. TITULAR          (qué pasó: MENOS / MÁS / PIERDE / GANA ...)
3. DETALLE          (la cifra exacta y el contexto)
4. ENCABEZADO/FUENTE (de qué tema es, qué período, de dónde sale)
```

Nada compite con la cifra.

---

## 2. Anatomía de la tarjeta (todas las partes)

```
┌──────────────────────────────────────────────┐
│ TEMA DE LA TARJETA · ÁMBITO                  │  ← A. Encabezado: tema (mono, mayúsculas, espaciado)
│ PERÍODO INICIO → PERÍODO FIN                 │  ← B. Período (mono, más apagado)
│                                              │
│ ▬▬▬▬                                         │  ← C. Barra de acento (color de la variación)
│ -00.000                                      │  ← D. CIFRA gigante (condensada, color)
│ PALABRA-CLAVE SUSTANTIVO                     │  ← E. Titular, renglón 1 (condensada, mayúsculas)
│ COMPLEMENTO CORTO                            │  ← F. Titular, renglón 2 (condensada, mayúsculas)
│                                              │
│ ──────────────────────────────────────────── │  ← G. Línea divisoria fina
│ Frase de detalle con la **cifra exacta**     │  ← H. Detalle (letra normal; la cifra resaltada en color)
│ Fuente: ORGANISMO                            │  ← I. Fuente (mono, chica, apagada)
└──────────────────────────────────────────────┘
```

| # | Parte | Qué lleva | Reglas |
|---|---|---|---|
| A | **Encabezado · tema** | De qué habla la tarjeta. Ej. `TEMA · ÁMBITO` | Mayúsculas, monoespaciada, letras separadas. Máx. ~30 caracteres. Nunca repite el titular. |
| B | **Período** | Desde cuándo hasta cuándo es la cifra. Ej. `AAAA → AAAA`, `DESDE AAAA`, `HASTA MES-AAAA` | Siempre presente: toda cifra dice hasta qué momento llega. Usa la flecha `→`. Más apagado que el tema. |
| C | **Barra de acento** | Una barrita horizontal corta | Mismo color que la cifra. Si la cifra es neutra (blanca), la barra va en naranja. |
| D | **Cifra** | El número. Ej. `-45.000`, `+34,2%`, `14 de 16`, `ρ -0,74` | Gigante, condensada, **nunca se corta** (`nowrap`). Con signo `+`/`-` cuando es una variación. Redondeada si es una cantidad grande (ver 5). |
| E | **Titular · renglón 1** | Palabra clave + sustantivo. Ej. `MENOS EMPLEOS`, `MÁS TEXTILES`, `PIERDE SALARIO` | Arranca con la **palabra clave** (MENOS, MÁS, PIERDE, GANA, CAE, SUBE, SIN). 2 o 3 palabras. |
| F | **Titular · renglón 2** | El complemento. Ej. `EN LA INDUSTRIA`, `DESDE AAAA`, `QUE HACE UN AÑO` | Corto. El corte entre el renglón 1 y el 2 es **manual y a propósito** (no depender del ancho). |
| G | **Divisoria** | Línea fina de 1 px | Separa el impacto (arriba) del detalle (abajo). Pegada al pie: el pie siempre queda abajo de la tarjeta. |
| H | **Detalle** | Una frase corta con el dato exacto o el contexto. Ej. «Exactamente **45.383** (-3,6%), del inicio al fin.» | Letra normal (no condensada). 1 o 2 renglones. La cifra exacta va en **negrita y del color de acento**. |
| I | **Fuente** | `Fuente: ORGANISMO` | Monoespaciada, chica, apagada. El organismo **correcto** de ese dato (no uno genérico). |

**Partes opcionales del conjunto** (fuera de la tarjeta):

| Parte | Qué lleva | Reglas |
|---|---|---|
| **Título de sección** | Título de la página o del bloque. Ej. «Hallazgos principales» | El estilo de subtítulo normal de la página. |
| **Encabezado de grupo** | Número + título del grupo de tarjetas. Ej. `01` + «Una frase que resume el grupo» | Número en mono, naranja. Título en negrita normal. Línea de 2 px debajo que separa el grupo del siguiente. |

---

## 3. Tipografía

| Uso | Familia | Tamaño base (fila de 5 en notebook) | Detalles |
|---|---|---|---|
| Cifra (tarjeta ancha) | **Anton** (condensada) | 3.3rem | `line-height: 1`, color de acento, `white-space: nowrap` |
| Cifra (tarjeta angosta) | Anton | 2.7rem | ídem |
| Titular (ancha) | Anton, MAYÚSCULAS | 1.3rem | `line-height: 1.12`, `letter-spacing: .02em`, color hueso |
| Titular (angosta) | Anton, MAYÚSCULAS | 1.12rem | ídem |
| Encabezado y período | **IBM Plex Mono** | .72rem | MAYÚSCULAS, `letter-spacing: .1em`; el período más apagado |
| Detalle | La fuente normal de la página | .92rem | `line-height: 1.45`, la cifra en `<b>` con color de acento |
| Fuente | IBM Plex Mono | .7rem | apagada |
| Número del grupo | IBM Plex Mono | .95rem | naranja, `letter-spacing: .08em` |
| Título del grupo | La fuente normal | 1.2rem | negrita 700 |

- Carga de fuentes (Google Fonts): `@import url('https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;500&display=swap');`
- Respaldo si no hay internet: `'Impact', 'Arial Narrow Bold', sans-serif` para la condensada y `ui-monospace, monospace` para la mono.
- La condensada (Anton) **solo** para cifra y titular. Nunca para textos largos.

---

## 4. Colores

La tarjeta tiene **fondo oscuro fijo**, igual en tema claro y oscuro (es un afiche, no depende del tema de la página).

| Elemento | Color |
|---|---|
| Fondo de la tarjeta | `#151311` (casi negro, cálido) |
| Texto principal (titular) | `#f3efe8` (blanco hueso) |
| Encabezado · tema | `#d2cbbf` |
| Período y fuente | `#a29a8d` |
| Detalle | `#efe9df` |
| Divisoria | `rgba(243,239,232,.18)` |
| **Borde de la tarjeta** | `1px solid rgba(255,255,255,.3)` + `box-shadow: 0 0 0 1px rgba(0,0,0,.25)` |
| Acento **negativo** (baja, se pierde) | `#ff5c3d` (naranja) |
| Acento **positivo** (sube, se gana) | `#4f9cf0` (azul) |
| Acento **neutro** (conteos, correlaciones, «3 de 24») | `#f3efe8` (la cifra en blanco; la barra y la negrita del detalle en naranja) |

Regla del color: **el color lo decide el dato**, no se elige a mano. Signo `-` → naranja, signo `+` → azul, sin signo → neutro.
La palabra clave del titular también tiene que coincidir con el signo (MENOS/PIERDE/CAE con `-`; MÁS/GANA/SUBE con `+`).

Por qué el borde claro es obligatorio: en tema oscuro la página es casi del mismo negro que la tarjeta, y sin borde **no se ven las divisiones**.

---

## 5. Reglas de contenido (cómo escribir cada tarjeta)

1. **La cifra con signo** cuando es una variación (`-`, `+`). El signo se queda: la palabra clave refuerza, no reemplaza.
2. **La palabra clave pega más que el signo**: el titular arranca con MENOS / MÁS / PIERDE / GANA / CAE / SUBE / SIN.
3. **Cantidades grandes, redondeadas** en la cifra; **la exacta, en el detalle**:
   - ≥ 10.000 → redondear a miles (`-45.383` → `-45.000`)
   - 1.000 a 9.999 → redondear a centenas
   - < 1.000 → tal cual
   - El detalle dice «Exactamente **45.383** …».
4. **Titular en dos renglones cortos**, cortados a mano: `PALABRA-CLAVE SUSTANTIVO` / `COMPLEMENTO`. Nunca una frase larga que el navegador corte donde quiera.
5. **Nada de repetir**: el titular no repite el encabezado; el detalle no repite el titular. Cada línea agrega algo.
6. **Todo dice hasta cuándo llega** (el período de la parte B).
7. **Fuente correcta por dato**: el organismo que publica ese dato en particular.
8. **Textos calculados, no escritos a mano**: si la cifra cambia de signo, la palabra clave y el color cambian solos (MENOS↔MÁS, PIERDE↔GANA).
9. **Honestidad**: la frase dice lo que muestra el número, sin exagerar. Si son asociaciones y no causas, se aclara en el detalle de la tarjeta del grupo.
10. **Formato de números local**: punto de miles y coma decimal (`45.383`, `-3,6%`, `+4,2 p.p.`).

---

## 6. La grilla (organización)

- Las tarjetas se agrupan por tema. **Cada grupo = un encabezado (número + título) + una fila de tarjetas.**
- Grilla de **12 columnas** con separación de `1rem`. Una fila típica de **5 tarjetas**:
  - **Ancha = 3 columnas.** Van anchas: **(a)** la tarjeta principal del grupo (la primera, el dato más importante) y **(b)** la tarjeta con más contenido de las demás.
  - **Angosta = 2 columnas.** Todas las otras.
  - 3 + 3 + 2 + 2 + 2 = **12**: la fila siempre queda completa, sin huecos.
- **El ancho depende del contenido**, nunca al revés: una tarjeta con poco contenido va angosta; **nunca una tarjeta grande y vacía**.
  - Medida de contenido: `largo(cifra) + 2 × largo(renglón más largo del titular) + largo(detalle sin HTML) / 2` (el titular pesa el doble porque es lo que se corta feo si la tarjeta es angosta).
- **Todas las tarjetas de una fila tienen el mismo alto** (`align-items: stretch`) y **el pie siempre al fondo** (`margin-top: auto`): las divisorias quedan alineadas.
- Separación entre grupos: `2.6rem` + la línea de 2 px del encabezado del grupo. Las divisiones tienen que **verse**.
- Otras cantidades de tarjetas por fila (repartir siempre 12 columnas):
  - 4 tarjetas → 3 + 3 + 3 + 3, o 4 + 3 + 3 + 2 (la principal más ancha).
  - 3 tarjetas → 4 + 4 + 4, o 6 + 3 + 3.
  - 6 tarjetas → 2 × 6.

---

## 7. Adaptación a la pantalla (responsive)

| Ancho | Grilla | Cambios |
|---|---|---|
| > 1250 px | 12 columnas, fila de 5 | Tamaños base de la sección 3 |
| 950 – 1250 px | 12 columnas, **sigue la fila de 5** | Todo un poco más chico: cifra 2.2rem (ancha 2.8rem), titular 1rem (ancha 1.15rem), encabezado .66rem, detalle .86rem; la fuente puede pasar a dos renglones |
| 640 – 950 px | 6 columnas, **dos renglones completos** | Las 2 anchas arriba (3 + 3) y las 3 angostas abajo (2 + 2 + 2), con `order` para que no queden huecos |
| < 640 px | 1 columna | Una tarjeta debajo de la otra |

Regla: **en ningún ancho puede aparecer una tarjeta gigante sola ni un hueco vacío en un renglón**.

---

## 8. Medidas internas de la tarjeta

| Elemento | Medida |
|---|---|
| Padding de la tarjeta | `1rem 1.05rem .9rem` |
| Radio de las esquinas | `12px` |
| Espacio encabezado → cifra | `.8rem` |
| Barra de acento | `2.4rem × 4px`, margen inferior `.6rem` |
| Cifra → titular | `.45rem` |
| Titular → divisoria | `.75rem` (y la divisoria empujada al fondo) |
| Divisoria → detalle | `.6rem` |
| Detalle → fuente | `.45rem` |

---

## 9. Lo que NO hay que hacer (aprendido a los golpes)

- ❌ **Cambiar solo las palabras** pensando que eso es «impacto». El impacto es **visual**: tamaño, peso, contraste y jerarquía.
- ❌ Poner el texto de apoyo como párrafo largo, o esconderlo en un desplegable «Ver el detalle». El detalle va **dentro** de la tarjeta, corto.
- ❌ **Borrar contenido** cuando piden «mostrarlo de otra manera». Reorganizar, nunca quitar.
- ❌ Titulares largos que se cortan en cualquier lado («MENOS EMPLEOS EN LA» / «INDUSTRIA»). Se cortan a mano, en dos renglones pensados.
- ❌ Todo el rótulo en mayúsculas finas y chiquitas: no pega. La mayúscula va en la tipografía condensada grande.
- ❌ **Tarjetas grandes con poco contenido** o una tarjeta gigante (3×2) rodeada de chicas: se ve desordenado y vacío.
- ❌ Tarjetas oscuras **sin borde** sobre fondo oscuro: no se ven las divisiones.
- ❌ Grillas que en pantallas medianas (1000–1150 px) dejan huecos o tarjetas de media pantalla.
- ❌ Advertencias en cajas de color o notas sueltas al pie («Ojo: …»). Si hace falta aclarar, va en el detalle de una tarjeta.
- ❌ Fuente equivocada o genérica («Fuente: INDEC» para un dato que es de otro organismo).
- ❌ Cifras sin período («-3,9%» ¿desde cuándo?).
- ❌ Texto de la fuente que se parte en dos renglones por ser largo: usar la sigla.

---

## 10. Controles antes de dar por terminado

1. **Foto de la sección entera** (captura con ventana muy alta, p. ej. 1366 × 4000) y mirarla completa: ¿se lee? ¿se ven las divisiones? ¿hay tarjetas vacías?
2. Revisar en **tema claro y tema oscuro**.
3. Revisar en **1920, 1366, 1250, 1100, 1000, 900 y 400 px**.
4. Medir por código que **nada se sale** de su tarjeta: para cifra, titular y fuente, `scrollWidth <= clientWidth` y el borde derecho dentro de la tarjeta.
5. Medir por código que **cada renglón de la grilla llena el ancho** (sin hueco a la derecha).
6. Verificar que cada cifra, signo, palabra clave y color **salen de los datos** y coinciden entre sí.
7. Verificar la **fuente** de cada tarjeta.
8. Si la persona dice que algo no se entiende o no le gusta y no queda claro qué quiere: **preguntar con opciones visuales** antes de rehacer.

---

## 11. Variables de una tarjeta (el «molde»)

```
tarjeta = {
  tema:      "TEMA · ÁMBITO",               # A. encabezado (mayúsculas)
  periodo:   "INICIO → FIN",                # B. período
  valor:     "-00.000",                     # D. cifra (con signo si es variación; redondeada)
  titular:   ("PALABRA-CLAVE SUSTANTIVO",   # E. renglón 1
              "COMPLEMENTO"),               # F. renglón 2
  detalle:   "Frase corta con la <b>cifra exacta</b>.",  # H.
  fuente:    "ORGANISMO",                   # I.
  tono:      "neg" | "pos" | "neu",         # color: lo decide el signo de la cifra
  tamaño:    "ancho" | "angosto",           # lo decide el contenido (sección 6)
}

grupo = {
  numero:   "01",
  titulo:   "Frase que resume el grupo",
  tarjetas: [principal, dato, dato, dato, dato],
}
```

---

## 12. Prompt listo para copiar y pegar

> Copiar desde «Quiero…» hasta el final del bloque y completar lo que está entre `[corchetes]`.

```text
Quiero mostrar cifras clave con TARJETAS DE IMPACTO tipo afiche, profesionales y formales, en [dashboard Streamlit / página HTML / informe / presentación].
Los datos son: [describir los datos o pegar las cifras]. Agrupalos en [N] grupos temáticos de [5] tarjetas.

FORMATO DE CADA TARJETA (en este orden, de arriba a abajo):
A. Encabezado: tema en MAYÚSCULAS, tipografía monoespaciada (IBM Plex Mono) .72rem, letter-spacing .1em, color #d2cbbf.
B. Período debajo del tema ("INICIO → FIN", "DESDE AAAA"), mismo estilo, color #a29a8d. Toda cifra dice hasta cuándo llega.
C. Barra de acento de 2.4rem × 4px del color de la cifra.
D. CIFRA GIGANTE en tipografía condensada (Anton): 3.3rem en tarjetas anchas, 2.7rem en angostas, line-height 1, sin cortes (nowrap).
   Con signo +/- si es una variación. Cantidades ≥ 10.000 redondeadas a miles (la exacta va en el detalle).
E-F. TITULAR en Anton, MAYÚSCULAS, en DOS renglones cortados a mano:
   renglón 1 = PALABRA CLAVE + sustantivo (MENOS EMPLEOS / MÁS IMPORTACIONES / PIERDE SALARIO / CAE EL EMPLEO / SIN EFECTO),
   renglón 2 = complemento corto (EN LA INDUSTRIA / DESDE AAAA). 1.3rem en anchas, 1.12rem en angostas, color #f3efe8.
   La palabra clave tiene que coincidir con el signo de la cifra y calcularse del dato (MENOS↔MÁS, PIERDE↔GANA).
G. Línea divisoria fina (1px rgba(243,239,232,.18)) empujada al fondo de la tarjeta.
H. Detalle en letra normal .92rem color #efe9df: una frase corta con la cifra exacta en negrita y color de acento ("Exactamente <b>45.383</b> (-3,6%), …").
I. "Fuente: ORGANISMO" en monoespaciada .7rem color #a29a8d, el organismo correcto de ese dato.

COLORES: fondo de tarjeta FIJO #151311 (igual en tema claro y oscuro), borde 1px solid rgba(255,255,255,.3) + box-shadow 0 0 0 1px rgba(0,0,0,.25)
(el borde es obligatorio: sin él no se ven las divisiones en tema oscuro), radio 12px, padding 1rem 1.05rem .9rem.
Acento: naranja #ff5c3d si la cifra baja (-), azul #4f9cf0 si sube (+), blanco #f3efe8 si es neutra (conteos, correlaciones; su barra en naranja).

GRILLA: cada grupo = encabezado (número "01" en mono naranja + título en negrita 1.2rem + línea de 2px debajo) y una fila de tarjetas
en grilla de 12 columnas con gap 1rem. La tarjeta principal del grupo y la de más contenido ocupan 3 columnas; las demás, 2 (3+3+2+2+2 = 12).
El ancho depende del contenido: NUNCA una tarjeta grande con poco contenido. Todas las de una fila con el mismo alto; el pie siempre al fondo.
Separación entre grupos 2.6rem.

RESPONSIVE: >1250px tamaños base; 950–1250px misma fila de 5 con letra un poco menor; 640–950px 6 columnas con las 2 anchas arriba (3+3)
y las 3 angostas abajo (2+2+2) usando order; <640px una columna. En ningún ancho puede haber huecos ni tarjetas gigantes solas.

REGLAS: todos los textos y colores calculados a partir de los datos (no escritos a mano); nada de párrafos largos, desplegables
"ver detalle", cajas de advertencia ni notas sueltas; no repetir información entre encabezado, titular y detalle; números con punto de miles
y coma decimal; la frase dice lo que muestra el número, sin exagerar.

ANTES DE ENTREGAR: sacá una captura de la sección ENTERA (ventana muy alta) en tema claro y oscuro y a 1920, 1366, 1100, 1000 y 900 px;
verificá por código que ninguna cifra/titular/fuente se sale de su tarjeta y que cada renglón de la grilla llena el ancho.
Si algo de lo que pido no queda claro, preguntame con opciones visuales antes de rehacer.
```

---

## 13. Plantilla HTML/CSS de referencia

Estructura (una tarjeta y un grupo):

```html
<div class="hallazgos">
  <section class="hz">
    <div class="hz-cab"><span class="hz-num">01</span><span class="hz-tit">TÍTULO DEL GRUPO</span></div>
    <div class="hz-grilla">
      <div class="afiche ancho neg">
        <div class="af-cab"><span>TEMA · ÁMBITO</span><span>INICIO → FIN</span></div>
        <div class="af-cuerpo">
          <div class="af-barra"></div>
          <div class="af-valor">-00.000</div>
          <div class="af-frase">PALABRA-CLAVE SUSTANTIVO<br>COMPLEMENTO</div>
        </div>
        <div class="af-pie">
          <div class="af-det">Exactamente <b>00.000</b>, contexto corto.</div>
          <div class="af-fuente">Fuente: ORGANISMO</div>
        </div>
      </div>
      <!-- …4 tarjetas más: class="afiche ancho|angosto neg|pos|neu" -->
    </div>
  </section>
</div>
```

Estilos:

```css
@import url('https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;500&display=swap');

.hallazgos { display: flex; flex-direction: column; gap: 2.6rem; margin: .6rem 0 1rem; }
.hz-cab { display: flex; align-items: baseline; gap: .9rem; padding-bottom: .55rem; margin-bottom: 1rem; border-bottom: 2px solid rgba(128,128,128,.5); }
.hz-num { font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: .95rem; font-weight: 500; color: #eb6834; letter-spacing: .08em; }
.hz-tit { font-size: 1.2rem; font-weight: 700; line-height: 1.3; }
.hz-grilla { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 1rem; align-items: stretch; }
.hz-grilla .ancho { grid-column: span 3; } .hz-grilla .angosto { grid-column: span 2; }

.afiche { background: #151311; color: #f3efe8; border: 1px solid rgba(255,255,255,.3); box-shadow: 0 0 0 1px rgba(0,0,0,.25);
          border-radius: 12px; padding: 1rem 1.05rem .9rem; display: flex; flex-direction: column; min-width: 0; --acento: #ff5c3d; }
.afiche.pos { --acento: #4f9cf0; } .afiche.neu { --acento: #f3efe8; }
.af-cab { display: flex; flex-direction: column; font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: .72rem; letter-spacing: .1em;
          text-transform: uppercase; color: #d2cbbf; line-height: 1.45; }
.af-cab span:last-child { color: #a29a8d; }
.af-cuerpo { padding: .8rem 0 .75rem; }
.af-barra { width: 2.4rem; height: 4px; background: var(--acento); margin-bottom: .6rem; }
.afiche.neu .af-barra { background: #ff5c3d; }
.af-valor { font-family: 'Anton', 'Impact', 'Arial Narrow Bold', sans-serif; font-weight: 400; color: var(--acento); line-height: 1;
            font-size: 2.7rem; white-space: nowrap; }
.af-frase { font-family: 'Anton', 'Impact', 'Arial Narrow Bold', sans-serif; font-weight: 400; text-transform: uppercase; line-height: 1.12;
            font-size: 1.12rem; margin-top: .45rem; letter-spacing: .02em; }
.ancho .af-valor { font-size: 3.3rem; } .ancho .af-frase { font-size: 1.3rem; }
.af-pie { margin-top: auto; border-top: 1px solid rgba(243,239,232,.18); padding-top: .6rem; }
.af-det { font-size: .92rem; line-height: 1.45; color: #efe9df; }
.af-det b { color: var(--acento); font-weight: 700; } .afiche.neu .af-det b { color: #ff5c3d; }
.af-fuente { font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: .7rem; color: #a29a8d; margin-top: .45rem; white-space: nowrap; }

@media (max-width: 1250px) {
  .hz-grilla { gap: .75rem; } .afiche { padding: .9rem .85rem .8rem; }
  .af-valor { font-size: 2.2rem; } .af-frase { font-size: 1rem; } .ancho .af-valor { font-size: 2.8rem; } .ancho .af-frase { font-size: 1.15rem; }
  .af-cab { font-size: .66rem; letter-spacing: .06em; } .af-det { font-size: .86rem; } .af-fuente { white-space: normal; }
}
@media (max-width: 950px) {
  .hz-grilla { grid-template-columns: repeat(6, minmax(0, 1fr)); }
  .hz-grilla .ancho { grid-column: span 3; order: 0; } .hz-grilla .angosto { grid-column: span 2; order: 1; }
  .hz-grilla .angosto .af-valor { font-size: 2.4rem; }
}
@media (max-width: 640px) { .hz-grilla { grid-template-columns: 1fr; } .hz-grilla .ancho, .hz-grilla .angosto { grid-column: auto; } }
```

Lógica de tamaños y colores (pseudocódigo, cualquier lenguaje):

```text
tono(valor)      = "neg" si empieza con "-", "pos" si empieza con "+", si no "neu"
redondo(x)       = redondear a miles si |x| ≥ 10.000; a centenas si |x| ≥ 1.000; si no, x   (mostrar con signo)
clave(v, +, -)   = palabra "+" si v > 0, si no palabra "-"                                  (MÁS/MENOS, GANA/PIERDE, SUBE/CAE)
contenido(t)     = largo(valor) + 2 × largo(renglón más largo del titular) + largo(detalle sin HTML) / 2
tamaños(grupo)   = la primera tarjeta → "ancho"; de las demás, la de mayor contenido → "ancho"; el resto → "angosto"
```

---

## 14. Cómo armar UNA sola tarjeta (paso a paso)

Para cuando no hace falta una grilla: una sola cifra protagonista (portada de un informe, una diapositiva, una publicación, el dato destacado de una página).
Es la misma tarjeta, pero **sola y más grande**, con proporción de afiche (cuadrada o casi) y todo escalado para ocupar el espacio.

### 14.1 Los pasos

**Paso 1 · Elegir el dato.** Uno solo: el que más pesa para la historia. Anotar:
- el valor exacto (ej. `-45.383`),
- qué mide (ej. «empleos en la industria»),
- el período que cubre (inicio y fin),
- el organismo que lo publica.

**Paso 2 · Decidir el tono** (lo decide el signo, no el gusto):

| El dato… | Signo | Tono | Color de acento | Palabras clave posibles |
|---|---|---|---|---|
| baja / se pierde | `-` | `neg` | naranja `#ff5c3d` | MENOS · PIERDE · CAE · BAJA |
| sube / se gana | `+` | `pos` | azul `#4f9cf0` | MÁS · GANA · SUBE · CRECE |
| no es una variación (conteo, proporción, correlación) | — | `neu` | blanco `#f3efe8` (barra naranja) | SIN · SOLO · (sin palabra de dirección) |

**Paso 3 · Preparar la cifra** (parte D):
- Variación → con signo (`-45.000`, `+34,2%`).
- Cantidad ≥ 10.000 → redondear a miles; 1.000–9.999 → a centenas; < 1.000 → tal cual. **Guardar la exacta para el detalle.**
- Formato local: punto de miles, coma decimal.
- Que entre en **un solo renglón**: máximo ~8 caracteres. Si es más largo (`+4,2 p.p.`, `ρ -0,74`), achicar el tamaño de la cifra, no cortarla.

**Paso 4 · Escribir el titular en dos renglones** (partes E y F):
- Renglón 1 = **PALABRA CLAVE + SUSTANTIVO**, 2 o 3 palabras: `MENOS EMPLEOS`.
- Renglón 2 = **complemento** corto, 2 a 4 palabras: `EN LA INDUSTRIA`.
- Leer los dos renglones seguidos junto con la cifra: tiene que sonar como un titular de diario → «-45.000 · MENOS EMPLEOS EN LA INDUSTRIA».
- Probar que la palabra clave coincide con el signo (MENOS con `-`).

**Paso 5 · Escribir el encabezado** (partes A y B):
- Tema, en mayúsculas: `TEMA · ÁMBITO` (ej. `EMPLEO INDUSTRIAL · PAÍS`). No repetir el titular.
- Período: `INICIO → FIN` (ej. `1T 2018 → 1T 2026`). En la tarjeta sola van **en la misma línea**: tema a la izquierda, período a la derecha.

**Paso 6 · Escribir el detalle** (parte H):
- Una sola frase, 1 o 2 renglones: la cifra exacta + el contexto que falta.
- La cifra exacta en `<b>` (sale en color de acento): «Exactamente **45.383**, del 1T 2018 al 1T 2026.»
- Si hace falta una aclaración metodológica (ej. «son asociaciones, no causas»), va acá, corta.

**Paso 7 · Poner la fuente** (parte I): `Fuente: ORGANISMO`, con el organismo que realmente publica ese dato. En la tarjeta sola va **a la derecha del detalle**.

**Paso 8 · Armar el HTML y aplicar el CSS** (14.3 y 14.4).

**Paso 9 · Revisar** (14.5).

### 14.2 Anatomía de la tarjeta sola

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  TEMA · ÁMBITO                           INICIO → FIN      │  ← A + B en una línea (mono, mayúsculas, muy espaciado)
│                                                            │
│                                                            │
│  ▬▬▬▬▬▬▬▬                                                  │  ← C. barra de acento (más larga y gruesa)
│  -00.000                                                   │  ← D. CIFRA: ocupa casi todo el ancho
│                                                            │
│          PALABRA-CLAVE SUSTANTIVO                          │  ← E. titular renglón 1 (muy grande)
│          COMPLEMENTO                                       │  ← F. titular renglón 2
│                                                            │
│  ────────────────────────────────────────────────────────  │  ← G. divisoria
│  Exactamente 00.000, contexto.            Fuente: ORGANISMO│  ← H a la izquierda, I a la derecha
│                                                            │
└────────────────────────────────────────────────────────────┘
```

Diferencias con la tarjeta de grilla:

| Aspecto | En grilla | Sola |
|---|---|---|
| Tamaño | 2 o 3 de 12 columnas | Ancho máximo ~560–720 px (o el que pida el formato), proporción cuadrada `aspect-ratio: 1` o casi |
| Encabezado | tema y período en dos renglones | tema y período **en una línea**, a los extremos |
| Barra | 2.4rem × 4px | ~5rem × 8px |
| Cifra | 2.7–3.3rem | escalada al ancho: `clamp(4.5rem, 18cqw, 9rem)` → casi todo el ancho |
| Titular | 1.1–1.3rem, alineado a la izquierda | `clamp(1.8rem, 7cqw, 3.4rem)`, puede ir **centrado** debajo de la cifra |
| Detalle / fuente | uno debajo del otro | en la misma línea, detalle a la izquierda y fuente a la derecha |
| Espacios | compactos | mucho aire: padding ~8% del ancho, la cifra y el titular en el centro vertical |

### 14.3 HTML de la tarjeta sola

```html
<div class="afiche-solo neg">
  <div class="as-cab"><span>TEMA · ÁMBITO</span><span>INICIO → FIN</span></div>
  <div class="as-cuerpo">
    <div class="as-barra"></div>
    <div class="as-valor">-00.000</div>
    <div class="as-frase">PALABRA-CLAVE SUSTANTIVO<br>COMPLEMENTO</div>
  </div>
  <div class="as-pie">
    <div class="as-det">Exactamente <b>00.000</b>, contexto corto.</div>
    <div class="as-fuente">Fuente: ORGANISMO</div>
  </div>
</div>
```

Cambiar la clase `neg` por `pos` o `neu` según el paso 2.

### 14.4 CSS de la tarjeta sola

```css
@import url('https://fonts.googleapis.com/css2?family=Anton&family=IBM+Plex+Mono:wght@400;500&display=swap');

.afiche-solo {
  --acento: #ff5c3d;
  container-type: inline-size;                 /* las medidas en cqw escalan con el ancho de la tarjeta */
  width: 100%; max-width: 640px; aspect-ratio: 1; margin: 0 auto;
  background: #151311; color: #f3efe8;
  border: 1px solid rgba(255,255,255,.3); box-shadow: 0 0 0 1px rgba(0,0,0,.25); border-radius: 14px;
  padding: 8cqw 8cqw 6cqw; box-sizing: border-box;
  display: flex; flex-direction: column;
}
.afiche-solo.pos { --acento: #4f9cf0; } .afiche-solo.neu { --acento: #f3efe8; }

.as-cab { display: flex; justify-content: space-between; gap: 1rem; font-family: 'IBM Plex Mono', ui-monospace, monospace;
          font-size: clamp(.65rem, 2.1cqw, .95rem); letter-spacing: .22em; text-transform: uppercase; color: #b9b2a6; }
.as-cab span:last-child { white-space: nowrap; }

.as-cuerpo { margin: auto 0; }                 /* cifra y titular en el centro vertical */
.as-barra { width: 17cqw; height: max(5px, 1.1cqw); background: var(--acento); margin-bottom: 3cqw; }
.afiche-solo.neu .as-barra { background: #ff5c3d; }
.as-valor { font-family: 'Anton', 'Impact', 'Arial Narrow Bold', sans-serif; font-weight: 400; color: var(--acento);
            font-size: clamp(4.5rem, 26cqw, 11rem); line-height: .95; letter-spacing: -.01em; white-space: nowrap; }
.as-frase { font-family: 'Anton', 'Impact', 'Arial Narrow Bold', sans-serif; font-weight: 400; text-transform: uppercase;
            font-size: clamp(1.8rem, 9cqw, 4.2rem); line-height: 1.05; letter-spacing: .01em; text-align: center; margin-top: 3cqw; }

.as-pie { border-top: 1px solid rgba(243,239,232,.2); padding-top: 3.5cqw; display: flex; justify-content: space-between;
          align-items: flex-end; gap: 1rem; flex-wrap: wrap; }
.as-det { font-size: clamp(.9rem, 3.4cqw, 1.5rem); line-height: 1.35; color: #efe9df; flex: 1 1 60%; }
.as-det b { color: var(--acento); font-weight: 700; } .afiche-solo.neu .as-det b { color: #ff5c3d; }
.as-fuente { font-family: 'IBM Plex Mono', ui-monospace, monospace; font-size: clamp(.6rem, 2cqw, .85rem); color: #8f887c; white-space: nowrap; }
```

Notas:
- `cqw` = % del ancho de la tarjeta: todo escala junto, se vea a 320 px o a 1080 px (sirve también para exportar como imagen cuadrada).
- Si la cifra tiene más de ~8 caracteres, bajar el `26cqw` de `.as-valor` (p. ej. a `20cqw`) hasta que entre en un renglón.
- Si va sobre fondo oscuro, el borde claro es obligatorio; sobre fondo claro se puede dejar igual.
- Para una diapositiva o imagen para redes: `max-width: none; width: 1080px;` y exportar la captura.

### 14.5 Revisión de la tarjeta sola

- [ ] La cifra entra en **un renglón** y ocupa casi todo el ancho.
- [ ] El titular son **dos renglones** cortados donde yo decidí, y leído con la cifra suena a titular.
- [ ] La palabra clave y el color **coinciden con el signo**.
- [ ] El período está arriba a la derecha y el detalle tiene la **cifra exacta** resaltada.
- [ ] La fuente es la **correcta** para ese dato.
- [ ] Ningún texto se repite entre encabezado, titular y detalle.
- [ ] Se ve bien a 360 px, a 640 px y al tamaño final (captura de la tarjeta entera).
- [ ] En tema oscuro se ve el borde.

### 14.6 Prompt corto para UNA tarjeta

```text
Armame UNA tarjeta de impacto tipo afiche (sola, cuadrada, máx. 640px, fondo fijo #151311, borde 1px rgba(255,255,255,.3), radio 14px).
Dato: [valor exacto] de [qué mide], período [inicio → fin], fuente [organismo].
Estructura: arriba en una línea, tema en mayúsculas mono espaciada a la izquierda ("[TEMA · ÁMBITO]") y período a la derecha;
barra de acento; CIFRA gigante en Anton que ocupe casi todo el ancho, con signo y redondeada ([cifra redondeada]);
titular en Anton mayúsculas, dos renglones cortados a mano, centrado: "[PALABRA CLAVE + SUSTANTIVO]" / "[COMPLEMENTO]";
línea divisoria; abajo a la izquierda el detalle en letra normal con la cifra exacta resaltada ("Exactamente <b>[valor exacto]</b>, [contexto].")
y a la derecha "Fuente: [organismo]" en mono chica.
Color de acento según el signo: naranja #ff5c3d si baja, azul #4f9cf0 si sube, blanco si es neutro. Escalá todo con el ancho (container queries, cqw).
Verificá que la cifra entre en un renglón y mostrame una captura de la tarjeta entera.
```

---

*Implementación de referencia en este proyecto:* `dashboard/paginas/resumen.py` (funciones `_afiche`, `_html_afiche`, `_contenido`, `_bloque`, `_redondo`, `_tono`)
y `dashboard/core/tema.py` (bloque CSS «hallazgos del Resumen»).
