"""beltoolkit - toolkit unificado Belentani (dsh 2026-09-20).

Subcomandos: audit | verify | deploy | ram | secrets | organize | gcheck
Reglas: stdlib + httpx; tokens SOLO por env; salidas enmascaradas; nada borra.
"""
import argparse, base64, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

try:
    import httpx
except ImportError:
    httpx = None

NL = chr(10)
DESK = Path("C:/Users/USER/Desktop")
HARNESS = DESK / "claude" / "deepseek-harness"
TEAM = "team_PW8qfFcgLWackpqpCQfifest"
GH_API = "https://api.github.com"
VC_API = "https://api.vercel.com"
SECRET_RE = re.compile(r"(ghp_[A-Za-z0-9]{10,}|gho_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9_]{10,}|sk-[A-Za-z0-9_-]{12,}|nvapi-[A-Za-z0-9_-]{12,}|gsk_[A-Za-z0-9]{12,}|vca_[A-Za-z0-9]{12,}|cfoat_[A-Za-z0-9_.-]{12,}|hf_[A-Za-z0-9]{12,}|AIza[A-Za-z0-9_-]{20,})")


def mask(text: str) -> str:
    """Enmascara cualquier secreto detectable en un texto."""
    return SECRET_RE.sub(lambda m: m.group(1)[:6] + "..." + m.group(1)[-4:], text)


def gh_headers() -> dict:
    """Cabeceras GitHub desde entorno."""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
    return {"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json", "User-Agent": "beltoolkit"}


def vc_headers() -> dict:
    """Cabeceras Vercel desde entorno."""
    return {"Authorization": "Bearer " + os.environ.get("VERCEL_TOKEN", "")}


def cmd_audit(args) -> int:
    """Digest de los JSON de auditoria mas recientes."""
    found = []
    for base in [Path("C:/Users/USER/Downloads"), DESK / "claude"]:
        if base.exists():
            for f in base.glob("*audit*.json"):
                found.append(f)
            for f in base.glob("GitHub_Perfil_*.json"):
                found.append(f)
    for f in found[: args.limit]:
        try:
            data = json.loads(f.read_text(encoding="utf-8-sig", errors="replace"))
            keys = list(data.keys())[:12] if isinstance(data, dict) else ["list", len(data)]
            print(str(f.name) + " -> " + str(keys))
        except Exception as exc:
            print(str(f.name) + " ERR " + str(exc)[:80])
    return 0


def cmd_verify(args) -> int:
    """Verifica licencias, SECURITY y repos privados en GitHub."""
    if httpx is None:
        print("httpx missing")
        return 2
    lic = ["belentani7", "belentani-the-judas-experience", "belent-cad", "arte-que-veste"]
    sec = ["agentbox", "open-school", "ManosAbiertas", "ux-academy-professional-program", "secure-t"]
    for repo in lic:
        r = httpx.get(GH_API + "/repos/belentani7/" + repo + "/license", headers=gh_headers(), timeout=30)
        print("license " + repo + ": " + ("OK" if r.status_code == 200 else "FALTA"))
    for repo in sec:
        r = httpx.get(GH_API + "/repos/belentani7/" + repo + "/contents/SECURITY.md", headers=gh_headers(), timeout=30)
        print("security " + repo + ": " + ("OK" if r.status_code == 200 else "FALTA"))
    return 0


def cmd_deploy(args) -> int:
    """Estado de despliegues por proyecto y (opcional) relanzamiento."""
    if httpx is None:
        print("httpx missing")
        return 2
    projects = httpx.get(VC_API + "/v9/projects?teamId=" + TEAM + "&limit=100", headers=vc_headers(), timeout=60).json()
    pmap = {p["name"]: p for p in projects.get("projects", [])}
    targets = args.projects.split(",") if args.projects else list(pmap)[:10]
    for name in targets:
        p = pmap.get(name)
        if not p:
            print(name + ": NO_PROJECT")
            continue
        info = httpx.get(VC_API + "/v9/projects/" + p["id"] + "?teamId=" + TEAM, headers=vc_headers(), timeout=60).json()
        paused = info.get("paused")
        deps = httpx.get(VC_API + "/v6/deployments?projectId=" + p["id"] + "&teamId=" + TEAM + "&limit=1",
                         headers=vc_headers(), timeout=60).json().get("deployments", [])
        state = deps[0].get("readyState") if deps else "none"
        print(name + ": paused=" + str(paused) + " state=" + str(state))
        if args.relaunch and paused:
            rr = httpx.post(VC_API + "/v1/projects/" + p["id"] + "/unpause?teamId=" + TEAM, headers=vc_headers(), timeout=60)
            print("  unpause " + str(rr.status_code))
    return 0


def cmd_ram(args) -> int:
    """Snapshot de RAM y top procesos (Windows via CIM)."""
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          "(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    free_kb = out.stdout.strip()
    print("RAM libre (KB): " + free_kb)
    tops = subprocess.run(["powershell", "-NoProfile", "-Command",
                           "Get-Process | Sort-Object WS -Descending | Select-Object -First 8 | ForEach-Object { $_.ProcessName + ' ' + [math]::Round($_.WS/1MB) }"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(tops.stdout.strip())
    return 0


def cmd_secrets(args) -> int:
    """Escaneo enmascarado de secretos en una ruta."""
    root = Path(args.path)
    hits = 0
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix.lower() in {".exe", ".dll", ".png", ".jpg", ".zip", ".mp4", ".woff", ".woff2"}:
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in SECRET_RE.finditer(text):
            line = text[: m.start()].count(NL) + 1
            print(mask(str(f)) + ":" + str(line) + " " + m.group(1)[:6] + "...")
            hits += 1
            if hits >= args.limit:
                print("limit reached")
                return 0
    print("secrets encontrados: " + str(hits))
    return 0


def cmd_organize(args) -> int:
    """Mueve archivos sueltos de raiz/Desktop a subcarpetas (dry-run por defecto)."""
    plan = []
    root = Path("C:/Users/USER")
    system_files = {"NTUSER.DAT", "NTUSER.DAT.LOG1", "NTUSER.DAT.LOG2", "ntuser.ini", "Desktop.ini"}
    for f in root.iterdir():
        if f.is_file() and not f.name.startswith(".") and f.name not in system_files:
            plan.append((f, root / "Downloads" / "_organizado-raiz" / classify(f.name)))
    desk = DESK
    for f in desk.iterdir():
        if f.is_file() and not f.name.startswith(".") and f.name not in system_files:
            plan.append((f, desk / "_ORDENADO" / classify(f.name)))
    for src, dst in plan:
        print(("MOVE " if args.apply else "DRY  ") + str(src) + " -> " + str(dst))
        if args.apply:
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                src.replace(dst)
            except PermissionError as e:
                print("  SKIP (locked): " + str(e)[:80])
    return 0


def classify(name: str) -> str:
    """Clasifica por extension a subcarpeta."""
    ext = Path(name).suffix.lower()
    if ext in {".py", ".ps1", ".sh", ".js", ".ts"}: return "scripts"
    if ext in {".md", ".txt", ".pdf", ".docx", ".json", ".csv"}: return "docs"
    if ext in {".png", ".jpg", ".jpeg", ".svg", ".webp", ".mp4", ".mp3", ".wav"}: return "media"
    if ext in {".zip", ".7z", ".tar", ".gz", ".rar"}: return "archivos-grandes"
    if ext in {".env", ".cfg", ".ini", ".yml", ".yaml", ".toml"}: return "config"
    return "misc"


def cmd_gcheck(args) -> int:
    """Estado de gcloud/gws/thing/autoclaw."""
    for label, cmd in [("gcloud", "gcloud auth list --filter='status:ACTIVE' --format='value(account)'"),
                       ("thing", "thing whoami"),
                       ("autoclaw", "Get-Process AutoClaw -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count")]:
        out = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        print(label + ": " + (out.stdout.strip() or out.stderr.strip())[:120])
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de subcomandos."""
    p = argparse.ArgumentParser(prog="toolkit", description="beltoolkit unificado")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit"); a.add_argument("--limit", type=int, default=8); a.set_defaults(fn=cmd_audit)
    v = sub.add_parser("verify"); v.set_defaults(fn=cmd_verify)
    d = sub.add_parser("deploy"); d.add_argument("--projects", default=""); d.add_argument("--relaunch", action="store_true"); d.set_defaults(fn=cmd_deploy)
    r = sub.add_parser("ram"); r.set_defaults(fn=cmd_ram)
    s = sub.add_parser("secrets"); s.add_argument("--path", required=True); s.add_argument("--limit", type=int, default=20); s.set_defaults(fn=cmd_secrets)
    o = sub.add_parser("organize"); o.add_argument("--apply", action="store_true"); o.set_defaults(fn=cmd_organize)
    g = sub.add_parser("gcheck"); g.set_defaults(fn=cmd_gcheck)
    return p


def main() -> int:
    """Punto de entrada."""
    args = build_parser().parse_args()
    return int(args.fn(args))


if __name__ == "__main__":
    sys.exit(main())
