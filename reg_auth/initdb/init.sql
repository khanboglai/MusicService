CREATE TABLE IF NOT EXISTS users ( 
    user_id BIGINT generated always as identity PRIMARY KEY, 
    user_login VARCHAR(100) NOT NULL, 
    password_hash VARCHAR(255) NOT NULL,
    user_role VARCHAR(20) NOT NULL
); 

