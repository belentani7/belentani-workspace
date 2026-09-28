# Auditoría de los 104 repos públicos de `belentani7`

**Fecha:** 2026-09-28  
**Método:** lectura de la API pública de GitHub. **Ningún repo se ha clonado.**  
**Endpoints usados:** `/users/belentani7/repos`, `/repos/{o}/{r}/git/trees/{branch}?recursive=1`, 
`/repos/{o}/{r}/commits` y `/repos/{o}/{r}/readme` (contenido completo, no solo el tamaño).  
**Perfil del titular:** creado el 2025-09-07. 104 repos públicos, todos creados en los últimos 13 meses.

Todo lo que sigue es **observable desde fuera**: no se ha leído ni una línea de código de
negocio, porque no hacía falta para valorarlo y porque el objetivo es medir lo que un
visitante, un revisor o un motor de búsqueda puede ver sin clonar.

---

## 1. Resumen ejecutivo

**Nota media del perfil: 59.8/100** (suma de los 20 aspectos: 63.5/100; penalizaciones: 3.7 puntos).

Seis conclusiones que se sostienen sobre los datos:

**1. Hay contenido de sobra y prueba de trabajo de menos.** La mediana de commits por repo es
**11** y **49 de 104 repos tienen cero tests**; 14 de 104 no tienen ningún workflow de CI. El
historial existe, pero es corto: 11 repos tienen 5 commits o menos, de modo que en una de cada
diez entradas de tu perfil el trabajo cabe en una tarde. Un repositorio sin tests ni CI es, para
un tercero, un archivo con aspecto de proyecto, y eso es exactamente lo que un motor de
búsqueda comprueba antes de recomendarte.

**2. La licencia es el agujero más grande y el más barato de cerrar.** 32 de 104 repos (31%) no tienen archivo LICENSE; solo 72 lo tienen. Es una línea de
texto y decide si tu código puede ser citado, reimplementado o indexado. Ninguna IA
recomienda un repo del que no puede hablar con propiedad. **Es la acción de mayor retorno
de todo este informe.**

**3. 17 repos (16%) compiten por el mismo título y ninguno es canónico.** El token `belentani` aparece en 25
repos, `duck` en 18, `omega` en 9 y `judas` en 7. Un visitante que busca
`belentani omega` encuentra varios resultados que dicen ser lo mismo, y GitHub no sabe
cuál es el bueno. **Elegir tres canónicos y archivar el resto sube la percepción de todos a
la vez.**

**4. 10 repos afirman calidades que no se pueden comprobar.** Textualmente:

   - `belentani-judas-era-omega`: *«Omega Core Experience 10/10»*
   - `duck-full-studio-pro`: *«FL Studio Ecosystem & Vault (Audited 10/10)»*
   - `ai-command-center-level10`: *«AI Command Center Level 10»*
   - `belentani-java-platform`: *«enterprise-grade Java backend»*, con 15 KB y cero tests

   Y en sentido contrario, varios repos hacen bien lo que estos hacen mal:
   `duck-zion-apex-public` publica *«gate currently 57/60»*, `agent-skills` declara
   *«311 skills»* y `duck-belentani-os-audited-2026-08-23` fecha su snapshot. **Un número
   parcial y verificable convence más que un 10/10**, porque se puede comprobar.

**5. El punto fuerte real es la actividad: 74 de 104 repos se movieron en los últimos 7 días.**
Eso no lo puede fabricar nadie y es la ventaja que tienes frente a un perfil inactivo. Pero
con **cero stars en 103 de 104 repos**, esa actividad no se traduce en nada externo: nadie sabe que
existe. Actividad sin distribución es trabajo privado.

**6. La mitad de tu perfil ni siquiera se puede abrir.** 28 de 104 READMEs no contienen ni un
comando de ejecución y 50 no tienen sección de uso. Para un tercero, ese repo no explica cómo
arranca. Es la carencia de menor coste y mayor beneficio de toda la lista.

---

## 2. El modelo de valoración: 20 aspectos observables

Cada aspecto se puntúa de 0 a 5 y todos se calculan **solo** con datos de la API y del
árbol de ficheros. No hay ninguna nota subjetiva.

| # | Aspecto | Qué mide exactamente | Media | 5/5 | 0/5 |
|---|---|---|---|---|---|
| 1 | Descripción | Texto de la descripción del repo: ausente, genérica o específica con tecnología y función. | **3.39** | 4 | 1 |
| 2 | Topics | Número de topics de GitHub. Son el índice de búsqueda interno de la plataforma. | **3.64** | 3 | 0 |
| 3 | README (contenido real) | Se leyó el README entero (no solo su tamaño): sección de uso, comandos de ejecución, bloques de código, secciones de arquitectura/variables/roadmap, índice e imágenes. | **3.46** | 35 | 5 |
| 4 | Licencia | Archivo LICENSE en el árbol más el SPDX que identifica la API. Sin licencia no hay reutilización legal. | **2.65** | 0 | 32 |
| 5 | Demo desplegada | URL de demo en homepage y si GitHub Pages está activo. Puntúa más un despliegue propio que un .github.io. | **3.33** | 0 | 17 |
| 6 | Volumen de código | Tamaño del repositorio en KB según la API. Masa de contenido versionado. | **3.77** | 32 | 0 |
| 7 | Lenguaje coherente | El lenguaje que declara GitHub coincide con los ficheros que hay realmente en el árbol. | **4.00** | 0 | 0 |
| 8 | Estructura de proyecto | Manifest (package.json / pyproject.toml / go.mod) más directorio src/ más lockfile. | **2.61** | 22 | 22 |
| 9 | Reproducibilidad | Se puede clonar y arrancar igual que en origen: .gitignore, lockfile y manifest con dependencias declaradas. | **3.97** | 53 | 3 |
| 10 | Tests | Ficheros de test detectados en el árbol (tests/, __tests__/, *.test.*, *_test.py). | **1.43** | 5 | 49 |
| 11 | CI/CD | Workflows en .github/workflows. Es lo único que avisa cuando algo deja de funcionar. | **2.72** | 21 | 14 |
| 12 | Documentación | Ficheros .md adicionales al README, directorio docs/ y guía de contribución. | **4.00** | 49 | 0 |
| 13 | Higiene de secretos | .env.example presente y .gitignore que excluye secretos. | **3.60** | 34 | 0 |
| 14 | Config de despliegue | Configuración de despliegue versionada: vercel.json, netlify.toml, fly.toml, Dockerfile o CI que despliega. | **1.53** | 1 | 9 |
| 15 | Actividad reciente | Días desde el último push. Evidencia de que el repo está vivo. | **4.71** | 74 | 0 |
| 16 | Historial de commits | Número de commits en la rama por defecto. Un repo entero en un commit no tiene historial. | **2.74** | 6 | 0 |
| 17 | Descubribilidad social | Stars más forks. Es la única señal de adopción real que GitHub expone sin métricas privadas. | **0.02** | 0 | 103 |
| 18 | Gestión de issues | Issues habilitadas, Discussions, guía de contribución y CODEOWNERS. | **3.51** | 2 | 0 |
| 19 | Nombre y marca | Calidad del nombre: kebab-case limpio frente a mayúsculas, guiones bajos o nombres de prueba. | **4.45** | 83 | 0 |
| 20 | Unicidad en el ecosistema | El repo ocupa un espacio propio en tu perfil, o compite con hermanos que reclaman el mismo título. | **3.99** | 68 | 0 |

**Cómo se lee:** 0-1 es invisible o inexistente, 2 es deficiente, 3 es correcto pero
incompleto, 4 es profesional, 5 es referenciable.

### Los 20 aspectos, agrupados por dónde más duele

| | Aspectos | Media |
|---|---|---|
| **Más débiles** | Descubribilidad social, Tests, Config de despliegue, Estructura de proyecto, Licencia, CI/CD, Historial de commits, Demo desplegada | 2.13 |
| **Más fuertes** | Actividad reciente, Nombre y marca, Lenguaje coherente, Documentación, Unicidad en el ecosistema, Reproducibilidad | 4.19 |

### Penalizaciones

Se descuentan después de la suma. Todas son defectos verificables, noTransient opiniones.

| Penalización | Puntos | Motivo |
|---|---|---|
| `ARCHIVADO` | -3 | Repo marcado como archivado: aparece como muerto. |
| `RECLAMO-INFLADO` | -4 | La descripción afirma una nota, un nivel o un estado («10/10», «level 10», «production-ready», «enterprise-grade») que no se puede comprobar en el repo. |
| `DUPLICADO` | -5 | Es una copia de otro repo. Publicar ambas divide la autoridad del perfil. |
| `GALERIA` | -3 | Colección de versiones, no un proyecto. |
| `CONFLICTO-PROP` | -3 | Muchos repos de tu perfil reclaman el mismo título y ninguno es canónico. |
| `UN-SOLO-COMMIT` | -2 | Todo el contenido en un único commit. |
| `SIN-LICENCIA` | -2 | Sin archivo LICENSE. |
| `SIN-CI` | -2 | Tiene manifest de build y ningún workflow. |
| `SIN-TESTS` | -2 | Tiene src/ y ningún test. |
| `SIN-DEMO` | -1 | Sin homepage: nadie ve el resultado sin clonar. |
| `SIN-VISIBILIDAD` | -1 | Cero stars y cero forks. |
| `README-MAGERNA` | -2 | README por debajo de 25 palabras. |
| `SIN-INSTRUCCIONES` | -2 | El README no contiene ni un comando de ejecución. |
| `PESADO` | -2 | Más de 100 MB de assets versionados. |

---

## 3. Lectura del conjunto

### 3.1 Distribución por tipo de proyecto

| Perfil | Repos | Nota media | Máx | Mín | Qué necesita |
|---|---|---|---|---|---|
| WEB_APP_TS | 51 | 62.0 | 79 | 42 | Aplicación web con frontend o backend que se construye y se despliega |
| SKILL_PACK | 11 | 58.8 | 72 | 42 | Pack de skills, prompts o registro de agentes |
| SITIO_ESTATICO | 11 | 51.1 | 67 | 39 | Sitio estático, portfolio o showcase |
| DOCS_PLATFORM | 6 | 68.8 | 80 | 54 | Plataforma educativa o documentación |
| AGENT_INFRA | 6 | 63.7 | 74 | 49 | Infraestructura de agentes u orquestación |
| PY_TOOL | 6 | 60.8 | 68 | 50 | Herramienta o CLI de Python |
| DUP_ARCHIVE | 4 | 56.5 | 71 | 48 | Copia, archivo o galería de versiones |
| PY_DATA | 4 | 63.5 | 67 | 60 | Python de datos, ML o pipeline |
| PLATFORM_JAVA | 2 | 45.0 | 52 | 38 | Plataforma Java server-side |
| DESIGN_SYSTEM | 2 | 31.5 | 32 | 31 | Sistema de diseño o tokens visuales |
| GO_CLI | 1 | 57.0 | 57 | 57 | Utilidad de línea de comandos en Go |

### 3.2 Los defectos que se repiten, en orden de coste de arreglar

| Defecto | Repos | Esfuerzo | Beneficio |
|---|---|---|---|
| Sin licencia | 32 | 1 línea por repo | Alto: sin esto nadie puede citarte ni reutilizarte |
| Historial de 5 commits o menos | 11 | un commit por cambio a partir de ahora | Medio: hoy el trabajo es invisible para un tercero |
| Sin instrucciones de ejecución | 27 | 1 comando en el README | Alto: sin esto el README no cumple su función |
| Conflicto de propiedad entre repos | 17 | 1 decisión | Alto: afecta al token completo del perfil |
| Sin homepage | 17 | 5 min si hay GitHub Pages | Medio: es lo primero que ve un visitante |
| Reclamo no verificable | 10 | 1 frase | Alto: es lo que hace que un revisarista no confíe |
| Sin CI | 8 (con manifest) | 1 fichero YAML | Alto: es la única prueba objetiva de que el repo vive |
| Sin tests | 49 sobre cero tests | Horas | Medio: bloquea el refactor con agente |
| Archivado sin cierre | 4 | 1 clic | Bajo, pero limpia ruido |

### 3.3 README: lo que de verdad se leyó

- Los 104 repos tienen README. Mediana real: **294 palabras**; media 539; máximo 7927.
- **28 de 104** no contienen **ni un solo comando de ejecución**. Un README sin comandos no dice cómo arrancar el proyecto.
- **50 de 104** no tienen sección de uso o instalación.
- Solo **5 de 104** tienen una imagen o captura. En repos de producto visual, esto es la mayor carencia: se describe un resultado que nadie ve.
- Solo **18 de 104** tienen badges.
- Idioma: 68 en español y 33 en inglés. Para posicionamiento conviene fijar uno o mantener las dos versiones.

### 3.4 El problema de fondo: cuatro ecosistemas compitiendo

| Token | Repos que lo reclaman | Consecuencia |
|---|---|---|
| `belentani` | 25 | Un tercero no sabe cuál es el bueno |
| `duck` | 18 | Un tercero no sabe cuál es el bueno |
| `omega` | 9 | Un tercero no sabe cuál es el bueno |
| `judas` | 7 | Un tercero no sabe cuál es el bueno |

Esto no lo arregla ninguna herramienta de IA. Es una decisión de estructura, y es la de
mayor impacto sobre cómo te recommended Google y las IAs.

---

## 4. Estudio de las herramientas creadoras de apps (estado real, septiembre 2026)

Esto es lo que existe hoy de verdad, con lo que cada una puede y lo que no. Precios y
capacidades verificados contra la documentación del propio fabricante.

### 4.1 Generadores en navegador (del prompt a la app desplegada)

| Plataforma | Dónde corre | Stack que produce | ¿Acepta repo existente? | Ejecuta y despliega | Precio 2026 | Mejor para |
|---|---|---|---|---|---|---|
| **Google AI Studio (Build mode)** | Navegador | React, Angular, Next.js; Android nativo en Kotlin/Compose; runtime Node.js | **Sí**, importación de GitHub con sincronización bidireccional | Sí, a Cloud Run | **Gratis**: 2 apps sin tarjeta | Del prompt a app full-stack en minutos |
| **Lovable** | Navegador | React con backend de Lovable o Supabase | Parcial: devuelve cambios a una rama de GitHub | Sí | Freemium | Producto web con login y datos |
| **Bolt.new** | Navegador (WebContainers) | Node.js. **Sin Python** | **Sí**, GitHub y exportación de vuelta | Sí | Freemium | App web con base de datos |
| **Replit Agent** | Navegador | Python **y** Node, PostgreSQL gestionado | **Sí**, repos públicos y privados | Sí | Freemium, por créditos | Python con hosting, y apps móviles |
| **v0 (Vercel)** | Navegador | Next.js, React, Tailwind | **Sí**, repos públicos y privados, monorepos | Preview deploy | De pago | Interfaz React/Next |
| **Databutton** | Navegador | FastAPI (Python) con React | Sin documentación de importación | Sí | De pago | Backend Python en navegador |
| **Firebase Studio** | Navegador | Múltiples | Sí | Sí | Gratis | **Se apaga el 22/03/2027**: migrar a AI Studio o Antigravity |

**Detalle relevante de Google AI Studio:** aprovisiona Firestore y Firebase Auth con
«Sign in with Google» cuando detecta que la app los necesita, guarda las claves en un gestor
de secretos del lado servidor (nunca en el cliente), integra Gmail, Sheets, Docs, Drive y
Calendar, genera imágenes con Nano Banana, construye **Android nativo** con emulador en el
navegador y publicación al Play Store, y exporta a Google Antigravity con el historial de
conversación y los secretos incluidos. Sin SDK y sin entorno local. Es, con diferencia, el
camino más corto de los que existen hoy entre una idea y una URL pública.

### 4.2 Agentes locales sobre repositorio existente

| Herramienta | Modelo | ¿Clave propia? | Precio 2026 | Punto fuerte |
|---|---|---|---|---|
| **Google Antigravity** | Gemini 3.x Flash/Pro, Claude, GPT-OSS | Parcial | **0 USD** con límites semanales básicos; Google AI Pro 20 USD | Orquestación multi-agente; tab completion sin límite de pago |
| **OpenCode** | Cualquiera (GLM, Gemini, Groq, local) | **Sí** | **0 USD** con BYOK | El más barato si ya traes clave de un modelo gratis |
| **Gemini CLI** | Gemini | Sí | **0 USD**, cuota gratuita | El más simple de instalar |
| **Cline / Kilo Code / Crush** | Cualquiera | **Sí** | **0 USD** con BYOK | Extensibles y manuales |
| **Claude Code** | Claude Opus/Sonnet | - | De pago | El agente único más fiable en refactors largos |
| **Codex CLI** | GPT | - | Incluido en planes Free/Go/Plus/Pro | Trabajo con repos y compilación |
| **ZCode (Z.ai)** | GLM-5.3, contexto 1M | - | Lite 12,60-18 USD/mes, Pro 56-80, Max 117,60-168 | Contexto largo y tareas autónomas de hasta 8 h |
| **Cursor** | Múltiples | Sí | De pago | Editor con indexado del repo |
| **GitHub Copilot** | Múltiples | - | Incluido en planes | Agente en la nube, de issues a PR |

**Z.ai en detalle:** el plan GLM Coding da GLM-5.3 con contexto de 1M de tokens; sus modelos
5.1 y 5.3 están diseñados para tareas de hasta 8 horas de ejecución autónoma. Funciona dentro
de Claude Code, Cline, OpenCode, Roo y Kilo, además de como IDE propio y como app de
escritorio. Z.ai declara 58,4 en SWE-bench Pro para el 5.1, por encima de GPT-5.4 y Claude
Opus 4.6. El contraste honesto: mediciones de terceros lo sitúan cerca de 62 frente a ~69 de
Claude Opus 4.8 en bruto, pero la ventaja está en las tareas largas, que es exactamente el
caso de un repositorio de orquestación de agentes.

### 4.3 La decisión de fondo: navegador o local

| | Navegador | Local |
|---|---|---|
| Instalar | nada | hay que instalar el cliente |
| Lenguajes | casi solo JS, salvo Replit, Emergent y Databutton | cualquiera |
| Python | limitado | sin límites |
| Ejecuta el código | sí, en su nube | sí, en tu máquina |
| Tus datos | en su infraestructura | en tu disco |
| Devuelve los cambios | a una rama, a veces | al árbol de trabajo, siempre |
| Coste | 0 al principio, crece con el uso | 0 con BYOK, o una suscripción |

**Regla práctica para tu caso:** de tus 104 repos, 51 son aplicaciones web y 20 son
Python (42 en TypeScript/JavaScript y 35 en HTML). El navegador gana en las web; en las de
Python, el agente local gana siempre.

---

## 5. Encaje recomendado por perfil

Esta es la tabla accionable. Cada perfil tiene su herramienta principal, su segunda opción,
dos alternativas y una advertencia concreta.

### WEB_APP_TS — Aplicación web con frontend o backend que se construye y se despliega (51 repos, nota media 62.0)

- **Principal: Google Antigravity (local)** — 0 USD con tab completion de Gemini Flash; admite Claude y GPT-OSS. Orquestación multi-agente para monorepos. Requiere instalar el IDE.
- **Segunda: Claude Code** — De pago. El agente único más fiable para refactors largos: lee CLAUDE.md y ejecuta el build en bucle.
- **Alternativa: Cursor** — De pago. Editor con indexado del repo; cómodo si ya trabajas dentro de un IDE.
- **Alternativa: Bolt.new** — 0 USD en navegador. Importa GitHub y devuelve los cambios a una rama. Solo Node.
- **No usar:** v0 (Next.js bonito pero incompatible con mantener este código), Replit y Lovable (no aceptan este repo tal cual)
- **Repos de este perfil:** `belentani-unified`, `linguaforge`, `belentani7`, `Belentani.cv-ai`, `Cruzando-el-charco`, `harmonia-hub`, `duck-ecosystem`, `belentani-experience-tour`, `belentaniexperience`, `belent-cad`, `lingua-aberta-empresa`, `pvc-u-frontend`, `system-one-unified`, `belentani-github-catalogo-minimalista`, `belentani-judas-web`, `belentani-omega-template`, `Belentanislide`, `duck-hub`, `tender-words-connect`, `secure-t`, `manos-abiertas-2026`, `win11-workspace`, `evidence-ledger`, `belentani-artista-unified`, `openclaw-workspace`, `duck-full-studio-pro`, `belentani_Omega`, `arte-que-veste`, `belentani-judas-era-omega`, `Duck-Omega`, `belentani-es-neon`, `fashion-stylist-ai`, `duck-lab`, `DUCK-ZION-PREMIUM`, `entrenador-jorge-bcn`, `Myopenhands`, `duck-music-lab`, `duck-belentani-os-audited-2026-08-23`, `belentani-judas-experience`, `duck-apps`, `duck-zion-apex-public`, `CARQUIDEC`, `Netlify`, `belentani-omega-immersive-portal`, `duck-apps-web`, `nexus-os`, `ai-command-center-level10`, `duck-studio-suite`, `omega-max-duck`, `judas-scifi-experience`, `omega-infinite-v4`

### SITIO_ESTATICO — Sitio estático, portfolio o showcase (11 repos, nota media 51.1)

- **Principal: Lovable** — Importa el repo desde GitHub, devuelve los cambios a una rama y despliega. Es el ciclo más corto hacia una URL pública.
- **Segunda: Google AI Studio (Build mode)** — 0 USD, 2 apps desplegadas gratis en Cloud Run sin tarjeta. Si lo que falta es backend, aprovisiona Firestore, Auth y Workspace solo.
- **Alternativa: Bolt.new** — 0 USD en navegador, con importación de GitHub.
- **Alternativa: Onlook** — Código abierto, edita tus componentes reales en vez de generar un mockup aparte.
- **No usar:** v0: regeneraría la página y perderías los assets ya optimizados
- **Repos de este perfil:** `llm-vfx-orchestrator`, `rh-fiscal-ultra-elite`, `NOIACORE`, `registro-proyectos-2026`, `local-agent`, `duck-2026`, `Steven-renovation`, `heyduck`, `belentani7.github.io`, `michelle-relayze-web`, `DuckHTML`

### PY_TOOL — Herramienta o CLI de Python (6 repos, nota media 60.8)

- **Principal: OpenCode o ZCode con BYOK** — 0-18 USD/mes. Lee el repo, ejecuta pytest y corrige. Barato y capaz para scripts.
- **Segunda: Claude Code** — De pago. Más fiable cuando el refactor toca varios ficheros a la vez.
- **Alternativa: Codex CLI** — De pago. Fuerte en trabajo con repos y compilación.
- **Alternativa: Gemini CLI** — 0 USD. Cuota gratuita; el candidato más obvio para no pagar.
- **No usar:** Replit y Bolt: su backend es Node y meterían el Python en un contenedor que no necesita
- **Repos de este perfil:** `comfyui-json-compiler`, `qbp-core`, `pvc-u-core`, `pbr-validator`, `belentani-the-judas-experience`, `deepseek-fix-verify`

### PY_DATA — Python de datos, ML o pipeline (4 repos, nota media 63.5)

- **Principal: Claude Code** — De pago. Sostiene una tarea larga sin perder el objetivo, que es lo que hace falta en un pipeline.
- **Segunda: Gemini CLI** — 0 USD con cuota gratuita. Suficiente para la mayoría de los pipelines.
- **Alternativa: Codex CLI** — De pago. Alternativa sólida.
- **Alternativa: Replit Agent** — De pago. Solo tiene sentido si además quieres el dataset alojado y ejecutándose.
- **No usar:** Plataformas web: aquí no hay nada que desplegar, hay una máquina que ejecutar
- **Repos de este perfil:** `gpu-cost-optimizer`, `belentani-video-forge`, `latent-consistency-bench`, `temporal-artifact-detector`

### SKILL_PACK — Pack de skills, prompts o registro de agentes (11 repos, nota media 58.8)

- **Principal: OpenCode o Claude Code en local, con tu propia clave** — 0-20 USD/mes. El trabajo es sobre ficheros locales de texto; la versión web de z.ai cobraría por prompt sin aportar nada.
- **Segunda: ZCode (Z.ai)** — 12,60-18 USD/mes el plan Lite con GLM-5.3. Buena opción si ya pagas ese plan para otras cosas.
- **Alternativa: Cline** — 0 USD en local con BYOK. Extensible, más manual.
- **Alternativa: Gemini CLI** — 0 USD, cuota gratuita generosa. El más simple de instalar.
- **No usar:** Plataformas de vibe coding web: aquí no hay app que construir
- **Repos de este perfil:** `cinematic-prompt-formatter`, `manus-ai-skill-pack`, `agent-skills`, `skills-registry`, `meta-skill`, `claude-skills-pack`, `duck-docs`, `skillforge`, `premium-effects-registry`, `MetaSkill`, `CODEX-OMEGA-SKILL`

### AGENT_INFRA — Infraestructura de agentes u orquestación (6 repos, nota media 63.7)

- **Principal: ZCode (GLM-5.3, contexto 1M)** — 12,60-18 USD/mes Lite. El más barato para contexto largo y tareas autónomas de hasta 8 horas.
- **Segunda: Claude Code** — De pago. La referencia en ejecución larga y fiable.
- **Alternativa: Google Antigravity** — 0 USD. Orquestación multi-agente real en local.
- **Alternativa: Codex CLI** — De pago. Alternativa sólida.
- **No usar:** Solo autocompletado: no van a seguir un objetivo de 50 pasos
- **Repos de este perfil:** `Belentani`, `oss-compass`, `omniagent`, `proofmesh`, `agentguard`, `noiacore-turbo-v2`

### DOCS_PLATFORM — Plataforma educativa o documentación (6 repos, nota media 68.8)

- **Principal: Claude Code** — De pago. Aquí lo que hace falta es consolidar contenido y migrar texto, no generar interfaz.
- **Segunda: Cursor** — De pago. Alternativa válida para edición de contenido a escala.
- **Alternativa: Google AI Studio (solo si pasa a ser app)** — 0 USD. Solo tiene sentido el día que necesite login y datos guardados.
- **Alternativa: OpenCode** — 0 USD con BYOK. Suficiente para trabajo de texto y estructura.
- **No usar:** Empezar otro repo de plataforma educativa: ya hay seis compitiendo
- **Repos de este perfil:** `ux-academy-professional-program`, `open-school`, `ManosAbiertas`, `aprende-brasil`, `WILLIAMSCHOOL`, `Oculus-Tv`

### GO_CLI — Utilidad de línea de comandos en Go (1 repos, nota media 57.0)

- **Principal: Claude Code** — De pago. Go se documenta solo: el agente itera sobre errores de compilación.
- **Segunda: Codex CLI** — De pago.
- **Alternativa: ZCode** — 12,60-18 USD/mes si ya lo usas.
- **Alternativa: Gemini CLI** — 0 USD.
- **No usar:** Plataformas de browser: no ejecutan Go
- **Repos de este perfil:** `agentbox`

### DESIGN_SYSTEM — Sistema de diseño o tokens visuales (2 repos, nota media 31.5)

- **Principal: Google Stitch o Figma Make, y después código** — Stitch es gratuito. Diseño primero, código después: el único orden que produce consistencia.
- **Segunda: Onlook** — Código abierto. Edita tus componentes React reales en vez de generar un mockup aparte.
- **Alternativa: Claude Code** — De pago. Para documentar los tokens y escribir el CSS a mano con criterio.
- **Alternativa: v0** — De pago. Solo para componentes sueltos, no para un sistema de tokens.
- **No usar:** Generar el CSS con un agente y esperar consistencia: no sale
- **Repos de este perfil:** `the-judas-experience`, `belentani-design-system`

### PLATFORM_JAVA — Plataforma Java server-side (2 repos, nota media 45.0)

- **Principal: Claude Code** — De pago. Necesitas un agente que ejecute el build; Java lo da gratis por tipado.
- **Segunda: Codex CLI** — De pago. Alternativa sólida.
- **Alternativa: ZCode** — 12,60-18 USD/mes si ya lo usas para Python.
- **Alternativa: Google Antigravity** — 0 USD.
- **No usar:** Plataformas de vibe coding: no compilan Java server-side
- **Repos de este perfil:** `belentani-monorepo`, `belentani-java-platform`

### DUP_ARCHIVE — Copia, archivo o galería de versiones (4 repos, nota media 56.5)

- **Principal: Ninguna herramienta: archivar** — 0 USD. El problema es una decisión, no una herramienta.
- **Segunda: Claude Code (solo para extraer lo aprovechable)** — De pago. Un único trabajo de consolidación; luego se archiva.
- **Alternativa: Cursor** — De pago. Mismo uso puntual.
- **Alternativa: OpenCode** — 0 USD con BYOK.
- **No usar:** Invertir horas de agente en un repo que debería estar archivado
- **Repos de este perfil:** `duck-unified-master`, `belentani-omega-showcase`, `ManosAbiertas-backup-v1`, `belentani-the-judas-experience-archive`

---

## 6. Ranking completo de los 104 repos

| # | Repo | Nota | Perfil | Leng | KB | Commits | Topics | README | 1ª herramienta |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [ux-academy-professional-program](https://github.com/belentani7/ux-academy-professional-program) | **80** | DOCS_PLATFORM | TypeScript | 2821 | 69 | 4 | 12998 B | Claude Code |
| 2 | [belentani-unified](https://github.com/belentani7/belentani-unified) | **79** | WEB_APP_TS | TypeScript | 127319 | 109 | 5 | 1969 B | Google Antigravity (local) |
| 3 | [open-school](https://github.com/belentani7/open-school) | **78** | DOCS_PLATFORM | TypeScript | 1810 | 72 | 3 | 7411 B | Claude Code |
| 4 | [linguaforge](https://github.com/belentani7/linguaforge) | **77** | WEB_APP_TS | TypeScript | 2104 | 126 | 3 | 19235 B | Google Antigravity (local) |
| 5 | [belentani7](https://github.com/belentani7/belentani7) | **76** | WEB_APP_TS | TypeScript | 791 | 97 | 5 | 2373 B | Google Antigravity (local) |
| 6 | [Belentani.cv-ai](https://github.com/belentani7/Belentani.cv-ai) | **76** | WEB_APP_TS | TypeScript | 2073 | 47 | 3 | 525 B | Google Antigravity (local) |
| 7 | [Cruzando-el-charco](https://github.com/belentani7/Cruzando-el-charco) | **74** | WEB_APP_TS | HTML | 8788 | 112 | 11 | 4074 B | Google Antigravity (local) |
| 8 | [Belentani](https://github.com/belentani7/Belentani) | **74** | AGENT_INFRA | TypeScript | 795 | 65 | 4 | 2197 B | ZCode (GLM-5.3, contexto 1M) |
| 9 | [ManosAbiertas](https://github.com/belentani7/ManosAbiertas) | **73** | DOCS_PLATFORM | TypeScript | 16513 | 102 | 4 | 1265 B | Claude Code |
| 10 | [harmonia-hub](https://github.com/belentani7/harmonia-hub) | **73** | WEB_APP_TS | TypeScript | 1218 | 30 | 4 | 28644 B | Google Antigravity (local) |
| 11 | [duck-ecosystem](https://github.com/belentani7/duck-ecosystem) | **73** | WEB_APP_TS | TypeScript | 477 | 43 | 3 | 5572 B | Google Antigravity (local) |
| 12 | [belentani-experience-tour](https://github.com/belentani7/belentani-experience-tour) | **72** | WEB_APP_TS | TypeScript | 125 | 12 | 5 | 5238 B | Google Antigravity (local) |
| 13 | [cinematic-prompt-formatter](https://github.com/belentani7/cinematic-prompt-formatter) | **72** | SKILL_PACK | Python | 99 | 13 | 5 | 4391 B | OpenCode / Claude Code (local, BYOK) |
| 14 | [belentaniexperience](https://github.com/belentani7/belentaniexperience) | **72** | WEB_APP_TS | TypeScript | 522 | 44 | 10 | 1931 B | Google Antigravity (local) |
| 15 | [manus-ai-skill-pack](https://github.com/belentani7/manus-ai-skill-pack) | **72** | SKILL_PACK | Python | 9845 | 24 | 4 | 1177 B | OpenCode / Claude Code (local, BYOK) |
| 16 | [duck-unified-master](https://github.com/belentani7/duck-unified-master) | **71** | DUP_ARCHIVE | HTML | 22576 | 15 | 3 | 4680 B | Claude Code (solo para consolidar) |
| 17 | [oss-compass](https://github.com/belentani7/oss-compass) | **71** | AGENT_INFRA | Python | 101 | 16 | 5 | 12912 B | ZCode (GLM-5.3, contexto 1M) |
| 18 | [belent-cad](https://github.com/belentani7/belent-cad) | **70** | WEB_APP_TS | TypeScript | 449 | 8 | 5 | 4322 B | Google Antigravity (local) |
| 19 | [lingua-aberta-empresa](https://github.com/belentani7/lingua-aberta-empresa) | **68** | WEB_APP_TS | HTML | 35 | 11 | 5 | 309 B | Google Antigravity (local) |
| 20 | [pvc-u-frontend](https://github.com/belentani7/pvc-u-frontend) | **68** | WEB_APP_TS | TypeScript | 63 | 13 | 3 | 365 B | Google Antigravity (local) |
| 21 | [comfyui-json-compiler](https://github.com/belentani7/comfyui-json-compiler) | **68** | PY_TOOL | Python | 55 | 12 | 5 | 5305 B | OpenCode / ZCode (BYOK) |
| 22 | [agent-skills](https://github.com/belentani7/agent-skills) | **67** | SKILL_PACK | Python | 8000 | 9 | 5 | 52865 B | OpenCode / Claude Code (local, BYOK) |
| 23 | [skills-registry](https://github.com/belentani7/skills-registry) | **67** | SKILL_PACK | TypeScript | 100 | 17 | 6 | 3005 B | OpenCode / Claude Code (local, BYOK) |
| 24 | [omniagent](https://github.com/belentani7/omniagent) | **67** | AGENT_INFRA | Python | 56 | 19 | 5 | 4220 B | ZCode (GLM-5.3, contexto 1M) |
| 25 | [llm-vfx-orchestrator](https://github.com/belentani7/llm-vfx-orchestrator) | **67** | SITIO_ESTATICO | HTML | 41 | 9 | 4 | 2561 B | Lovable |
| 26 | [gpu-cost-optimizer](https://github.com/belentani7/gpu-cost-optimizer) | **67** | PY_DATA | Python | 43 | 13 | 4 | 1870 B | Claude Code |
| 27 | [system-one-unified](https://github.com/belentani7/system-one-unified) | **66** | WEB_APP_TS | TypeScript | 469 | 2 | 5 | 1833 B | Google Antigravity (local) |
| 28 | [belentani-github-catalogo-minimalista](https://github.com/belentani7/belentani-github-catalogo-minimalista) | **66** | WEB_APP_TS | TypeScript | 177 | 11 | 6 | 653 B | Google Antigravity (local) |
| 29 | [belentani-judas-web](https://github.com/belentani7/belentani-judas-web) | **66** | WEB_APP_TS | TypeScript | 70 | 16 | 4 | 1278 B | Google Antigravity (local) |
| 30 | [aprende-brasil](https://github.com/belentani7/aprende-brasil) | **66** | DOCS_PLATFORM | TypeScript | 1635 | 27 | 3 | 7272 B | Claude Code |
| 31 | [proofmesh](https://github.com/belentani7/proofmesh) | **66** | AGENT_INFRA | TypeScript | 254 | 11 | 5 | 2389 B | ZCode (GLM-5.3, contexto 1M) |
| 32 | [belentani-omega-template](https://github.com/belentani7/belentani-omega-template) | **66** | WEB_APP_TS | HTML | 17760 | 23 | 4 | 2514 B | Google Antigravity (local) |
| 33 | [meta-skill](https://github.com/belentani7/meta-skill) | **66** | SKILL_PACK | HTML | 44 | 17 | 4 | 2819 B | OpenCode / Claude Code (local, BYOK) |
| 34 | [Belentanislide](https://github.com/belentani7/Belentanislide) | **65** | WEB_APP_TS | HTML | 569 | 10 | 5 | 1169 B | Google Antigravity (local) |
| 35 | [duck-hub](https://github.com/belentani7/duck-hub) | **65** | WEB_APP_TS | TypeScript | 452 | 5 | 3 | 1111 B | Google Antigravity (local) |
| 36 | [qbp-core](https://github.com/belentani7/qbp-core) | **65** | PY_TOOL | Python | 46 | 9 | 4 | 4800 B | OpenCode / ZCode (BYOK) |
| 37 | [tender-words-connect](https://github.com/belentani7/tender-words-connect) | **65** | WEB_APP_TS | TypeScript | 659 | 112 | 6 | 3539 B | Google Antigravity (local) |
| 38 | [secure-t](https://github.com/belentani7/secure-t) | **64** | WEB_APP_TS | HTML | 70465 | 5 | 5 | 797 B | Google Antigravity (local) |
| 39 | [manos-abiertas-2026](https://github.com/belentani7/manos-abiertas-2026) | **64** | WEB_APP_TS | HTML | 52 | 10 | 6 | 2982 B | Google Antigravity (local) |
| 40 | [win11-workspace](https://github.com/belentani7/win11-workspace) | **64** | WEB_APP_TS | TypeScript | 280 | 6 | 3 | 4633 B | Google Antigravity (local) |
| 41 | [belentani-video-forge](https://github.com/belentani7/belentani-video-forge) | **64** | PY_DATA | Python | 5617 | 11 | 5 | 2129 B | Claude Code |
| 42 | [evidence-ledger](https://github.com/belentani7/evidence-ledger) | **64** | WEB_APP_TS | HTML | 139 | 9 | 5 | 2078 B | Google Antigravity (local) |
| 43 | [belentani-artista-unified](https://github.com/belentani7/belentani-artista-unified) | **63** | WEB_APP_TS | HTML | 63961 | 17 | 4 | 792 B | Google Antigravity (local) |
| 44 | [pvc-u-core](https://github.com/belentani7/pvc-u-core) | **63** | PY_TOOL | Python | 325 | 8 | 5 | 6732 B | OpenCode / ZCode (BYOK) |
| 45 | [pbr-validator](https://github.com/belentani7/pbr-validator) | **63** | PY_TOOL | Python | 38 | 8 | 5 | 1979 B | OpenCode / ZCode (BYOK) |
| 46 | [latent-consistency-bench](https://github.com/belentani7/latent-consistency-bench) | **63** | PY_DATA | Python | 43 | 8 | 4 | 4550 B | Claude Code |
| 47 | [WILLIAMSCHOOL](https://github.com/belentani7/WILLIAMSCHOOL) | **62** | DOCS_PLATFORM | TypeScript | 2144 | 15 | 2 | 270 B | Claude Code |
| 48 | [openclaw-workspace](https://github.com/belentani7/openclaw-workspace) | **62** | WEB_APP_TS | HTML | 88835 | 7 | 3 | 1696 B | Google Antigravity (local) |
| 49 | [duck-full-studio-pro](https://github.com/belentani7/duck-full-studio-pro) | **62** | WEB_APP_TS | HTML | 1332 | 37 | 3 | 1815 B | Google Antigravity (local) |
| 50 | [belentani_Omega](https://github.com/belentani7/belentani_Omega) | **62** | WEB_APP_TS | HTML | 90001 | 37 | 4 | 9290 B | Google Antigravity (local) |
| 51 | [arte-que-veste](https://github.com/belentani7/arte-que-veste) | **61** | WEB_APP_TS | HTML | 856 | 18 | 4 | 250 B | Google Antigravity (local) |
| 52 | [belentani-judas-era-omega](https://github.com/belentani7/belentani-judas-era-omega) | **60** | WEB_APP_TS | TypeScript | 10992 | 20 | 5 | 533 B | Google Antigravity (local) |
| 53 | [temporal-artifact-detector](https://github.com/belentani7/temporal-artifact-detector) | **60** | PY_DATA | Python | 43 | 8 | 5 | 3148 B | Claude Code |
| 54 | [Duck-Omega](https://github.com/belentani7/Duck-Omega) | **60** | WEB_APP_TS | TypeScript | 523 | 43 | 3 | 333 B | Google Antigravity (local) |
| 55 | [belentani-es-neon](https://github.com/belentani7/belentani-es-neon) | **59** | WEB_APP_TS | JavaScript | 6107 | 5 | 4 | 1062 B | Google Antigravity (local) |
| 56 | [fashion-stylist-ai](https://github.com/belentani7/fashion-stylist-ai) | **59** | WEB_APP_TS | HTML | 318 | 3 | 3 | 10834 B | Google Antigravity (local) |
| 57 | [duck-lab](https://github.com/belentani7/duck-lab) | **59** | WEB_APP_TS | TypeScript | 332 | 12 | 3 | 2422 B | Google Antigravity (local) |
| 58 | [DUCK-ZION-PREMIUM](https://github.com/belentani7/DUCK-ZION-PREMIUM) | **59** | WEB_APP_TS | HTML | 208012 | 6 | 3 | 4580 B | Google Antigravity (local) |
| 59 | [entrenador-jorge-bcn](https://github.com/belentani7/entrenador-jorge-bcn) | **59** | WEB_APP_TS | HTML | 1224 | 24 | 4 | 2598 B | Google Antigravity (local) |
| 60 | [Myopenhands](https://github.com/belentani7/Myopenhands) | **58** | WEB_APP_TS | TypeScript | 275 | 7 | 3 | 264 B | Google Antigravity (local) |
| 61 | [agentbox](https://github.com/belentani7/agentbox) | **57** | GO_CLI | Go | 42 | 8 | 4 | 7254 B | Claude Code |
| 62 | [duck-music-lab](https://github.com/belentani7/duck-music-lab) | **57** | WEB_APP_TS | HTML | 64 | 11 | 4 | 2200 B | Google Antigravity (local) |
| 63 | [duck-belentani-os-audited-2026-08-23](https://github.com/belentani7/duck-belentani-os-audited-2026-08-23) | **57** | WEB_APP_TS | TypeScript | 393 | 19 | 3 | 371 B | Google Antigravity (local) |
| 64 | [rh-fiscal-ultra-elite](https://github.com/belentani7/rh-fiscal-ultra-elite) | **57** | SITIO_ESTATICO | HTML | 49 | 9 | 4 | 1666 B | Lovable |
| 65 | [NOIACORE](https://github.com/belentani7/NOIACORE) | **57** | SITIO_ESTATICO | HTML | 8414 | 9 | 3 | 20458 B | Lovable |
| 66 | [belentani-the-judas-experience](https://github.com/belentani7/belentani-the-judas-experience) | **56** | PY_TOOL | Python | 63 | 10 | 6 | 1578 B | OpenCode / ZCode (BYOK) |
| 67 | [belentani-judas-experience](https://github.com/belentani7/belentani-judas-experience) | **56** | WEB_APP_TS | TypeScript | 1171 | 8 | 3 | 459 B | Google Antigravity (local) |
| 68 | [duck-apps](https://github.com/belentani7/duck-apps) | **56** | WEB_APP_TS | HTML | 873 | 16 | 2 | 1989 B | Google Antigravity (local) |
| 69 | [duck-zion-apex-public](https://github.com/belentani7/duck-zion-apex-public) | **56** | WEB_APP_TS | TypeScript | 543 | 15 | 2 | 1977 B | Google Antigravity (local) |
| 70 | [CARQUIDEC](https://github.com/belentani7/CARQUIDEC) | **56** | WEB_APP_TS | HTML | 517592 | 31 | 3 | 398 B | Google Antigravity (local) |
| 71 | [belentani-omega-showcase](https://github.com/belentani7/belentani-omega-showcase) | **55** | DUP_ARCHIVE | HTML | 18654 | 8 | 4 | 712 B | Claude Code (solo para consolidar) |
| 72 | [agentguard](https://github.com/belentani7/agentguard) | **55** | AGENT_INFRA | Python | 31 | 6 | 4 | 8998 B | ZCode (GLM-5.3, contexto 1M) |
| 73 | [claude-skills-pack](https://github.com/belentani7/claude-skills-pack) | **55** | SKILL_PACK | HTML | 80 | 13 | 4 | 2680 B | OpenCode / Claude Code (local, BYOK) |
| 74 | [Netlify](https://github.com/belentani7/Netlify) | **55** | WEB_APP_TS | JavaScript | 2877 | 279 | 4 | 1782 B | Google Antigravity (local) |
| 75 | [duck-docs](https://github.com/belentani7/duck-docs) | **54** | SKILL_PACK | TypeScript | 6876 | 8 | 2 | 772 B | OpenCode / Claude Code (local, BYOK) |
| 76 | [belentani-omega-immersive-portal](https://github.com/belentani7/belentani-omega-immersive-portal) | **54** | WEB_APP_TS | JavaScript | 8244 | 30 | 4 | 333 B | Google Antigravity (local) |
| 77 | [Oculus-Tv](https://github.com/belentani7/Oculus-Tv) | **54** | DOCS_PLATFORM | TypeScript | 1536 | 32 | 4 | 4146 B | Claude Code |
| 78 | [skillforge](https://github.com/belentani7/skillforge) | **53** | SKILL_PACK | Python | 45 | 7 | 4 | 5541 B | OpenCode / Claude Code (local, BYOK) |
| 79 | [duck-apps-web](https://github.com/belentani7/duck-apps-web) | **53** | WEB_APP_TS | HTML | 886 | 6 | 2 | 1596 B | Google Antigravity (local) |
| 80 | [registro-proyectos-2026](https://github.com/belentani7/registro-proyectos-2026) | **53** | SITIO_ESTATICO | HTML | 60 | 11 | 3 | 244 B | Lovable |
| 81 | [premium-effects-registry](https://github.com/belentani7/premium-effects-registry) | **52** | SKILL_PACK | Python | 10 | 6 | 6 | 512 B | OpenCode / Claude Code (local, BYOK) |
| 82 | [belentani-monorepo](https://github.com/belentani7/belentani-monorepo) | **52** | PLATFORM_JAVA | Java | 157 | 10 | 2 | 362 B | Claude Code |
| 83 | [nexus-os](https://github.com/belentani7/nexus-os) | **52** | WEB_APP_TS | JavaScript | 776 | 7 | 4 | 6083 B | Google Antigravity (local) |
| 84 | [ManosAbiertas-backup-v1](https://github.com/belentani7/ManosAbiertas-backup-v1) | **52** | DUP_ARCHIVE | TypeScript | 12503 | 83 | 6 | 6067 B | Claude Code (solo para consolidar) |
| 85 | [local-agent](https://github.com/belentani7/local-agent) | **52** | SITIO_ESTATICO | PowerShell | 159 | 4 | 5 | 2098 B | Lovable |
| 86 | [deepseek-fix-verify](https://github.com/belentani7/deepseek-fix-verify) | **50** | PY_TOOL | Python | 42 | 9 | 3 | 221 B | OpenCode / ZCode (BYOK) |
| 87 | [ai-command-center-level10](https://github.com/belentani7/ai-command-center-level10) | **50** | WEB_APP_TS | TypeScript | 624 | 19 | 3 | 2172 B | Google Antigravity (local) |
| 88 | [noiacore-turbo-v2](https://github.com/belentani7/noiacore-turbo-v2) | **49** | AGENT_INFRA | Python | 219 | 2 | 3 | 13382 B | ZCode (GLM-5.3, contexto 1M) |
| 89 | [duck-2026](https://github.com/belentani7/duck-2026) | **49** | SITIO_ESTATICO | HTML | 5541 | 17 | 4 | 3422 B | Lovable |
| 90 | [Steven-renovation](https://github.com/belentani7/Steven-renovation) | **49** | SITIO_ESTATICO | HTML | 5881 | 27 | 4 | 421 B | Lovable |
| 91 | [belentani-the-judas-experience-archive](https://github.com/belentani7/belentani-the-judas-experience-archive) | **48** | DUP_ARCHIVE | HTML | 37840 | 9 | 3 | 2042 B | Claude Code (solo para consolidar) |
| 92 | [duck-studio-suite](https://github.com/belentani7/duck-studio-suite) | **48** | WEB_APP_TS | TypeScript | 186 | 10 | 3 | 261 B | Google Antigravity (local) |
| 93 | [heyduck](https://github.com/belentani7/heyduck) | **48** | SITIO_ESTATICO | HTML | 57767 | 16 | 2 | 3087 B | Lovable |
| 94 | [MetaSkill](https://github.com/belentani7/MetaSkill) | **47** | SKILL_PACK | Python | 18 | 5 | 8 | 3293 B | OpenCode / Claude Code (local, BYOK) |
| 95 | [belentani7.github.io](https://github.com/belentani7/belentani7.github.io) | **46** | SITIO_ESTATICO | HTML | 92 | 13 | 3 | 2657 B | Lovable |
| 96 | [omega-max-duck](https://github.com/belentani7/omega-max-duck) | **46** | WEB_APP_TS | TypeScript | 279 | 4 | 2 | 2732 B | Google Antigravity (local) |
| 97 | [judas-scifi-experience](https://github.com/belentani7/judas-scifi-experience) | **46** | WEB_APP_TS | TypeScript | 164 | 6 | 3 | 25790 B | Google Antigravity (local) |
| 98 | [michelle-relayze-web](https://github.com/belentani7/michelle-relayze-web) | **45** | SITIO_ESTATICO | HTML | 3694 | 8 | 3 | 1177 B | Lovable |
| 99 | [omega-infinite-v4](https://github.com/belentani7/omega-infinite-v4) | **42** | WEB_APP_TS | HTML | 11 | 8 | 3 | 109 B | Google Antigravity (local) |
| 100 | [CODEX-OMEGA-SKILL](https://github.com/belentani7/CODEX-OMEGA-SKILL) | **42** | SKILL_PACK | PowerShell | 28 | 8 | 4 | 1939 B | OpenCode / Claude Code (local, BYOK) |
| 101 | [DuckHTML](https://github.com/belentani7/DuckHTML) | **39** | SITIO_ESTATICO | HTML | 35 | 14 | 3 | 1736 B | Lovable |
| 102 | [belentani-java-platform](https://github.com/belentani7/belentani-java-platform) | **38** | PLATFORM_JAVA | Java | 15 | 9 | 3 | 322 B | Claude Code |
| 103 | [the-judas-experience](https://github.com/belentani7/the-judas-experience) | **32** | DESIGN_SYSTEM | CSS | 2249 | 2 | 4 | 2592 B | Figma Make / Google Stitch -> codigo |
| 104 | [belentani-design-system](https://github.com/belentani7/belentani-design-system) | **31** | DESIGN_SYSTEM | CSS | 4 | 3 | 6 | 901 B | Figma Make / Google Stitch -> codigo |

---

## 7. Dossier repo por repo (104 fichas)

Ordenados de mejor a peor. Cada ficha trae los 20 aspectos, las penalizaciones con su
motivo, la herramienta que mejor encaja y la primera acción concreta.

### 1. ux-academy-professional-program — 80/100

[https://github.com/belentani7/ux-academy-professional-program](https://github.com/belentani7/ux-academy-professional-program) · **DOCS_PLATFORM** · TypeScript · 2821 KB · 69 commits · 318 ficheros · creado 2026-08-27 · último push hace 0 días

> Trilingual UX/Product Design learning platform — practice exercises, evaluation system, and capstone projects

**Los 20 aspectos** — suma 81/100, penalizaciones -1, nota final 80/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 1669 palabras · 13 encabezados · 3 bloques de código · 22 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 10 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Contenido más estructura de curso. El cuello de botella real no es la calidad del texto: es la duplicación. Hay al menos seis repos de plataforma educativa compitiendo por el mismo título. El agente sirve para consolidar, no para añadir una séptima copia.

- Segunda opción: **Cursor**
- Alternativas: **Google AI Studio (si pasa a ser app)** · **OpenCode**

**Primera acción:** Elegir un único repo canónico para el contenido educativo, migrar lo bueno y convertir el resto en archivados con enlace al canónico.

**Evitar:** Empezar otro repo de plataforma educativa: ya hay seis.

---

### 2. belentani-unified — 79/100

[https://github.com/belentani7/belentani-unified](https://github.com/belentani7/belentani-unified) · **WEB_APP_TS** · TypeScript · 127319 KB · 109 commits · 4203 ficheros · creado 2026-09-04 · último push hace 0 días

> Unified monorepo: AION + Nexus + artist work (belentani). Duck/client repos excluded. Code organization only.

**Los 20 aspectos** — suma 85/100, penalizaciones -6, nota final 79/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **5/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **5/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **5/5** | Unicidad en el ecosistema | **3/5** |

**README leído:** 292 palabras · 6 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 3 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 4 repos comparten el token 'unified'. Ninguno es canonico.) — -3
- `PESADO` (124 MB de assets versionados: clonar es lento y el despliegue tarda.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 4 repos comparten el token 'unified' → 3/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 3. open-school — 78/100

[https://github.com/belentani7/open-school](https://github.com/belentani7/open-school) · **DOCS_PLATFORM** · TypeScript · 1810 KB · 72 commits · 176 ficheros · creado 2026-09-02 · último push hace 0 días

> Instituto educativo digital universal — cursos modulares, certificaciones verificables, accesibilidad WCAG, offline-first

**Los 20 aspectos** — suma 79/100, penalizaciones -1, nota final 78/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 1035 palabras · 13 encabezados · 2 bloques de código · 6 enlaces · 0 imágenes · 1 badges · idioma es · comandos de ejecución: 8 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Contenido más estructura de curso. El cuello de botella real no es la calidad del texto: es la duplicación. Hay al menos seis repos de plataforma educativa compitiendo por el mismo título. El agente sirve para consolidar, no para añadir una séptima copia.

- Segunda opción: **Cursor**
- Alternativas: **Google AI Studio (si pasa a ser app)** · **OpenCode**

**Primera acción:** Elegir un único repo canónico para el contenido educativo, migrar lo bueno y convertir el resto en archivados con enlace al canónico.

**Evitar:** Empezar otro repo de plataforma educativa: ya hay seis.

---

### 4. linguaforge — 77/100

[https://github.com/belentani7/linguaforge](https://github.com/belentani7/linguaforge) · **WEB_APP_TS** · TypeScript · 2104 KB · 126 commits · 279 ficheros · creado 2026-08-15 · último push hace 2 días

> Forja linguistica: herramientas de traduccion y adaptacion multilingue.

**Los 20 aspectos** — suma 78/100, penalizaciones -1, nota final 77/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **2/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **5/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **1/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 2201 palabras · 28 encabezados · 3 bloques de código · 25 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 15 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 5. belentani7 — 76/100

[https://github.com/belentani7/belentani7](https://github.com/belentani7/belentani7) · **WEB_APP_TS** · TypeScript · 791 KB · 97 commits · 281 ficheros · creado 2026-08-11 · último push hace 2 días

> Belentani + NOIACORE | Frontend, creative technology and educational platforms

**Los 20 aspectos** — suma 77/100, penalizaciones -1, nota final 76/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **2/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 236 palabras · 4 encabezados · 0 bloques de código · 17 enlaces · 1 imágenes · 0 badges · idioma es · comandos de ejecución: 1 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 6. Belentani.cv-ai — 76/100

[https://github.com/belentani7/Belentani.cv-ai](https://github.com/belentani7/Belentani.cv-ai) · **WEB_APP_TS** · TypeScript · 2073 KB · 47 commits · 231 ficheros · creado 2026-08-05 · último push hace 2 días

> AI-powered document studio — CVs, cover letters, presentations. €0.99 one-time, GDPR compliant, AES-256

**Los 20 aspectos** — suma 77/100, penalizaciones -1, nota final 76/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **2/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 72 palabras · 4 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 8 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 7. Cruzando-el-charco — 74/100

[https://github.com/belentani7/Cruzando-el-charco](https://github.com/belentani7/Cruzando-el-charco) · **WEB_APP_TS** · HTML · 8788 KB · 112 commits · 95 ficheros · creado 2026-08-07 · último push hace 0 días

> Cruzando el Charco, impulsado por noiacore.com y creado por Pedro Belentani, es un portal gratuito y confidencial de acogida, supervivencia y arraigo para hombres migrantes LGBT+ en L'Hospitalet y Barcelona. Información directa y práctica sobre papeles, salud, vivienda y comunidad.

**Los 20 aspectos** — suma 75/100, penalizaciones -1, nota final 74/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **5/5** | CI/CD | **5/5** |
| Topics | **5/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **5/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **3/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 548 palabras · 8 encabezados · 3 bloques de código · 1 enlaces · 0 imágenes · 1 badges · idioma es · comandos de ejecución: 2 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 8. Belentani — 74/100

[https://github.com/belentani7/Belentani](https://github.com/belentani7/Belentani) · **AGENT_INFRA** · TypeScript · 795 KB · 65 commits · 331 ficheros · creado 2026-07-31 · último push hace 2 días

> NOIACORE LAB — plataforma digital de Pedro Belentani: catálogo, agente, automatización, observabilidad y diseño cinematográfico.

**Los 20 aspectos** — suma 75/100, penalizaciones -1, nota final 74/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **2/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **2/5** |
| Tests | **5/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 268 palabras · 8 encabezados · 3 bloques de código · 3 enlaces · 3 imágenes · 3 badges · idioma es · comandos de ejecución: 13 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: ZCode (GLM-5.3, contexto 1M)**

La orquestación multi-agente es un problema de contexto largo: hay que sostener el estado de muchos pasos. GLM-5.3 con 1M de contexto es el más barato para eso (Lite ~12,60 USD/mes) y sus modelos 5.1 y 5.3 están diseñados para tareas autónomas de hasta 8 horas. Antigravity aporta la orquestación multi-agente real en local, gratis.

- Segunda opción: **Claude Code**
- Alternativas: **Google Antigravity (multi-agente)** · **Codex CLI**

**Primera acción:** Documentar el protocolo en un README de 20 líneas y cubrir el núcleo con tests. Un orquestador sin tests es código que no se puede cambiar.

**Evitar:** Solo autocompletado: no van a seguir un objetivo de 50 pasos.

---

### 9. ManosAbiertas — 73/100

[https://github.com/belentani7/ManosAbiertas](https://github.com/belentani7/ManosAbiertas) · **DOCS_PLATFORM** · TypeScript · 16513 KB · 102 commits · 1504 ficheros · creado 2026-08-23 · último push hace 0 días

> Plataforma educativa gratuita: cursos IA/Office, creador CV, guías derechos y recursos para migrantes y comunidades.

**Los 20 aspectos** — suma 76/100, penalizaciones -3, nota final 73/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **5/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **2/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 139 palabras · 10 encabezados · 4 bloques de código · 6 enlaces · 0 imágenes · 1 badges · idioma es · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Contenido más estructura de curso. El cuello de botella real no es la calidad del texto: es la duplicación. Hay al menos seis repos de plataforma educativa compitiendo por el mismo título. El agente sirve para consolidar, no para añadir una séptima copia.

- Segunda opción: **Cursor**
- Alternativas: **Google AI Studio (si pasa a ser app)** · **OpenCode**

**Primera acción:** Elegir un único repo canónico para el contenido educativo, migrar lo bueno y convertir el resto en archivados con enlace al canónico.

**Evitar:** Empezar otro repo de plataforma educativa: ya hay seis.

---

### 10. harmonia-hub — 73/100

[https://github.com/belentani7/harmonia-hub](https://github.com/belentani7/harmonia-hub) · **WEB_APP_TS** · TypeScript · 1218 KB · 30 commits · 209 ficheros · creado 2026-08-18 · último push hace 2 días

> Harmonia Hub - plataforma de coordinacion y bienestar.

**Los 20 aspectos** — suma 74/100, penalizaciones -1, nota final 73/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **2/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 3360 palabras · 33 encabezados · 23 bloques de código · 3 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 11. duck-ecosystem — 73/100

[https://github.com/belentani7/duck-ecosystem](https://github.com/belentani7/duck-ecosystem) · **WEB_APP_TS** · TypeScript · 477 KB · 43 commits · 232 ficheros · creado 2026-08-18 · último push hace 2 días

> Ecosistema DUCK - herramientas, GUIs y apps del estudio creativo DUCK.

**Los 20 aspectos** — suma 74/100, penalizaciones -1, nota final 73/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **4/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **4/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 653 palabras · 15 encabezados · 3 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 1 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 12. belentani-experience-tour — 72/100

[https://github.com/belentani7/belentani-experience-tour](https://github.com/belentani7/belentani-experience-tour) · **WEB_APP_TS** · TypeScript · 125 KB · 12 commits · 56 ficheros · creado 2026-09-15 · último push hace 2 días

> Living UI/UX library (thick glossy red glassmorphism) that grows itself: one new React component generated every day, no API. 175 assets indexed.

**Los 20 aspectos** — suma 75/100, penalizaciones -3, nota final 72/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 720 palabras · 14 encabezados · 6 bloques de código · 2 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 18 · sección de uso: sí

**Penalizaciones**

- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 13. cinematic-prompt-formatter — 72/100

[https://github.com/belentani7/cinematic-prompt-formatter](https://github.com/belentani7/cinematic-prompt-formatter) · **SKILL_PACK** · Python · 99 KB · 13 commits · 37 ficheros · creado 2026-08-16 · último push hace 2 días

> Translate cinematic language into optimized prompts for Stable Diffusion, Flux, and SDXL models.

**Los 20 aspectos** — suma 72/100, penalizaciones 0, nota final 72/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **2/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 622 palabras · 20 encabezados · 4 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 2 · sección de uso: sí

**Sin penalizaciones.**

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 14. belentaniexperience — 72/100

[https://github.com/belentani7/belentaniexperience](https://github.com/belentani7/belentaniexperience) · **WEB_APP_TS** · TypeScript · 522 KB · 44 commits · 108 ficheros · creado 2026-08-15 · último push hace 2 días

> Portfolio premium de Pedro Belentani: Trust & Safety, sistemas de IA, automatización, ingeniería de software y creative tech.

**Los 20 aspectos** — suma 73/100, penalizaciones -1, nota final 72/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **5/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 157 palabras · 6 encabezados · 2 bloques de código · 6 enlaces · 0 imágenes · 5 badges · idioma es · comandos de ejecución: 4 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 15. manus-ai-skill-pack — 72/100

[https://github.com/belentani7/manus-ai-skill-pack](https://github.com/belentani7/manus-ai-skill-pack) · **SKILL_PACK** · Python · 9845 KB · 24 commits · 3017 ficheros · creado 2026-08-15 · último push hace 2 días

> Pack de skills para agentes de codigo (estilo Manus/Claude) listos para produccion.

**Los 20 aspectos** — suma 74/100, penalizaciones -2, nota final 72/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 110 palabras · 6 encabezados · 1 bloques de código · 6 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Buena práctica detectada (afirmación concreta y comprobable):**
- `253 skills` → cuantifica el contenido con un numero verificable

**Penalizaciones**

- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 16. duck-unified-master — 71/100

[https://github.com/belentani7/duck-unified-master](https://github.com/belentani7/duck-unified-master) · **DUP_ARCHIVE** · HTML · 22576 KB · 15 commits · 1208 ficheros · creado 2026-08-26 · último push hace 2 días

> DUCK ecosystem consolidation — 9 repos unified into one monorepo with apps, docs, and shared infrastructure

**Los 20 aspectos** — suma 79/100, penalizaciones -8, nota final 71/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **2/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **4/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **5/5** | Unicidad en el ecosistema | **3/5** |

**README leído:** 678 palabras · 30 encabezados · 5 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 20 · sección de uso: sí

**Afirmaciones no verificables detectadas:**
- `production-ready` → afirma estar listo para produccion sin evidencia

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: 'production-ready' (afirma estar listo para produccion sin evidencia). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 4 repos comparten el token 'unified'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 4 repos comparten el token 'unified' → 3/5

**Herramienta principal: Claude Code (solo para consolidar)**

Un backup o una galería de versiones no se desarrolla: se decide su futuro. Un agente solo tiene sentido para extraer lo aprovechable y moverlo al repo canónico. Cuatro copias vivas de lo mismo es el problema, y no lo arregla ninguna herramienta: lo arregla una decisión.

- Segunda opción: **Ninguna: archivar**
- Alternativas: **Cursor** · **OpenCode**

**Primera acción:** Archivar con isArchived=true o borrar, dejando un único repo canónico. Solo esto ya sube la percepción de todo el perfil.

**Evitar:** Invertir horas de agente en un repo que debería estar archivado.

---

### 17. oss-compass — 71/100

[https://github.com/belentani7/oss-compass](https://github.com/belentani7/oss-compass) · **AGENT_INFRA** · Python · 101 KB · 16 commits · 45 ficheros · creado 2026-08-16 · último push hace 24 días

> Universal validation envelopes with auditable 2-of-3 node confirmation

**Los 20 aspectos** — suma 72/100, penalizaciones -1, nota final 71/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **4/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 1576 palabras · 15 encabezados · 9 bloques de código · 7 enlaces · 1 imágenes · 4 badges · idioma es · comandos de ejecución: 2 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: ZCode (GLM-5.3, contexto 1M)**

La orquestación multi-agente es un problema de contexto largo: hay que sostener el estado de muchos pasos. GLM-5.3 con 1M de contexto es el más barato para eso (Lite ~12,60 USD/mes) y sus modelos 5.1 y 5.3 están diseñados para tareas autónomas de hasta 8 horas. Antigravity aporta la orquestación multi-agente real en local, gratis.

- Segunda opción: **Claude Code**
- Alternativas: **Google Antigravity (multi-agente)** · **Codex CLI**

**Primera acción:** Documentar el protocolo en un README de 20 líneas y cubrir el núcleo con tests. Un orquestador sin tests es código que no se puede cambiar.

**Evitar:** Solo autocompletado: no van a seguir un objetivo de 50 pasos.

---

### 18. belent-cad — 70/100

[https://github.com/belentani7/belent-cad](https://github.com/belentani7/belent-cad) · **WEB_APP_TS** · TypeScript · 449 KB · 8 commits · 65 ficheros · creado 2026-09-16 · último push hace 2 días

> Open-source architectural CAD for architects: paper-sketch digitization to 3D, photorealistic renders and standards bank (PT/ES/EN). React 19 + Vite + Three.js.

**Los 20 aspectos** — suma 73/100, penalizaciones -3, nota final 70/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **5/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 561 palabras · 8 encabezados · 3 bloques de código · 2 enlaces · 0 imágenes · 2 badges · idioma es · comandos de ejecución: 5 · sección de uso: no

**Penalizaciones**

- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 19. lingua-aberta-empresa — 68/100

[https://github.com/belentani7/lingua-aberta-empresa](https://github.com/belentani7/lingua-aberta-empresa) · **WEB_APP_TS** · HTML · 35 KB · 11 commits · 73 ficheros · creado 2026-09-10 · último push hace 12 días

> lingua-aberta como empresa: producto web full-stack con precios, pagos Stripe, área de cliente y plan de negocio de 90 días.

**Los 20 aspectos** — suma 69/100, penalizaciones -1, nota final 68/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **1/5** | Higiene de secretos | **5/5** |
| Licencia | **2/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **2/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **1/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 47 palabras · 3 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 2 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 20. pvc-u-frontend — 68/100

[https://github.com/belentani7/pvc-u-frontend](https://github.com/belentani7/pvc-u-frontend) · **WEB_APP_TS** · TypeScript · 63 KB · 13 commits · 35 ficheros · creado 2026-09-03 · último push hace 2 días

> PVC-U Dashboard — Liquid Glass/Neon Aesthetic con React 19 + Vite 7

**Los 20 aspectos** — suma 69/100, penalizaciones -1, nota final 68/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **3/5** | Documentación | **1/5** |
| README (contenido real) | **1/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **1/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 53 palabras · 1 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 1 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 21. comfyui-json-compiler — 68/100

[https://github.com/belentani7/comfyui-json-compiler](https://github.com/belentani7/comfyui-json-compiler) · **PY_TOOL** · Python · 55 KB · 12 commits · 42 ficheros · creado 2026-08-16 · último push hace 2 días

> Translate natural language creative briefs into valid ComfyUI JSON workflows using LLMs.

**Los 20 aspectos** — suma 69/100, penalizaciones -1, nota final 68/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 568 palabras · 22 encabezados · 10 bloques de código · 1 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 1 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / ZCode (BYOK)**

Son scripts en Python: el valor está en el fichero, no en el frontend. Lo que hace falta es un agente que lea el repo, ejecute pytest y corrija. OpenCode con GLM de Z.ai (plan Lite ~12,60-18 USD/mes) o Gemini CLI con cuota gratuita dan capacidad de frontera a coste cero o muy bajo; Claude Code es más fiable en refactors largos.

- Segunda opción: **Claude Code**
- Alternativas: **Codex CLI** · **Gemini CLI (gratis)**

**Primera acción:** Ejecutar el CLI tal cual está, documentar entrada y salida reales en el README y añadir un pyproject.toml con dependencias declaradas. Sin tests no se puede refactorizar después.

**Evitar:** Replit o Bolt: su backend es Node; meterían este Python en un contenedor que no necesita.

---

### 22. agent-skills — 67/100

[https://github.com/belentani7/agent-skills](https://github.com/belentani7/agent-skills) · **SKILL_PACK** · Python · 8000 KB · 9 commits · 3584 ficheros · creado 2026-09-15 · último push hace 2 días

> Colección de 311 skills para agentes CLI (Claude Code, OpenCode, Codex, Cline, Qwen, Gemini, ZCode). PT>ES>EN>CA.

**Los 20 aspectos** — suma 68/100, penalizaciones -1, nota final 67/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **2/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 7927 palabras · 7 encabezados · 3 bloques de código · 1 enlaces · 0 imágenes · 1 badges · idioma en · comandos de ejecución: 10 · sección de uso: sí

**Buena práctica detectada (afirmación concreta y comprobable):**
- `311 skills` → cuantifica el contenido con un numero verificable

**Penalizaciones**

- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 23. skills-registry — 67/100

[https://github.com/belentani7/skills-registry](https://github.com/belentani7/skills-registry) · **SKILL_PACK** · TypeScript · 100 KB · 17 commits · 18 ficheros · creado 2026-09-02 · último push hace 2 días

> Global CLI agent skill distribution system — discover, install, manage skills for Qwen Code, Claude Code, Cline, OpenCode

**Los 20 aspectos** — suma 69/100, penalizaciones -2, nota final 67/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **1/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 392 palabras · 12 encabezados · 5 bloques de código · 1 enlaces · 0 imágenes · 1 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 24. omniagent — 67/100

[https://github.com/belentani7/omniagent](https://github.com/belentani7/omniagent) · **AGENT_INFRA** · Python · 56 KB · 19 commits · 43 ficheros · creado 2026-08-16 · último push hace 24 días

> One CLI to route AI tasks to the best model.

**Los 20 aspectos** — suma 68/100, penalizaciones -1, nota final 67/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 576 palabras · 24 encabezados · 5 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 4 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: ZCode (GLM-5.3, contexto 1M)**

La orquestación multi-agente es un problema de contexto largo: hay que sostener el estado de muchos pasos. GLM-5.3 con 1M de contexto es el más barato para eso (Lite ~12,60 USD/mes) y sus modelos 5.1 y 5.3 están diseñados para tareas autónomas de hasta 8 horas. Antigravity aporta la orquestación multi-agente real en local, gratis.

- Segunda opción: **Claude Code**
- Alternativas: **Google Antigravity (multi-agente)** · **Codex CLI**

**Primera acción:** Documentar el protocolo en un README de 20 líneas y cubrir el núcleo con tests. Un orquestador sin tests es código que no se puede cambiar.

**Evitar:** Solo autocompletado: no van a seguir un objetivo de 50 pasos.

---

### 25. llm-vfx-orchestrator — 67/100

[https://github.com/belentani7/llm-vfx-orchestrator](https://github.com/belentani7/llm-vfx-orchestrator) · **SITIO_ESTATICO** · HTML · 41 KB · 9 commits · 39 ficheros · creado 2026-08-16 · último push hace 24 días

> Autonomous VFX pipeline orchestration using LLMs connected to ComfyUI APIs.

**Los 20 aspectos** — suma 68/100, penalizaciones -1, nota final 67/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 313 palabras · 13 encabezados · 6 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 3 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 26. gpu-cost-optimizer — 67/100

[https://github.com/belentani7/gpu-cost-optimizer](https://github.com/belentani7/gpu-cost-optimizer) · **PY_DATA** · Python · 43 KB · 13 commits · 41 ficheros · creado 2026-08-16 · último push hace 24 días

> Optimize GPU compute costs in diffusion pipelines by up to 70%.

**Los 20 aspectos** — suma 68/100, penalizaciones -1, nota final 67/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 278 palabras · 10 encabezados · 4 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Los pipelines de ML y GPU necesitan razonamiento sobre la lógica, no generación de interfaz. Claude Code y Codex sostienen una tarea larga sin perder el objetivo. Gemini CLI tiene cuota gratuita y es el candidato más obvio para no pagar nada. Replit Agent solo aporta si además quieres el dataset alojado y ejecutándose.

- Segunda opción: **Gemini CLI (gratis)**
- Alternativas: **Codex CLI** · **Replit Agent**

**Primera acción:** Fijar el dataset de entrada y la métrica de éxito antes de tocar código, y pinear requirements.txt. Sin eso el agente optimiza a ciegas.

**Evitar:** Plataformas de vibe coding web: aquí no hay nada que desplegar, hay una máquina que ejecutar.

---

### 27. system-one-unified — 66/100

[https://github.com/belentani7/system-one-unified](https://github.com/belentani7/system-one-unified) · **WEB_APP_TS** · TypeScript · 469 KB · 2 commits · 161 ficheros · creado 2026-09-24 · último push hace 2 días

> System One — motor de decisiones tipado, determinista y offline (POST /v1/systemone)

**Los 20 aspectos** — suma 70/100, penalizaciones -4, nota final 66/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **2/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **1/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **3/5** |

**README leído:** 253 palabras · 7 encabezados · 3 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 8 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 4 repos comparten el token 'unified'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 4 repos comparten el token 'unified' → 3/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 28. belentani-github-catalogo-minimalista — 66/100

[https://github.com/belentani7/belentani-github-catalogo-minimalista](https://github.com/belentani7/belentani-github-catalogo-minimalista) · **WEB_APP_TS** · TypeScript · 177 KB · 11 commits · 31 ficheros · creado 2026-09-16 · último push hace 2 días

> Catálogo web minimalista de los repositorios públicos de belentani7 — React + Vite + TypeScript con datos vivos de la GitHub API.

**Los 20 aspectos** — suma 69/100, penalizaciones -3, nota final 66/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 100 palabras · 5 encabezados · 1 bloques de código · 1 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 3 · sección de uso: sí

**Penalizaciones**

- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 29. belentani-judas-web — 66/100

[https://github.com/belentani7/belentani-judas-web](https://github.com/belentani7/belentani-judas-web) · **WEB_APP_TS** · TypeScript · 70 KB · 16 commits · 57 ficheros · creado 2026-09-07 · último push hace 2 días

> Judas Experience Creative OS - web (Vite) + SEO

**Los 20 aspectos** — suma 72/100, penalizaciones -6, nota final 66/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **1/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 128 palabras · 3 encabezados · 1 bloques de código · 6 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 7 repos comparten el token 'judas'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 7 repos comparten el token 'judas' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 30. aprende-brasil — 66/100

[https://github.com/belentani7/aprende-brasil](https://github.com/belentani7/aprende-brasil) · **DOCS_PLATFORM** · TypeScript · 1635 KB · 27 commits · 164 ficheros · creado 2026-09-03 · último push hace 2 días

> Plataforma educativa brasileña interactiva con tutor IA, trilhas y voz preparada para OpenVoice

**Los 20 aspectos** — suma 69/100, penalizaciones -3, nota final 66/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 1049 palabras · 16 encabezados · 4 bloques de código · 1 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 20 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Contenido más estructura de curso. El cuello de botella real no es la calidad del texto: es la duplicación. Hay al menos seis repos de plataforma educativa compitiendo por el mismo título. El agente sirve para consolidar, no para añadir una séptima copia.

- Segunda opción: **Cursor**
- Alternativas: **Google AI Studio (si pasa a ser app)** · **OpenCode**

**Primera acción:** Elegir un único repo canónico para el contenido educativo, migrar lo bueno y convertir el resto en archivados con enlace al canónico.

**Evitar:** Empezar otro repo de plataforma educativa: ya hay seis.

---

### 31. proofmesh — 66/100

[https://github.com/belentani7/proofmesh](https://github.com/belentani7/proofmesh) · **AGENT_INFRA** · TypeScript · 254 KB · 11 commits · 167 ficheros · creado 2026-08-18 · último push hace 24 días

> Evidence-first change intelligence with strict 6-criteria, 3-node, 3-level gates

**Los 20 aspectos** — suma 71/100, penalizaciones -5, nota final 66/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 309 palabras · 5 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 5 · sección de uso: no

**Afirmaciones no verificables detectadas:**
- `10/10` → puntua su propio trabajo con una nota sobre 10

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: '10/10' (puntua su propio trabajo con una nota sobre 10). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: ZCode (GLM-5.3, contexto 1M)**

La orquestación multi-agente es un problema de contexto largo: hay que sostener el estado de muchos pasos. GLM-5.3 con 1M de contexto es el más barato para eso (Lite ~12,60 USD/mes) y sus modelos 5.1 y 5.3 están diseñados para tareas autónomas de hasta 8 horas. Antigravity aporta la orquestación multi-agente real en local, gratis.

- Segunda opción: **Claude Code**
- Alternativas: **Google Antigravity (multi-agente)** · **Codex CLI**

**Primera acción:** Documentar el protocolo en un README de 20 líneas y cubrir el núcleo con tests. Un orquestador sin tests es código que no se puede cambiar.

**Evitar:** Solo autocompletado: no van a seguir un objetivo de 50 pasos.

---

### 32. belentani-omega-template — 66/100

[https://github.com/belentani7/belentani-omega-template](https://github.com/belentani7/belentani-omega-template) · **WEB_APP_TS** · HTML · 17760 KB · 23 commits · 359 ficheros · creado 2026-08-16 · último push hace 2 días

> BELENTANI OMEGA: Plantilla de experiencia web inmersiva y canon conceptual.

**Los 20 aspectos** — suma 70/100, penalizaciones -4, nota final 66/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 331 palabras · 5 encabezados · 0 bloques de código · 1 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 1 · sección de uso: sí

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 9 repos comparten el token 'omega'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 9 repos comparten el token 'omega' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 33. meta-skill — 66/100

[https://github.com/belentani7/meta-skill](https://github.com/belentani7/meta-skill) · **SKILL_PACK** · HTML · 44 KB · 17 commits · 32 ficheros · creado 2026-07-20 · último push hace 24 días

> Zero-token skill router for Claude Code and Qwen Code. Routes agent requests to the right skill without burning LLM tokens.

**Los 20 aspectos** — suma 66/100, penalizaciones 0, nota final 66/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **5/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **1/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 372 palabras · 8 encabezados · 4 bloques de código · 1 enlaces · 0 imágenes · 3 badges · idioma es · comandos de ejecución: 1 · sección de uso: sí

**Sin penalizaciones.**

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 34. Belentanislide — 65/100

[https://github.com/belentani7/Belentanislide](https://github.com/belentani7/Belentanislide) · **WEB_APP_TS** · HTML · 569 KB · 10 commits · 55 ficheros · creado 2026-09-11 · último push hace 2 días

> App AI Studio (Gemini) con pack abierto de datos de modelos LLM (OpenRouter) y scripts de análisis — sin claves API.

**Los 20 aspectos** — suma 68/100, penalizaciones -3, nota final 65/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **2/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 114 palabras · 4 encabezados · 1 bloques de código · 5 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 35. duck-hub — 65/100

[https://github.com/belentani7/duck-hub](https://github.com/belentani7/duck-hub) · **WEB_APP_TS** · TypeScript · 452 KB · 5 commits · 251 ficheros · creado 2026-08-30 · último push hace 2 días

> DUCK hub — Astro-based portal connecting all DUCK ecosystem apps and tools

**Los 20 aspectos** — suma 68/100, penalizaciones -3, nota final 65/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **4/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 159 palabras · 5 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 5 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 36. qbp-core — 65/100

[https://github.com/belentani7/qbp-core](https://github.com/belentani7/qbp-core) · **PY_TOOL** · Python · 46 KB · 9 commits · 35 ficheros · creado 2026-08-16 · último push hace 24 días

> Core SDK for the Quadrachy Binding Protocol - structured format for defining and validating.

**Los 20 aspectos** — suma 66/100, penalizaciones -1, nota final 65/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 530 palabras · 20 encabezados · 4 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 4 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / ZCode (BYOK)**

Son scripts en Python: el valor está en el fichero, no en el frontend. Lo que hace falta es un agente que lea el repo, ejecute pytest y corrija. OpenCode con GLM de Z.ai (plan Lite ~12,60-18 USD/mes) o Gemini CLI con cuota gratuita dan capacidad de frontera a coste cero o muy bajo; Claude Code es más fiable en refactors largos.

- Segunda opción: **Claude Code**
- Alternativas: **Codex CLI** · **Gemini CLI (gratis)**

**Primera acción:** Ejecutar el CLI tal cual está, documentar entrada y salida reales en el README y añadir un pyproject.toml con dependencias declaradas. Sin tests no se puede refactorizar después.

**Evitar:** Replit o Bolt: su backend es Node; meterían este Python en un contenedor que no necesita.

---

### 37. tender-words-connect — 65/100

[https://github.com/belentani7/tender-words-connect](https://github.com/belentani7/tender-words-connect) · **WEB_APP_TS** · TypeScript · 659 KB · 112 commits · 154 ficheros · creado 2026-08-03 · último push hace 0 días

> Mapa de comprension y herramientas sobre TLP, vinculos y gestion emocional.

**Los 20 aspectos** — suma 68/100, penalizaciones -3, nota final 65/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **2/5** |
| README (contenido real) | **1/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **5/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 510 palabras · 1 encabezados · 0 bloques de código · 1 enlaces · 0 imágenes · 1 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 38. secure-t — 64/100

[https://github.com/belentani7/secure-t](https://github.com/belentani7/secure-t) · **WEB_APP_TS** · HTML · 70465 KB · 5 commits · 687 ficheros · creado 2026-09-25 · último push hace 2 días

> Universidad digital de ciberseguridad e IA - cursos, campus, auditoria, modelos locales

**Los 20 aspectos** — suma 69/100, penalizaciones -5, nota final 64/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **0/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **0/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **4/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 78 palabras · 3 encabezados · 0 bloques de código · 1 enlaces · 0 imágenes · 1 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-CI` (Tiene manifest de build y ningun workflow: nada verifica que siga compilando.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 39. manos-abiertas-2026 — 64/100

[https://github.com/belentani7/manos-abiertas-2026](https://github.com/belentani7/manos-abiertas-2026) · **WEB_APP_TS** · HTML · 52 KB · 10 commits · 28 ficheros · creado 2026-09-08 · último push hace 12 días

> Manos Abiertas 2026 — Instituto Universal William: currículum abierto, generador de CV y datos abiertos de acogida en España.

**Los 20 aspectos** — suma 65/100, penalizaciones -1, nota final 64/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **2/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **4/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 398 palabras · 11 encabezados · 4 bloques de código · 1 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 4 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 40. win11-workspace — 64/100

[https://github.com/belentani7/win11-workspace](https://github.com/belentani7/win11-workspace) · **WEB_APP_TS** · TypeScript · 280 KB · 6 commits · 113 ficheros · creado 2026-09-02 · último push hace 8 días

> Windows 11 workspace - TypeScript desktop-style web environment.

**Los 20 aspectos** — suma 65/100, penalizaciones -1, nota final 64/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **2/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 594 palabras · 18 encabezados · 5 bloques de código · 0 enlaces · 0 imágenes · 4 badges · idioma en · comandos de ejecución: 9 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 41. belentani-video-forge — 64/100

[https://github.com/belentani7/belentani-video-forge](https://github.com/belentani7/belentani-video-forge) · **PY_DATA** · Python · 5617 KB · 11 commits · 37 ficheros · creado 2026-08-28 · último push hace 2 días

> Pipeline de videos cortos automáticos - Belentani ecosystem

**Los 20 aspectos** — suma 65/100, penalizaciones -1, nota final 64/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 294 palabras · 9 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 1 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Los pipelines de ML y GPU necesitan razonamiento sobre la lógica, no generación de interfaz. Claude Code y Codex sostienen una tarea larga sin perder el objetivo. Gemini CLI tiene cuota gratuita y es el candidato más obvio para no pagar nada. Replit Agent solo aporta si además quieres el dataset alojado y ejecutándose.

- Segunda opción: **Gemini CLI (gratis)**
- Alternativas: **Codex CLI** · **Replit Agent**

**Primera acción:** Fijar el dataset de entrada y la métrica de éxito antes de tocar código, y pinear requirements.txt. Sin eso el agente optimiza a ciegas.

**Evitar:** Plataformas de vibe coding web: aquí no hay nada que desplegar, hay una máquina que ejecutar.

---

### 42. evidence-ledger — 64/100

[https://github.com/belentani7/evidence-ledger](https://github.com/belentani7/evidence-ledger) · **WEB_APP_TS** · HTML · 139 KB · 9 commits · 42 ficheros · creado 2026-08-18 · último push hace 24 días

> Local-first evidence receipts for AI and Trust & Safety decisions

**Los 20 aspectos** — suma 65/100, penalizaciones -1, nota final 64/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 318 palabras · 7 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 5 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 43. belentani-artista-unified — 63/100

[https://github.com/belentani7/belentani-artista-unified](https://github.com/belentani7/belentani-artista-unified) · **WEB_APP_TS** · HTML · 63961 KB · 17 commits · 1167 ficheros · creado 2026-09-12 · último push hace 2 días

> belentani-the-experience

**Los 20 aspectos** — suma 69/100, penalizaciones -6, nota final 63/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **2/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **0/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **5/5** | Unicidad en el ecosistema | **3/5** |

**README leído:** 116 palabras · 3 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 4 repos comparten el token 'unified'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 4 repos comparten el token 'unified' → 3/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 44. pvc-u-core — 63/100

[https://github.com/belentani7/pvc-u-core](https://github.com/belentani7/pvc-u-core) · **PY_TOOL** · Python · 325 KB · 8 commits · 29 ficheros · creado 2026-09-03 · último push hace 2 días

> Protocolo de Validación Continua Universal — Kernel de gobernanza para Empresas de IA Autónomas Enterprise (HIPAA, PCI-DSS, GDPR)

**Los 20 aspectos** — suma 65/100, penalizaciones -2, nota final 63/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **2/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **2/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **4/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **1/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 636 palabras · 25 encabezados · 6 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 4 · sección de uso: sí

**Penalizaciones**

- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / ZCode (BYOK)**

Son scripts en Python: el valor está en el fichero, no en el frontend. Lo que hace falta es un agente que lea el repo, ejecute pytest y corrija. OpenCode con GLM de Z.ai (plan Lite ~12,60-18 USD/mes) o Gemini CLI con cuota gratuita dan capacidad de frontera a coste cero o muy bajo; Claude Code es más fiable en refactors largos.

- Segunda opción: **Claude Code**
- Alternativas: **Codex CLI** · **Gemini CLI (gratis)**

**Primera acción:** Ejecutar el CLI tal cual está, documentar entrada y salida reales en el README y añadir un pyproject.toml con dependencias declaradas. Sin tests no se puede refactorizar después.

**Evitar:** Replit o Bolt: su backend es Node; meterían este Python en un contenedor que no necesita.

---

### 45. pbr-validator — 63/100

[https://github.com/belentani7/pbr-validator](https://github.com/belentani7/pbr-validator) · **PY_TOOL** · Python · 38 KB · 8 commits · 35 ficheros · creado 2026-08-16 · último push hace 24 días

> Validates PBR texture sets for correctness and compatibility with game engines.

**Los 20 aspectos** — suma 64/100, penalizaciones -1, nota final 63/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **2/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 233 palabras · 10 encabezados · 7 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 3 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / ZCode (BYOK)**

Son scripts en Python: el valor está en el fichero, no en el frontend. Lo que hace falta es un agente que lea el repo, ejecute pytest y corrija. OpenCode con GLM de Z.ai (plan Lite ~12,60-18 USD/mes) o Gemini CLI con cuota gratuita dan capacidad de frontera a coste cero o muy bajo; Claude Code es más fiable en refactors largos.

- Segunda opción: **Claude Code**
- Alternativas: **Codex CLI** · **Gemini CLI (gratis)**

**Primera acción:** Ejecutar el CLI tal cual está, documentar entrada y salida reales en el README y añadir un pyproject.toml con dependencias declaradas. Sin tests no se puede refactorizar después.

**Evitar:** Replit o Bolt: su backend es Node; meterían este Python en un contenedor que no necesita.

---

### 46. latent-consistency-bench — 63/100

[https://github.com/belentani7/latent-consistency-bench](https://github.com/belentani7/latent-consistency-bench) · **PY_DATA** · Python · 43 KB · 8 commits · 36 ficheros · creado 2026-08-16 · último push hace 24 días

> Benchmarking visual consistency in AI-generated content.

**Los 20 aspectos** — suma 64/100, penalizaciones -1, nota final 63/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 542 palabras · 22 encabezados · 5 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 3 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Los pipelines de ML y GPU necesitan razonamiento sobre la lógica, no generación de interfaz. Claude Code y Codex sostienen una tarea larga sin perder el objetivo. Gemini CLI tiene cuota gratuita y es el candidato más obvio para no pagar nada. Replit Agent solo aporta si además quieres el dataset alojado y ejecutándose.

- Segunda opción: **Gemini CLI (gratis)**
- Alternativas: **Codex CLI** · **Replit Agent**

**Primera acción:** Fijar el dataset de entrada y la métrica de éxito antes de tocar código, y pinear requirements.txt. Sin eso el agente optimiza a ciegas.

**Evitar:** Plataformas de vibe coding web: aquí no hay nada que desplegar, hay una máquina que ejecutar.

---

### 47. WILLIAMSCHOOL — 62/100

[https://github.com/belentani7/WILLIAMSCHOOL](https://github.com/belentani7/WILLIAMSCHOOL) · **DOCS_PLATFORM** · TypeScript · 2144 KB · 15 commits · 62 ficheros · creado 2026-09-08 · último push hace 0 días

> Escola digital comunitária — currículo Nepal adaptado, design institucional, acceso abierto

**Los 20 aspectos** — suma 65/100, penalizaciones -3, nota final 62/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **2/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **2/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 33 palabras · 3 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma ? · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Contenido más estructura de curso. El cuello de botella real no es la calidad del texto: es la duplicación. Hay al menos seis repos de plataforma educativa compitiendo por el mismo título. El agente sirve para consolidar, no para añadir una séptima copia.

- Segunda opción: **Cursor**
- Alternativas: **Google AI Studio (si pasa a ser app)** · **OpenCode**

**Primera acción:** Elegir un único repo canónico para el contenido educativo, migrar lo bueno y convertir el resto en archivados con enlace al canónico.

**Evitar:** Empezar otro repo de plataforma educativa: ya hay seis.

---

### 48. openclaw-workspace — 62/100

[https://github.com/belentani7/openclaw-workspace](https://github.com/belentani7/openclaw-workspace) · **WEB_APP_TS** · HTML · 88835 KB · 7 commits · 412 ficheros · creado 2026-08-28 · último push hace 2 días

> OpenClaw workspace config

**Los 20 aspectos** — suma 67/100, penalizaciones -5, nota final 62/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **2/5** | CI/CD | **0/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **3/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 202 palabras · 8 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-CI` (Tiene manifest de build y ningun workflow: nada verifica que siga compilando.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 49. duck-full-studio-pro — 62/100

[https://github.com/belentani7/duck-full-studio-pro](https://github.com/belentani7/duck-full-studio-pro) · **WEB_APP_TS** · HTML · 1332 KB · 37 commits · 249 ficheros · creado 2026-08-18 · último push hace 2 días

> DUCK Full Studio Pro - FL Studio Ecosystem & Vault (Audited 10/10)

**Los 20 aspectos** — suma 67/100, penalizaciones -5, nota final 62/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **2/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 247 palabras · 6 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 3 · sección de uso: no

**Afirmaciones no verificables detectadas:**
- `10/10` → puntua su propio trabajo con una nota sobre 10

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: '10/10' (puntua su propio trabajo con una nota sobre 10). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 50. belentani_Omega — 62/100

[https://github.com/belentani7/belentani_Omega](https://github.com/belentani7/belentani_Omega) · **WEB_APP_TS** · HTML · 90001 KB · 37 commits · 797 ficheros · creado 2026-07-10 · último push hace 0 días

> Belentani Omega — artist ecosystem connecting music, code, and creative technology

**Los 20 aspectos** — suma 66/100, penalizaciones -4, nota final 62/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **3/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 1187 palabras · 20 encabezados · 2 bloques de código · 13 enlaces · 0 imágenes · 5 badges · idioma en · comandos de ejecución: 2 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 9 repos comparten el token 'omega'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 9 repos comparten el token 'omega' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 51. arte-que-veste — 61/100

[https://github.com/belentani7/arte-que-veste](https://github.com/belentani7/arte-que-veste) · **WEB_APP_TS** · HTML · 856 KB · 18 commits · 63 ficheros · creado 2026-08-16 · último push hace 2 días

> Arte Que Veste - moda autoral y arte vestible; catalogo y tienda creativa.

**Los 20 aspectos** — suma 64/100, penalizaciones -3, nota final 61/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 33 palabras · 3 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 52. belentani-judas-era-omega — 60/100

[https://github.com/belentani7/belentani-judas-era-omega](https://github.com/belentani7/belentani-judas-era-omega) · **WEB_APP_TS** · TypeScript · 10992 KB · 20 commits · 186 ficheros · creado 2026-08-18 · último push hace 2 días

> BELENTANI // JUDAS ERA - Omega Core Experience 10/10

**Los 20 aspectos** — suma 68/100, penalizaciones -8, nota final 60/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 70 palabras · 4 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 7 · sección de uso: no

**Afirmaciones no verificables detectadas:**
- `10/10` → puntua su propio trabajo con una nota sobre 10

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: '10/10' (puntua su propio trabajo con una nota sobre 10). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 9 repos comparten el token 'omega'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 9 repos comparten el token 'omega' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 53. temporal-artifact-detector — 60/100

[https://github.com/belentani7/temporal-artifact-detector](https://github.com/belentani7/temporal-artifact-detector) · **PY_DATA** · Python · 43 KB · 8 commits · 35 ficheros · creado 2026-08-16 · último push hace 24 días

> Python tool for detecting flickering and temporal artifacts in AI-generated videos.

**Los 20 aspectos** — suma 61/100, penalizaciones -1, nota final 60/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **1/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 370 palabras · 28 encabezados · 8 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 4 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Los pipelines de ML y GPU necesitan razonamiento sobre la lógica, no generación de interfaz. Claude Code y Codex sostienen una tarea larga sin perder el objetivo. Gemini CLI tiene cuota gratuita y es el candidato más obvio para no pagar nada. Replit Agent solo aporta si además quieres el dataset alojado y ejecutándose.

- Segunda opción: **Gemini CLI (gratis)**
- Alternativas: **Codex CLI** · **Replit Agent**

**Primera acción:** Fijar el dataset de entrada y la métrica de éxito antes de tocar código, y pinear requirements.txt. Sin eso el agente optimiza a ciegas.

**Evitar:** Plataformas de vibe coding web: aquí no hay nada que desplegar, hay una máquina que ejecutar.

---

### 54. Duck-Omega — 60/100

[https://github.com/belentani7/Duck-Omega](https://github.com/belentani7/Duck-Omega) · **WEB_APP_TS** · TypeScript · 523 KB · 43 commits · 254 ficheros · creado 2026-08-12 · último push hace 2 días

> DUCK Omega - ecosistema artistico y productivo del proyecto Duck/Zion (Belentani).

**Los 20 aspectos** — suma 66/100, penalizaciones -6, nota final 60/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **3/5** |
| Tests | **4/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 43 palabras · 3 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 9 repos comparten el token 'omega'. Ninguno es canonico.) — -3
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 9 repos comparten el token 'omega' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 55. belentani-es-neon — 59/100

[https://github.com/belentani7/belentani-es-neon](https://github.com/belentani7/belentani-es-neon) · **WEB_APP_TS** · JavaScript · 6107 KB · 5 commits · 68 ficheros · creado 2026-09-24 · último push hace 2 días

> Belentani Judas Era — portfolio visual estatico (dark pop, R&B, neon)

**Los 20 aspectos** — suma 60/100, penalizaciones -1, nota final 59/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 150 palabras · 7 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 5 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 56. fashion-stylist-ai — 59/100

[https://github.com/belentani7/fashion-stylist-ai](https://github.com/belentani7/fashion-stylist-ai) · **WEB_APP_TS** · HTML · 318 KB · 3 commits · 10 ficheros · creado 2026-08-26 · último push hace 24 días

> AI-powered fashion stylist — visual recommendation engine using computer vision and style classification

**Los 20 aspectos** — suma 62/100, penalizaciones -3, nota final 59/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **0/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **0/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **4/5** | Historial de commits | **1/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 1498 palabras · 46 encabezados · 8 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 8 · sección de uso: sí

**Penalizaciones**

- `SIN-CI` (Tiene manifest de build y ningun workflow: nada verifica que siga compilando.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 57. duck-lab — 59/100

[https://github.com/belentani7/duck-lab](https://github.com/belentani7/duck-lab) · **WEB_APP_TS** · TypeScript · 332 KB · 12 commits · 122 ficheros · creado 2026-08-22 · último push hace 2 días

> DUCK Lab - laboratorio de prototipos del universo DUCK/Zion.

**Los 20 aspectos** — suma 64/100, penalizaciones -5, nota final 59/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **0/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **0/5** | Config de despliegue | **0/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 378 palabras · 8 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 7 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-CI` (Tiene manifest de build y ningun workflow: nada verifica que siga compilando.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 58. DUCK-ZION-PREMIUM — 59/100

[https://github.com/belentani7/DUCK-ZION-PREMIUM](https://github.com/belentani7/DUCK-ZION-PREMIUM) · **WEB_APP_TS** · HTML · 208012 KB · 6 commits · 962 ficheros · creado 2026-08-16 · último push hace 2 días

> DUCK/BELENTANI Canal Zion — Studio OS, Ecosystem y Toolkit de producción musical, afinación y mastering.

**Los 20 aspectos** — suma 62/100, penalizaciones -3, nota final 59/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **2/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **3/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 726 palabras · 11 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 10 · sección de uso: no

**Penalizaciones**

- `PESADO` (203 MB de assets versionados: clonar es lento y el despliegue tarda.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 59. entrenador-jorge-bcn — 59/100

[https://github.com/belentani7/entrenador-jorge-bcn](https://github.com/belentani7/entrenador-jorge-bcn) · **WEB_APP_TS** · HTML · 1224 KB · 24 commits · 178 ficheros · creado 2026-08-15 · último push hace 24 días

> Empresa 100 generada con IA por Belentani

**Los 20 aspectos** — suma 62/100, penalizaciones -3, nota final 59/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **3/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 363 palabras · 8 encabezados · 3 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 6 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 60. Myopenhands — 58/100

[https://github.com/belentani7/Myopenhands](https://github.com/belentani7/Myopenhands) · **WEB_APP_TS** · TypeScript · 275 KB · 7 commits · 89 ficheros · creado 2026-09-07 · último push hace 8 días

> Myopenhands

**Los 20 aspectos** — suma 61/100, penalizaciones -3, nota final 58/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **2/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **2/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 33 palabras · 3 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma ? · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 61. agentbox — 57/100

[https://github.com/belentani7/agentbox](https://github.com/belentani7/agentbox) · **GO_CLI** · Go · 42 KB · 8 commits · 32 ficheros · creado 2026-09-01 · último push hace 2 días

> Disposable cloud sandboxes for AI agents. Spin up isolated VMs for Claude, Aider, Codex, Qwen. $4/month, Terraform-powered.

**Los 20 aspectos** — suma 59/100, penalizaciones -2, nota final 57/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 879 palabras · 23 encabezados · 9 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 1 · sección de uso: sí

**Penalizaciones**

- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Go tiene tipado fuerte y errores de compilación explícitos: un agente que compila en bucle resuelve solo casi todo. Cualquier agente local sirve; la diferencia está en quién entienda mejor el error de compilación y sepa no «arreglar» lo que no está roto.

- Segunda opción: **Codex CLI**
- Alternativas: **ZCode** · **Gemini CLI**

**Primera acción:** Añadir `go test ./...` a CI. Es un comando y convierte el repo en algo que un agente puede refactorizar sin miedo.

**Evitar:** Plataformas de browser: no ejecutan Go.

---

### 62. duck-music-lab — 57/100

[https://github.com/belentani7/duck-music-lab](https://github.com/belentani7/duck-music-lab) · **WEB_APP_TS** · HTML · 64 KB · 11 commits · 26 ficheros · creado 2026-08-26 · último push hace 2 días

> DUCK Music Lab — interactive music production playground, beat sequencer and audio experimentation tool

**Los 20 aspectos** — suma 62/100, penalizaciones -5, nota final 57/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **4/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 312 palabras · 11 encabezados · 3 bloques de código · 1 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 3 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 63. duck-belentani-os-audited-2026-08-23 — 57/100

[https://github.com/belentani7/duck-belentani-os-audited-2026-08-23](https://github.com/belentani7/duck-belentani-os-audited-2026-08-23) · **WEB_APP_TS** · TypeScript · 393 KB · 19 commits · 226 ficheros · creado 2026-08-22 · último push hace 2 días

> DUCK Belentani OS - snapshot auditado 2026-08-23 del sistema operativo creativo.

**Los 20 aspectos** — suma 62/100, penalizaciones -5, nota final 57/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **4/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 52 palabras · 3 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Buena práctica detectada (afirmación concreta y comprobable):**
- `snapshot auditado 2026-08-23` → publica un estado medido y fechado

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 64. rh-fiscal-ultra-elite — 57/100

[https://github.com/belentani7/rh-fiscal-ultra-elite](https://github.com/belentani7/rh-fiscal-ultra-elite) · **SITIO_ESTATICO** · HTML · 49 KB · 9 commits · 19 ficheros · creado 2026-08-18 · último push hace 2 días

> Suite RH/fiscal con automatizacion de calculos e informes.

**Los 20 aspectos** — suma 58/100, penalizaciones -1, nota final 57/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **3/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 210 palabras · 4 encabezados · 3 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 1 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 65. NOIACORE — 57/100

[https://github.com/belentani7/NOIACORE](https://github.com/belentani7/NOIACORE) · **SITIO_ESTATICO** · HTML · 8414 KB · 9 commits · 66 ficheros · creado 2026-08-16 · último push hace 13 días

> Multi-agent intelligence system — concept, architecture, and orchestration framework for autonomous AI agents

**Los 20 aspectos** — suma 58/100, penalizaciones -1, nota final 57/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **1/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **2/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **2/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 2942 palabras · 18 encabezados · 4 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 2 · sección de uso: no

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 66. belentani-the-judas-experience — 56/100

[https://github.com/belentani7/belentani-the-judas-experience](https://github.com/belentani7/belentani-the-judas-experience) · **PY_TOOL** · Python · 63 KB · 10 commits · 82 ficheros · creado 2026-09-09 · último push hace 2 días

> Python SaaS GUI del ecosistema Belentani: portal cinematográfico, narrativa Judas Era y CMS Studio (FastAPI + Jinja2 + HTMX).

**Los 20 aspectos** — suma 62/100, penalizaciones -6, nota final 56/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **2/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **1/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 195 palabras · 6 encabezados · 2 bloques de código · 6 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 7 repos comparten el token 'judas'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 7 repos comparten el token 'judas' → 2/5

**Herramienta principal: OpenCode / ZCode (BYOK)**

Son scripts en Python: el valor está en el fichero, no en el frontend. Lo que hace falta es un agente que lea el repo, ejecute pytest y corrija. OpenCode con GLM de Z.ai (plan Lite ~12,60-18 USD/mes) o Gemini CLI con cuota gratuita dan capacidad de frontera a coste cero o muy bajo; Claude Code es más fiable en refactors largos.

- Segunda opción: **Claude Code**
- Alternativas: **Codex CLI** · **Gemini CLI (gratis)**

**Primera acción:** Ejecutar el CLI tal cual está, documentar entrada y salida reales en el README y añadir un pyproject.toml con dependencias declaradas. Sin tests no se puede refactorizar después.

**Evitar:** Replit o Bolt: su backend es Node; meterían este Python en un contenedor que no necesita.

---

### 67. belentani-judas-experience — 56/100

[https://github.com/belentani7/belentani-judas-experience](https://github.com/belentani7/belentani-judas-experience) · **WEB_APP_TS** · TypeScript · 1171 KB · 8 commits · 64 ficheros · creado 2026-08-29 · último push hace 2 días

> The Judas Experience - interactive TypeScript web project.

**Los 20 aspectos** — suma 62/100, penalizaciones -6, nota final 56/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 53 palabras · 4 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 4 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 7 repos comparten el token 'judas'. Ninguno es canonico.) — -3
- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 7 repos comparten el token 'judas' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 68. duck-apps — 56/100

[https://github.com/belentani7/duck-apps](https://github.com/belentani7/duck-apps) · **WEB_APP_TS** · HTML · 873 KB · 16 commits · 86 ficheros · creado 2026-08-18 · último push hace 2 días

> iDuck GUI + DUCK STATION (mobile) + DUCK FL STUDIO (DAW web) — apps ao vivo

**Los 20 aspectos** — suma 59/100, penalizaciones -3, nota final 56/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 294 palabras · 6 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 1 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 69. duck-zion-apex-public — 56/100

[https://github.com/belentani7/duck-zion-apex-public](https://github.com/belentani7/duck-zion-apex-public) · **WEB_APP_TS** · TypeScript · 543 KB · 15 commits · 171 ficheros · creado 2026-08-18 · último push hace 2 días

> DUCK ZION Apex — professional vocal production platform; audited snapshot, gate currently 57/60

**Los 20 aspectos** — suma 63/100, penalizaciones -7, nota final 56/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 275 palabras · 5 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 6 · sección de uso: no

**Afirmaciones no verificables detectadas:**
- `10/10` → puntua su propio trabajo con una nota sobre 10
- `7/10` → puntua su propio trabajo con una nota sobre 10

**Buena práctica detectada (afirmación concreta y comprobable):**
- `57/60` → puntua con un numero concreto y parcial (no 10/10)
- `snapshot, gate currently 57/60` → publica un estado medido y fechado

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: '10/10' (puntua su propio trabajo con una nota sobre 10); '7/10' (puntua su propio trabajo con una nota sobre 10). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 70. CARQUIDEC — 56/100

[https://github.com/belentani7/CARQUIDEC](https://github.com/belentani7/CARQUIDEC) · **WEB_APP_TS** · HTML · 517592 KB · 31 commits · 404 ficheros · creado 2026-08-02 · último push hace 2 días

> Parametric architecture studio — AI-driven bioclimatic design and energy optimization

**Los 20 aspectos** — suma 61/100, penalizaciones -5, nota final 56/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **2/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 46 palabras · 3 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `PESADO` (505 MB de assets versionados: clonar es lento y el despliegue tarda.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 71. belentani-omega-showcase — 55/100

[https://github.com/belentani7/belentani-omega-showcase](https://github.com/belentani7/belentani-omega-showcase) · **DUP_ARCHIVE** · HTML · 18654 KB · 8 commits · 482 ficheros · creado 2026-09-22 · último push hace 2 días

> Galeria navegable de todas las versiones del proyecto web BELENTANI OMEGA / JUDAS ERA - publicado en GitHub Pages

**Los 20 aspectos** — suma 59/100, penalizaciones -4, nota final 55/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **0/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **1/5** | Higiene de secretos | **5/5** |
| Licencia | **2/5** | Config de despliegue | **0/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **5/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 105 palabras · 4 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `GALERIA` (Coleccion de versiones, no un proyecto. No aporta nada nuevo al perfil.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** galeria de versiones → 2/5

**Herramienta principal: Claude Code (solo para consolidar)**

Un backup o una galería de versiones no se desarrolla: se decide su futuro. Un agente solo tiene sentido para extraer lo aprovechable y moverlo al repo canónico. Cuatro copias vivas de lo mismo es el problema, y no lo arregla ninguna herramienta: lo arregla una decisión.

- Segunda opción: **Ninguna: archivar**
- Alternativas: **Cursor** · **OpenCode**

**Primera acción:** Archivar con isArchived=true o borrar, dejando un único repo canónico. Solo esto ya sube la percepción de todo el perfil.

**Evitar:** Invertir horas de agente en un repo que debería estar archivado.

---

### 72. agentguard — 55/100

[https://github.com/belentani7/agentguard](https://github.com/belentani7/agentguard) · **AGENT_INFRA** · Python · 31 KB · 6 commits · 31 ficheros · creado 2026-09-01 · último push hace 2 días

> The firewall for your AI budget. Monitor spending, enforce limits, auto-pause agents, route overflow to cheaper models. Go daemon.

**Los 20 aspectos** — suma 59/100, penalizaciones -4, nota final 55/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **0/5** | Config de despliegue | **2/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **2/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 836 palabras · 40 encabezados · 10 bloques de código · 3 enlaces · 0 imágenes · 3 badges · idioma es · comandos de ejecución: 13 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: ZCode (GLM-5.3, contexto 1M)**

La orquestación multi-agente es un problema de contexto largo: hay que sostener el estado de muchos pasos. GLM-5.3 con 1M de contexto es el más barato para eso (Lite ~12,60 USD/mes) y sus modelos 5.1 y 5.3 están diseñados para tareas autónomas de hasta 8 horas. Antigravity aporta la orquestación multi-agente real en local, gratis.

- Segunda opción: **Claude Code**
- Alternativas: **Google Antigravity (multi-agente)** · **Codex CLI**

**Primera acción:** Documentar el protocolo en un README de 20 líneas y cubrir el núcleo con tests. Un orquestador sin tests es código que no se puede cambiar.

**Evitar:** Solo autocompletado: no van a seguir un objetivo de 50 pasos.

---

### 73. claude-skills-pack — 55/100

[https://github.com/belentani7/claude-skills-pack](https://github.com/belentani7/claude-skills-pack) · **SKILL_PACK** · HTML · 80 KB · 13 commits · 50 ficheros · creado 2026-08-16 · último push hace 2 días

> 20 production-ready skills for AI coding assistants.

**Los 20 aspectos** — suma 61/100, penalizaciones -6, nota final 55/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 369 palabras · 12 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 0 · sección de uso: sí

**Afirmaciones no verificables detectadas:**
- `production-ready` → afirma estar listo para produccion sin evidencia

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: 'production-ready' (afirma estar listo para produccion sin evidencia). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 74. Netlify — 55/100

[https://github.com/belentani7/Netlify](https://github.com/belentani7/Netlify) · **WEB_APP_TS** · JavaScript · 2877 KB · 279 commits · 93 ficheros · creado 2026-08-04 · último push hace 29 días

> Next.js 16 frontend laboratory with image tooling, verified lint, tests and deployment previews.

**Los 20 aspectos** — suma 62/100, penalizaciones -7, nota final 55/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **4/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **4/5** |
| Demo desplegada | **0/5** | Actividad reciente | **4/5** |
| Volumen de código | **5/5** | Historial de commits | **5/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **1/5** |
| Tests | **1/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 224 palabras · 4 encabezados · 3 bloques de código · 5 enlaces · 1 imágenes · 0 badges · idioma en · comandos de ejecución: 14 · sección de uso: no

**Penalizaciones**

- `ARCHIVADO` (GitHub lo marca como archivado: no recibe cambios y aparece como repo muerto en el perfil.) — -3
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 75. duck-docs — 54/100

[https://github.com/belentani7/duck-docs](https://github.com/belentani7/duck-docs) · **SKILL_PACK** · TypeScript · 6876 KB · 8 commits · 316 ficheros · creado 2026-08-30 · último push hace 2 días

> DUCK studio documentation — audit reports, prompt engineering, delivery specs

**Los 20 aspectos** — suma 58/100, penalizaciones -4, nota final 54/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **0/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 117 palabras · 3 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 76. belentani-omega-immersive-portal — 54/100

[https://github.com/belentani7/belentani-omega-immersive-portal](https://github.com/belentani7/belentani-omega-immersive-portal) · **WEB_APP_TS** · JavaScript · 8244 KB · 30 commits · 65 ficheros · creado 2026-08-28 · último push hace 2 días

> BELENTANI OMEGA — immersive 3D creative portal experience

**Los 20 aspectos** — suma 60/100, penalizaciones -6, nota final 54/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **1/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 36 palabras · 3 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 9 repos comparten el token 'omega'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 9 repos comparten el token 'omega' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 77. Oculus-Tv — 54/100

[https://github.com/belentani7/Oculus-Tv](https://github.com/belentani7/Oculus-Tv) · **DOCS_PLATFORM** · TypeScript · 1536 KB · 32 commits · 284 ficheros · creado 2026-08-06 · último push hace 29 días

> Repositório multilíngue de código aberto com livros e materiais audiovisuais educativos.

**Los 20 aspectos** — suma 63/100, penalizaciones -9, nota final 54/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **0/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **5/5** |
| Licencia | **0/5** | Config de despliegue | **3/5** |
| Demo desplegada | **0/5** | Actividad reciente | **4/5** |
| Volumen de código | **4/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **3/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 608 palabras · 12 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 11 · sección de uso: no

**Penalizaciones**

- `ARCHIVADO` (GitHub lo marca como archivado: no recibe cambios y aparece como repo muerto en el perfil.) — -3
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-CI` (Tiene manifest de build y ningun workflow: nada verifica que siga compilando.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Contenido más estructura de curso. El cuello de botella real no es la calidad del texto: es la duplicación. Hay al menos seis repos de plataforma educativa compitiendo por el mismo título. El agente sirve para consolidar, no para añadir una séptima copia.

- Segunda opción: **Cursor**
- Alternativas: **Google AI Studio (si pasa a ser app)** · **OpenCode**

**Primera acción:** Elegir un único repo canónico para el contenido educativo, migrar lo bueno y convertir el resto en archivados con enlace al canónico.

**Evitar:** Empezar otro repo de plataforma educativa: ya hay seis.

---

### 78. skillforge — 53/100

[https://github.com/belentani7/skillforge](https://github.com/belentani7/skillforge) · **SKILL_PACK** · Python · 45 KB · 7 commits · 38 ficheros · creado 2026-09-01 · último push hace 8 días

> Universal package manager for AI coding skills. Write once, install everywhere.

**Los 20 aspectos** — suma 54/100, penalizaciones -1, nota final 53/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **1/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **0/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 746 palabras · 16 encabezados · 7 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 1 · sección de uso: sí

**Penalizaciones**

- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 79. duck-apps-web — 53/100

[https://github.com/belentani7/duck-apps-web](https://github.com/belentani7/duck-apps-web) · **WEB_APP_TS** · HTML · 886 KB · 6 commits · 97 ficheros · creado 2026-08-30 · último push hace 2 días

> DUCK web applications — catalog, sequencer, station, FL Studio tools

**Los 20 aspectos** — suma 58/100, penalizaciones -5, nota final 53/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **5/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 237 palabras · 6 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 80. registro-proyectos-2026 — 53/100

[https://github.com/belentani7/registro-proyectos-2026](https://github.com/belentani7/registro-proyectos-2026) · **SITIO_ESTATICO** · HTML · 60 KB · 11 commits · 16 ficheros · creado 2026-08-18 · último push hace 2 días

> Registro maestro de proyectos Pedro Belentani 2026

**Los 20 aspectos** — suma 56/100, penalizaciones -3, nota final 53/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 27 palabras · 3 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 81. premium-effects-registry — 52/100

[https://github.com/belentani7/premium-effects-registry](https://github.com/belentani7/premium-effects-registry) · **SKILL_PACK** · Python · 10 KB · 6 commits · 10 ficheros · creado 2026-09-03 · último push hace 13 días

> Curated collection of 50+ GitHub repos for premium frontend visual effects — liquid logos, 3D/WebGL, GLSL shaders, GSAP, particles, cyberpunk UI

**Los 20 aspectos** — suma 55/100, penalizaciones -3, nota final 52/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **4/5** |
| Topics | **4/5** | Documentación | **1/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **0/5** | Actividad reciente | **4/5** |
| Volumen de código | **2/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **1/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 82 palabras · 11 encabezados · 4 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 82. belentani-monorepo — 52/100

[https://github.com/belentani7/belentani-monorepo](https://github.com/belentani7/belentani-monorepo) · **PLATFORM_JAVA** · Java · 157 KB · 10 commits · 26 ficheros · creado 2026-09-02 · último push hace 2 días

> Belentani monorepo: UX Academy + ManosAbiertas + Belentani platforms. TurboRepo, Next.js, TypeScript.

**Los 20 aspectos** — suma 56/100, penalizaciones -4, nota final 52/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 44 palabras · 3 encabezados · 2 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma ? · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Java con build server necesita un agente que ejecute el build. Con el volumen actual y sin tests, el repo está en estado de esqueleto: la prioridad es la estructura y un build que pase, no generar más código.

- Segunda opción: **Codex CLI**
- Alternativas: **ZCode** · **Google Antigravity**

**Primera acción:** Un pom.xml o build.gradle que compile en GitHub Actions, aunque el código sea mínimo. Sin build no hay CI posible.

**Evitar:** Plataformas de vibe coding: no compilan Java server-side.

---

### 83. nexus-os — 52/100

[https://github.com/belentani7/nexus-os](https://github.com/belentani7/nexus-os) · **WEB_APP_TS** · JavaScript · 776 KB · 7 commits · 125 ficheros · creado 2026-09-01 · último push hace 8 días

> Neon Glass Operating System. Browser-based OS shell with 38+ apps, cyberpunk aesthetics, zero dependencies.

**Los 20 aspectos** — suma 53/100, penalizaciones -1, nota final 52/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **0/5** |
| Topics | **4/5** | Documentación | **1/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **0/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **4/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 813 palabras · 26 encabezados · 3 bloques de código · 4 enlaces · 0 imágenes · 4 badges · idioma en · comandos de ejecución: 3 · sección de uso: sí

**Penalizaciones**

- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 84. ManosAbiertas-backup-v1 — 52/100

[https://github.com/belentani7/ManosAbiertas-backup-v1](https://github.com/belentani7/ManosAbiertas-backup-v1) · **DUP_ARCHIVE** · TypeScript · 12503 KB · 83 commits · 1657 ficheros · creado 2026-08-04 · último push hace 15 días

> Plataforma educativa multilingue con cursos gratuitos, CV guiado, asistentes offline y accesibilidad.

**Los 20 aspectos** — suma 68/100, penalizaciones -16, nota final 52/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **5/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **4/5** |
| Demo desplegada | **0/5** | Actividad reciente | **4/5** |
| Volumen de código | **5/5** | Historial de commits | **4/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **5/5** | Gestión de issues | **5/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **3/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **1/5** |

**README leído:** 786 palabras · 12 encabezados · 2 bloques de código · 2 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 11 · sección de uso: no

**Afirmaciones no verificables detectadas:**
- `definitiva` → autoevaluacion superlativa en la description

**Penalizaciones**

- `ARCHIVADO` (GitHub lo marca como archivado: no recibe cambios y aparece como repo muerto en el perfil.) — -3
- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: 'definitiva' (autoevaluacion superlativa en la description). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `DUPLICADO` (Es una copia. Publicar copia y original a la vez divide la autoridad del perfil.) — -5
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** copia explicita → 1/5

**Herramienta principal: Claude Code (solo para consolidar)**

Un backup o una galería de versiones no se desarrolla: se decide su futuro. Un agente solo tiene sentido para extraer lo aprovechable y moverlo al repo canónico. Cuatro copias vivas de lo mismo es el problema, y no lo arregla ninguna herramienta: lo arregla una decisión.

- Segunda opción: **Ninguna: archivar**
- Alternativas: **Cursor** · **OpenCode**

**Primera acción:** Archivar con isArchived=true o borrar, dejando un único repo canónico. Solo esto ya sube la percepción de todo el perfil.

**Evitar:** Invertir horas de agente en un repo que debería estar archivado.

---

### 85. local-agent — 52/100

[https://github.com/belentani7/local-agent](https://github.com/belentani7/local-agent) · **SITIO_ESTATICO** · PowerShell · 159 KB · 4 commits · 29 ficheros · creado 2026-08-02 · último push hace 8 días

> Archived reference: Windows OpenManus/Ollama setup. Preserved for documentation; current work uses remote providers on modest hardware.

**Los 20 aspectos** — suma 54/100, penalizaciones -2, nota final 52/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **0/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **0/5** |
| Demo desplegada | **0/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 267 palabras · 10 encabezados · 6 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 2 · sección de uso: sí

**Penalizaciones**

- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 86. deepseek-fix-verify — 50/100

[https://github.com/belentani7/deepseek-fix-verify](https://github.com/belentani7/deepseek-fix-verify) · **PY_TOOL** · Python · 42 KB · 9 commits · 66 ficheros · creado 2026-09-09 · último push hace 2 días

> DeepSeek fix verification scripts (Python).

**Los 20 aspectos** — suma 56/100, penalizaciones -6, nota final 50/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **5/5** |
| Licencia | **0/5** | Config de despliegue | **2/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 25 palabras · 3 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / ZCode (BYOK)**

Son scripts en Python: el valor está en el fichero, no en el frontend. Lo que hace falta es un agente que lea el repo, ejecute pytest y corrija. OpenCode con GLM de Z.ai (plan Lite ~12,60-18 USD/mes) o Gemini CLI con cuota gratuita dan capacidad de frontera a coste cero o muy bajo; Claude Code es más fiable en refactors largos.

- Segunda opción: **Claude Code**
- Alternativas: **Codex CLI** · **Gemini CLI (gratis)**

**Primera acción:** Ejecutar el CLI tal cual está, documentar entrada y salida reales en el README y añadir un pyproject.toml con dependencias declaradas. Sin tests no se puede refactorizar después.

**Evitar:** Replit o Bolt: su backend es Node; meterían este Python en un contenedor que no necesita.

---

### 87. ai-command-center-level10 — 50/100

[https://github.com/belentani7/ai-command-center-level10](https://github.com/belentani7/ai-command-center-level10) · **WEB_APP_TS** · TypeScript · 624 KB · 19 commits · 194 ficheros · creado 2026-08-18 · último push hace 2 días

> AI Command Center Level 10 - Unified Open Source Workspace

**Los 20 aspectos** — suma 59/100, penalizaciones -9, nota final 50/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **0/5** |
| Topics | **3/5** | Documentación | **5/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **0/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **4/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **2/5** | Unicidad en el ecosistema | **3/5** |

**README leído:** 281 palabras · 6 encabezados · 5 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 9 · sección de uso: no

**Afirmaciones no verificables detectadas:**
- `level 10` → se autocalifica con un nivel numerico

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: 'level 10' (se autocalifica con un nivel numerico). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-CI` (Tiene manifest de build y ningun workflow: nada verifica que siga compilando.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** declara ser el unificado → 3/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 88. noiacore-turbo-v2 — 49/100

[https://github.com/belentani7/noiacore-turbo-v2](https://github.com/belentani7/noiacore-turbo-v2) · **AGENT_INFRA** · Python · 219 KB · 2 commits · 71 ficheros · creado 2026-09-02 · último push hace 2 días

> BarriServei AI - Autonomous local services platform with AI intake, Stripe escrow, WhatsApp integration

**Los 20 aspectos** — suma 57/100, penalizaciones -8, nota final 49/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **0/5** |
| Topics | **3/5** | Documentación | **3/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **5/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **1/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 1306 palabras · 46 encabezados · 19 bloques de código · 5 enlaces · 0 imágenes · 3 badges · idioma en · comandos de ejecución: 17 · sección de uso: sí

**Afirmaciones no verificables detectadas:**
- `production-ready` → afirma estar listo para produccion sin evidencia

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: 'production-ready' (afirma estar listo para produccion sin evidencia). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `SIN-CI` (Tiene manifest de build y ningun workflow: nada verifica que siga compilando.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: ZCode (GLM-5.3, contexto 1M)**

La orquestación multi-agente es un problema de contexto largo: hay que sostener el estado de muchos pasos. GLM-5.3 con 1M de contexto es el más barato para eso (Lite ~12,60 USD/mes) y sus modelos 5.1 y 5.3 están diseñados para tareas autónomas de hasta 8 horas. Antigravity aporta la orquestación multi-agente real en local, gratis.

- Segunda opción: **Claude Code**
- Alternativas: **Google Antigravity (multi-agente)** · **Codex CLI**

**Primera acción:** Documentar el protocolo en un README de 20 líneas y cubrir el núcleo con tests. Un orquestador sin tests es código que no se puede cambiar.

**Evitar:** Solo autocompletado: no van a seguir un objetivo de 50 pasos.

---

### 89. duck-2026 — 49/100

[https://github.com/belentani7/duck-2026](https://github.com/belentani7/duck-2026) · **SITIO_ESTATICO** · HTML · 5541 KB · 17 commits · 34 ficheros · creado 2026-08-18 · último push hace 2 días

> DUCK 2026 - iteracion anual del ecosistema DUCK.

**Los 20 aspectos** — suma 54/100, penalizaciones -5, nota final 49/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 428 palabras · 7 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 90. Steven-renovation — 49/100

[https://github.com/belentani7/Steven-renovation](https://github.com/belentani7/Steven-renovation) · **SITIO_ESTATICO** · HTML · 5881 KB · 27 commits · 19 ficheros · creado 2026-08-10 · último push hace 2 días

> Este proyecto contiene la estructura local de una web comercial para servicios de reformas. La carpeta agrupa variantes HTML, recursos visuales, vídeos y documentación breve preparada para organizar el material antes de subirlo a GitHub.

**Los 20 aspectos** — suma 54/100, penalizaciones -5, nota final 49/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **5/5** | CI/CD | **0/5** |
| Topics | **4/5** | Documentación | **3/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **3/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **3/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 55 palabras · 3 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 91. belentani-the-judas-experience-archive — 48/100

[https://github.com/belentani7/belentani-the-judas-experience-archive](https://github.com/belentani7/belentani-the-judas-experience-archive) · **DUP_ARCHIVE** · HTML · 37840 KB · 9 commits · 143 ficheros · creado 2026-08-22 · último push hace 2 días

> Archivo oficial de The Judas Experience - experiencia musical interactiva.

**Los 20 aspectos** — suma 56/100, penalizaciones -8, nota final 48/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **1/5** |

**README leído:** 292 palabras · 5 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 3 · sección de uso: no

**Penalizaciones**

- `DUPLICADO` (Es una copia. Publicar copia y original a la vez divide la autoridad del perfil.) — -5
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** copia explicita → 1/5

**Herramienta principal: Claude Code (solo para consolidar)**

Un backup o una galería de versiones no se desarrolla: se decide su futuro. Un agente solo tiene sentido para extraer lo aprovechable y moverlo al repo canónico. Cuatro copias vivas de lo mismo es el problema, y no lo arregla ninguna herramienta: lo arregla una decisión.

- Segunda opción: **Ninguna: archivar**
- Alternativas: **Cursor** · **OpenCode**

**Primera acción:** Archivar con isArchived=true o borrar, dejando un único repo canónico. Solo esto ya sube la percepción de todo el perfil.

**Evitar:** Invertir horas de agente en un repo que debería estar archivado.

---

### 92. duck-studio-suite — 48/100

[https://github.com/belentani7/duck-studio-suite](https://github.com/belentani7/duck-studio-suite) · **WEB_APP_TS** · TypeScript · 186 KB · 10 commits · 109 ficheros · creado 2026-08-22 · último push hace 2 días

> Duck Studio Suite - suite integrada de produccion musical web.

**Los 20 aspectos** — suma 53/100, penalizaciones -5, nota final 48/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **0/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 37 palabras · 3 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 93. heyduck — 48/100

[https://github.com/belentani7/heyduck](https://github.com/belentani7/heyduck) · **SITIO_ESTATICO** · HTML · 57767 KB · 16 commits · 123 ficheros · creado 2026-07-16 · último push hace 24 días

> HEYDUCK - hub web del universo DUCK: apps, musica y herramientas de produccion.

**Los 20 aspectos** — suma 51/100, penalizaciones -3, nota final 48/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **3/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **5/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 419 palabras · 10 encabezados · 2 bloques de código · 2 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 2 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 94. MetaSkill — 47/100

[https://github.com/belentani7/MetaSkill](https://github.com/belentani7/MetaSkill) · **SKILL_PACK** · Python · 18 KB · 5 commits · 9 ficheros · creado 2026-08-16 · último push hace 15 días

> Zero-token task router for AI coding agents — classifies requests locally without burning LLM tokens. 16 archetypes, 4 complexity tiers, in-context classification.

**Los 20 aspectos** — suma 50/100, penalizaciones -3, nota final 47/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **5/5** | CI/CD | **2/5** |
| Topics | **5/5** | Documentación | **2/5** |
| README (contenido real) | **5/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **0/5** | Actividad reciente | **4/5** |
| Volumen de código | **2/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **2/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 403 palabras · 13 encabezados · 5 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 95. belentani7.github.io — 46/100

[https://github.com/belentani7/belentani7.github.io](https://github.com/belentani7/belentani7.github.io) · **SITIO_ESTATICO** · HTML · 92 KB · 13 commits · 19 ficheros · creado 2026-08-31 · último push hace 2 días

> BELENTANI // OMEGA CORE — JUDAS_OS v12.0 · organismo vivo · 432 Hz

**Los 20 aspectos** — suma 51/100, penalizaciones -5, nota final 46/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **3/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **2/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 422 palabras · 5 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 96. omega-max-duck — 46/100

[https://github.com/belentani7/omega-max-duck](https://github.com/belentani7/omega-max-duck) · **WEB_APP_TS** · TypeScript · 279 KB · 4 commits · 170 ficheros · creado 2026-08-22 · último push hace 24 días

> DUCK Ω-MAX Studio OS — CRM, producción musical, operaciones y automatizaciones para clientes y proyectos.

**Los 20 aspectos** — suma 54/100, penalizaciones -8, nota final 46/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **0/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **0/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **3/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 389 palabras · 6 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 4 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 9 repos comparten el token 'omega'. Ninguno es canonico.) — -3
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-CI` (Tiene manifest de build y ningun workflow: nada verifica que siga compilando.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 9 repos comparten el token 'omega' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 97. judas-scifi-experience — 46/100

[https://github.com/belentani7/judas-scifi-experience](https://github.com/belentani7/judas-scifi-experience) · **WEB_APP_TS** · TypeScript · 164 KB · 6 commits · 102 ficheros · creado 2026-08-18 · último push hace 15 días

> Judas sci-fi experience - TypeScript interactive web project.

**Los 20 aspectos** — suma 52/100, penalizaciones -6, nota final 46/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **2/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **4/5** |
| Volumen de código | **3/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **3/5** | Gestión de issues | **2/5** |
| Reproducibilidad | **5/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 2812 palabras · 18 encabezados · 11 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 2 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 7 repos comparten el token 'judas'. Ninguno es canonico.) — -3
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 7 repos comparten el token 'judas' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 98. michelle-relayze-web — 45/100

[https://github.com/belentani7/michelle-relayze-web](https://github.com/belentani7/michelle-relayze-web) · **SITIO_ESTATICO** · HTML · 3694 KB · 8 commits · 16 ficheros · creado 2026-08-29 · último push hace 2 días

> Web oficial de Michelle Relayze — portfolio y presencia artística

**Los 20 aspectos** — suma 48/100, penalizaciones -3, nota final 45/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **3/5** | Documentación | **1/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **1/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **5/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **0/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 178 palabras · 5 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 1 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 99. omega-infinite-v4 — 42/100

[https://github.com/belentani7/omega-infinite-v4](https://github.com/belentani7/omega-infinite-v4) · **WEB_APP_TS** · HTML · 11 KB · 8 commits · 12 ficheros · creado 2026-09-05 · último push hace 6 días

> Omega Infinite v4 - HTML prototype; consolidation candidate with omega-infinite-os.

**Los 20 aspectos** — suma 50/100, penalizaciones -8, nota final 42/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **1/5** |
| README (contenido real) | **0/5** | Higiene de secretos | **3/5** |
| Licencia | **4/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **2/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **4/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 15 palabras · 1 encabezados · 0 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 9 repos comparten el token 'omega'. Ninguno es canonico.) — -3
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `README-MAGERNA` (README de 15 palabras: no explica ni como se ejecuta.) — -2
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 9 repos comparten el token 'omega' → 2/5

**Herramienta principal: Google Antigravity (local)**

Es código real con build, así que hace falta un agente que entienda lo que ya hay, no un generador desde cero. Antigravity es la opción local más completa y gratuita (tab completion con Gemini Flash sin límite de pago, y admite Claude y GPT-OSS) y aporta orquestación multi-agente para monorepos. Claude Code es el mejor agente único para refactors largos y para leer un CLAUDE.md.

- Segunda opción: **Claude Code**
- Alternativas: **Cursor** · **Bolt.new**

**Primera acción:** Escribir un CLAUDE.md con la arquitectura real y el comando de build, y pedir un solo objetivo por sesión. Comprobar el build antes y después.

**Evitar:** v0 genera Next.js bonito, que es justo lo contrario de mantener este código.

---

### 100. CODEX-OMEGA-SKILL — 42/100

[https://github.com/belentani7/CODEX-OMEGA-SKILL](https://github.com/belentani7/CODEX-OMEGA-SKILL) · **SKILL_PACK** · PowerShell · 28 KB · 8 commits · 21 ficheros · creado 2026-08-28 · último push hace 2 días

> CODEX Omega Skill - Belentani ecosystem

**Los 20 aspectos** — suma 49/100, penalizaciones -7, nota final 42/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **2/5** | CI/CD | **2/5** |
| Topics | **4/5** | Documentación | **5/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **2/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **3/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 226 palabras · 5 encabezados · 3 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 9 repos comparten el token 'omega'. Ninguno es canonico.) — -3
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 9 repos comparten el token 'omega' → 2/5

**Herramienta principal: OpenCode / Claude Code (local, BYOK)**

Un pack de skills es texto estructurado con convenciones precisas. Lo que falta es un agente que valide que cada SKILL.md cumple el esquema y que el registro no tenga duplicados. Las herramientas locales con BYOK salen gratis o casi: aquí el presupuesto, no la capacidad, es el cuello de botella.

- Segunda opción: **ZCode**
- Alternativas: **Cline** · **Gemini CLI**

**Primera acción:** Añadir un validador automático del esquema (el propio skillforge o MetaSkill de este perfil) y ejecutarlo en CI sobre cada PR.

**Evitar:** Z.ai web: se paga por prompt y aquí el trabajo es sobre archivo local; se pierde la tarifa.

---

### 101. DuckHTML — 39/100

[https://github.com/belentani7/DuckHTML](https://github.com/belentani7/DuckHTML) · **SITIO_ESTATICO** · HTML · 35 KB · 14 commits · 11 ficheros · creado 2026-08-22 · último push hace 2 días

> Experimentos HTML del universo DUCK - interfaces y prototipos rapidos.

**Los 20 aspectos** — suma 44/100, penalizaciones -5, nota final 39/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **3/5** | CI/CD | **4/5** |
| Topics | **3/5** | Documentación | **2/5** |
| README (contenido real) | **1/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **4/5** | Actividad reciente | **5/5** |
| Volumen de código | **2/5** | Historial de commits | **3/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **2/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 234 palabras · 5 encabezados · 0 bloques de código · 7 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: no

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** 18 repos comparten el token 'duck' → 2/5

**Herramienta principal: Lovable**

Es código estático que ya funciona: ninguna herramienta necesita reescribirlo. Lovable importa el repo desde GitHub y devuelve los cambios a una rama, con despliegue incluido, y es el ciclo más corto para pasar de «funciona en local» a «tiene URL pública». Google AI Studio es la alternativa si lo que falta es backend (Firestore + Auth + Workspace) sin salir del navegador: 2 apps gratis en Cloud Run, sin tarjeta, y exportación a Antigravity con el historial y los secretos.

- Segunda opción: **Google AI Studio (Build mode)**
- Alternativas: **Bolt.new** · **Onlook**

**Primera acción:** Importar el repo en Lovable y pedir solo lo que falta (responsive, SEO, OG image, analítica). No regenerar la página desde cero: los assets ya están optimizados.

**Evitar:** Regenerar con v0: perderías los assets y el trabajo visual ya hecho.

---

### 102. belentani-java-platform — 38/100

[https://github.com/belentani7/belentani-java-platform](https://github.com/belentani7/belentani-java-platform) · **PLATFORM_JAVA** · Java · 15 KB · 9 commits · 38 ficheros · creado 2026-09-01 · último push hace 2 días

> Belentani Platform — enterprise-grade Java backend with JPA entities, security layers, and microservice architecture blueprint

**Los 20 aspectos** — suma 50/100, penalizaciones -12, nota final 38/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **2/5** |
| Topics | **3/5** | Documentación | **4/5** |
| README (contenido real) | **2/5** | Higiene de secretos | **3/5** |
| Licencia | **0/5** | Config de despliegue | **1/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **2/5** | Historial de commits | **2/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **2/5** | Gestión de issues | **4/5** |
| Reproducibilidad | **2/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 35 palabras · 3 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma en · comandos de ejecución: 0 · sección de uso: sí

**Afirmaciones no verificables detectadas:**
- `enterprise-grade` → afirma nivel empresarial sin evidencia

**Penalizaciones**

- `RECLAMO-INFLADO` (Afirmacion no verificable sobre si mismo: 'enterprise-grade' (afirma nivel empresarial sin evidencia). Es exactamente lo que un revisor detecta como inventado y lo que penaliza tanto a Google como a las IAs al recomendarte.) — -4
- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-TESTS` (Tiene codigo fuente en src/ y ningun test.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Claude Code**

Java con build server necesita un agente que ejecute el build. Con el volumen actual y sin tests, el repo está en estado de esqueleto: la prioridad es la estructura y un build que pase, no generar más código.

- Segunda opción: **Codex CLI**
- Alternativas: **ZCode** · **Google Antigravity**

**Primera acción:** Un pom.xml o build.gradle que compile en GitHub Actions, aunque el código sea mínimo. Sin build no hay CI posible.

**Evitar:** Plataformas de vibe coding: no compilan Java server-side.

---

### 103. the-judas-experience — 32/100

[https://github.com/belentani7/the-judas-experience](https://github.com/belentani7/the-judas-experience) · **DESIGN_SYSTEM** · CSS · 2249 KB · 2 commits · 14 ficheros · creado 2026-08-29 · último push hace 29 días

**Los 20 aspectos** — suma 40/100, penalizaciones -8, nota final 32/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **0/5** | CI/CD | **0/5** |
| Topics | **4/5** | Documentación | **3/5** |
| README (contenido real) | **4/5** | Higiene de secretos | **1/5** |
| Licencia | **4/5** | Config de despliegue | **0/5** |
| Demo desplegada | **0/5** | Actividad reciente | **4/5** |
| Volumen de código | **5/5** | Historial de commits | **1/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **0/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **2/5** |

**README leído:** 356 palabras · 8 encabezados · 1 bloques de código · 6 enlaces · 3 imágenes · 6 badges · idioma es · comandos de ejecución: 1 · sección de uso: no

**Penalizaciones**

- `ARCHIVADO` (GitHub lo marca como archivado: no recibe cambios y aparece como repo muerto en el perfil.) — -3
- `CONFLICTO-PROP` (Muchos repos reclaman el mismo titulo: 7 repos comparten el token 'judas'. Ninguno es canonico.) — -3
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1

**Unicidad:** 7 repos comparten el token 'judas' → 2/5

**Herramienta principal: Figma Make / Google Stitch -> codigo**

Un design system se valida en pantalla leyendo tokens, no leyendo CSS. El orden correcto es diseño primero: definir en Figma o Stitch, exportar, y solo entonces generar código. Onlook es el único que edita tus componentes React reales en vez de generar un mockup aparte que luego copias.

- Segunda opción: **Onlook**
- Alternativas: **Claude Code** · **v0**

**Primera acción:** Publicar los tokens como CSS custom properties dentro de un README renderizable, que es lo que un buscador puede indexar de un design system.

**Evitar:** Generar el CSS con un agente y esperar consistencia: no sale.

---

### 104. belentani-design-system — 31/100

[https://github.com/belentani7/belentani-design-system](https://github.com/belentani7/belentani-design-system) · **DESIGN_SYSTEM** · CSS · 4 KB · 3 commits · 3 ficheros · creado 2026-09-26 · último push hace 2 días

> Belentani Design System: glass thick red-neon, glitch machine, coding rain. CSS+JS drop-in para todo el ecosistema.

**Los 20 aspectos** — suma 37/100, penalizaciones -6, nota final 31/100

| Aspecto | Pts | Aspecto | Pts |
|---|---|---|---|
| Descripción | **4/5** | CI/CD | **0/5** |
| Topics | **4/5** | Documentación | **1/5** |
| README (contenido real) | **3/5** | Higiene de secretos | **1/5** |
| Licencia | **0/5** | Config de despliegue | **0/5** |
| Demo desplegada | **0/5** | Actividad reciente | **5/5** |
| Volumen de código | **1/5** | Historial de commits | **1/5** |
| Lenguaje coherente | **4/5** | Descubribilidad social | **0/5** |
| Estructura de proyecto | **0/5** | Gestión de issues | **3/5** |
| Reproducibilidad | **0/5** | Nombre y marca | **5/5** |
| Tests | **0/5** | Unicidad en el ecosistema | **5/5** |

**README leído:** 89 palabras · 4 encabezados · 1 bloques de código · 0 enlaces · 0 imágenes · 0 badges · idioma es · comandos de ejecución: 0 · sección de uso: sí

**Penalizaciones**

- `SIN-LICENCIA` (Sin licencia: legalmente nadie puede reutilizarlo y las IAs lo tratan como contenido no reutilizable.) — -2
- `SIN-DEMO` (Sin homepage: nadie ve el resultado sin clonar.) — -1
- `SIN-VISIBILIDAD` (Cero stars y cero forks.) — -1
- `SIN-INSTRUCCIONES` (El README no contiene ni un comando de ejecucion: no hay forma de arrancarlo.) — -2

**Unicidad:** sin conflicto observable → 5/5

**Herramienta principal: Figma Make / Google Stitch -> codigo**

Un design system se valida en pantalla leyendo tokens, no leyendo CSS. El orden correcto es diseño primero: definir en Figma o Stitch, exportar, y solo entonces generar código. Onlook es el único que edita tus componentes React reales en vez de generar un mockup aparte que luego copias.

- Segunda opción: **Onlook**
- Alternativas: **Claude Code** · **v0**

**Primera acción:** Publicar los tokens como CSS custom properties dentro de un README renderizable, que es lo que un buscador puede indexar de un design system.

**Evitar:** Generar el CSS con un agente y esperar consistencia: no sale.

---

## 8. Orden de ejecución sugerido

Si solo vas a hacer seis cosas, en este orden:

1. **Añadir LICENSE a los 32 repos que no la tienen.** Un fichero, 31% de los repos, y decide si tu código puede ser citado. Escribe `MIT` y ya.
2. **Meter un comando de ejecución en los 27 READMEs que no lo tienen.** Una línea por repo convierte el README en instrucción en lugar de descripción.
3. **Elegir tres repos canónicos** y archivar o renombrar el resto de los que reclaman `belentani`, `duck` y `omega`. Afecta a más de la mitad del perfil de una sentada.
4. **Retirar los 10 reclamos de calidad sin evidencia** y sustituirlos por un número parcial y medible, como ya haces bien en `duck-zion-apex-public` (57/60) y `agent-skills` (311 skills).
5. **Añadir un workflow mínimo** (build o test) a los 8 repos con manifest y sin CI. Es la prueba objetiva de que el proyecto vive, y es lo que una IA comprueba antes de recomendarlo.
6. **Empezar a commitear por cambio, no por sesión.** 2509 commits repartidos en 104 repos (mediana 11) no cuentan una historia que un tercero pueda seguir. A partir de hoy, un commit por cambio, con un mensaje que explique el porqué.

Lo que **no** conviene hacer: abrir otros 104 repos. El problema de este perfil no es la
falta de cantidad, es que una cola de repos con una media de 63/100 y cero stars se lee como
una cola de borradores. Subir la media de los que ya existen mueve la percepción más que
crear más.

---

*Informe generado el 2026-09-28 a partir de 104 repositorios y cuatro endpoints de la API de GitHub, sin clonar nada.*