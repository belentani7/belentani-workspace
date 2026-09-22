#!/usr/bin/env python3
"""
Extrae API keys del entorno PowerShell y configura VS Code / Continue.
No imprime claves. Usa dry-run por defecto.
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple
import argparse


KEY_MAP = {
    "anthropic": "ANTHROPIC_API_KEY",
    "opencode": "OPENCODE_API_KEY",
    "openzen": "OPENZEN_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
}


def get_ps_env(var: str) -> Optional[str]:
    """Lee variable de entorno desde PowerShell (incluye perfil de usuario)."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", f"[Environment]::GetEnvironmentVariable('{var}', 'User')"],
            capture_output=True, text=True, timeout=10
        )
        val = result.stdout.strip()
        if val:
            return val
        # Fallback: variable de proceso actual
        return os.environ.get(var)
    except Exception:
        return os.environ.get(var)


def extract_keys() -> Dict[str, Optional[str]]:
    found = {}
    for name, env_var in KEY_MAP.items():
        val = get_ps_env(env_var)
        found[name] = val
        status = "OK" if val else "MISSING"
        print(f"  [{status}] {name.upper()} ({env_var})")
    return found


def ensure_vscode_dirs() -> Tuple[Path, Path]:
    """Directorios de configuración VS Code (user y workspace)."""
    user_config = Path(os.environ.get("APPDATA", "")) / "Code" / "User"
    # Workspace = directorio actual si no es System32, sino home del usuario
    cwd = Path.cwd()
    if "system32" in str(cwd).lower() or "windows" in str(cwd).lower():
        workspace_config = Path.home() / "vscode-workspace"
    else:
        workspace_config = cwd / ".vscode"
    user_config.mkdir(parents=True, exist_ok=True)
    workspace_config.mkdir(parents=True, exist_ok=True)
    return user_config, workspace_config


def write_continue_config_yaml(keys: Dict[str, str], config_path: Path, dry_run: bool = True) -> bool:
    """Escribe config.yaml moderno para Continue (model providers)."""
    # Ensure parent directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_content = f"""# Continue config - generado automáticamente
# No commitear este archivo si contiene claves reales

version: 2

models:
  - name: "anthropic-claude"
    provider: "anthropic"
    model: "claude-3-5-sonnet-20241022"
    apiKey: "{keys.get('anthropic', '')}"
    roles:
      - chat
      - edit
      - autocomplete

  - name: "deepseek-chat"
    provider: "deepseek"
    model: "deepseek-chat"
    apiKey: "{keys.get('deepseek', '')}"
    roles:
      - chat
      - edit

  - name: "opencode"
    provider: "openai"
    model: "gpt-4o"
    apiKey: "{keys.get('opencode', '')}"
    baseUrl: "https://api.opencode.ai/v1"
    roles:
      - chat
      - edit

  - name: "openzen"
    provider: "openai"
    model: "zen-model"
    apiKey: "{keys.get('openzen', '')}"
    baseUrl: "https://api.openzen.ai/v1"
    roles:
      - chat

# Modelo por defecto para chat
defaultModel: "anthropic-claude"

# Tab completion
tabAutocompleteModel:
  provider: "anthropic"
  model: "claude-3-5-haiku-20241022"
  apiKey: "{keys.get('anthropic', '')}"

# Context providers
contextProviders:
  - name: "codebase"
    params: {{}}
  - name: "docs"
    params: {{}}
  - name: "terminal"
    params: {{}}
  - name: "diff"
    params: {{}}
  - name: "open"
    params: {{}}
  - name: "problems"
    params: {{}}
  - name: "folder"
    params: {{}}
  - name: "code"
    params: {{}}

# Slash commands personalizados
slashCommands:
  - name: "explain"
    description: "Explicar código seleccionado"
    prompt: "Explica este código detalladamente:"
  - name: "test"
    description: "Generar tests"
    prompt: "Escribe tests comprehensivos para este código:"
  - name: "refactor"
    description: "Refactorizar"
    prompt: "Refactoriza este código para que sea más limpio y mantenible:"
  - name: "security"
    description: "Auditoría de seguridad"
    prompt: "Revisa este código por vulnerabilidades de seguridad:"

# Reglas del proyecto
rules:
  - "Usa TypeScript strict mode"
  - "No uses 'any' sin justificación"
  - "Tests antes que implementación (TDD)"
  - "No commitees secretos ni claves API"
  - "Dry-run antes de cambios destructivos"
"""

    if dry_run:
        print(f"\n[DRY-RUN] Se escribiría en: {config_path}")
        print("--- CONTENIDO (claves ocultas) ---")
        for line in yaml_content.split("\n"):
            if "apiKey:" in line and '""' not in line:
                print(line.replace(line.split('"')[1], "***" if '"' in line else ""))
            else:
                print(line)
        return True

    try:
        config_path.write_text(yaml_content, encoding="utf-8")
        print(f"[OK] Config escrito: {config_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Escribiendo config: {e}")
        return False


def write_env_file(keys: Dict[str, str], env_path: Path, dry_run: bool = True) -> bool:
    """Escribe .env para el workspace (no commitear)."""
    lines = ["# API Keys - NO COMMITEAR", ""]
    for name, env_var in KEY_MAP.items():
        val = keys.get(name)
        if val:
            lines.append(f"{env_var}={val}")
        else:
            lines.append(f"# {env_var}=  # No configurado")
    content = "\n".join(lines) + "\n"

    if dry_run:
        print(f"\n[DRY-RUN] .env se escribiría en: {env_path}")
        print("--- CONTENIDO (claves ocultas) ---")
        for line in content.split("\n"):
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                print(f"{k}=***")
            else:
                print(line)
        return True

    try:
        env_path.write_text(content, encoding="utf-8")
        print(f"[OK] .env escrito: {env_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Escribiendo .env: {e}")
        return False


def write_vscode_settings(keys: Dict[str, str], settings_path: Path, dry_run: bool = True) -> bool:
    """Actualiza settings.json de VS Code para Continue."""
    existing = {}
    if settings_path.exists():
        try:
            existing = json.loads(settings_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Config Continue en settings.json
    continue_config = {
        "continue.apiKey": keys.get("anthropic", ""),
        "continue.model": "claude-3-5-sonnet-20241022",
        "continue.enableTabAutocomplete": True,
    }

    merged = {**existing, **continue_config}

    if dry_run:
        print(f"\n[DRY-RUN] settings.json se actualizaría en: {settings_path}")
        print(json.dumps(continue_config, indent=2).replace(keys.get("anthropic", ""), "***"))
        return True

    try:
        settings_path.write_text(json.dumps(merged, indent=2), encoding="utf-8")
        print(f"[OK] settings.json actualizado: {settings_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Escribiendo settings.json: {e}")
        return False


def install_continue_extension(dry_run: bool = True) -> bool:
    """Instala la extensión Continue en VS Code."""
    if dry_run:
        print("\n[DRY-RUN] Instalaría extensión: Continue.continue")
        return True
    try:
        result = subprocess.run(
            ["code", "--install-extension", "Continue.continue", "--force"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            print("[OK] Extensión Continue instalada")
            return True
        else:
            print(f"[WARN] No se pudo instalar (¿VS Code en PATH?): {result.stderr}")
            return False
    except FileNotFoundError:
        print("[WARN] 'code' no encontrado en PATH. Instala manualmente: Continue.continue")
        return False
    except Exception as e:
        print(f"[ERROR] Instalando extensión: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Configura API keys para VS Code / Continue")
    parser.add_argument("--apply", action="store_true", help="Aplicar cambios (por defecto dry-run)")
    parser.add_argument("--workspace-only", action="store_true", help="Solo configurar workspace actual")
    parser.add_argument("--install-ext", action="store_true", help="Instalar extensión Continue")
    args = parser.parse_args()

    dry_run = not args.apply

    print("=" * 60)
    print("EXTRACIÓN DE API KEYS DESDE POWERSHELL")
    print("=" * 60)

    keys = extract_keys()
    configured = {k: v for k, v in keys.items() if v}
    missing = [k for k, v in keys.items() if not v]

    print(f"\nConfiguradas: {len(configured)} | Faltantes: {len(missing)}")
    if missing:
        print(f"Faltantes: {', '.join(m.upper() for m in missing)}")
        print("  Define en PowerShell: [Environment]::SetEnvironmentVariable('KEY', 'valor', 'User')")

    if not configured:
        print("\n[ERROR] No hay claves configuradas. Abortando.")
        return 1

    print("\n" + "=" * 60)
    print("CONFIGURANDO VS CODE / CONTINUE")
    print("=" * 60)

    user_config, workspace_config = ensure_vscode_dirs()
    target_config = workspace_config if args.workspace_only else user_config

    ok = True
    ok &= write_continue_config_yaml(configured, target_config / "continue" / "config.yaml", dry_run)
    ok &= write_env_file(configured, workspace_config / ".env", dry_run)
    ok &= write_vscode_settings(configured, target_config / "settings.json", dry_run)

    if args.install_ext:
        ok &= install_continue_extension(dry_run)

    print("\n" + "=" * 60)
    if dry_run:
        print("DRY-RUN COMPLETADO. Usa --apply para escribir cambios.")
    else:
        print("CONFIGURACIÓN APLICADA.")
        print(f"Reinicia VS Code para cargar la configuración.")
    print("=" * 60)

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())