# setup.ps1 — Run once to initialise all databases, migrate, and seed data
# Prerequisites: Docker running with container "some-postgres", Python 3.10+ in PATH

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "==> Installing Python dependencies..." -ForegroundColor Cyan
pip install -r "$root\requirements.txt"

Write-Host "`n==> Creating PostgreSQL databases..." -ForegroundColor Cyan
Get-Content "$root\init-db.sql" | docker exec -i some-postgres psql -U postgres

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
    @{ Name="recommender-ai-service"; Port=8011 }
)

foreach ($svc in $services) {
    $dir = Join-Path $root $svc.Name
    Write-Host "`n==> Migrating $($svc.Name)..." -ForegroundColor Cyan
    Push-Location $dir
    python manage.py migrate --run-syncdb 2>&1
    Write-Host "==> Seeding $($svc.Name)..." -ForegroundColor Cyan
    python manage.py seed_data 2>&1
    Pop-Location
}

Write-Host "`n==> Setup complete! Run .\start_all.ps1 to start all services." -ForegroundColor Green
