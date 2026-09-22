# keys-check.ps1 - Verificacion en vivo de API keys (endpoints /models, sin inferencia).
# Nunca imprime valores de claves: solo nombre, estado y longitud.
# Salida: produccion\keys-live.json

$ErrorActionPreference = 'Continue'
$outDir = 'C:\Users\USER\Desktop\produccion'
$vault  = 'C:\Users\USER\.secrets\vault\cli-coders-pack.api-keys.env'

function Get-Keys {
    $k = @{}
    # 1. Entorno de proceso (heredado)
    Get-ChildItem env: | Where-Object { $_.Name -match 'KEY|TOKEN' } | ForEach-Object { $k[$_.Name] = $_.Value }
    # 2. Entorno de usuario (registro)
    try {
        [Environment]::GetEnvironmentVariables('User').GetEnumerator() |
            Where-Object { $_.Key -match 'KEY|TOKEN' } |
            ForEach-Object { if (-not $k.ContainsKey($_.Key)) { $k[$_.Key] = [string]$_.Value } }
    } catch {}
    # 3. Vault canonico (gana)
    if (Test-Path $vault) {
        Get-Content $vault | ForEach-Object {
            $l = $_.Trim()
            if ($l -eq '' -or $l.StartsWith('#') -or $l -notmatch '=') { return }
            $i = $l.IndexOf('='); $k[$l.Substring(0,$i).Trim()] = $l.Substring($i+1).Trim()
        }
    }
    return $k
}

$keys = Get-Keys

# (etiqueta, nombre de variable, url, tipo de auth)
$tests = @(
    @('OpenRouter',      'OPENROUTER_API_KEY',   'https://openrouter.ai/api/v1/models',                  'bearer'),
    @('OpenRouter key2', 'OPENROUTER_KEY_2',     'https://openrouter.ai/api/v1/models',                  'bearer'),
    @('OpenRouter key3', 'OPENROUTER_KEY_3',     'https://openrouter.ai/api/v1/models',                  'bearer'),
    @('OpenRouter key4', 'OPENROUTER_KEY_4',     'https://openrouter.ai/api/v1/models',                  'bearer'),
    @('Groq',            'GROQ_API_KEY',         'https://api.groq.com/openai/v1/models',                'bearer'),
    @('DeepSeek',        'DEEPSEEK_API_KEY',     'https://api.deepseek.com/models',                      'bearer'),
    @('DeepSeek 2',      'DEEPSEEK_API_KEY_2',   'https://api.deepseek.com/models',                      'bearer'),
    @('Gemini',          'GEMINI_API_KEY',       'https://generativelanguage.googleapis.com/v1beta/models','query'),
    @('Cerebras',        'CEREBRAS_API_KEY',     'https://api.cerebras.ai/v1/models',                    'bearer'),
    @('NVIDIA NIM',      'NVIDIA_API_KEY',       'https://integrate.api.nvidia.com/v1/models',           'bearer'),
    @('NVIDIA alt',      'NVIDIA_ALT_KEY',       'https://integrate.api.nvidia.com/v1/models',           'bearer'),
    @('Z.AI (GLM)',      'Z_AI_API_KEY',         'https://api.z.ai/api/paas/v4/models',                  'bearer'),
    @('Morph',           'MORPH_API_KEY',        'https://api.morphllm.com/v1/models',                   'bearer'),
    @('OpenCode Zen',    'OPENCODE_ZEN_KEY',     'https://opencode.ai/zen/v1/models',                    'bearer'),
    @('OpenZen',         'OPENZEN_API_KEY',      'https://api.openzen.ai/v1/models',                     'bearer'),
    @('HuggingFace',     'HF_TOKEN',             'https://huggingface.co/api/models?limit=1',            'bearer'),
    @('OpenAI',          'OPENAI_API_KEY',       'https://api.openai.com/v1/models',                     'bearer'),
    @('Anthropic',       'ANTHROPIC_API_KEY',    'https://api.anthropic.com/v1/models',                  'anthropic')
)

$rows = @()
foreach ($t in $tests) {
    $label, $var, $url, $auth = $t
    $key = $keys[$var]
    if ([string]::IsNullOrWhiteSpace($key)) {
        $rows += [pscustomobject]@{ Provider = $label; Var = $var; Status = 'SIN CLAVE'; Http = ''; Models = 0; Len = 0 }
        continue
    }
    $headers = @{}
    if ($auth -eq 'bearer')    { $headers['Authorization'] = "Bearer $key" }
    if ($auth -eq 'anthropic') { $headers['x-api-key'] = $key; $headers['anthropic-version'] = '2023-06-01' }
    $uri = $url
    if ($auth -eq 'query')     { $uri = "$url`?key=$key" }

    try {
        $r = Invoke-WebRequest -Uri $uri -Headers $headers -TimeoutSec 25 -SkipHttpErrorCheck
        $code = [int]$r.StatusCode
        $n = 0
        try {
            $j = $r.Content | ConvertFrom-Json
            if ($j.data)   { $n = @($j.data).Count }
            elseif ($j.models) { $n = @($j.models).Count }
        } catch {}
        $status = switch ($code) {
            200 { 'FUNCIONA' }
            401 { 'CLAVE INVALIDA' }
            403 { 'PROHIBIDO' }
            429 { 'LIMITE' }
            400 { 'BAD REQUEST' }
            404 { 'URL?' }
            default { "HTTP $code" }
        }
    } catch {
        $code = 0; $n = 0; $status = 'ERROR RED'
    }
    $rows += [pscustomobject]@{ Provider = $label; Var = $var; Status = $status; Http = $code; Models = $n; Len = $key.Length }
}

$rows | Format-Table -AutoSize

$ok = @($rows | Where-Object { $_.Status -eq 'FUNCIONA' })
"`nOperativas: $($ok.Count) de $($rows.Count)"
"OK -> " + (($ok | ForEach-Object { $_.Provider }) -join ', ')

if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir -Force | Out-Null }
$rows | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $outDir 'keys-live.json') -Encoding UTF8
"Escrito: $outDir\keys-live.json"
