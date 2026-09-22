# =====================================================================
# VERIFICADOR DE PRODUCCION ONLINE  (verify-online.ps1)  v2
# Decide si un repo local es BORRABLE de forma segura.
#
# v2 - corrige bug: el parametro se llamaba $args (variable automatica
#      reservada de PowerShell), no se enlazaba, git recibia comandos
#      vacios y devolvia su texto de ayuda -> todo salia SUCIO en falso.
#
# Regla: SAFE_TO_DELETE solo si se cumple TODO:
#   1. Tiene remoto configurado
#   2. El remoto es alcanzable
#   3. El arbol de trabajo esta limpio
#   4. El HEAD local == HEAD remoto
#   5. 0 commits locales sin pushear
#   6. 0 archivos sin trackear relevantes
# =====================================================================

param(
  [string]$Inventory = "C:\Users\USER\Desktop\inventario-produccion.json",
  [string]$OutDir    = "C:\Users\USER\Desktop\produccion",
  [int]$MaxRepos     = 0
)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

if(-not (Test-Path $OutDir)){ New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
$work = Join-Path $env:TEMP "vfy_$([guid]::NewGuid().ToString('N').Substring(0,8))"
New-Item -ItemType Directory -Path $work -Force | Out-Null

$EDU  = 'school|academy|academia|curso|educa|lingua|aprende|manos|abiertas|william|willian|univers|student|learn|taller|ilacaf|guia-ia|aula|formac|natalia-marinho|recursos-educativos|edu-engine'
$EXCL = 'DEFENSA|DEUDAFIX|financ|deuda|expediente'

# --- Lanzador de git (cmd redirection evita el bug de captura de PS) ---
function Invoke-Git {
  param([string]$RepoPath, [string]$CmdArgs, [string]$Tag)
  $o = Join-Path $work "$Tag.out"
  $e = Join-Path $work "$Tag.err"
  Remove-Item $o,$e -Force -ErrorAction SilentlyContinue
  $line = 'git -C "{0}" {1} > "{2}" 2> "{3}"' -f $RepoPath, $CmdArgs, $o, $e
  cmd /c $line | Out-Null
  $code = $LASTEXITCODE
  $so = if(Test-Path $o){ Get-Content $o -Raw -ErrorAction SilentlyContinue } else { "" }
  $se = if(Test-Path $e){ Get-Content $e -Raw -ErrorAction SilentlyContinue } else { "" }
  return [pscustomobject]@{ Out = $so; Err = $se; Code = $code }
}

$rows = Get-Content $Inventory -Raw | ConvertFrom-Json
if($MaxRepos -gt 0){ $rows = @($rows) | Select-Object -First $MaxRepos }
$rows = @($rows)
Write-Host "Repos a verificar: $($rows.Count)" -ForegroundColor Cyan

# --- 1. safe.directory ------------------------------------------------
Write-Host "`n[1/4] Registrando safe.directory..." -ForegroundColor Yellow
foreach($r in $rows){
  $p = $r.Path -replace '\\','/'
  cmd /c ('git config --global --add safe.directory "{0}" 2>nul' -f $p) | Out-Null
}
Write-Host "  listo" -ForegroundColor Green

# --- 2. Verificacion --------------------------------------------------
Write-Host "`n[2/4] Verificando estado online..." -ForegroundColor Yellow
$results = New-Object System.Collections.ArrayList
$i = 0
foreach($r in $rows){
  $i++
  if($i % 10 -eq 0){ Write-Host "  ... $i / $($rows.Count)" -ForegroundColor DarkGray }

  $verdict=""; $reason=""; $localHead=""; $remoteHead=""
  $dirty=""; $unpushed=""; $untracked=""; $reach=""

  if($r.Name -match $EXCL){
    $verdict="EXCLUDED"; $reason="exclusion legal/personal"
  }
  elseif($r.Name -match $EDU){
    $verdict="KEEP_EDU"; $reason="educacional - se conserva siempre"
  }
  elseif(-not $r.Remote){
    $verdict="NO_REMOTE"; $reason="sin remoto: borrar = perder"
  }
  else {
    $st = Invoke-Git $r.Path "status --porcelain" "st"
    if($st.Code -ne 0 -and $st.Err -match 'dubious ownership'){
      $verdict="GIT_BLOCKED"; $reason="git bloqueado por ownership"
    } elseif($st.Code -ne 0){
      $verdict="GIT_ERROR"; $reason=($st.Err -split "`n")[0]
    } else {
      $dirty = if($st.Out -and $st.Out.Trim()){ "SUCIO" } else { "limpio" }

      $hd = Invoke-Git $r.Path "rev-parse HEAD" "hd"
      if($hd.Code -ne 0){ $verdict="NO_COMMITS"; $reason="repo sin commits" }
      else {
        $localHead = $hd.Out.Trim()
        $br = Invoke-Git $r.Path "rev-parse --abbrev-ref HEAD" "br"
        $branch = $br.Out.Trim()
        if(-not $branch -or $branch -eq 'HEAD'){ $branch = "main" }

        $lr = Invoke-Git $r.Path "ls-remote origin $branch" "lr"
        if($lr.Code -ne 0 -or -not $lr.Out.Trim()){
          $reach = "no"
          $errTxt = "$($lr.Err) $($lr.Out)"
          if($errTxt -match 'Authentication failed|could not read Username|terminal prompts disabled|403'){
            $verdict="AUTH_REQUIRED"; $reason="remoto existe pero git no tiene credenciales"
          } elseif($errTxt -match 'not found|does not exist|404|Repository not found'){
            $verdict="REMOTE_MISSING"; $reason="el repo remoto no existe"
          } else {
            $verdict="UNREACHABLE"; $reason=($errTxt -split "`n" | Where-Object {$_ -match '\S'} | Select-Object -First 1)
          }
        } else {
          $reach = "si"
          $remoteHead = ($lr.Out.Trim() -split '\s+')[0]
          if($remoteHead -eq $localHead){
            $cnt = Invoke-Git $r.Path "rev-list --count origin/$branch..HEAD" "cnt"
            $unpushed = if($cnt.Code -eq 0){ $cnt.Out.Trim() } else { "?" }
            $ut = Invoke-Git $r.Path "ls-files --others --exclude-standard" "ut"
            $untracked = if($ut.Code -eq 0 -and $ut.Out.Trim()){ (@($ut.Out -split "`n" | Where-Object {$_ -match '\S'})).Count } else { 0 }

            if($unpushed -eq "0" -and $dirty -eq "limpio" -and $untracked -eq 0){
              $verdict="SAFE_TO_DELETE"; $reason="pusheado, limpio, sin pendientes"
            } else {
              $verdict="PENDING"; $reason="sin pushear=$unpushed; arbol=$dirty; sin trackear=$untracked"
            }
          } else {
            $verdict="DIVERGED"; $reason="HEAD local != remoto"
          }
        }
      }
    }
  }

  [void]$results.Add([pscustomobject]@{
    Name=$r.Name; Path=$r.Path; Remote=$r.Remote; Branch=$r.Branch
    Verdict=$verdict; Reason=$reason; Dirty=$dirty; Unpushed=$unpushed
    Untracked=$untracked; Reachable=$reach; LocalHead=$localHead; RemoteHead=$remoteHead
  })
}

# --- 3. Guardar -------------------------------------------------------
Write-Host "`n[3/4] Guardando..." -ForegroundColor Yellow
$results | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $OutDir "verificacion-online.json") -Encoding utf8
$results | Export-Csv -Path (Join-Path $OutDir "verificacion-online.csv") -NoTypeInformation -Encoding utf8

# --- 4. Resumen -------------------------------------------------------
Write-Host "`n[4/4] Resumen:" -ForegroundColor Yellow
$order = @('SAFE_TO_DELETE','KEEP_EDU','PENDING','DIVERGED','NO_REMOTE','AUTH_REQUIRED','REMOTE_MISSING','UNREACHABLE','GIT_BLOCKED','GIT_ERROR','NO_COMMITS','EXCLUDED')
foreach($k in $order){
  $g = $results | Where-Object { $_.Verdict -eq $k }
  if($g.Count -gt 0){
    $color = switch($k){
      'SAFE_TO_DELETE' {'Green'} 'KEEP_EDU' {'Cyan'} 'NO_REMOTE' {'Magenta'}
      'EXCLUDED' {'DarkGray'} 'PENDING' {'Yellow'} 'DIVERGED' {'Red'} default {'DarkYellow'}
    }
    Write-Host ("  {0,-16} {1,4}" -f $k, $g.Count) -ForegroundColor $color
  }
}
Write-Host "  $('-'*22)"
Write-Host ("  {0,-16} {1,4}" -f 'TOTAL', $results.Count)

$safe = $results | Where-Object { $_.Verdict -eq 'SAFE_TO_DELETE' }
$bytes = 0
foreach($s in $safe){ $bytes += (Get-ChildItem $s.Path -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum }
Write-Host ("`nRecuperable si se borra: {0} MB" -f [math]::Round($bytes/1MB,0)) -ForegroundColor Green
Write-Host "Informe: $(Join-Path $OutDir 'verificacion-online.csv')" -ForegroundColor Green

Remove-Item $work -Recurse -Force -ErrorAction SilentlyContinue
