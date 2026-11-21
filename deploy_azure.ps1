# Azure App Service Deployment Script for VayuMitra (PowerShell)
# Exactly matching the single-port fullstack Azure architecture used in TerraDetective.

param(
    [string]$ResourceGroup = "rg-vayumitra",
    [string]$PlanName = "plan-vayumitra",
    [string]$AppName = "vayumitra-app",
    [string]$Location = "centralindia"
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

# 3. Create Azure Resource Group & Linux App Service Plan (B1 / F1)
Write-Host "`n[2/4] Provisioning Azure Resources..." -ForegroundColor Yellow
az group create --name $ResourceGroup --location $Location

az appservice plan create `
    --name $PlanName `
    --resource-group $ResourceGroup `
    --sku B1 `
    --is-linux

# 4. Create Web App (Python 3.11 runtime)
Write-Host "`n[3/4] Creating Web App ($AppName)..." -ForegroundColor Yellow
az webapp create `
    --resource-group $ResourceGroup `
    --plan $PlanName `
    --name $AppName `
    --runtime "PYTHON:3.11"

# 5. Configure Gunicorn startup command and environment variables
Write-Host "`n[4/4] Configuring Startup Command & Deploying Zip..." -ForegroundColor Yellow
az webapp config set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --startup-file "gunicorn --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --chdir backend app.main:app"

az webapp config appsettings set `
    --resource-group $ResourceGroup `
    --name $AppName `
    --settings PYTHONPATH="backend" SCM_DO_BUILD_DURING_DEPLOYMENT="true"

# Package and deploy via Azure zip deploy
$ZipFile = "$ProjectRoot\vayumitra_deploy.zip"
if (Test-Path $ZipFile) { Remove-Item $ZipFile -Force }

Write-Host "Packaging deployment payload ($ZipFile)..." -ForegroundColor Yellow
Compress-Archive -Path "backend", "data", "frontend\dist", "requirements.txt", ".webappignore" -DestinationPath $ZipFile

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
