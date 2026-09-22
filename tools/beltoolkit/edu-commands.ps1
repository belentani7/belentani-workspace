# edu-commands.ps1 — PowerShell cheatsheet for 8 educational repos
# Usage: . .\edu-commands.ps1  (dot-source to load functions)

$EDU_REPOS = @(
    "aprende-brasil",
    "lingua-aberta",
    "linguaforge",
    "WILLIAMSCHOOL",
    "open-school",
    "manus-ai-skill-pack",
    "secure-t-university",
    "ux-academy-professional-program"
)
$REPOS_BASE = "C:\Users\USER\repos"

function Edu-Status {
    foreach ($r in $EDU_REPOS) {
        $p = "$REPOS_BASE\$r"
        if (!(Test-Path "$p\.git")) { Write-Host "  - $r NOT FOUND"; continue }
        Push-Location $p
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        $dirty = (git status --porcelain 2>$null | Measure-Object).Count
        $hash = git rev-parse --short HEAD 2>$null
        $mark = if ($dirty -eq 0) { "+" } else { "!" }
        Write-Host "  $mark $($r.PadRight(40)) $($branch.PadRight(10)) dirty=$dirty $hash"
        Pop-Location
    }
}

function Edu-Redeploy {
    param([string]$Repo = "ALL")
    $targets = if ($Repo -eq "ALL") { $EDU_REPOS } else { @($Repo) }
    foreach ($r in $targets) {
        $p = "$REPOS_BASE\$r"
        if (!(Test-Path "$p\.git")) { Write-Host "  SKIP $r"; continue }
        Push-Location $p
        git commit --allow-empty -m "chore: trigger Vercel redeploy"
        git push origin (git rev-parse --abbrev-ref HEAD)
        Write-Host "  OK $r"
        Pop-Location
    }
}

function Edu-Verify {
    $urls = @{
        "aprende-brasil" = "https://aprende-brasil.vercel.app"
        "lingua-aberta" = "https://lingua-aberta.vercel.app"
        "linguaforge" = "https://linguaforge.vercel.app"
        "WILLIAMSCHOOL" = "https://williamschool.vercel.app"
        "open-school" = "https://open-school-gamma.vercel.app"
        "manus-ai-skill-pack" = "https://manus-ai-skill-pack.vercel.app"
        "secure-t-university" = "https://secure-t-university.vercel.app"
        "ux-academy-professional-program" = "https://ux-academy-professional.vercel.app"
    }
    foreach ($r in $urls.Keys) {
        try {
            $resp = Invoke-WebRequest -Uri $urls[$r] -TimeoutSec 15 -UseBasicParsing -ErrorAction Stop
            Write-Host "  $($r.PadRight(40)) $($resp.StatusCode)"
        } catch {
            Write-Host "  $($r.PadRight(40)) ERR $($_.Exception.Message)"
        }
    }
}

function Edu-Aider {
    param(
        [Parameter(Mandatory)][string]$Repo,
        [Parameter(Mandatory)][string]$Message
    )
    $p = "$REPOS_BASE\$Repo"
    if (!(Test-Path "$p\.git")) { Write-Host "Repo not found: $Repo"; return }
    Push-Location $p
    aider --model deepseek/deepseek-v4-flash --no-auto-commits --message $Message
    Pop-Location
}

function Edu-Build {
    param([string]$Repo = "ALL")
    $targets = if ($Repo -eq "ALL") { $EDU_REPOS } else { @($Repo) }
    foreach ($r in $targets) {
        $p = "$REPOS_BASE\$r"
        if (!(Test-Path "$p\package.json")) { Write-Host "  SKIP $r (no package.json)"; continue }
        Push-Location $p
        Write-Host "  Building $r..."
        npm run build 2>&1 | Select-Object -Last 5
        Pop-Location
    }
}

Write-Host "Edu commands loaded: Edu-Status, Edu-Redeploy, Edu-Verify, Edu-Aider, Edu-Build"
