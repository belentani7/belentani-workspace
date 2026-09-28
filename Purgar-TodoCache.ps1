param(
    [switch]$Borrar,
    [string]$Report = "$env:USERPROFILE\Desktop\cache-final.csv"
)

$sw = [System.Diagnostics.Stopwatch]::StartNew()
$safe = @('Documents','_MEDIA','Music','Pictures','Videos','Movies','Downloads','Desktop',
          '.ssh','.gnupg','.aws','.config','.claude','.opencode','.kilo','.cursor',
          '.vscode','.belentani','.agents','.tools','Programs','Google','nvm',
          'Microsoft','Packages','rustdesk','Zed','Cursor','Claude','BraveSoftware',
          'electron','electron-builder','GitKrakenCLI','GitHub CLI','com.minimax.hub.global')

$cacheNames = @('Cache','cache','Temp','temp','CrashDumps','D3DSCache','WebCache',
    'INetCache','Temporary Internet Files','Caches','Service Worker','GPUCache',
    'Code Cache','DawnGraphiteCache','DawnWebGPUCache','CachedData','logs','Logs',
    'Crashpad','CacheStorage','ThumbnailCache','thumbcache','ShaderCache',
    'npm-cache','pnpm-cache','yarn-cache','uv','pip','go-build','node-gyp',
    'numba','Jedi','pylint','deno','CEF','fontconfig','goimports',
    'pipx','ImageMagick','ElevatedDiagnostics','Sentry','PeerDistRepub',
    'Package Cache','Python Entry Points','SquirrelTemp','ChromeExtensionCache',
    'Velopack','ms-playwright-mcp','trivy','typst','Pandoc','next-swc',
    'cursor-compile-cache','prisma-nodejs','checkpoint-nodejs',
    'github-copilot-sdk','node-addon-native-custom-loader',
    'antigravity-updater','autoclaw-updater','lm-studio-updater',
    'kimi-desktop-updater','velopack','codebufffreebuff-desktop-updater',
    'zcodedesktop-updater','@codebufffreebuff-desktop-updater',
    '@zcodedesktop-updater','.rustup','.cargo','.bun','.npmrc')

function IsSafe([string]$path) {
    foreach ($s in $safe) { if ($path -like "*\$s\*" -or $path -like "*\$s") { return $true } }
    return $false
}

Write-Host "Buscando cachés..." -ForegroundColor Cyan
$all = @()
$stack = New-Object System.Collections.Stack
$stack.Push("$env:LOCALAPPDATA")
$stack.Push("$env:APPDATA")
while ($stack.Count -gt 0) {
    $dir = $stack.Pop()
    if (IsSafe $dir) { continue }
    try {
        foreach ($d in [System.IO.Directory]::GetDirectories($dir)) {
            $name = [System.IO.Path]::GetFileName($d)
            if ($cacheNames -contains $name -or $name -like '*Cache*' -or $name -like '*temp*' -or $name -like '*Temp*') {
                try {
                    $di = New-Object System.IO.DirectoryInfo $d
                    $size = 0L; $fc = 0
                    foreach ($f in $di.GetFiles('*','AllDirectories')) { $size += $f.Length; $fc++ }
                    if ($size -gt 0) {
                        $all += [pscustomobject]@{ Path=$d; MB=[math]::Round($size/1MB,2); Files=$fc }
                    }
                } catch {}
                continue
            }
            if (-not (IsSafe $d)) { $stack.Push($d) }
        }
    } catch {}
}

$all = @($all) | Sort-Object MB -Descending
$total = [math]::Round((($all | Measure-Object MB -Sum).Sum),1)
Write-Host ("Cachés: {0:N0} | Total: {1:N1} MB ({2:N2} GB)" -f $all.Count, $total, ($total/1024)) -ForegroundColor Yellow
if ($all.Count) { $all | Export-Csv -LiteralPath $Report -NoTypeInformation -Encoding UTF8; Write-Host "Informe: $Report" -ForegroundColor Green }
if ($Borrar -and $all.Count) {
    $ok=0; $mb=0
    foreach ($a in $all) { try { Remove-Item -LiteralPath $a.Path -Recurse -Force -ErrorAction Stop; $ok++; $mb += $a.MB } catch {} }
    Write-Host ("Borrados: {0:N0} | Liberado: {1:N1} MB" -f $ok, $mb) -ForegroundColor Green
}
Write-Host ("Tiempo: {0:N1}s" -f $sw.Elapsed.TotalSeconds) -ForegroundColor DarkGray