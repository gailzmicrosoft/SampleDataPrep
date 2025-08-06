# Azure Databricks TPC-H Sample Data Review

## Overview
This document captures the results of exploring TPC-H sample data available in Azure Databricks workspace for our multi-tier data architecture solution accelerator.

---

## Step 3: TPC-H Data Access and Validation Testing

### TPC-H Tables with Record Counts

| Table Name | Record Count | Description |
|------------|--------------|-------------|
| **customer** | 750,000 | Customer master data |
| **lineitem** | 29,999,795 | Order line items (largest table) |
| **nation** | 25 | Country/nation reference data |
| **orders** | 7,500,000 | Order headers |
| **part** | 1,000,000 | Product/part master data |
| **partsupp** | 4,000,000 | Part supplier relationships |
| **region** | 5 | Geographic regions |
| **supplier** | 50,000 | Supplier master data |

**Total Records:** ~43.3 million across all tables

---

## Sample Data Previews

### 👥 Customer Data Preview
```
+---------+------------------+------------+-----------+
|c_custkey|            c_name|c_mktsegment|c_nationkey|
+---------+------------------+------------+-----------+
|   412445|Customer#000412445|    BUILDING|         21|
|   412446|Customer#000412446|   MACHINERY|         20|
|   412447|Customer#000412447|  AUTOMOBILE|          7|
|   412448|Customer#000412448|   MACHINERY|          6|
|   412449|Customer#000412449|   HOUSEHOLD|         14|
+---------+------------------+------------+-----------+
```

**Key Fields for Mapping:**
- `c_custkey` → CustomerId
- `c_name` → CustomerName  
- `c_mktsegment` → CustomerSegment
- `c_nationkey` → NationKey (geographic reference)

### 📦 Product (Part) Data Preview
```
+---------+--------------------+--------+--------------------+-------------+
|p_partkey|              p_name| p_brand|              p_type|p_retailprice|
+---------+--------------------+--------+--------------------+-------------+
|   727497|misty burnished t...|Brand#32|MEDIUM BURNISHED ...|      1524.46|
|   727498|cornsilk blue kha...|Brand#25|STANDARD BRUSHED ...|      1525.46|
|   727499|spring lace cyan ...|Brand#41|SMALL BRUSHED NICKEL|      1526.46|
|   727500|indian tan black ...|Brand#14|PROMO POLISHED STEEL|      1527.47|
|   727501|burlywood seashel...|Brand#51|  LARGE PLATED BRASS|      1528.47|
+---------+--------------------+--------+--------------------+-------------+
```

**Key Fields for Mapping:**
- `p_partkey` → ProductId
- `p_name` → ProductName
- `p_brand` → BrandName
- `p_type` → ProductType
- `p_retailprice` → RetailPrice

### 🛒 Orders Data Preview
```
+----------+---------+-------------+------------+-----------+
|o_orderkey|o_custkey|o_orderstatus|o_totalprice|o_orderdate|
+----------+---------+-------------+------------+-----------+
|  13710944|   227285|            O|   162169.66| 1995-10-11|
|  13710945|   225010|            O|   252273.67| 1997-09-29|
|  13710946|   238820|            O|   179947.16| 1997-10-31|
|  13710947|   581233|            O|    33843.49| 1995-05-25|
|  13710948|    10033|            O|    42500.65| 1995-09-04|
+----------+---------+-------------+------------+-----------+
```

**Key Fields for Mapping:**
- `o_orderkey` → OrderId
- `o_custkey` → CustomerId (foreign key)
- `o_orderstatus` → OrderStatus
- `o_totalprice` → TotalAmount
- `o_orderdate` → OrderDate

### 📋 LineItem Data Preview
```
+----------+---------+----------+---------------+----------+
|l_orderkey|l_partkey|l_quantity|l_extendedprice|l_discount|
+----------+---------+----------+---------------+----------+
|  15997987|   295335|     50.00|       66516.00|      0.01|
|  15997988|   332059|     49.00|       53460.96|      0.08|
|  15997988|   904286|     37.00|       47738.88|      0.07|
|  15997988|   327898|     13.00|       25036.44|      0.09|
|  15997988|   973125|     29.00|       34744.32|      0.10|
+----------+---------+----------+---------------+----------+
```

**Key Fields for Mapping:**
- `l_orderkey` → OrderId (foreign key)
- `l_partkey` → ProductId (foreign key)
- `l_quantity` → Quantity
- `l_extendedprice` → ExtendedPrice
- `l_discount` → DiscountAmount

---

## Data Relationship Validation

### 🔗 Cross-Table Join Test Results
```
+------------------+----------+------------+-------------+----------+
|            c_name|o_orderkey|o_totalprice|o_orderstatus|line_items|
+------------------+----------+------------+-------------+----------+
|Customer#000081256|        65|   102231.29|            P|         3|
|Customer#000149641|       293|    54127.26|            F|         3|
|Customer#000474169|       418|    60931.63|            P|         3|
|Customer#000213527|       705|   114728.83|            O|         2|
|Customer#000375892|       964|   230430.47|            O|         4|
+------------------+----------+------------+-------------+----------+
```

✅ **Validation Results:**
- Customer → Orders → LineItems relationships work correctly
- Multi-table joins execute successfully
- Data integrity is maintained across tables

### 🌍 Geographic Reference Data
```
+---------+-----------+
|   n_name|     r_name|
+---------+-----------+
|  ALGERIA|     AFRICA|
|ARGENTINA|    AMERICA|
|   BRAZIL|    AMERICA|
|   CANADA|    AMERICA|
|    EGYPT|MIDDLE EAST|
| ETHIOPIA|     AFRICA|
|   FRANCE|     EUROPE|
|  GERMANY|     EUROPE|
|    INDIA|       ASIA|
|INDONESIA|       ASIA|
+---------+-----------+
```

✅ **Geographic Coverage:** 25 nations across 5 regions

---

## Schema Mapping Requirements

### Bronze → Silver Tier Mapping Needed

| **TPC-H Schema (Bronze)** | **Target Schema (Silver)** | **Transformation** |
|---------------------------|-----------------------------|--------------------|
| `tpch.customer.c_custkey` | `master_data.Customer.CustomerId` | Direct mapping |
| `tpch.customer.c_name` | `master_data.Customer.CustomerName` | Direct mapping |
| `tpch.customer.c_mktsegment` | `master_data.Customer.CustomerSegment` | Direct mapping |
| `tpch.part.p_partkey` | `master_data.Product.ProductId` | Direct mapping |
| `tpch.part.p_name` | `master_data.Product.ProductName` | Direct mapping |
| `tpch.part.p_brand` | `master_data.Product.BrandName` | Direct mapping |
| `tpch.orders.o_orderkey` | `sales.Order.OrderId` | Direct mapping |
| `tpch.orders.o_custkey` | `sales.Order.CustomerId` | Direct mapping |
| `tpch.lineitem.l_orderkey` | `sales.OrderLine.OrderId` | Direct mapping |
| `tpch.lineitem.l_partkey` | `sales.OrderLine.ProductId` | Direct mapping |

---

## Architecture Readiness Assessment

### ✅ Bronze Tier Data Source Validation

**Perfect for Solution Accelerator:**
- ✅ **Industry Standard:** TPC-H is universally recognized benchmark
- ✅ **Realistic Volume:** 43+ million records for performance testing
- ✅ **Different Schemas:** Requires mapping (demonstrates transformation)
- ✅ **Complete Relationships:** Customer → Orders → LineItems flow
- ✅ **Rich Data Types:** Strings, numbers, dates, decimals
- ✅ **Geographic Dimensions:** Nation/Region hierarchies available

### 🎯 Next Steps for Implementation

1. **Bronze Tier Setup:** TPC-H data ready as-is in Databricks
2. **Silver Tier Mapping:** Implement schema transformation notebooks
3. **Gold Tier Enhancement:** Add business metrics and KPIs
4. **Power BI Integration:** Connect to Gold tier for reporting

### 📊 Data Quality Metrics

- **Completeness:** ✅ All expected tables present
- **Consistency:** ✅ Cross-table relationships validated
- **Accuracy:** ✅ TPC-H standard data quality
- **Timeliness:** ✅ Immediately available for development

---

## Conclusion

✅ **TPC-H data in Azure Databricks provides an ideal Bronze tier data source for our solution accelerator**

🎯 **Ready for Bronze → Silver → Gold pipeline development**

📊 **Realistic enterprise data with schema mapping requirements perfectly demonstrates the value proposition**

🔄 **Next: Begin Silver tier transformation notebook development**



# Licensing and Disclaimer Suggestion 

Question: This is nice finding. Do we need a license to use this TPC-H dataset? 

Great question! The TPC-H dataset usage for development and demonstration purposes is generally acceptable, but let me clarify the licensing considerations:

## TPC-H Dataset Licensing Overview

### ✅ **What's Generally Allowed (Your Use Case):**

**Development & Education:**

- ✅ **Solution Accelerator Development** - Building enterprise architecture patterns
- ✅ **Proof of Concept** - Demonstrating Bronze→Silver→Gold pipelines
- ✅ **Training & Documentation** - Teaching data architecture concepts
- ✅ **Internal Testing** - Performance and functionality validation

**Your specific use case (building a solution accelerator with enterprise architecture patterns) falls into the educational/development category.**

### ⚠️ **What Requires Licensing:**

**Commercial Benchmarking:**

- ❌ **Publishing Performance Results** - Official TPC-H benchmark comparisons
- ❌ **Marketing Claims** - "Faster than TPC-H benchmark" statements
- ❌ **Competitive Analysis** - Formal database performance testing

### 🎯 **Recommendation for Your Solution Accelerator:**

**Totally Fine to Use Because:**

1. **Educational Purpose** - Teaching enterprise data architecture
2. **Development Tool** - Building reusable patterns and templates
3. **Sample Data Source** - Demonstrating schema mapping and transformation
4. **No Performance Claims** - Not publishing benchmark results

**Best Practices:**

- ✅ **Clear Attribution** - Mention "uses TPC-H sample data for demonstration"
- ✅ **Educational Context** - Emphasize learning and development purpose
- ✅ **No Benchmark Claims** - Don't publish performance comparisons
- ✅ **Alternative Data Option** - Offer to substitute with generated data if needed

### 📋 **Suggested Disclaimer for Your Documentation:**

**Data Source Attribution**

This solution accelerator uses TPC-H sample data for demonstration and 

educational purposes. TPC-H is an industry-standard dataset perfect for 

showcasing enterprise data architecture patterns. For production 

implementations, customers would use their own enterprise data sources.