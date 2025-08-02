[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory = $false)]
    [string]$WorkspaceName = "databricks-workspace-$(Get-Random -Maximum 9999)",
    
    [Parameter(Mandatory = $false)]
    [string]$Location = "East US",
    
    [Parameter(Mandatory = $false)]
    [ValidateSet("standard", "premium")]
    [string]$PricingTier = "premium",
    
    [Parameter(Mandatory = $false)]
    [bool]$EnableUnityCatalog = $false,
    
    [Parameter(Mandatory = $false)]
    [string]$SubscriptionId
)

# Set error action preference
$ErrorActionPreference = "Stop"

Write-Host "🚀 Azure Databricks Workspace Deployment Script" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Login to Azure if not already logged in
try {
    $context = Get-AzContext
    if (-not $context) {
        Write-Host "🔐 Logging into Azure..." -ForegroundColor Yellow
        Connect-AzAccount
    }
} catch {
    Write-Host "🔐 Logging into Azure..." -ForegroundColor Yellow
    Connect-AzAccount
}

# Set subscription if provided
if ($SubscriptionId) {
    Write-Host "📋 Setting subscription to: $SubscriptionId" -ForegroundColor Yellow
    Set-AzContext -SubscriptionId $SubscriptionId
}

# Get current subscription info
$currentContext = Get-AzContext
Write-Host "📋 Current Subscription: $($currentContext.Subscription.Name)" -ForegroundColor Cyan
Write-Host "📋 Current Tenant: $($currentContext.Tenant.Id)" -ForegroundColor Cyan

# Check if resource group exists, create if not
Write-Host "🔍 Checking resource group: $ResourceGroupName" -ForegroundColor Yellow
$resourceGroup = Get-AzResourceGroup -Name $ResourceGroupName -ErrorAction SilentlyContinue

if (-not $resourceGroup) {
    Write-Host "📁 Creating resource group: $ResourceGroupName in $Location" -ForegroundColor Yellow
    $resourceGroup = New-AzResourceGroup -Name $ResourceGroupName -Location $Location
    Write-Host "✅ Resource group created successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Resource group already exists" -ForegroundColor Green
}

# Create managed resource group name
$managedResourceGroupName = "databricks-rg-$WorkspaceName-$(Get-Random -Maximum 99999)"
$managedResourceGroupId = "/subscriptions/$($currentContext.Subscription.Id)/resourceGroups/$managedResourceGroupName"

Write-Host "📊 Deployment Parameters:" -ForegroundColor Cyan
Write-Host "  Workspace Name: $WorkspaceName" -ForegroundColor White
Write-Host "  Location: $Location" -ForegroundColor White
Write-Host "  Pricing Tier: $PricingTier" -ForegroundColor White
Write-Host "  Unity Catalog: $EnableUnityCatalog" -ForegroundColor White
Write-Host "  Managed RG: $managedResourceGroupName" -ForegroundColor White

# Create deployment parameters
$deploymentParams = @{
    workspaceName = $WorkspaceName
    location = $Location
    pricingTier = $PricingTier
    managedResourceGroupId = $managedResourceGroupId
    enableUnityCatalog = $EnableUnityCatalog
    tags = @{
        Environment = "Development"
        Project = "SampleDataPrep"
        CreatedBy = "PowerShell"
        Purpose = "Learning"
        CreatedDate = (Get-Date).ToString("yyyy-MM-dd")
    }
}

try {
    Write-Host "🚀 Starting Azure Databricks workspace deployment..." -ForegroundColor Yellow
    
    # Deploy using Bicep template
    $bicepTemplatePath = Join-Path $PSScriptRoot "..\bicep\databricks-workspace.bicep"
    
    if (Test-Path $bicepTemplatePath) {
        Write-Host "📄 Using Bicep template: $bicepTemplatePath" -ForegroundColor Cyan
        
        $deployment = New-AzResourceGroupDeployment `
            -ResourceGroupName $ResourceGroupName `
            -TemplateFile $bicepTemplatePath `
            -TemplateParameterObject $deploymentParams `
            -Name "DatabricksWorkspace-$(Get-Date -Format 'yyyyMMdd-HHmmss')" `
            -Verbose
    } else {
        Write-Host "📄 Bicep template not found, using direct PowerShell deployment" -ForegroundColor Yellow
        
        # Direct PowerShell deployment
        $workspace = New-AzDatabricksWorkspace `
            -ResourceGroupName $ResourceGroupName `
            -Name $WorkspaceName `
            -Location $Location `
            -Sku $PricingTier `
            -ManagedResourceGroupId $managedResourceGroupId `
            -Tag $deploymentParams.tags
            
        $deployment = @{
            Outputs = @{
                workspaceName = @{ Value = $workspace.Name }
                workspaceId = @{ Value = $workspace.Id }
                workspaceUrl = @{ Value = "https://$($workspace.WorkspaceUrl)/" }
            }
        }
    }
    
    Write-Host "✅ Azure Databricks workspace deployed successfully!" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    
    # Display deployment results
    Write-Host "📊 Deployment Results:" -ForegroundColor Green
    Write-Host "  Workspace Name: $($deployment.Outputs.workspaceName.Value)" -ForegroundColor White
    Write-Host "  Workspace URL: $($deployment.Outputs.workspaceUrl.Value)" -ForegroundColor White
    Write-Host "  Resource ID: $($deployment.Outputs.workspaceId.Value)" -ForegroundColor White
    
    Write-Host "" -ForegroundColor White
    Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Navigate to: $($deployment.Outputs.workspaceUrl.Value)" -ForegroundColor White
    Write-Host "  2. Sign in with your Azure AD credentials" -ForegroundColor White
    Write-Host "  3. Create your first notebook" -ForegroundColor White
    Write-Host "  4. Upload your Product_samples.csv file" -ForegroundColor White
    
} catch {
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    throw
}
