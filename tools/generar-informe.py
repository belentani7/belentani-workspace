#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generar-informe.py - Genera C:\\Users\\USER\\Desktop\\produccion\\INFORME-REPOS.md
a partir de los artefactos JSON ya verificados. No toca ningun repo.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

B = Path(r"C:\Users\USER\Desktop\produccion")
OUT = B / "INFORME-REPOS.md"

estado = json.loads((B / "estado.json").read_text(encoding="utf-8"))
gh = json.loads((B / "github-inventario.json").read_text(encoding="utf-8"))
div = json.loads((B / "diverged-analisis.json").read_text(encoding="utf-8"))
cruce = json.loads((B / "auditoria-cruce.json").read_text(encoding="utf-8"))
pub = json.loads((B / "faltan-publicar.json").read_text(encoding="utf-8"))
pend = json.loads((B / "pending-exacto.json").read_text(encoding="utf-8"))
grupos = json.loads((B / "pending-grupos.json").read_text(encoding="utf-8"))
integ = json.loads((B / "integridad-git.json").read_text(encoding="utf-8"))

L: list[str] = []
w = L.append

# ---------------- cabecera ----------------
w("# INFORME DE REPOSITORIOS — auditoría de solo lectura")
w("")
w(f"**Fecha de generación:** {datetime.now():%Y-%m-%d %H:%M}  ")
w("**Alcance:** 264 repos locales (`estado.json`) contra 456 repos en GitHub "
  "(`github-inventario.json`)  ")
w("**Modo:** solo lectura. No se ha borrado, modificado ni pusheado nada.")
w("")
w("> **Nota de método.** Los números de este informe se recalcularon en vivo "
  "contra git y contra GitHub. Donde el dato de partida (`estado.json`) resultó "
  "ser un artefacto de medición, se dice explícitamente y se da el valor "
  "corregido. Al final hay una sección de **verificaciones y limitaciones**.")
w("")

# ---------------- 1. resumen ----------------
w("## 1. Resumen ejecutivo")
w("")
w("| Métrica | Valor |")
w("|---|---|")
w(f"| Repos locales analizados | **{len(estado)}** |")
w(f"| Espacio total ocupado | **{sum(x.get('size_mb') or 0 for x in estado):,.1f} MB** |")
w(f"| Repos en GitHub (inventario) | {len(gh)} "
  f"({sum(1 for r in gh if not r['private'])} públicos / "
  f"{sum(1 for r in gh if r['private'])} privados) |")
w(f"| Repos locales que **casan por nombre** con GitHub | "
  f"{len(estado) - len(cruce['faltantes_reales']) - len(cruce['faltantes_anidados'])} |")
w(f"| Repos locales **ausentes** de GitHub (bruto) | "
  f"{len(cruce['faltantes_reales']) + len(cruce['faltantes_anidados'])} |")
w(f"| ↳ excluidos por ser subcarpeta anidada | {len(cruce['faltantes_anidados'])} |")
w(f"| ↳ **ausentes reales** | **{len(cruce['faltantes_reales'])}** |")
w(f"| ↳ de esos, clones de terceros (upstream ya existe) | "
  f"{len(pub['clones_terceros'])} |")
w(f"| ↳ **propios que faltan por publicar** | "
  f"**{len(pub['propios_remoto_404']) + len(pub['sin_remoto'])}** |")
w("")
w("### Hallazgos que cambian la acción a tomar")
w("")
n404 = len(pub["propios_remoto_404"])
nsin = len(pub["sin_remoto"])
w(f"1. **Solo {n404 + nsin} repos propios están realmente sin publicar**, no 47. "
  f"De los 47 ausentes reales, **{len(pub['clones_terceros'])} son clones de "
  "repositorios de terceros** cuyo upstream sí existe en GitHub: no son trabajo "
  "tuyo por publicar.")
w("2. **`BELENTANI-OS_2` (383,1 MB) no es un repositorio git.** Su carpeta `.git` "
  "existe pero está **vacía (0 entradas)**. Contiene 383 MB de material real "
  "(incluido `06_ARCHIVO/brain.db` de 181,6 MB) **sin ningún control de "
  "versiones ni copia remota**. Es el mayor riesgo de pérdida del inventario.")
w("3. **Los 42 repos `PENDING` NO tienen commits sin pushear.** Se midió el SHA "
  "remoto de cada rama con `git ls-remote` y **coincide exactamente con el HEAD "
  "local en los 42**. El problema es exclusivamente árbol de trabajo sucio "
  "(19 repos) o archivos sin trackear (7 repos).")
w("4. **El veredicto `UNREACHABLE` de `deepseek-harness` es un falso positivo.** "
  "El remoto responde correctamente; la causa real es un *refspec* de fetch "
  "anómalo (solo tags) en el clon local.")
w("5. **123 repos están marcados `DIVERGED`, pero solo 6 tienen trabajo local "
  "por delante.** Los otros 104 están simplemente **por detrás** del remoto "
  "(recuperables) y 13 tienen historiales separados.")
w("")

# ---------------- 2. tabla por veredicto ----------------
w("## 2. Tabla resumen de los 264 repos por veredicto")
w("")
orden = ["DIVERGED", "PENDING", "SAFE_TO_DELETE", "KEEP_EDU", "NO_REMOTE",
         "REMOTE_MISSING", "UNREACHABLE", "NO_COMMITS"]
tot_n = tot_mb = 0
w("| Veredicto | Repos | Tamaño (MB) | % del total | Significado operativo |")
w("|---|---:|---:|---:|---|")
sig = {
    "DIVERGED": "HEAD local ≠ remoto (ver §4 para el desglose real)",
    "PENDING": "Con cambios locales pendientes de decidir (ver §5)",
    "SAFE_TO_DELETE": "Pusheado, limpio, sin pendientes",
    "KEEP_EDU": "Material educacional: se conserva siempre",
    "NO_REMOTE": "Sin remoto configurado",
    "REMOTE_MISSING": "El remoto configurado ya no existe (404)",
    "UNREACHABLE": "No alcanzable (ver §7: falso positivo)",
    "NO_COMMITS": "Repo sin commits",
}
for v in orden:
    sub = [x for x in estado if x["verdict"] == v]
    if not sub:
        continue
    m = sum(x.get("size_mb") or 0 for x in sub)
    tot_n += len(sub)
    tot_mb += m
    w(f"| `{v}` | {len(sub)} | {m:,.1f} | {m / sum(x.get('size_mb') or 0 for x in estado) * 100:.1f}% | {sig[v]} |")
w(f"| **TOTAL** | **{tot_n}** | **{tot_mb:,.1f}** | 100% | |")
w("")

# ---------------- 3. faltan por publicar ----------------
w("## 3. Repos que faltan por publicar")
w("")
w("Criterio: repo local del `estado.json` cuyo nombre/URL **no aparece** en "
  "`github-inventario.json`, excluyendo subcarpetas anidadas dentro de otro repo "
  "(se detectó buscando un `.git` en los directorios padre) y excluyendo clones "
  "cuyo remoto apunta a un repositorio upstream de terceros que ya existe.")
w("")

w("### 3.1 Propios con remoto configurado que devuelve 404 ({} repos)".format(n404))
w("")
w("Verificado con `git ls-remote` **y** con la API REST de GitHub (HTTP 404), "
  "usando un token válido: dos repos de control del mismo propietario "
  "(`belentani-platform`, `hbo-noir-icons`) devolvieron HTTP 200, por lo que el "
  "404 es genuino y no un fallo de credenciales.")
w("")
w("| Repo | Ruta | Tamaño | Remoto configurado | Commits | Sin commitear |")
w("|---|---|---:|---|---:|---:|")
for x in sorted(pub["propios_remoto_404"], key=lambda y: -(y["size_mb"] or 0)):
    w(f'| `{x["name"]}` | `{x["path"]}` | {x["size_mb"]:,.1f} MB | `{x["remote"]}` | '
      f'{x["n_commits"]} | {x["n_cambios_sin_commit"]} |')
w("")

w(f"### 3.2 Sin remoto alguno ({nsin} repos)")
w("")
w("| Repo | Ruta | Tamaño | Commits | Sin commitear | Nota |")
w("|---|---|---:|---:|---:|---|")
notas = {
    "BELENTANI-OS_2": "**.git VACÍO** — no es un repo; 383 MB sin versionar",
    "belentani-cv-work": "HEAD no nace (sin commits); 6 archivos sin trackear",
    "3-workspace": "51 cambios sin commitear",
    "letra-office": "95 cambios sin commitear",
    "judas-experience-expanded": "8 commits; 2 cambios sin commitear",
    "saas-plasma_2": "9 commits; 1 cambio sin commitear",
    "frontend": "2 commits; 5 cambios sin commitear",
    "server": "2 commits; 9 cambios sin commitear",
    "aurea3d-premium": "1 commit; árbol limpio",
}
for x in sorted(pub["sin_remoto"], key=lambda y: -(y["size_mb"] or 0)):
    sc = x["n_cambios_sin_commit"]
    sc = "—" if sc is None else sc
    w(f'| `{x["name"]}` | `{x["path"]}` | {x["size_mb"]:,.1f} MB | {x["n_commits"]} | '
      f'{sc} | {notas.get(x["name"], "")} |')
w("")

w("### 3.3 Excluidos del listado anterior (y por qué)")
w("")
w(f"- **{len(cruce['faltantes_anidados'])} subcarpetas anidadas** dentro de otro "
  "repo con `.git` en un directorio padre: no son repositorios independientes.")
w(f"- **{len(pub['clones_terceros'])} clones de terceros**: su remoto apunta a un "
  "upstream que ya existe en GitHub bajo otro propietario "
  "(p. ej. `ollama/ollama`, `audacity/audacity`, `spotify/pedalboard`, "
  "`anthropics/skills`). No son trabajo propio pendiente de publicar.")
w("- **3 repos vacíos** (`BELENTANI-BRAIN`, `MiSaaS`, `PORTFOLIO`) casaron por "
  "nombre con el inventario de GitHub pero su `.git` local está **corrupto** "
  "(faltan `HEAD`, `config`, `objects`…). No tienen commits: nada que publicar. "
  "Ver §6.")
w("")
w("**Total con contenido propio realmente sin publicar: "
  f"{n404 + nsin} repos ≈ "
  f"{sum(x['size_mb'] or 0 for x in pub['propios_remoto_404']) + sum(x['size_mb'] or 0 for x in pub['sin_remoto']):,.1f} MB.**")
w("")

w("<details><summary>Listado completo de los 34 clones de terceros (informativo)</summary>")
w("")
w("| Repo local | Tamaño | Veredicto | Upstream |")
w("|---|---:|---|---|")
for x in sorted(pub["clones_terceros"], key=lambda y: -(y["size_mb"] or 0)):
    w(f'| `{x["name"]}` | {x["size_mb"]:,.1f} MB | `{x["verdict"]}` | `{x["remote"]}` |')
w("")
w("</details>")
w("")

# ---------------- 4. DIVERGED ----------------
w("## 4. Repos `DIVERGED` clasificados")
w("")
w("`analizar-diverged.py` ejecutado sobre los 123 repos `DIVERGED`. "
  "**Recalculado después de forma independiente: el resultado coincide exactamente "
  "(6 / 104 / 13, 0 sin clasificar).**")
w("")
w("| Categoría | Repos | MB | Qué significa | Riesgo |")
w("|---|---:|---:|---|---|")
mb_d = sum(x["mb"] for x in div["delante"])
mb_t = sum(x["mb"] for x in div["detras"])
mb_a = sum(x["mb"] for x in div["ambos"])
w(f'| **Solo por DELANTE** | {len(div["delante"])} | {mb_d:,.1f} | Hay commits locales que no están en el remoto | **Alto: trabajo sin publicar** |')
w(f'| **Solo por DETRÁS** | {len(div["detras"])} | {mb_t:,.1f} | El remoto es superconjunto del local | Bajo: recuperable |')
w(f'| **AMBOS lados** | {len(div["ambos"])} | {mb_a:,.1f} | Historiales separados | Medio: decisión manual |')
w("")

w('### 4.1 Solo por DELANTE — trabajo local sin publicar (6 repos)')
w("")
w("Estos son los únicos repos `DIVERGED` con commits que no existen en el remoto.")
w("")
w("| Repo | Commits por delante | Tamaño | Rama | ¿Rama existe en remoto? | Ruta |")
w("|---|---:|---:|---|---|---|")
ramas = {
    "agentbox": ("HEAD (detached)", "no — se crearía al pushear"),
    "nexus-data": ("HEAD (detached)", "no — se crearía al pushear"),
    "belentani-v2": ("main", "sí"),
    "manus-ai-skill-pack": ("main", "sí"),
    "securetea": ("main", "sí"),
    "voice-ai-agency": ("codex/voice-ai-foundation-20260808", "sí"),
}
for x in sorted(div["delante"], key=lambda y: -y["ahead"]):
    br, ex = ramas.get(x["name"], ("?", "?"))
    w(f'| `{x["name"]}` | +{x["ahead"]} | {x["mb"]:,.1f} MB | `{br}` | {ex} | `{x["path"]}` |')
w("")
w("> **Atención:** `agentbox` y `nexus-data` están en **HEAD desacoplado "
  "(detached HEAD)**. Un `git push` normal no publicaría nada; habría que usar "
  "`git push origin HEAD:main` o crear antes una rama.")
w("")

w('### 4.2 AMBOS lados — historiales separados (13 repos)')
w("")
w("| Repo | Delante | Detrás | Tamaño | Ruta |")
w("|---|---:|---:|---:|---|")
for x in sorted(div["ambos"], key=lambda y: -(y["ahead"] + y["behind"])):
    w(f'| `{x["name"]}` | +{x["ahead"]} | −{x["behind"]} | {x["mb"]:,.1f} MB | `{x["path"]}` |')
w("")
w("Los 4 primeros (`duck-ecosystem`, `judas-experience`, `noiacore-lab`, "
  "`noiacore`) tienen el mayor número de commits divergentes: son los que más "
  "probablemente necesiten un merge real y no un simple push.")
w("")

w('### 4.3 Solo por DETRÁS — el remoto es superconjunto (104 repos)')
w("")
w(f"En estos repos **no hay ningún commit local que falte en el remoto**: el "
  f"remoto contiene todo el trabajo local y más. Total {mb_t:,.1f} MB. "
  "Se listan los 104 completos, ordenados por tamaño: los mayores son los "
  "candidatos naturales a recuperar espacio en disco.")
w("")
w("| Repo | Commits por detrás | Tamaño | Ruta |")
w("|---|---:|---:|---|")
for x in sorted(div["detras"], key=lambda y: -y["mb"]):
    w(f'| `{x["name"]}` | −{x["behind"]} | {x["mb"]:,.1f} MB | `{x["path"]}` |')
w("")

# ---------------- 5. PENDING ----------------
w("## 5. Repos `PENDING` agrupados por causa")
w("")
w(f"Los {len(pend['filas'])} repos `PENDING`. Se midió el estado real de cada uno "
  "**sin escribir nada en los repos** (sin `fetch`): el SHA de la rama remota se "
  "obtuvo con `git ls-remote` y se comparó con el `HEAD` local.")
w("")
w("### 5.1 Resultado principal: no hay commits sin pushear")
w("")
w(f"| Estado de push | Repos |")
w("|---|---:|")
for k, v in pend["estado_push"].items():
    w(f"| {k} | {v} |")
w("")
w("**En los 42 repos el SHA remoto de la rama coincide exactamente con el `HEAD` "
  "local.** Es decir: no hay ningún commit pendiente de subir. Todo lo que queda "
  "pendiente está en el **árbol de trabajo**, no en la historia.")
w("")
w("> **Corrección de un dato del estado inicial.** `estado.json` registra "
  "`unpushed = -1` (indeterminado) en 20 de estos 42 repos. Se comprobó la causa: "
  "en los 42 casos el valor −1 coincide exactamente con **no tener rama upstream "
  "configurada**, de modo que `git rev-list @{u}..HEAD` falla. Es un artefacto de "
  "medición, no trabajo sin publicar. Comprobado: 42 coincidencias, 0 discrepancias.")
w("")

w("### 5.2 Agrupación por causa")
w("")
w("| Causa | Repos | Qué hacer |")
w("|---|---:|---|")
w(f'| **Árbol sucio + archivos sin trackear** | {len(grupos["SUCIO+UNTRACKED"])} | Revisar y commitear o descartar |')
w(f'| **Solo árbol sucio** (sin untracked) | {len(grupos["SOLO_SUCIO"])} | `git checkout` / commitear |')
w(f'| **Solo archivos sin trackear** | {len(grupos["SOLO_UNTRACKED"])} | Decidir si añadir a `.gitignore` o trackear |')
w(f'| **Limpio y al día** (sin causa pendiente) | {len(grupos["LIMPIO_Y_AL_DIA"])} | Ninguna acción |')
w("")

for titulo, clave, extra in [
    ("5.2.1 Árbol sucio + archivos sin trackear", "SUCIO+UNTRACKED", True),
    ("5.2.2 Solo árbol sucio", "SOLO_SUCIO", True),
    ("5.2.3 Solo archivos sin trackear", "SOLO_UNTRACKED", True),
    ("5.2.4 Limpio y al día (el veredicto `PENDING` no tiene causa real)", "LIMPIO_Y_AL_DIA", False),
]:
    w(f"**{titulo} — {len(grupos[clave])} repos**")
    w("")
    por = {f["name"]: f for f in pend["filas"]}
    if extra:
        w("| Repo | Cambios trackeados | Sin trackear | Commits |")
        w("|---|---:|---:|---:|")
        for n in sorted(grupos[clave]):
            f = por[n]
            w(f'| `{n}` | {f["n_dirty"]} | {f["n_untracked"]} | {f["n_commits"]} |')
    else:
        for n in sorted(grupos[clave]):
            w(f"- `{n}`")
    w("")

w("### 5.3 Contenido exacto de los archivos sin trackear")
w("")
w("| Repo | Archivos sin trackear |")
w("|---|---|")
for f in pend["filas"]:
    if f["n_untracked"]:
        vals = ", ".join(f"`{u}`" for u in f["untracked_muestras"])
        w(f'| `{f["name"]}` | {vals}{" …" if f["n_untracked"] > len(f["untracked_muestras"]) else ""} |')
w("")
w("Patrón claro: casi todos los archivos sin trackear son **artefactos de build o "
  "lockfiles** (`package-lock.json`, `dist/`, `logs/`, `.pnpm-approved-builds.json`). "
  "La acción correcta es **añadirlos a `.gitignore`**, no commitearlos.")
w("")

# ---------------- 6. integridad ----------------
w("## 6. Integridad de git en los 264 repos")
w("")
w("| Diagnóstico | Repos |")
w("|---|---:|")
for k, v in integ["resumen"].items():
    w(f"| {k} | {v} |")
w("")
w("| Repo | Diagnóstico | Tamaño | Veredicto | Ruta |")
w("|---|---|---:|---|---|")
for f in integ["filas"]:
    if f["diag"] != "OK":
        w(f'| `{f["name"]}` | {f["diag"]} | {f["size_mb"]:,.1f} MB | `{f["verdict"]}` | `{f["path"]}` |')
w("")
w("Detalle del caso grave: en `BELENTANI-OS_2` el directorio `.git` existe pero "
  "está **completamente vacío**. El `git` no lo reconoce como repositorio. Los "
  "383,1 MB de contenido (entre ellos `06_ARCHIVO/brain.db`, 181,6 MB) **no están "
  "versionados ni tienen remoto**. En `BELENTANI-BRAIN`, `MiSaaS` y `PORTFOLIO` el "
  "`.git` está incompleto (7 entradas, sin `HEAD` ni `config`); su contenido es "
  "despreciable (<0,1 MB cada uno).")
w("")

# ---------------- 7. verificaciones ----------------
w("## 7. Verificaciones y limitaciones")
w("")
w("Todo lo siguiente se comprobó explícitamente durante la auditoría:")
w("")
w("- **Coincidencia exacta del análisis DIVERGED.** Se recalculó `ahead`/`behind` "
  "de los 123 repos DIVERGED por un camino independiente y el resultado fue "
  "idéntico: 6 por delante, 104 por detrás, 13 en ambos, 0 sin clasificar.")
w("- **Los 404 de GitHub son reales.** `git ls-remote` y la API REST devolvieron "
  "404 para los 8 remotos con propietario propio que git reporta como «not "
  "found» (los 4 de §3.1 —`william-game` comparte remoto con su copia en "
  "cuarentena— más los 4 nombres anidados `omega-os`, `omega-os-v4`, "
  "`judas-red-front` y `desktop`/`engine`), mientras que dos repos de control del "
  "mismo propietario devolvieron HTTP 200 con el mismo token. Por tanto no es un "
  "problema de credenciales ni de permisos.")
w("- **Las credenciales de git funcionan.** `ls-remote` respondió correctamente "
  "tanto en repos públicos como **privados** del inventario, lo que descarta que "
  "los fallos de acceso expliquen los resultados anteriores.")
w("- **Los 42 PENDING están al día en push.** El SHA remoto (`ls-remote`) coincide "
  "con el HEAD local en los 42; se verificó además a mano en 5 repos.")
w("- **`UNREACHABLE` es un falso positivo.** `deepseek-harness` responde a "
  "`git ls-remote` (rama remota por defecto `master`, SHA `ddefc45f`). El clon "
  "local tiene un *refspec* de fetch anómalo — solo `refs/tags/dsh-v0.1.1-rc.2` — "
  "en lugar del estándar `+refs/heads/*:refs/remotes/origin/*`; por eso no existen "
  "refs `origin/*` y el script original lo marcó como inalcanzable. Su HEAD local "
  "(`b150a55`) **es** el tag remoto `dsh-v0.1.1-rc.2`, y la rama remota por defecto "
  "es `master`, no `main`.")
w("- **81 de los 264 repos tienen un `refspec` de fetch no estándar**: 49 "
  "restringidos a una sola rama (`+refs/heads/<rama>:...`), 31 **sin ningún "
  "`refspec`** y 1 solo de tags (`deepseek-harness`). Son clones "
  "`--single-branch` o con configuración recortada. Esto es la causa raíz de "
  "buena parte de los valores `-1` y de los falsos `UNREACHABLE` del estado "
  "inicial.")
w("")
w("**Lo que NO se pudo comprobar:**")
w("")
w("- **No se determinó si los commits locales por delante están ya en alguna otra "
  "rama remota** más allá de la rama por defecto. Se comparó contra la rama "
  "configurada/por defecto (`origin/main`, `origin/master` o la rama del repo).")
w("- **No se verificó el contenido de los 383 MB de `BELENTANI-OS_2`** más allá de "
  "listar tamaños y los archivos mayores: sin `.git` no hay historia que auditar.")
w("- **No se consultó si los 456 repos del inventario están todos accesibles**: "
  "se probaron 10 (6 privados, 4 públicos) como muestra de control, no los 456.")
w("- **`REMOTE_MISSING` (6 repos) y varios `NO_REMOTE` son subcarpetas anidadas** "
  "de otros repos. En concreto, de los 6 `REMOTE_MISSING`, 5 son subcarpetas "
  "anidadas (`omega-os`, `omega-os-v4`, `judas-red-front`, `desktop`, `engine`) "
  "y solo `2-icons-backup-export` es un repositorio con entidad propia "
  "(listado en §3.1). Los 6 no se detallan en §6 porque su git está íntegro: el "
  "problema es únicamente que el remoto devuelve 404.")
w("")

# ---------------- 8. recomendaciones ----------------
w("## 8. Recomendaciones, ordenadas por impacto")
w("")
w("### Prioridad 1 — detener la pérdida de datos")
w("")
w("1. **`BELENTANI-OS_2` (383,1 MB).** El `.git` está vacío: ese contenido no está "
  "versionado en ninguna parte. Antes de cualquier otra cosa, verificar si existe "
  "una copia en otro disco o backup; después, `git init` + commit + `git remote add` "
  "y publicar como **repositorio privado**. Es el único elemento del inventario "
  "donde un fallo de disco significaría pérdida total e irreversible.")
w("2. **Decidir el destino de `06_ARCHIVO/brain.db` (181,6 MB).** Una base de datos "
  "de ese tamaño no debería entrar en git. Conviene publicarla como release asset, "
  "en almacenamiento aparte, o cifrada; el repositorio debe llevar solo el código y "
  "la documentación.")
w("3. **Publicar los 4 repos propios cuyo remoto devuelve 404** "
  "(`2-icons-backup-export` —que aún tiene 9 cambios sin commitear—, `edu-engine`, "
  "`william-game` y su copia en cuarentena). El remoto configurado apunta a un "
  "repositorio que ya no existe; hay que crear el repositorio y volver a enlazarlo.")
w("")
w("### Prioridad 2 — publicar el trabajo que ya está commiteado")
w("")
w("4. **Pushear los 6 repos `DIVERGED` por delante** (≈211 MB, 11 commits en total). "
  "Son los únicos repos donde existe trabajo commiteado que no está en el remoto: "
  "`manus-ai-skill-pack` (+4), `belentani-v2` (+2), `securetea` (+2), `agentbox` (+1), "
  "`nexus-data` (+1), `voice-ai-agency` (+1).")
w("5. **Resolver primero el detached HEAD de `agentbox` y `nexus-data`.** Están en "
  "HEAD desacoplado: hay que crear la rama (`git switch -c main`) o pushear "
  "explícitamente (`git push origin HEAD:main`), o el push no publicará nada.")
w("6. **Publicar los 9 repos sin remoto** que sí tienen commits: "
  "`judas-experience-expanded` (8 commits, 23,4 MB), `3-workspace` (5 commits, "
  "13,7 MB), `saas-plasma_2` (9 commits), `letra-office` (4 commits), "
  "`belentani-cv-work` (6 archivos sin commitear), `frontend` y `server` "
  "(2 commits cada uno), `aurea3d-premium` (1 commit).")
w("")
w("### Prioridad 3 — limpiar el árbol de trabajo (los 42 PENDING)")
w("")
w("7. **Añadir a `.gitignore` los artefactos de build.** Los archivos sin trackear "
  "son casi todos lockfiles y salidas de build (`package-lock.json`, `dist/`, "
  "`logs/`, `.pnpm-approved-builds.json`). Es un cambio de una línea por repo y "
  "elimina la causa en 7 repos.")
w("8. **Revisar los 19 repos con árbol sucio, empezando por los grandes.** "
  "`03-aion-enterprise-multiagente-saas-wfm` (63 cambios), `pedalboard` (55), "
  "`SongGeneration` (51), "
  "`Retrieval-based-Voice-Conversion-WebUI` (49) y `SongGeneration-Studio` (35) "
  "concentran la mayor parte. **Ojo:** en varios de ellos los cambios son "
  "**borrados** (`D`) de binarios y assets pesados (`__pycache__`, `.wav`, `.mp3`, "
  "`.png`), es decir, limpiezas locales que probablemente conviene **descartar** "
  "(`git checkout -- .`) en lugar de commitear.")
w("9. **Descartar el veredicto `PENDING` en 18 repos.** Están limpios y al día: el "
  "veredicto no tiene causa real. Conviene reclasificarlos a `SAFE_TO_DELETE` / "
  "`KEEP` para que el estado refleje la realidad.")
w("")
w("### Prioridad 4 — saneamiento de la configuración")
w("")
w("10. **Normalizar el `refspec` de fetch en 81 repos.** Restaurar "
  "`+refs/heads/*:refs/remotes/origin/*` y configurar el upstream "
  "(`git branch --set-upstream-to`). Esto elimina de raíz los `unpushed = -1`, los "
  "falsos `UNREACHABLE` y permite que las mediciones futuras sean automáticas.")
w("11. **Corregir el veredicto de `deepseek-harness`** de `UNREACHABLE` a algo como "
  "`THIRD_PARTY_CLONE` o `DETACHED`: es un clon de un repo de terceros situado en "
  "un tag, no un repositorio inalcanzable.")
w("12. **Recuperar espacio con los 104 repos solo-por-detrás.** Como el remoto "
  "contiene todo el trabajo local, son los candidatos seguros a borrado local: "
  "3.800,9 MB. Los mayores: `BELENTANI-OS` (1.202,3 MB), "
  "`natively-cluely-ai-assistant` (818,8 MB), `paperclip` (490,7 MB), "
  "`omarchy` (309,6 MB). **Antes de borrar cualquiera, confirmar que su rama "
  "remota existe** (los 6 por delante de §4.1 tienen prioridad y no deben tocarse).")
w("13. **Reparar o retirar los `.git` corruptos** (`BELENTANI-BRAIN`, `MiSaaS`, "
  "`PORTFOLIO`): reinicializarlos o eliminarlos. Ocupan poco, pero ensucian el "
  "inventario y ya han producido falsos positivos en el cruce por nombre.")
w("")
w("**Regla de seguridad sugerida:** los 6 por delante y los 13 en ambos lados no "
  "deben borrarse bajo ningún concepto hasta que su publicación esté confirmada.")
w("")

# ---------------- 9. anexo ----------------
w("## 9. Anexo — artefactos generados")
w("")
w("Todos en `C:\\Users\\USER\\Desktop\\produccion\\`:")
w("")
w("| Archivo | Contenido |")
w("|---|---|")
w("| `INFORME-REPOS.md` | Este informe |")
w("| `diverged-analisis.json` | Clasificación de los 123 DIVERGED |")
w("| `auditoria-cruce.json` | Cruce local↔GitHub y medición de los 42 PENDING |")
w("| `faltan-publicar.json` | Propios sin publicar / sin remoto / clones de terceros |")
w("| `pending-exacto.json` | Estado de push real de los 42 PENDING |")
w("| `pending-grupos.json` | Agrupación de los PENDING por causa |")
w("| `pending-diagnostico.json` | Diagnóstico intermedio de los PENDING |")
w("| `integridad-git.json` | Integridad de git de los 264 repos |")
w("")
w("Scripts usados, en `C:\\Users\\USER\\Desktop\\tools\\`: `auditoria-cruce.py`, "
  "`verificar-faltantes.py`, `api-check-ausentes.py`, `clasificar-publicar.py`, "
  "`diagnosticar-pending.py`, `pending-exacto.py`, `verificar-diverged.py`, "
  "`detalle-final.py`, `scan-integridad.py`, `generar-informe.py`.")
w("")

OUT.write_text("\n".join(L), encoding="utf-8")
print(f"Informe escrito: {OUT}")
print(f"Lineas: {len(L)}  Bytes: {OUT.stat().st_size:,}")
