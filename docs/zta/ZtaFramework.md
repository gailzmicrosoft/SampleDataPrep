# Zero Trust Architecture Framework for Azure Applications

<Draft>

**Zero Trust Principles and References**

[What is Zero Trust? | Microsoft Learn](https://learn.microsoft.com/en-us/security/zero-trust/zero-trust-overview)

**Assumptions and Prerequisites** 

It is assumed that your organizations have established foundations for develop and deploy zero trust architecture or applications: 

[Assumptions and Prerequisites for ZTA](./ZtaPrerequisites.md) 

---

## **Core Principles of Zero Trust**
1. **Verify Explicitly**: Always authenticate and authorize based on all available data points (e.g., user identity, location, device health, service identity).
2. **Use Least Privilege Access**: Limit access to only what is necessary for users, applications, and services.
3. **Assume Breach**: Design the architecture as if the network is already compromised.

## **Key Concepts for Implementation**

1. **Start with Identity**: Secure all resources with Azure AD and managed identities.
2. **Segment the Network**: Use VNets, NSGs, and private endpoints to isolate resources.
3. **Encrypt Everything**: Ensure encryption at rest and in transit for all data.
4. **Monitor Continuously**: Use Azure Monitor, Defender, and Sentinel for real-time insights.
5. **Automate Compliance**: Use Azure Policy and IaC to enforce security configurations.

---

## **Framework Layers**

### **1. Identity and Access Management**
- **Azure Active Directory (Azure AD)**:
  - Centralize identity management for users, applications, and services.
  - Use **Conditional Access Policies** to enforce access restrictions based on risk levels, device compliance, and location.
  - Enable **Multi-Factor Authentication (MFA)** for all users.
- **Managed Identities**:
  - Use **System-Assigned** or **User-Assigned Managed Identities** for applications and services to securely access Azure resources without managing credentials.
- **Role-Based Access Control (RBAC)**:
  - Assign granular permissions using Azure RBAC roles for all resources.
  - Avoid assigning broad roles like `Owner` or `Contributor` unless absolutely necessary.

---

### **2. Network Security**
- **Private Endpoints**:
  - Use **Private Endpoints** to securely connect to Azure services (e.g., Storage, PostgreSQL, Cosmos DB) over a private network.
  - Disable public network access for all resources unless required.
- **Virtual Network (VNet) Integration**:
  - Integrate all resources (e.g., Azure Container Apps, Azure Functions) with a **Virtual Network**.
  - Use **VNet Service Endpoints** or **Private Link** for secure communication between resources.
- **Network Security Groups (NSGs)**:
  - Apply **NSGs** to subnets and VMs to restrict inbound and outbound traffic.
  - Allow only required ports and IP ranges.
- **Azure Firewall**:
  - Deploy **Azure Firewall** to inspect and filter traffic between VNets and the internet.
  - Use **Application Rules** to restrict outbound traffic to specific FQDNs (e.g., `*.database.windows.net` for Azure SQL).
- **DNS Security**:
  - Use **Azure Private DNS Zones** to resolve private endpoints within the VNet.
  - Disable public DNS resolution for sensitive resources.

---

### **3. Storage and Database Security** 

- **Storage Access:** No anonymous public access, no key-based client     access. Implement private end point. 
- **Storage Protection:** Enable Microsoft Defender for Storage 
- **Immutable Storage**: Enable **immutable storage policies** for critical data to prevent tampering or deletion.
- **Database Access**: Setup private end point access, set up managed identity as     principal for initial database administration. 
- **Data Loss Prevention (DLP)**: Use DLP solutions to prevent unauthorized     access and sharing of sensitive data.
- **Backup and Recovery**:
  - Configure **automated backups** for databases (e.g., PostgreSQL, SQL DB, Cosmos DB).
  - Enable **point-in-time restore** for critical data.
- **Encryption**:     Ensure that data is encrypted both at rest and in transit.

---
### **4. Data Protection**

- **Encryption**:
  - Enable **encryption at rest** for all resources using **Microsoft-managed keys** or **customer-managed keys (CMK)** in Azure Key Vault.
  - Enforce **encryption in transit** by requiring HTTPS or SSL/TLS for all connections.
- **Azure Key Vault**:
  - Store secrets, certificates, and encryption keys in **Azure Key Vault**.
  - Use **Key Vault Access Policies** or **Azure RBAC** to control access.

---

### **5. Application Security and SDLC**

- **Secure Development Lifecycle (SDLC)**: Integrate security into the development     lifecycle to identify and mitigate vulnerabilities early.
- **Application Identity**: Set up application identity and grant necessary     privileges during deployment and initial set up. 
- **Sensitive Information Management**: Use Azure Key Vault to store all sensitive information including end points and keys. Do not use environment variables to store keys or end points that can be easily stored and retrieved from Azure Key Vault. Use managed identity to access Key Vault. 

---

### **6. Monitoring and Threat Detection**

- **Azure Monitor**:
  - Enable **Azure Monitor** to collect metrics and logs for all resources.
  - Send logs to a **Log Analytics Workspace** for centralized monitoring.
- **Azure Defender**:
  - Enable **Azure Defender** for all supported resources (e.g., Storage, SQL, Cosmos DB, Kubernetes).
  - Use **Azure Defender for Containers** to scan container images for vulnerabilities.
- **Audit Logs**:
  - Enable **Activity Logs** and **Diagnostic Logs** for all resources.
  - Monitor access patterns and detect anomalies.
- **Threat Detection**:
  - Use **Azure Sentinel** for advanced threat detection and response.
  - Integrate with **Microsoft Defender for Cloud** for security recommendations.

---

### **7. Automation and Governance**
- **Infrastructure as Code (IaC)**:
  - Use **Bicep** or **Terraform** to define and deploy secure configurations for all resources.
  - Include security configurations (e.g., private endpoints, RBAC) in the IaC templates.
- **Azure Policy**:
  - Enforce compliance using **Azure Policy**.
  - Example policies:
    - Require private endpoints for all resources.
    - Enforce encryption with customer-managed keys.
    - Deny public network access.
- **DevSecOps**:
  - Integrate security checks into the CI/CD pipeline.
  - Use tools like **Azure DevOps** or **GitHub Actions** to automate deployments.

---

## Detailed Guidance for Implementation 

Refer to below document for requirement for specific azure resources: 

1. [Azure Storage](./AzureStorage.md)
2. [Azure Container App](./ContainerApp.md)
3. [Azure PostgreSQL](./PostgreSQL.md)
4. [Azure Key Vault](./AzureKeyVault.md)
5. [Azure Virtual Machine](./AzureVM.md)

