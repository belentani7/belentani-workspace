# cli-db-guard.ps1 — Keep CLI coder databases under 400 MB
# Deletes oversized DBs/caches; tools recreate them on next launch.

$maxMB = 400
$logFile = "$env:USERPROFILE\Documents\cli-db-guard.log"

function Log($msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm') | $msg"
    Write-Host $line
    Add-Content $logFile $line
}

function Get-SizeMB($path) {
    if (-not (Test-Path $path)) { return 0 }
    $item = Get-Item $path -Force -ErrorAction SilentlyContinue
    if ($item.PSIsContainer) {
        return [math]::Round((Get-ChildItem $path -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB, 2)
    }
    $total = $item.Length
    # include WAL/SHM sidecars
    $wal = "$path-wal"; $shm = "$path-shm"
    if (Test-Path $wal) { $total += (Get-Item $wal -Force).Length }
    if (Test-Path $shm) { $total += (Get-Item $shm -Force).Length }
    return [math]::Round($total / 1MB, 2)
}

function Prune($label, $path, $isDir = $false) {
    $size = Get-SizeMB $path
    if ($size -le $maxMB) {
        Log "$label : ${size} MB — OK"
        return
    }
    Log "$label : ${size} MB — OVER ${maxMB} MB, pruning..."
    if ($isDir) {
        Remove-Item "$path\*" -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        Remove-Item $path -Force -ErrorAction SilentlyContinue
        Remove-Item "$path-wal" -Force -ErrorAction SilentlyContinue
        Remove-Item "$path-shm" -Force -ErrorAction SilentlyContinue
    }
    Log "$label : pruned successfully"
}

Log "=== cli-db-guard run started ==="

# OpenCode — SQLite session DB
Prune "OpenCode DB" "$env:USERPROFILE\.local\share\opencode\opencode.db"

# Kilo Code — SQLite session DB
Prune "Kilo DB" "$env:USERPROFILE\.local\share\kilo\kilo.db"

# Claude Code — vm_bundles sandbox
Prune "Claude vm_bundles" "$env:APPDATA\Claude\vm_bundles" $true

# Claude Code — caches
Prune "Claude Cache" "$env:APPDATA\Claude\Cache" $true
Prune "Claude Code Cache" "$env:APPDATA\Claude\Code Cache" $true
Prune "Claude Session Storage" "$env:APPDATA\Claude\Session Storage" $true

# OpenClaw — npm cache and workspace
Prune "OpenClaw npm cache" "$env:USERPROFILE\.openclaw\npm" $true
Prune "OpenClaw workspace" "$env:USERPROFILE\.openclaw\workspace" $true

# Aider — chat history (append-only, trim if huge)
$aiderHistory = "$env:USERPROFILE\.aider.chat.history.md"
$aiderSize = Get-SizeMB $aiderHistory
if ($aiderSize -gt $maxMB) {
    Log "Aider history : ${aiderSize} MB — truncating to last 500 lines"
    $lines = Get-Content $aiderHistory -Tail 500
    Set-Content $aiderHistory ($lines -join "`n")
    Log "Aider history : truncated"
}

# Temp + pip cache (always clean)
Remove-Item "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue

Log "=== cli-db-guard run finished ==="
