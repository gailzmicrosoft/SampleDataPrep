Yes, Microsoft Fabric **still supports creating a warehouse with sample data**, including **AdventureWorks-style data**, but the process is slightly different from the older Synapse experience. Here's how you can do it now:

------

### ✅ **How to Create a Warehouse with Sample Data in Microsoft Fabric**

1. **Go to the Microsoft Fabric Portal**
    Navigate to Microsoft Fabric and sign in.
2. **Open the Home Hub**
    In the left navigation pane, select the **Home** hub.
3. **Create a Sample Warehouse**
   - Under the **"New"** section, look for the **"Warehouse sample"** card.
   - Click it, give your warehouse a name, and select **Create**.
4. **Automatic Data Load**
   - Fabric will automatically create a new **Warehouse** and load **sample data** into it.
   - This includes **tables and views** similar to what you’d find in AdventureWorksDW.
   - The data is ready for querying using **T-SQL**.
5. **Use Sample Data in Existing Warehouse**
   - If you already have a warehouse, you can still load sample data by selecting the **"Use sample database"** card from the warehouse interface.

🔗 [Full Microsoft Learn Guide](https://learn.microsoft.com/en-us/fabric/data-warehouse/create-warehouse-sample) [[1\]](https://learn.microsoft.com/en-us/fabric/data-warehouse/create-warehouse-sample)

------

Would you like help exploring the tables that get created or writing queries to extract specific insights from this sample data?


References

[1] [Create a Warehouse Sample - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-warehouse/create-warehouse-sample)