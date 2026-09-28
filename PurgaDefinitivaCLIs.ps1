$ErrorActionPreference = 'SilentlyContinue'
$User = $env:USERPROFILE
$Targets = @(
    "$User\.claude\cache", "$User\.claude\sessions", "$User\.claude\projects", "$User\.claude\telemetry", "$User\.claude\tmp", "$User\.claude\backups", "$User\.claude\shell-snapshots", "$User\.claude\file-history", "$User\.claude\paste-cache", "$User\.claude\plugins",
    "$User\.opencode", "$User\AppData\Local\opencode", "$User\AppData\Roaming\opencode",
    "$User\.codex", "$User\AppData\Local\Codex", "$User\AppData\Roaming\Codex",
    "$User\.gemini", "$User\AppData\Local\gemini",
    "$User\.kilo", "$User\AppData\Local\kilo",
    "$User\Documents\AgentStorage\cache", "$User\Documents\AgentStorage\data\kilo\log", "$User\Documents\AgentStorage\data\kilo\storage\session_diff", "$User\Documents\AgentStorage\data\kilo\storage\session_share",
    "$User\Documents\AgentStorage\data\mimocode\log", "$User\Documents\AgentStorage\data\opencode\log", "$User\Documents\AgentStorage\data\opencode",
    "$User\AppData\Local\Temp\kilo*", "$User\AppData\Local\Temp\opencode*", "$User\AppData\Local\Temp\codex*", "$User\AppData\Local\Temp\claude*", "$User\AppData\Local\Temp\gemini*", "$User\AppData\Local\Temp\node_modules", "$User\AppData\Local\Temp\.next", "$User\AppData\Local\Temp\.turbo",
    "$User\AppData\Local\npm-cache", "$User\AppData\Local\pip\Cache", "$User\.cache"
)
$Freed = 0
foreach ($T in $Targets) {
    Get-Item -Path $T -Force -EA 0 | ForEach-Object {
        $S = (Get-ChildItem $_.FullName -Recurse -Force -EA 0 | Measure-Object Length -Sum).Sum
        if (-not $S) { $S = $_.Length }
        Remove-Item $_.FullName -Recurse -Force -EA 0
        $Freed += $S
    }
    Get-ChildItem -Path $T -Force -EA 0 | ForEach-Object {
        $S = (Get-ChildItem $_.FullName -Recurse -Force -EA 0 | Measure-Object Length -Sum).Sum
        if (-not $S) { $S = $_.Length }
        Remove-Item $_.FullName -Recurse -Force -EA 0
        $Freed += $S
    }
}
Get-ChildItem -Path "$User\.opencode", "$User\.codex", "$User\.gemini", "$User\.claude" -Filter "node_modules" -Recurse -Directory -Force -EA 0 | Remove-Item -Recurse -Force -EA 0
Write-Host "Purga completada. Espacio liberado: $([math]::Round($Freed / 1MB, 2)) MB" -ForegroundColor Magenta
