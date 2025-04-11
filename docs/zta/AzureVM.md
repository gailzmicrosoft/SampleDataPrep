# Implementing Zero Trust Architecture for Azure Virtual Machines (VMs)

Draft 
This guide outlines the key requirements and best practices for implementing Zero Trust Architecture for Azure Virtual Machines (VMs). The focus is on applying principles of least privilege, strong authentication, network segmentation, and continuous monitoring.

**Key Features of This Document**

1. Identity and Access Management: Focuses on Azure AD, RBAC, and managed identities.
2. Network Security: Covers NSGs, private endpoints, and Azure Bastion.
3. Data Protection: Includes disk encryption and secure boot.
4. Monitoring and Threat Detection: Highlights Azure Monitor and Defender for Servers.
5. Backup and Recovery: Discusses Azure Backup and snapshots.
6. Example Bicep Configuration: Provides a complete example for deploying a secure VM.

---

## **1. Identity and Access Management**

### **Use Azure Active Directory (Azure AD) for Authentication**
- Enable **Azure AD login** for VMs to replace traditional username/password authentication.
- Assign **Azure RBAC roles** to users or groups for VM access (e.g., `Virtual Machine Administrator Login` or `Virtual Machine User Login`).

**Example**:
```bicep
osProfile: {
  adminUsername: 'azureuser'
  linuxConfiguration: {
    disablePasswordAuthentication: true
    ssh: {
      publicKeys: [
        {
          path: '/home/azureuser/.ssh/authorized_keys'
          keyData: '<your-ssh-public-key>'
        }
      ]
    }
  }
}
```

### **Use Managed Identities**
- Assign a **System-Assigned** or **User-Assigned Managed Identity** to the VM for secure access to Azure resources (e.g., Key Vault, Storage).

**Example**:
```bicep
identity: {
  type: 'SystemAssigned'
}
```

---

## **2. Network Security**

### **Restrict Public IP Access**
- Avoid assigning public IP addresses to VMs unless absolutely necessary.
- Use **Azure Bastion** for secure RDP/SSH access to VMs without exposing them to the internet.

**Example**:
```bicep
publicIpAddress: null
```

### **Use Network Security Groups (NSGs)**
- Apply **NSGs** to restrict inbound and outbound traffic to the VM.
- Allow only required ports (e.g., SSH on port 22 or RDP on port 3389) from trusted IP ranges.

**Example**:
```bicep
securityRules: [
  {
    name: 'AllowSSH'
    properties: {
      priority: 100
      direction: 'Inbound'
      access: 'Allow'
      protocol: 'Tcp'
      sourcePortRange: '*'
      destinationPortRange: '22'
      sourceAddressPrefix: '203.0.113.0/24'
      destinationAddressPrefix: '*'
    }
  }
]
```

### **Use Private Endpoints**
- Use **private endpoints** to securely connect VMs to Azure services (e.g., Storage, SQL) over a private network.

---

## **3. Data Protection**

### **Enable Disk Encryption**
- Use **Azure Disk Encryption** to encrypt OS and data disks with **Azure-managed keys** or **customer-managed keys (CMK)** in Azure Key Vault.

**Example**:
```bicep
osDisk: {
  encryptionSettings: {
    enabled: true
    diskEncryptionKey: {
      sourceVault: {
        id: '<key-vault-id>'
      }
      secretUrl: '<key-vault-secret-url>'
    }
  }
}
```

### **Secure Boot and Virtual TPM**
- Enable **Secure Boot** and **vTPM** for enhanced security on supported VM sizes.

---

## **4. Monitoring and Threat Detection**

### **Enable Azure Monitor and Logs**
- Enable **Azure Monitor** to track VM performance and activity.
- Send logs to a **Log Analytics Workspace** for centralized monitoring.

**Example**:
```bicep
diagnosticsProfile: {
  bootDiagnostics: {
    enabled: true
    storageUri: '<storage-account-uri>'
  }
}
```

### **Enable Azure Defender for Servers**
- Use **Azure Defender for Servers** to detect and respond to potential threats, such as malware or brute-force attacks.

---

## **5. Access Control Policies**

### **Use Conditional Access Policies**
- Enforce **Conditional Access** policies to restrict VM access based on user location, device compliance, or risk level.

### **Use Just-in-Time (JIT) Access**
- Enable **JIT VM Access** to allow temporary access to VMs for specific users and time periods.

---

## **6. Backup and Recovery**

### **Enable Azure Backup**
- Use **Azure Backup** to create regular backups of VM disks and configurations.

**Example**:
```bicep
backupPolicy: {
  name: 'DailyBackupPolicy'
  schedule: {
    frequency: 'Daily'
    time: '02:00'
  }
}
```

### **Enable Snapshot Protection**
- Use **disk snapshots** for point-in-time recovery of VM disks.

---

## **7. Example Bicep Configuration**
```bicep
resource vm 'Microsoft.Compute/virtualMachines@2022-03-01' = {
  name: vmName
  location: location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B2ms'
    }
    osProfile: {
      computerName: vmName
      adminUsername: 'azureuser'
      linuxConfiguration: {
        disablePasswordAuthentication: true
        ssh: {
          publicKeys: [
            {
              path: '/home/azureuser/.ssh/authorized_keys'
              keyData: '<your-ssh-public-key>'
            }
          ]
        }
      }
    }
    storageProfile: {
      osDisk: {
        createOption: 'FromImage'
        managedDisk: {
          storageAccountType: 'Standard_LRS'
        }
      }
      imageReference: {
        publisher: 'Canonical'
        offer: 'UbuntuServer'
        sku: '18.04-LTS'
        version: 'latest'
      }
    }
    networkProfile: {
      networkInterfaces: [
        {
          id: nic.id
        }
      ]
    }
    diagnosticsProfile: {
      bootDiagnostics: {
        enabled: true
        storageUri: '<storage-account-uri>'
      }
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}
```


By following these practices, you can implement a robust Zero Trust Architecture for Azure Virtual Machines, ensuring secure and compliant access to your infrastructure.