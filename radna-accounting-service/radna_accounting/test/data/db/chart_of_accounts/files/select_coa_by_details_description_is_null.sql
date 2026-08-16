SELECT
    account_id,
    name,
    type,
    description,
    account_mapping,
    created_date,
    updated_date
FROM chart_of_accounts
WHERE 1=1
AND account_id = :coa_account_id
AND name = :coa_name
AND type = :coa_type
AND description IS NULL
AND (
    account_mapping IS NULL
    OR (
        account_mapping IS NOT NULL
        AND account_mapping = :coa_account_mapping
    )
)