## **Prerequisites for ZTA**

It is assumed that organizations have already established below foundations to build and deploy zero trust architectures. For example, the organizations have implemented Microsoft 365 using [Zero Trust deployment plan with Microsoft 365 | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/security/microsoft-365-zero-trust?view=o365-worldwide&bc=%2Fsecurity%2Fzero-trust%2Fbreadcrumb%2Ftoc.json&toc=%2Fsecurity%2Fzero-trust%2Ftoc.json), or equivalent. 

In addition, organizations have established below secure foundations in Azure: 

1. **Azure Landing Zones**:

   Have implemented Azure Landing Zones as part of the cloud adoption framework. This includes:

   - Identity and access management.
   - Network topology and connectivity.
   - Resource organization and governance.
   - Security, compliance, and monitoring.

   - Reference: [Azure Landing Zones | Microsoft Learn](vscode-file://vscode-app/c:/Users/gazho/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-sandbox/workbench/workbench.html)

2. **Azure Infrastructure Setup**:

   Have set up the foundational Secure Azure infrastructure, including:

   - **Identity Management**: Centralized identity management using Azure Active Directory (Azure AD).
   - **Network Isolation**: Virtual Networks (VNets), Network Security Groups (NSGs), and private endpoints for resource isolation.
   - **Azure Policies**: Governance policies to enforce compliance and security standards.

3. **Azure Governance**:

   Have implemented Azure Governance to manage resources effectively, including:

   - Azure Management Groups for hierarchical organization.
   - Azure Blueprints for consistent resource deployment.
   - Azure Policy for compliance enforcement.
   - Reference: [Azure governance documentation | Microsoft Learn](https://learn.microsoft.com/en-us/azure/governance/)

4. **Zero Trust Principles**:

   Have adopted Zero Trust principles as a core security strategy, including:

   - Verifying explicitly for all access requests.
   - Enforcing least privilege access.
   - Assuming breach and designing systems accordingly.

   Reference:[What is Zero Trust? | Microsoft Learn](https://learn.microsoft.com/en-us/security/zero-trust/zero-trust-overview)

5. **Well-Architected Framework**:

   Have followed the **Azure Well-Architected Framework** to ensure best practices for reliability, security, cost optimization, operational excellence, and performance efficiency.

   - Reference: [Azure Well-Architected Framework - Microsoft Azure Well-Architected Framework | Microsoft Learn](https://learn.microsoft.com/en-us/azure/well-architected/)

6. **Compliance Requirements**:

   Have identified and implemented compliance requirements (e.g., GDPR, HIPAA, ISO 27001) using Azure Policy and Microsoft Compliance Manager.

   References:

   -  [Azure compliance documentation | Microsoft Learn](https://learn.microsoft.com/en-us/azure/compliance/)
   - [Azure Policy documentation | Microsoft Learn](https://learn.microsoft.com/en-us/azure/governance/policy/)
   - [Azure Blueprints documentation | Microsoft Learn](https://learn.microsoft.com/en-us/azure/governance/blueprints/)

7. **Security Baseline**:

   Have established a security baseline for Azure resources, including:

   - Enabling **Azure Security Center** (Microsoft Defender for Cloud).
   - Configuring **Azure Monitor** and **Log Analytics** for centralized monitoring.
   - Setting up **Azure Sentinel** for Security Information and Event Management (SIEM).

8. **DevSecOps Practices**:

   Have integrated **DevSecOps** practices into their development lifecycle, ensuring security is embedded into CI/CD pipelines.

   - Reference: [Security in DevOps (DevSecOps) - Azure DevOps | Microsoft Learn](https://learn.microsoft.com/en-us/devops/operate/security-in-devops)
