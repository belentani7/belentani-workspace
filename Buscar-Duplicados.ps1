param(
    [string[]]$Roots = @(
        "$env:USERPROFILE\Documents",
        "$env:USERPROFILE\_MEDIA",
        "$env:USERPROFILE\Music",
        "$env:USERPROFILE\Videos",
        "$env:USERPROFILE\Pictures",
        "$env:USERPROFILE\Movies",
        "$env:USERPROFILE\Downloads",
        "$env:USERPROFILE\Desktop"
    ),
    [int]$MinMB = 1,
    [switch]$Borrar,
    [string]$Report = "$env:USERPROFILE\Desktop\duplicados.csv"
)

$minBytes = $MinMB * 1MB
$sw = [System.Diagnostics.Stopwatch]::StartNew()

Write-Host "Escaneando archivos >= $MinMB MB ..." -ForegroundColor Cyan
$files = foreach ($r in $Roots) {
    if (Test-Path -LiteralPath $r) {
        Get-ChildItem -LiteralPath $r -Recurse -File -Force -ErrorAction SilentlyContinue
    }
}
$files = $files | Where-Object { $_.Length -ge $minBytes }
Write-Host ("Candidatos: {0:N0} archivos" -f $files.Count) -ForegroundColor Cyan

$groups = $files | Group-Object Length | Where-Object { $_.Count -gt 1 }

$dups = @()
foreach ($g in $groups) {
    $hashGroups = $g.Group | Group-Object {
        (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256 -ErrorAction SilentlyContinue).Hash
    } | Where-Object { $_.Name -and $_.Count -gt 1 }

    foreach ($hg in $hashGroups) {
        $keep = $hg.Group | Sort-Object LastWriteTime | Select-Object -First 1
        foreach ($f in ($hg.Group | Where-Object { $_.FullName -ne $keep.FullName })) {
            $dups += [pscustomobject]@{
                Conservar = $keep.FullName
                Duplicado = $f.FullName
                MB        = [math]::Round($f.Length / 1MB, 2)
            }
        }
    }
}

$totalMB = if ($dups.Count) { [math]::Round((($dups | Measure-Object MB -Sum).Sum), 1) } else { 0 }
Write-Host ("Duplicados: {0:N0} archivos | Recuperable: {1:N1} MB ({2:N2} GB)" -f $dups.Count, $totalMB, ($totalMB/1024)) -ForegroundColor Yellow

if ($dups.Count) {
    $dups | Sort-Object MB -Descending | Export-Csv -LiteralPath $Report -NoTypeInformation -Encoding UTF8
    Write-Host "Informe: $Report" -ForegroundColor Green
}

if ($Borrar -and $dups.Count) {
    Write-Host "Borrando duplicados (se conserva la copia mas antigua)..." -ForegroundColor Red
    $ok = 0; $kb = 0
    foreach ($d in $dups) {
        try {
            Remove-Item -LiteralPath $d.Duplicado -Force -ErrorAction Stop
            $ok++; $kb += $d.MB
        } catch { Write-Host "No se pudo: $($d.Duplicado)" -ForegroundColor DarkYellow }
    }
    Write-Host ("Borrados: {0:N0} | Liberado: {1:N1} MB" -f $ok, $kb) -ForegroundColor Green
}

Write-Host ("Tiempo: {0:N1}s" -f $sw.Elapsed.TotalSeconds) -ForegroundColor DarkGray
