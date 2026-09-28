# Belentani Agent OS — autonomía sin Cursor
# Regla: free-first. No instalar colecciones enteras.

$ErrorActionPreference = "Continue"
$os = "C:\Users\USER\USO\belentani-agent-os"
$prompt = "C:\Users\USER\USO\PROMPT-MAESTRO.txt"

Write-Host "`n=== BELENTANI AUTONOMIA ===" -ForegroundColor Cyan
Write-Host "1) Agent OS   : $os"
Write-Host "2) Prompt     : $prompt"
Write-Host "3) OpenCode   : comando /mision"
Write-Host "4) Kilo model : keyrotor/auto (free)"
Write-Host "5) Pistas     : disco | belentani-web | consultoria`n"

if ($args.Count -eq 0) {
  Write-Host "Uso:" -ForegroundColor Yellow
  Write-Host "  .\START-AUTONOMIA.ps1 disco"
  Write-Host "  .\START-AUTONOMIA.ps1 belentani-web"
  Write-Host "  .\START-AUTONOMIA.ps1 consultoria"
  Write-Host "  .\START-AUTONOMIA.ps1 `"tu objetivo libre`""
  Write-Host "`nPrompt para pegar en el agente:"
  Get-Content $prompt -Raw
  exit 0
}

$mision = $args -join " "
switch -Regex ($mision) {
  "disco|album|musica|stem" {
    Write-Host "→ Pista DISCO" -ForegroundColor Green
    if (Test-Path "C:\Users\USER\Belentani") { Get-ChildItem "C:\Users\USER\Belentani" -Filter *.wav | Select-Object Name, Length }
  }
  "belentani-web|web|unified|judas" {
    Write-Host "→ Pista BELENTANI-WEB" -ForegroundColor Green
    Write-Host "Carpeta: C:\Users\USER\Desktop\belentani-unified"
  }
  "consult|auditor" {
    Write-Host "→ Pista CONSULTORIA" -ForegroundColor Green
    Write-Host "Carpeta: C:\Users\USER\USO"
  }
}

$env:PYTHONIOENCODING = "utf-8"
Set-Location $os
python "$os\core\harness_cli.py" $mision
Write-Host "`nSiguiente: abre OpenCode/Kilo y escribe /mision $mision" -ForegroundColor Cyan
