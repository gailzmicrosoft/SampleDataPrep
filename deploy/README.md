# Azure Databricks Workspace Deployment

This folder contains Infrastructure as Code (IaC) templates for deploying Azure Databricks workspaces.

## 🎯 Available Options

### 1. Bicep Template Deployment
```bash
# Deploy using Azure CLI
az deployment group create \
  --resource-group "my-resource-group" \
  --template-file "./bicep/databricks-workspace.bicep" \
  --parameters "@./bicep/databricks-workspace.parameters.json"
```

### 2. PowerShell Script Deployment
```powershell
# Deploy using PowerShell
.\powershell\Deploy-DatabricksWorkspace.ps1 `
  -ResourceGroupName "my-resource-group" `
  -WorkspaceName "my-databricks-workspace" `
  -Location "East US" `
  -PricingTier "premium"
```

## 📋 Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `workspaceName` | Name of the Databricks workspace | Auto-generated | Any valid name |
| `location` | Azure region | Resource group location | Any Azure region |
| `pricingTier` | Pricing tier | `premium` | `standard`, `premium` |
| `enableUnityCatalog` | Enable Unity Catalog | `false` | `true`, `false` |

## 🏗️ What Gets Created

- **Azure Databricks Workspace** - Main workspace resource
- **Managed Resource Group** - Auto-created by Databricks
- **Default configurations** - Standard security and network settings

## 🔐 Prerequisites

1. **Azure Subscription** with sufficient permissions
2. **Resource Group** (created automatically if doesn't exist)
3. **Azure PowerShell** or **Azure CLI** installed
4. **Contributor** role on the subscription or resource group

## 🚀 Quick Start

1. **Clone this repository**
2. **Update parameters** in `databricks-workspace.parameters.json`
3. **Run deployment script** using your preferred method
4. **Access your workspace** using the output URL

## 📊 Workspace Configuration

The deployed workspace includes:
- ✅ **Premium tier** - Full feature access
- ✅ **Hive Metastore** - Default data catalog
- ✅ **Standard networking** - Public access enabled
- ✅ **Auto-termination** - Cost optimization
- ✅ **Development tags** - Resource organization

## 🎯 Post-Deployment Steps

1. **Navigate to workspace URL**
2. **Sign in with Azure AD**
3. **Create your first cluster**
4. **Upload sample data**
5. **Start developing!**
