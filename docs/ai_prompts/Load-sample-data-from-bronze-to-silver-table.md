I need to write a new notebook with name already created for you to fill in. The notebook will be attached to Fabric Lakehouse named **MAAG_LH_SILVER** (default, you don't need to specify the name in notebook, it is assumed). In this lake house, we created tables with schema name '**shared**'. now I need to load the sample data in MAAG_LH_Bronze, location: 'Files/samples_fabric/shared/CustomerRelationshipType_Samples.csv. The data needs to be loaded to the Table CustomerRelationshipType under schema 'shared'. The table schema is defined in this file named Model_Shared_Data.ipynb



GitHub Copilot has trouble with the correct path pointing to the source file. Codd did not work. 

I need to search documents to guide Copilot: 



[Load data into your lakehouse with a notebook - Microsoft Fabric | Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-load-data)



It still comes up with code that not working. I then point to the specific code 





`import pandas as pd df = pd.read_parquet("abfss://DevExpBuildDemo@msit-onelake.dfs.fabric.microsoft.com/Marketing_LH.Lakehouse/Files/sample.parquet")`



Found this path from Fabric Workspace, and give it to Copilot. 

"abfss://Fabric_MAAG@onelake.dfs.fabric.microsoft.com/MAAG_LH_Bronze.Lakehouse/Files/samples_fabric/shared/CustomerRelationshipType_Samples.csv"



==========================================================================

This is a good piece of work. Thanks for the partnership. 



Now I need another notebook, lets name it **Load_Table_Silver_to_Gold_CustomerRelationshipType.ipynb.** This time, from MAAG_LH_Silver Lakehouse Table CustomerRelationshipType (schema name: shared)  to MAAG_LH_Gold Lakehouse table CustomerRelationshipType with schema 'shared'. This time, the the MAAG_LH_Gold lakehouse will be attached as default lakehouse. You only need to define source as absolute path. 

Let me know if you have questions. 

