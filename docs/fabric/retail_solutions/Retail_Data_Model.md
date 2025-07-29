After the fabric retail solution is deployed, you will have File with type `Retail solutions`. This file holds all information together. You will have three lake houses named with below suffixes: 

- _IDM_LH_bronze   (where you would upload your source data sets)
- _IDM_LH_silver      (where the standard retail data models are deployed, which can be extended dynamically) 
- _IDM_LH_gold        (where the data is ready for analytics and queries from PBI to generate insights)

 

You can update the entities of retail data models by below steps 

1. Click the retail solution file 

2. In middle of the screen see heading "Manage deployed capabilities", under it you will see the 'Retail industry data model'. Click it. 

3. You will be brought to a GUI to see what has been deployed. You can add or subtract entities from here (if the data model does not have data populated yet)

   

For reference, you can review [medallion lakehouse architecture page](https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion) for more information. 

