# Azure App Service Deployment Script for VayuMitra (PowerShell)
# Matches the single-port fullstack Azure architecture from TerraDetective.

param(
    [string]$ResourceGroup = "niu_nw_25_0397_rg_9975",
    [string]$PlanName = "terradetective-plan",
    [string]$AppName = "vayumitra-demo",
    [string]$Location = "indiasouthcentral"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  VayuMitra — Azure App Service Single-Port Deployment    " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Step into project root
Set-Location $ProjectRoot

# 2. Build Frontend UI Production Distribution
Write-Host "`n[1/4] Compiling React + Tailwind production assets..." -ForegroundColor Yellow
Set-Location "$ProjectRoot\frontend"
npm run build
Set-Location $ProjectRoot

# 3. Create Web App (Python 3.11 runtime) if not already created
Write-Host "`n[2/4] Ensuring Web App ($AppName)..." -ForegroundColor Yellow
az webapp create `
    --resource-group $ResourceGroup `
    --plan $PlanName `
    --name $AppName `
    --runtime "PYTHON:3.11"

# 4. Configure Gunicorn startup command and environment variables
Write-Host "`n[3/4] Configuring Startup Command & Environment Variables..." -ForegroundColor Yellow
az webapp config set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --startup-file "gunicorn --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --chdir backend app.main:app"

az webapp config appsettings set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --settings PYTHONPATH="backend" SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# 5. Package and deploy via Azure zip deploy
$ZipFile = "$ProjectRoot\vayumitra_azure.zip"
Write-Host "`n[4/4] Packaging & Deploying payload ($ZipFile)..." -ForegroundColor Yellow
python -c "import zipfile, os; from pathlib import Path; root = Path(r'$ProjectRoot'); zip_path = root / 'vayumitra_azure.zip'; z = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED); [z.write(p, p.relative_to(root)) for folder in ['backend', 'data', 'frontend/dist'] for p in (root / folder).rglob('*') if p.is_file()]; z.write(root / 'requirements.txt', 'requirements.txt'); z.write(root / '.webappignore', '.webappignore'); z.close(); print('Zip created size:', os.path.getsize(zip_path))"

Write-Host "Deploying package to Azure App Service..." -ForegroundColor Yellow
az webapp deploy `
    --resource-group $ResourceGroup `
    --name $AppName `
    --src-path $ZipFile `
    --type zip

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " Deployment Complete!" -ForegroundColor Green
Write-Host " Live App URL: https://$AppName.azurewebsites.net" -ForegroundColor Green
Write-Host " Swagger API:  https://$AppName.azurewebsites.net/docs" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
