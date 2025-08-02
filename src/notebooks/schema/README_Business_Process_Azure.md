# Enterprise Simplified Data Model and Business Process (Sales and Finance Domains with Shared Master Customer and Product Data) 

## Overview

This document describes the enterprise data architecture consisting of shared master data and domain-specific business processes. The model reduces complexity from 64 tables in one domain (Sales) to 16 tables for two domains (Sales and Finance) while maintaining essential business functionality to showcase **Order-to-Cash (O2C)** business process, that operates on Microsoft Fabric Platform.

## Microsoft Fabric Lakehouse Architecture

### Three-Lakehouse Shortcut Architecture
This architecture leverages Microsoft Fabric Shortcuts to enable domain separation while maintaining data consistency without duplication.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Master Data    │    │  Sales Domain   │    │ Finance Domain  │
│   Lakehouse     │    │   Lakehouse     │    │   Lakehouse     │
│                 │    │                 │    │                 │
│ • Customer      │◄───┤ → Customer*     │◄───┤ → Customer*     │
│ • Product       │◄───┤ → Product*      │    │ → Product*      │
│ • Location      │    │ • Order         │◄───┤ → Order*        │
│ • Category      │    │ • OrderLine     │◄───┤ → OrderLine*    │
│ • CustomerXXX   │    │ • OrderPayment  │◄───┤ → OrderPayment* │
│   (9 tables)    │    │   (3 tables)    │    │ • Account       │
└─────────────────┘    └─────────────────┘    │ • Invoice       │
                                              │ • Payment       │
                                              │ • Transaction   │
                                              │   (4 + 5* tables)│
                                              └─────────────────┘

* = Shortcut to other Lakehouses (no data duplication)
```

### Shortcut Benefits
- **Zero Data Duplication**: Customer and Product data exists only in Master Data Lakehouse
- **Cross-Domain Access**: Finance can directly access Sales data via shortcuts
- **Real-time Consistency**: All domains see same master data instantly via shortcuts
- **Domain Isolation**: Each team manages their own lakehouse independently
- **Performance Optimized**: Shortcuts provide near-native performance within same region

### Enhanced Cross-Domain Capabilities
```
Finance Domain Cross-Domain Queries:
• Join Customer* (Master Data) + Invoice (Finance) 
• Join Product* (Master Data) + Order* (Sales) + Transaction (Finance)
• Join Order* (Sales) + Payment (Finance) for O2C reporting
```

## Data Processing Pipeline Architecture

### Order-to-Cash Data Flow Pipeline
This diagram shows how data flows from Master Data and Sales Domain to update/append Finance tables through processing notebooks.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Master Data    │    │  Sales Domain   │    │ Finance Domain  │
│   (Populated)   │    │   (Populated)   │    │ (Existing Data) │
│                 │    │                 │    │                 │
│ ✓ Customer      │    │ ✓ Order         │    │ ◐ Account       │
│ ✓ Product       │    │ ✓ OrderLine     │    │ ◐ Invoice       │
│ ✓ Location      │    │ ✓ OrderPayment  │    │ ◐ Payment       │
│ ✓ Category      │    │                 │    │ ◐ Transaction   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────┐    ┌──────┘                       │
                     │    │                              │
                     ▼    ▼                              ▼
            ┌─────────────────────────────────────────────────┐
            │          Data Processing Pipeline               │
            │                      (MVP/POC)                  │
            │                                                 │
            │  📓 Process_Order_to_Invoice.ipynb             │
            │  📓 Process_Payment_to_Transaction.ipynb       │
            │                                                 │
            │  Future: Complex Finance Business Logic        │
            │  📓 Process_Chart_of_Accounts.ipynb (Future)   │
            │  📓 Process_Financial_Reporting.ipynb (Future) │
            └─────────────────────────────────────────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────┐
                     │    Finance Domain       │
                     │      (Updated)          │
                     │                         │
                     │ ✓ Account (existing)    │
                     │ ✓ Invoice (+ new)       │
                     │ ✓ Payment (+ new)       │
                     │ ✓ Transaction (+ new)   │
                     └─────────────────────────┘

✓ = Populated Data
◐ = Existing Data (to be updated/appended)
📓 = Processing Notebook
```

### Pipeline Processing Notebooks (MVP Scope)

#### 1. Process_Order_to_Invoice.ipynb (MVP)
```
Purpose: Generate invoices from new completed orders
Input:   Sales.Order + Sales.OrderLine + Master.Customer
Output:  Finance.Invoice (APPEND new invoices)
Logic:   
  - Filter NEW Orders with status = 'Completed'
  - Filter out Orders already invoiced
  - Aggregate OrderLine amounts
  - Create Invoice record per Order
  - Link to Customer via CustomerId
```

#### 2. Process_Payment_to_Transaction.ipynb (MVP)
```
Purpose: Create financial transactions from new payments
Input:   Sales.OrderPayment + Finance.Invoice + Finance.Account
Output:  Finance.Payment + Finance.Transaction (APPEND new records)
Logic:   
  - Filter NEW OrderPayments not yet processed
  - Match OrderPayment to existing Invoice
  - Create Payment record
  - Generate basic Transaction records
  - Simple accounting entries (no complex business rules)
```

### Future Finance Business Logic (Out of MVP Scope)
```
📓 Process_Chart_of_Accounts.ipynb (Future)
   - Complex account hierarchy management
   - Account code standardization
   - Multi-currency handling

📓 Process_Financial_Reporting.ipynb (Future)
   - Month-end close procedures
   - Account reconciliation
   - Financial statement generation
   - Compliance reporting
```

### Data Processing Sequence (MVP)
```
Step 1: Process New Sales to Finance
├── Run Process_Order_to_Invoice.ipynb
└── Run Process_Payment_to_Transaction.ipynb

Step 2: Future Enhancement
└── Add complex Finance business logic notebooks
```

## Order-to-Cash (O2C) Business Process

**Order-to-Cash** is a fundamental enterprise business process that encompasses the complete customer transaction lifecycle - from initial order placement through final payment receipt and cash application.

### Standard O2C Process Flow
```
1. Order Creation      → Sales Domain (Order Management)
2. Order Processing    → Sales Domain (OrderLine, Pricing)
3. Order Fulfillment   → Sales Domain (OrderPayment)
4. Invoice Generation  → Finance Domain (Billing)
5. Payment Processing  → Finance Domain (Collections)
6. Cash Application    → Finance Domain (Accounting)
```

### Our Implementation
Our simplified model captures the core O2C process across two domains:
- **Sales Domain**: Handles customer orders and initial payment processing
- **Finance Domain**: Manages invoicing, payment tracking, and financial accounting

## Architecture Principles

### Domain-Driven Design
- **Shared Master Data**: Single source of truth for Customer, Product, Location entities
- **Sales Domain**: Order processing and customer transactions
- **Finance Domain**: Invoicing, payments, and financial transactions
- **Clean Separation**: Each domain manages its own business logic while sharing master data

### Enterprise Benefits
- **Scalability**: Easy to add new domains (HR, Supply Chain, Inventory)
- **Data Governance**: Centralized master data management
- **Performance**: Flexible deployment options (shared vs. synchronized)
- **Maintenance**: Lower complexity and operational costs

## Schema Architecture

### 1. Master Data Foundation (`master_data` schema)
**Purpose**: Shared reference data used across all business domains

#### Customer Master Data (7 tables)
- **Customer**: Core customer information (individuals, businesses, government)
- **CustomerTradeName**: Business trade names and periods
- **CustomerRelationshipType**: VIP, Premium, Standard classifications
- **Location**: Physical addresses with geospatial data
- **CustomerLocation**: Customer-to-location relationships with time periods
- **CustomerAccount**: Customer account management
- **CustomerAccountLocation**: Account-to-location relationships

#### Product Master Data (2 tables)
- **Product**: Complete product catalog with pricing, status, lifecycle dates
- **Category**: Product categorization and brand information

### 2. Sales Domain (`retail_simple` schema)
**Purpose**: Order processing and sales transactions

#### Sales Tables (3 tables)
- **Order**: Sales order headers with customer, totals, shipping, billing
- **OrderLine**: Individual line items with product, quantity, pricing
- **OrderPayment**: Payment processing and transaction tracking

#### Key Integrations
- `Order.CustomerId` → `master_data.Customer.CustomerId`
- `OrderLine.ProductId` → `master_data.Product.ProductId`

### 3. Finance Domain (`retail_simple` schema)
**Purpose**: Financial accounting and transaction management

#### Finance Tables (4 tables)
- **Account**: Chart of accounts (Assets, Liabilities, Revenue, Expenses)
- **Invoice**: Customer billing linked to sales orders
- **Payment**: Customer payment processing and tracking
- **Transaction**: Double-entry accounting transactions

#### Key Integrations
- `Invoice.CustomerId` → `master_data.Customer.CustomerId`
- `Invoice.OrderId` → `retail_simple.Order.OrderId`
- `Payment.CustomerId` → `master_data.Customer.CustomerId`
- `Transaction.OrderId` → `retail_simple.Order.OrderId`

## Business Process Flows

### Core Order-to-Cash (O2C) Process
**Assumption**: Customers are already onboarded and business is generating sales

```
Order-to-Cash Process Flow:

1. ORDER MANAGEMENT (Sales Domain)
   Customer places order → retail_simple.Order
   Add line items → retail_simple.OrderLine  
   Process payment → retail_simple.OrderPayment

2. FINANCIAL PROCESSING (Finance Domain)
   Generate invoice → retail_simple.Invoice (linked to Order)
   Record payment → retail_simple.Payment (linked to Invoice)
   Create accounting entries → retail_simple.Transaction

3. CASH APPLICATION (Finance Domain)
   Revenue Recognition:
   - Debit: Accounts Receivable (Asset)
   - Credit: Sales Revenue (Revenue)
   
   Payment Receipt:
   - Debit: Cash (Asset)
   - Credit: Accounts Receivable (Asset)
```

### Enterprise O2C Data Pipeline
```
Master Data → Sales Domain → Finance Domain
     ↓             ↓              ↓
  Customer     →  Order    →   Invoice
  Product      →  OrderLine →   Payment  
  Location                  →   Transaction
                             →   Account
```

## Implementation Guidelines

### Deployment Sequence
1. **Run Model_Shared_Data.ipynb** - Creates master data foundation (Customer, Product, Location)
2. **Run Model_Sales_Domain.ipynb** - Creates sales tables with FK references (Order processing)
3. **Run Model_Finance_Domain.ipynb** - Creates finance tables with FK references (Cash management)

### Schema Options
- **Option 1**: Three separate lakehouses with shortcuts (Recommended for Fabric)
- **Option 2**: Separate databases (`master_data` + `retail_simple`)
- **Option 3**: Single database (`retail_simple` for all tables)
- **Option 4**: Cloud deployment with synchronization processes

## Cross-Domain Relationships

### Master Data References
| Domain | Table | References Master Data |
|--------|-------|----------------------|
| Sales | Order | Customer.CustomerId |
| Sales | OrderLine | Product.ProductId |
| Finance | Invoice | Customer.CustomerId |
| Finance | Transaction | Customer.CustomerId |

### Inter-Domain References
| Source Domain | Target Domain | Relationship |
|---------------|---------------|-------------|
| Sales.Order | Finance.Invoice | OrderId |
| Sales.OrderPayment | Finance.Payment | Business Logic |
| Finance.Invoice | Finance.Payment | InvoiceId |
| Finance.Payment | Finance.Transaction | TransactionId |

## Data Governance

### Master Data Management
- **Customer Data**: Single source managed in `master_data.Customer`
- **Product Data**: Centralized catalog in `master_data.Product`
- **Reference Data**: Shared lookups (CustomerRelationshipType, Category)

### Data Quality Rules
- **Referential Integrity**: All foreign keys must reference valid master data
- **Business Rules**: SellStartDate > CreatedDate, Payment ≤ Invoice Amount
- **Audit Trail**: CreatedBy/UpdatedBy fields on key entities

## Sample Data Generation

### Current Capabilities
- **Product Samples**: 295 records with realistic distributions (brands, dates, status)
- **Customer Samples**: 513 records with phone numbers, demographics, relationship types
- **Business Rules**: Date validation, status distributions, brand allocation (Fabrikam 70%, Alpine Ski House 30%)

### Planned Extensions
- **Order Generation**: Link to Customer and Product samples (O2C order creation)
- **Invoice Generation**: Derive from Order data (O2C billing process)
- **Payment Generation**: Realistic payment patterns and methods (O2C cash receipt)

## Enterprise Value Proposition

### Business Benefits
- **Industry Standard**: Implements proven Order-to-Cash business process
- **Compliance Ready**: Supports financial reporting and audit requirements
- **Scalable Architecture**: Ready for additional domains (Supply Chain, HR, CRM)
- **Microsoft Fabric Optimized**: Built for modern cloud data platforms with Shortcuts

### Technical Benefits
- **75% Complexity Reduction**: From 64 to 16 tables while maintaining functionality
- **Domain Separation**: Clean boundaries between Sales and Finance operations
- **Master Data Governance**: Single source of truth for Customer and Product data
- **Performance Optimized**: Delta Lake format with Spark processing and Fabric Shortcuts
- **Zero ETL**: No data movement or synchronization jobs between domains
- **Domain Separation**: Clean boundaries between Sales and Finance operations
- **Master Data Governance**: Single source of truth for Customer and Product data
- **Performance Optimized**: Delta Lake format with Spark processing and Fabric Shortcuts
- **Zero ETL**: No data movement or synchronization jobs between domains
