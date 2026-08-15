SELECT
    month,
    year
FROM accounting_periods
WHERE 1=1
AND month = :period_month
AND year = :period_year