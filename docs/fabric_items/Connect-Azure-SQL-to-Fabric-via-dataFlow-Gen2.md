### **step-by-Step: Connect Azure SQL to Fabric via Dataflows Gen2**

#### **1. Prerequisites**

- An **Azure SQL Database** with your data (e.g., WideWorldImporters).
- A **Microsoft Fabric workspace** with Data Factory enabled.
- Appropriate **permissions** to access both environments.

------

#### **2. Set Up the Azure SQL Connection in Fabric**

1. Go to your **Fabric workspace**.

2. Select **Data Factory** from the left pane.

3. Click **“Manage connections and gateways”** from the settings menu.

4. Click **“+ New”** to create a new connection.

5. In the

    

   New connection pane

   :

   - **Connection type**: Select **SQL Server**.

   - **Server**: Enter your Azure SQL server name (e.g., `yourserver.database.windows.net`).

   - **Database**: Enter the name of your Azure SQL DB.

   - Authentication

     : Choose one of the supported types:

     - **Basic** (username/password)
     - **Organizational account** (OAuth2)
     - **Service Principal** (for enterprise setups)