SELECT * 
FROM public.orders
WHERE customer_first_name = 'Mikaela'; 

SELECT * 
FROM public.orders
WHERE customer_first_name = 'Mikaela'
  AND customer_last_name = 'Lee'
  ORDER BY order_date
  --ORDER BY order_date DESC
LIMIT 5;