## **Prerequisites for ZTA**

It is assumed that organizations have already established below foundations to build and deploy zero trust architectures. For example, the organizations have implemented Microsoft 365 using [Zero Trust deployment plan with Microsoft 365 | Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/security/microsoft-365-zero-trust?view=o365-worldwide&bc=%2Fsecurity%2Fzero-trust%2Fbreadcrumb%2Ftoc.json&toc=%2Fsecurity%2Fzero-trust%2Ftoc.json) or equivalent. 

In addition, organizations have established below secure foundations in Azure:

## **Prerequisites for ZTA in Azure**

It is assumed that organizations have established below secure foundations in Azure to enable the development and deployment of Azure Applications: 

1. **Azure Landing Zones and Infrastructure Setup**:
   - Have implemented **Azure Landing Zones** as part of the cloud adoption framework, which includes the foundational infrastructure setup. This ensures:
     - **Identity Management**: Centralized identity management using Azure Active Directory (Azure AD).
     - **Network Topology and Connectivity**: Virtual Networks (VNets), Network Security Groups (NSGs), and private endpoints for resource isolation.
     - **Resource Organization and Governance**: Use of Azure Management Groups, subscriptions, and resource groups for logical organization.
     - **Security, Compliance, and Monitoring**:
       - Governance policies using **Azure Policy** to enforce compliance and security standards.
       - Monitoring and logging using **Azure Monitor** and **Log Analytics**.
     - **Scalability and Performance**: A scalable architecture that supports workload growth while maintaining performance.
   - Reference: [Azure Landing Zones](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/)
2. **Secure Network Connectivity**:
   - **Hybrid Connectivity**: Secure on-premises to Azure communication using Azure ExpressRoute or VPN Gateway.
   - **Private Endpoints**: Use private endpoints to securely access Azure services.
   - **Azure Firewall**: Deploy Azure Firewall to inspect and filter traffic.
   - **DNS Security**: Use Azure Private DNS Zones for private endpoint resolution.
3. **Azure Governance**:
   - Have implemented Azure Governance to manage resources effectively, including:
     - Azure Management Groups for hierarchical organization.
     - Azure Blueprints for consistent resource deployment.
     - Azure Policy for compliance enforcement.
   - Reference: [Azure governance documentation | Microsoft Learn](https://learn.microsoft.com/en-us/azure/governance/)
4. **Well-Architected Framework**:
   - Have followed the **Azure Well-Architected Framework (WAF)** to ensure best practices for reliability, security, cost optimization, operational excellence, and performance efficiency.
   - Have established best practices  and processes to implement the security pillar defined by Azure WAF: [Security design principles - Microsoft Azure Well-Architected Framework | Microsoft Learn](https://learn.microsoft.com/en-us/azure/well-architected/security/principles). The principles include zero trust model, and the security principles of **confidentiality**, **integrity**, and **availability**, also known as the *CIA Triad*.
   - Reference: [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework)
6. **Security Baseline**:
   - Have established a security baseline for Azure resources, including:
     - Enabling **Azure Security Center** (Microsoft Defender for Cloud).
     - Configuring **Azure Monitor** and **Log Analytics** for centralized monitoring.
     - Setting up **Azure Sentinel** for Security Information and Event Management (SIEM).
7. **DevSecOps Practices**:
   - Have integrated **DevSecOps** practices into their development lifecycle, ensuring security is embedded into CI/CD pipelines.
   - Reference: [Security in DevOps (DevSecOps)](https://learn.microsoft.com/en-us/devops/operate/security-in-devops)