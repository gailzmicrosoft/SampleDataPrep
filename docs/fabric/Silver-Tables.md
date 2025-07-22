🎯 ANALYZING SILVER LAYER STRUCTURE ============================================================ 🔍 Discovering all tables in silver lakehouse...

 ✅ Found 57 tables total 🎯 PHASE 1 KEY TABLES IDENTIFICATION ============================================= 

✅ Found: Party -> Party 

✅ Found: Location -> Location 

✅ Found: Customer -> Customer 

✅ Found: Brand -> Brand 

✅ Found: Order -> Order 

✅ Found: OrderLine -> OrderLine 

✅ Found: Invoice -> Invoice 

✅ Found: InvoiceLine -> InvoiceLine 

📊 Phase 1 Status: 8/8 key tables found 



📊 ALL TABLES SUMMARY (Name & Column Count) 



📊 TABLE SUMMARY (Name & Column Count)
==================================================

🎯 PHASE 1 KEY TABLES IDENTIFICATION 

 1. Brand     🎯                       |  9 columns | 0 rows
 2. BrandCategory                  |  3 columns | 0 rows
 3. BrandProduct                   |  5 columns | 0 rows
 4. BrandType                      |  3 columns | 0 rows
 5. Customer  🎯                       |  9 columns | 0 rows
 6. CustomerAccount                | 13 columns | 0 rows
 7. CustomerAccountEmail           |  7 columns | 0 rows
 8. CustomerAccountLocation        |  8 columns | 0 rows
 9. CustomerAccountTelephoneNumber |  9 columns | 0 rows
10. CustomerGroup                  |  4 columns | 0 rows
11. CustomerLocation               |  8 columns | 0 rows
12. CustomerName                   |  6 columns | 0 rows
13. CustomerNameComponent          |  6 columns | 0 rows
14. CustomerNamePrefix             |  5 columns | 0 rows
15. CustomerNameSuffix             |  5 columns | 0 rows
16. CustomerRelationshipType       |  3 columns | 0 rows
17. CustomerStatusType             |  3 columns | 0 rows
18. CustomerTelephoneNumber        |  9 columns | 0 rows
19. CustomerTradeName              |  5 columns | 0 rows
20. CustomerType                   |  3 columns | 0 rows
21. HouseholdLocation              |  5 columns | 0 rows
22. IndividualCustomer             |  8 columns | 0 rows
23. Invoice      🎯                    | 20 columns | 0 rows
24. InvoiceLine      🎯                | 16 columns | 0 rows
25. Location        🎯                 | 19 columns | 0 rows
26. Order             🎯               | 78 columns | 0 rows
27. OrderActivityType              |  3 columns | 0 rows
28. OrderAdjustment                |  4 columns | 0 rows
29. OrderCharge                    |  5 columns | 0 rows
30. OrderChargeType                |  4 columns | 0 rows
31. OrderClassification            |  3 columns | 0 rows
32. OrderCondition                 |  3 columns | 0 rows
33. OrderDeliveryTerm              |  3 columns | 0 rows
34. OrderFinanceTerm               |  3 columns | 0 rows
35. OrderHold                      |  6 columns | 0 rows
36. OrderLanguageUsage             |  4 columns | 0 rows
37. OrderLine      🎯                  | 47 columns | 0 rows
38. OrderLineAdjustment            |  8 columns | 0 rows
39. OrderLineAdjustmentReason      |  3 columns | 0 rows
40. OrderLineCharge                |  6 columns | 0 rows
41. OrderLineHold                  |  7 columns | 0 rows
42. OrderLineStatus                |  5 columns | 0 rows
43. OrderPartyRelationshipType     |  3 columns | 0 rows
44. OrderPayment                   |  3 columns | 0 rows
45. OrderProcessingStatus          |  3 columns | 0 rows
46. OrderRelatedParty              |  4 columns | 0 rows
47. OrderSalesTerm                 |  3 columns | 0 rows
48. OrderStatus                    |  4 columns | 0 rows
49. OrderStatusType                |  3 columns | 0 rows
50. OrderType                      |  3 columns | 0 rows
51. Party      🎯                      |  4 columns | 0 rows
52. PartyLocation                  |  8 columns | 0 rows
53. PartyTelephoneNumber           |  9 columns | 0 rows
54. Retailer                       |  8 columns | 0 rows
55. SalesOrderCondition            |  3 columns | 0 rows
56. UsLocation                     |  3 columns | 0 rows
57. UsaLocation                    | 19 columns | 0 rows

======================================================= 

🔍 DETAILED STRUCTURE FOR PHASE 1 KEY TABLES ======================================================= 

📊 TABLE: Party --------------- Columns (4):  

• PartyId                   | StringType()         | NOT NULL  

• PartyName                 | StringType()         | NULL  

• PartyTypeId               | StringType()         | NULL  

• GlobalLocationNumber      | DecimalType(13,1)    | NULL 

======================================================= 

📊 TABLE: Location ------------------ Columns (19):  

• LocationId                | StringType()         | NOT NULL  

• LocationName              | StringType()         | NULL  

• LocationDescription       | StringType()         | NULL  

• LocationAddressLine1      | StringType()         | NULL  

• LocationAddressLine2      | StringType()         | NULL  

• LocationCity              | StringType()         | NULL  

• LocationStateId           | StringType()         | NULL  

• LocationZipCode           | DecimalType(11,1)    | NULL 

• LocationNote              | StringType()         | NULL  

• LocationLatitude          | DecimalType(10,7)    | NULL  

• LocationLongitude         | DecimalType(10,7)    | NULL  

• LocationDatum             | StringType()         | NULL  

• LocationElevation         | DecimalType(18,8)    | NULL  

• LocationElevationUnitOfMeasureId | StringType()         | NULL  

• GlobalLocationNumber      | DecimalType(13,1)    | NULL  

• TimezoneId                | StringType()         | NULL  

• DaylightSavingsTimeObservedIndicator | BooleanType()        | NULL  

• CountryId                 | StringType()         | NULL  

• SubdivisionId             | StringType()         | NULL 

======================================================= 

📊 TABLE: Customer ------------------ Columns (9):  

• CustomerId                | StringType()         | NOT NULL  

• CustomerEstablishedDate   | DateType()           | NULL 

 • CustomerTypeId            | StringType()         | NULL  

• ResponsibilityCenterId    | StringType()         | NULL  

• LedgerId                  | StringType()         | NULL  

• LedgerAccountNumber       | StringType()         | NULL 

 • CustomerNote              | StringType()         | NULL  

• PartyId                   | StringType()         | NULL  

• GlobalLocationNumber      | DecimalType(13,1)    | NULL 

======================================================= 

📊 TABLE: Brand --------------- Columns (9):  

• BrandId                   | StringType()         | NOT NULL  

• BrandName                 | StringType()         | NULL  

• BrandDescription          | StringType()         | NULL  

• BrandMark                 | BinaryType()         | NULL  

• BrandTrademark            | BinaryType()         | NULL  

• BrandLogo                 | BinaryType()         | NULL  

• BrandTypeId               | StringType()         | NULL  

• BrandCategoryId           | StringType()         | NULL  

• BrandOwningPartyId        | StringType()         | NULL 

======================================================= 

📊 TABLE: Order --------------- Columns (78): 

 • OrderId                   | StringType()         | NULL  

• OrderConfirmationNumber   | StringType()         | NULL  

• OrderEnteredByEmployeeId  | StringType()         | NULL 

 • NumberOfOrderLines        | IntegerType()        | NULL  

• OrderReceivedTimestamp    | TimestampType()      | NULL  

• OrderEntryTimestamp       | TimestampType()      | NULL 

 • CustomerCreditCheckTimestamp | TimestampType()      | NULL 

 • OrderConfirmationTimestamp | TimestampType()      | NULL 

 • OrderRequestedDeliveryDate | DateType()           | NULL 

 • OrderCommittedDeliveryDate | DateType()           | NULL  

• ShipmentConfirmationTimestamp | TimestampType()      | NULL  

• OrderActualDeliveryTimestamp | TimestampType()      | NULL 

 • OrderTotalRetailPriceAmount | DecimalType(18,2)    | NULL  

• OrderTotalActualSalesPriceAmount | DecimalType(18,2)    | NULL  

• OrderTotalAdjustmentPercentage | DecimalType(18,8)    | NULL  

• OrderTotalAdjustmentAmount | DecimalType(18,2)    | NULL  

• OrderTotalAmount          | DecimalType(18,2)    | NULL 

 • TotalShippingChargeAmount | DecimalType(18,2)    | NULL  

• OrderTotalTaxAmount       | DecimalType(18,2)    | NULL 

 • OrderTotalInvoicedAmount  | DecimalType(18,2)    | NULL  

• TotalGratuityAmount       | DecimalType(18,2)    | NULL  

• TotalPaidAmount           | DecimalType(18,2)    | NULL  

• TotalCommissionsPayableAmount | DecimalType(18,2)    | NULL  

• SplitCommissionsIndicator | BooleanType()        | NULL  

• OrderBookedDate           | DateType()           | NULL 

 • OrderBilledDate           | DateType()           | NULL  

• OrderBacklogReportedDate  | DateType()           | NULL 

 • OrderBacklogReleasedDate  | DateType()           | NULL 

 • OrderCancellationDate     | DateType()           | NULL  

• OrderReturnedDate         | DateType()           | NULL 

 • ShipmentToName            | StringType()         | NULL  

• ShipmentToLocationId      | StringType()         | NULL  

• ShipmentId                | StringType()         | NULL 

 • CarrierId                 | StringType()         | NULL  

• ShipmentMethodId          | StringType()         | NULL  

• RequestedShipmentCarrierName | StringType()         | NULL  

• AlternateCarrierAcceptableIndicator | BooleanType()        | NULL 

 • ActualShipmentCarrierName | StringType()         | NULL  

• ShipOrderCompleteIndicator | BooleanType()        | NULL  

• TotalOrderWeight          | DecimalType(18,8)    | NULL 

 • WeightUomId               | StringType()         | NULL 

 • TotalOrderFreightChargeAmount | DecimalType(18,2)    | NULL 

 • EarliestDeliveryWindowTimestamp | TimestampType()      | NULL 

 • LatestDeliveryWindowTimestamp | TimestampType()      | NULL  

• AcknowledgementRequiredIndicator | BooleanType()        | NULL  

• ExpediteOrderIndicator    | BooleanType()        | NULL  

• DropShipmentIndicator     | BooleanType()        | NULL  

• ServiceOrderIndicator     | BooleanType()        | NULL 

 • ProductOrderIndicator     | BooleanType()        | NULL  

• OrderDeliveryInstructions | StringType()         | NULL  

• CustomerCreditCheckNote   | StringType()         | NULL  

• MessageToCustomer         | StringType()         | NULL  

• CustomerId                | StringType()         | NULL  

• CustomerAccountId         | StringType()         | NULL  

• WarehouseId               | StringType()         | NULL 

 • StoreId                   | StringType()         | NULL 

 • CustomerIdentificationMethodId | StringType()         | NULL 

 • PoNumber                  | StringType()         | NULL  

• MarketingEventId          | StringType()         | NULL  

• AdvertisingEventId        | StringType()         | NULL 

 • SalesMethodId             | StringType()         | NULL  

• PaymentMethodId           | StringType()         | NULL  

• BillingCycleId            | StringType()         | NULL 

 • ContractId                | StringType()         | NULL 

 • SalesChannelId            | StringType()         | NULL  

• DistributionChannelId     | StringType()         | NULL 

 • OrderTypeId               | StringType()         | NULL 

 • OrderClassificationId     | StringType()         | NULL 

 • RejectionReasonId         | StringType()         | NULL 

 • OrderProcessingStatusId   | StringType()         | NULL  

• IsoCurrencyCode           | StringType()         | NULL  

• PointOfSaleId             | StringType()         | NULL 

 • ResponsibilityCenterId    | StringType()         | NULL  

• VendorId                  | StringType()         | NULL  

• DeviceId                  | StringType()         | NULL  

• SoftwareProductId         | StringType()         | NULL  

• SoftwareProductVersionNumber | IntegerType()        | NULL 

 • PromotionOfferId          | StringType()         | NULL 

======================================================= 

📊 TABLE: OrderLine ------------------- Columns (47):  

• OrderId                   | StringType()         | NULL  

• OrderLineNumber           | IntegerType()        | NOT NULL 

 • ProductId                 | StringType()         | NULL  

• ItemSku                   | StringType()         | NULL 

 • Quantity                  | DecimalType(18,2)    | NULL 

 • ProductListPriceAmount    | DecimalType(18,2)    | NULL 

 • ProductSalesPriceAmount   | DecimalType(18,2)    | NULL 

 • ProductAdjustmentAmount   | DecimalType(18,2)    | NULL 

 • ProductAdjustmentPercentage | DecimalType(18,8)    | NULL 

 • TotalOrderLineAdjustmentAmount | DecimalType(18,2)    | NULL  

• TotalOrderLineAmount      | DecimalType(18,2)    | NULL  

• PriceUomId                | StringType()         | NULL 

 • QuantityBooked            | IntegerType()        | NULL  

• QuantityBilled            | IntegerType()        | NULL  

• QuantityBacklog           | IntegerType()        | NULL  

• AcceptedQuantity          | DecimalType(18,2)    | NULL  

• QuantityCancelled         | IntegerType()        | NULL  

• QuantityReturned          | IntegerType()        | NULL 

 • QuantityUomId             | StringType()         | NULL  

• BookedDate                | DateType()           | NULL  

• BilledDate                | DateType()           | NULL  

• CancelledTimestamp        | TimestampType()      | NULL  

• ReturnedDate              | DateType()           | NULL  

• RequestedDeliveryDate     | DateType()           | NULL  

• CommittedDeliveryDate     | DateType()           | NULL  

• PlannedPickDate           | DateType()           | NULL  

• ActualPickTimestamp       | TimestampType()      | NULL  

• PlannedShipmentDate       | DateType()           | NULL  

• ActualShipmentTimestamp   | TimestampType()      | NULL  

• PlannedDeliveryDate       | DateType()           | NULL  

• ActualDeliveryTimestamp   | TimestampType()      | NULL  

• ShipmentConfirmationTimestamp | TimestampType()      | NULL 

 • DropShipOrderLineItemIndicator | BooleanType()        | NULL  

• WaybillNumber             | IntegerType()        | NULL  

• TareWeight                | DecimalType(18,8)    | NULL  

• NetWeight                 | DecimalType(18,8)    | NULL 

 • WeightUomId               | StringType()         | NULL  

• EarliestDeliveryWindowTimestamp | TimestampType()      | NULL  

• LatestDeliveryWindowTimestamp | TimestampType()      | NULL 

 • ReturnToStockIndicator    | BooleanType()        | NULL  

• ReturnToStoreIndicator    | BooleanType()        | NULL 

 • OrderLineTypeId           | StringType()         | NULL  

• RejectionReasonId         | StringType()         | NULL  

• WorkOrderId               | StringType()         | NULL 

 • TaskId                    | StringType()         | NULL  

• BuyClassId                | StringType()         | NULL  

• PromotionOfferId          | StringType()         | NULL 

======================================================= 

📊 TABLE: Invoice ----------------- Columns (20):  

• InvoiceId                 | StringType()         | NOT NULL  

• CustomerAccountId         | StringType()         | NULL 

 • InvoiceDate               | DateType()           | NULL 

 • InvoiceToName             | StringType()         | NULL  

• InvoiceToPartyId          | StringType()         | NULL  

• InvoiceToLocationId       | StringType()         | NULL  

• InvoiceToTelephoneNumber  | DecimalType(15,1)    | NULL  

• InvoiceToFaxNumber        | DecimalType(15,1)    | NULL  

• InvoiceToEmailAddress     | StringType()         | NULL  

• InvoiceNote               | StringType()         | NULL  

• TotalInvoiceProductAmount | DecimalType(18,2)    | NULL  

• TotalInvoiceChargesAmount | DecimalType(18,2)    | NULL 

 • TotalInvoiceAdjustmentsAmount | DecimalType(18,2)    | NULL  

• TotalInvoiceTaxesAmount   | DecimalType(18,2)    | NULL  

• TotalInvoiceAmount        | DecimalType(18,2)    | NULL  

• InvoiceModeId             | StringType()         | NULL  

• IsoCurrencyCode           | StringType()         | NULL  

• InvoiceStatusId           | StringType()         | NULL  

• IsoLanguageId             | StringType()         | NULL  

• OrderId                   | StringType()         | NULL 

======================================================= 

📊 TABLE: InvoiceLine --------------------- Columns (16):  

• InvoiceId                 | StringType()         | NULL 

 • InvoiceLineNumber         | IntegerType()        | NOT NULL  

• Quantity                  | DecimalType(18,2)    | NULL  

• UnitPriceAmount           | DecimalType(18,2)    | NULL 

 • SalesPriceAmount          | DecimalType(18,2)    | NULL 

 • InvoiceLineItemNote       | StringType()         | NULL 

 • ProductId                 | StringType()         | NULL 

 • ItemSku                   | StringType()         | NULL 

 • TotalProductInvoiceAmount | DecimalType(18,2)    | NULL  

• ChargeId                  | StringType()         | NULL  

• InvoiceLineChargeAmount   | DecimalType(18,2)    | NULL  

• InvoiceLineAdjustmentsAmount | DecimalType(18,2)    | NULL 

 • OrderLineNumber           | IntegerType()        | NULL 

 • IsoCurrencyCode           | StringType()         | NULL  

• InvoiceLineTypeId         | StringType()         | NULL  

• OrderId                   | StringType()         | NULL 





