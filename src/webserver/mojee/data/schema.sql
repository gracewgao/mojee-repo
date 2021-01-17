-- table for users
CREATE TABLE IF NOT EXISTS user (
    id SERIAL,
    username VARCHAR(100) NOT NULL UNIQUE,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    created_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    updated_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
);

-- admin user
WITH exst AS (
    SELECT id
    FROM user 
    WHERE username = 'admin'
)
INSERT INTO user
(id, username, email_address)
SELECT 0 AS id, 'admin' AS username, 'admin@mojee.com' AS email_address
WHERE NOT EXISTS (SELECT id FROM exst);


-- images table
CREATE TABLE IF NOT EXISTS images ( 
    image_id SERIAL,
    filename VARCHAR(37) NOT NULL UNIQUE,
    detail VARCHAR(300),
    created_on DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
    owner_id INT NOT NULL REFERENCES user(id) DEFAULT 0,
);


-- many-to-many associations for keywords and images
CREATE TABLE IF NOT EXISTS keywords_images (
    id SERIAL,
    image_id INT NOT NULL REFERENCES images(image_id),
    keyword VARCHAR(100) NOT NULL,
    score INT NOT NULL,
);


-- many-to-many associations for mojees and keywords
CREATE TABLE IF NOT EXISTS mojees_keywords (
    id SERIAL,
    emoji VARCHAR(100) NOT NULL,
    keyword VARCHAR(100) NOT NULL,
);