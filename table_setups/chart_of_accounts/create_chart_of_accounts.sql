CREATE TABLE radna_db.chart_of_accounts (
	id UUID DEFAULT gen_random_uuid() NOT NULL,
    account_id VARCHAR(30) NOT NULL,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    description VARCHAR(50),
    account_mapping VARCHAR(30),
    created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (id),
    UNIQUE (account_id),
    UNIQUE (name)
);