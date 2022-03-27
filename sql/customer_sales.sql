SELECT
    BillingState AS state
  , sum(Total) AS total_sales
FROM
    chinook.invoices
    JOIN analysis_customers USING (CustomerId)
GROUP BY
    BillingState
