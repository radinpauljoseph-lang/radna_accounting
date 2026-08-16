SELECT
    month,
    year
    id
FROM transaction_ids
WHERE 1=1
AND month = :ti_month
AND year = :ti_year
AND id = :ti_id