SELECT
            id, 
            account_id, 
            name,
            type,
            description, 
            account_mapping, 
            created_date, 
            updated_date
        FROM chart_of_accounts
        WHERE 1=1
        AND type = '<coa_type>'