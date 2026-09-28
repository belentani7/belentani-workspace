# belentani-workspace

Espacio de trabajo de Pedro Belentani (`belentani7`). Repositorio **privado**.

Aquí vive configuración de editor, automatización de GitHub y scripts de
mantenimiento del equipo. **No** contiene código de aplicación, ni documentos
personales, ni PDFs ni claves: cada proyecto tiene su propio repositorio.

## 📦 Contenido

39 ficheros versionados, agrupados:

| Grupo | Ficheros | Qué es |
|---|---|---|
| Documentación | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `PRODUCTION_CHECKLIST.md`, `PROTOCOLO-SDD-MAESTRO.md`, `PROTOCOLO_COMPLETO_BELENTANI_VISUAL_ENGINE.md` | Guías, protocolo E0–E6 y criterios de publicación |
| Auditoría CI | `.github/workflows/ci.yml`, `.github/pull_request_template.md` | Higiene automática en push y PR (secretos, JSON, HTML) |
| Informes 2026-09 | `INFORME_belentani7_2026-09-28.md`, `REPORTE-LIMPIEZA-REPOS-2026-09-28.md`, `REPORTE_ESCRITORIO_2026-09-28.md`, `REPORTE-SUBIDA-REPOS-DESKTOP-2026-09-28.md` | Auditoría de repos, limpieza, estado del Escritorio y esta subida |
| Mantenimiento Windows | `WinPurge.ps1`, `PurgaDefinitivaCLIs.ps1`, `Purgar-TodoCache.ps1`, `Buscar-Duplicados.ps1`, `fix-keyboard-p30.ps1`, `test-teclado.ps1`, `mantenimiento.bat`, `Reset-OpenCode.bat` | Limpieza y ajustes del equipo |
| Asistentes locales | `Agente de voz.cmd`, `JARVIS.cmd`, `START-AUTONOMIA.ps1` | Lanzadores de voz/asistentes |
| Qwen local (offline) | `download-qwen-zip.ps1`, `download-qwen-zip.sh`, `download_qwen2.py`, `qwen2_local_runner.py`, `run_qwen2.bat`, `install_offline.ps1` | Descarga y ejecución de Qwen2 en local |
| Editor | `.editorconfig`, `.vscode/` (7 ficheros) | Formato y tareas por lenguaje |
| Base | `.gitignore`, `.freebuff/project-id` | Exclusiones de seguridad y metadato Freebuff |

## 🚀 Clonar

```bash
git clone https://github.com/belentani7/belentani-workspace.git
```

## 🛡️ Auditoría en CI

`.github/workflows/ci.yml` se ejecuta en cada push a `main` y en cada PR:

- **Bloqueante** — ningún fichero de credenciales trackeado (`.env`, `.pem`,
  `.p12`, `.pfx`, `id_rsa`, `id_ed25519`, `.keystore`, `.npmrc`, `.netrc`).
- **Bloqueante** — ningún patrón de credenciales en el contenido
  (claves de OpenAI, Google, AWS, Anthropic, Slack, claves PEM, tokens de GitHub).
- **Informativo** — JSON válido y HTML con `<title>` y meta description.

## 🧭 Protocolo

Este repo sigue **protocolo-etapas (E0-E6)** — SDD para agentes:

1. **E0 Intake** → Entender
2. **E1 Spec** → Qué es "terminado"
3. **E2 Plan** → Tareas + dependencias
4. **E3 Build** → Ejecutar + verificar local
5. **E4 Verify** → Evidencia real (no promesas)
6. **E5 Ship** → Commit + Push + URL verificada
7. **E6 Learn** → Memoria + cerrar sesión

## 🌍 Idiomas

Orden fijo: **PT > ES > EN > CA** — `["pt","es","en","ca"]`

---

*Actualizado 2026-09-28 · protocolo-etapas E5 Ship*
