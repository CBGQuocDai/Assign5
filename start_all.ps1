# start_all.ps1 — Start all 12 services in separate windows
$root = $PSScriptRoot

$services = @(
    @{ Name="staff-service";          Port=8001 },
    @{ Name="manager-service";        Port=8002 },
    @{ Name="customer-service";       Port=8003 },
    @{ Name="catalog-service";        Port=8004 },
    @{ Name="book-service";           Port=8005 },
    @{ Name="cart-service";           Port=8006 },
    @{ Name="order-service";          Port=8007 },
    @{ Name="ship-service";           Port=8008 },
    @{ Name="pay-service";            Port=8009 },
    @{ Name="comment-rate-service";   Port=8010 },
    @{ Name="recommender-ai-service"; Port=8011 },
    @{ Name="api-gateway";            Port=8000 }
)

foreach ($svc in $services) {
    $dir = Join-Path $root $svc.Name
    $port = $svc.Port
    $title = "$($svc.Name) :$port"
    Write-Host "Starting $title ..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", `
        "Set-Location '$dir'; Write-Host '$title' -ForegroundColor Yellow; python manage.py runserver $port"
}

Write-Host "`nAll services started. API Gateway: http://localhost:8000" -ForegroundColor Green
