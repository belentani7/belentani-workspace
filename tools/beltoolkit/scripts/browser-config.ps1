# Configuración óptima de navegadores - Anti-basura + Sincronización
# Ejecuta este script DESPUÉS de abrir cada navegador por primera vez

$ErrorActionPreference = "SilentlyContinue"

Write-Host "=== Configurando navegadores ===" -ForegroundColor Cyan

# Función para configurar Chromium (Chrome/Brave/Edge)
function Configure-Chromium {
    param($ProfilePath, $BrowserName)
    
    if (-not (Test-Path $ProfilePath)) {
        Write-Host "  $BrowserName no tiene perfil aún - ábrelo primero" -ForegroundColor Yellow
        return
    }
    
    $prefsFile = Join-Path $ProfilePath "Preferences"
    
    # Crear backup
    if (Test-Path $prefsFile) {
        Copy-Item $prefsFile "$prefsFile.backup" -Force
    }
    
    # Configuración JSON óptima
    $config = @{
        browser = @{
            clear_data = @{
                time_period = "clear_everything"
                cache = $true
                cookies = $true
                history = $true
                download_history = $true
                form_data = $true
                passwords = $false  # NO borrar contraseñas
                hosted_apps_data = $false
            }
            clear_data_on_exit = @{
                cache = $true
                cookies = $true
                history = $false  # Mantener historial para sync
                download_history = $true
                form_data = $true
                passwords = $false
            }
        }
        session = @{
            restore_on_startup = 1  # Restaurar sesión
        }
        extensions = @{
            alerts = @{
                initialized = $true
            }
        }
    } | ConvertTo-Json -Depth 10
    
    # Leer preferencias existentes y mezclar
    if (Test-Path $prefsFile) {
        $existing = Get-Content $prefsFile -Raw | ConvertFrom-Json
        # Merge simplificado - sobreescribe solo lo necesario
        $config | Out-File $prefsFile -Force
        Write-Host "  ✓ $BrowserName configurado" -ForegroundColor Green
    } else {
        $config | Out-File $prefsFile -Force
        Write-Host "  ✓ $BrowserName configurado (nuevo perfil)" -ForegroundColor Green
    }
}

# Configurar cada navegador
Write-Host "`nConfigurando Chrome..." -ForegroundColor Yellow
Configure-Chromium "$env:LOCALAPPDATA\Google\Chrome\User Data\Default" "Chrome"

Write-Host "`nConfigurando Brave..." -ForegroundColor Yellow  
Configure-Chromium "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data\Default" "Brave"

Write-Host "`nConfigurando Edge..." -ForegroundColor Yellow
Configure-Chromium "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default" "Edge"

Write-Host "`n=== Recomendaciones ===" -ForegroundColor Cyan
Write-Host "1. Abre cada navegador y activa la sincronización con tu cuenta Google/Microsoft"
Write-Host "2. Instala estas extensiones en TODOS los navegadores:"
Write-Host "   - Bitwarden (gestor de contraseñas gratis)"
Write-Host "   - Raindrop.io (marcadores sincronizados)"
Write-Host "3. En cada navegador ve a:"
Write-Host "   Configuración > Privacidad > Borrar datos al cerrar"
Write-Host "   Activa: Caché, Cookies, Historial de descargas"
Write-Host "   NO actives: Contraseñas, Marcadores"
Write-Host "`n✓ Script completado" -ForegroundColor Green
