CREATE DATABASE if not exists banking_user;
USE banking_user;

CREATE TABLE if not exists users (
    bank_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE if not exists user_profile (
    bank_id INT PRIMARY KEY,
    aadhar VARCHAR(12) UNIQUE NOT NULL,
    pan VARCHAR(10) UNIQUE NOT NULL,
    mobile VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    address TEXT NOT NULL,
    pin_code VARCHAR(6) NOT NULL,
    profile_photo VARCHAR(255) NOT NULL,
    transaction_pin varchar(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (bank_id) REFERENCES users(bank_id) ON DELETE CASCADE
);

INSERT INTO user_balance (bank_id, balance)
VALUES (366314, 1000.00)
ON DUPLICATE KEY UPDATE balance = 10000.00;

ALTER TABLE user_profile
add username VARCHAR(255);

SET SQL_SAFE_UPDATES = 0;
delete from user_profile;
ALTER TABLE user_profile MODIFY transaction_pin INT;



CREATE TABLE if not exists password_reset (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id INT NOT NULL,
    otp INT NOT NULL,
    expires_at DATETIME NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES users(bank_id) ON DELETE CASCADE
);

drop table if exists user_balance;

CREATE TABLE if not exists user_balance (
    bank_id INT PRIMARY KEY,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0,
        CONSTRAINT fk_balance_user
        FOREIGN KEY (bank_id)
        REFERENCES user_profile(bank_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);



SELECT * FROM user_balance;


CREATE TABLE if not exists transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id INT NOT NULL,
    type ENUM('credit','debit') NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    balance_after DECIMAL(15,2) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tx_user
        FOREIGN KEY (bank_id)
        REFERENCES user_profile(bank_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);



CREATE TABLE if not exists money_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    status ENUM('pending','approved','rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_req_sender
        FOREIGN KEY (sender_id) REFERENCES user_profile(bank_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_req_receiver
        FOREIGN KEY (receiver_id) REFERENCES user_profile(bank_id)
        ON DELETE CASCADE
);


CREATE TABLE if not exists sub_admins (
    subadmin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    branch_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_cash (
    cash_id INT AUTO_INCREMENT PRIMARY KEY,
    subadmin_id INT NOT NULL,
    opening_cash DECIMAL(15,2),
    closing_cash DECIMAL(15,2),
    cash_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (subadmin_id) REFERENCES sub_admins(subadmin_id)
);

CREATE TABLE bank_daily_transactions (
    txn_id INT AUTO_INCREMENT PRIMARY KEY,
    subadmin_id INT NOT NULL,
    user_bank_id INT,
    type ENUM('credit','debit') NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (subadmin_id) REFERENCES sub_admins(subadmin_id),
    FOREIGN KEY (user_bank_id) REFERENCES user_profile(bank_id)
);

CREATE TABLE if not exists admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

drop table admins;
INSERT INTO admins (username, password)
VALUES ('admin', '$2y$10$Nz15edlngIw.t1qZvM.GkuADI8HhVK93JH8kbDzDqAbK87S0Y.klq
');

DELETE FROM admins WHERE username='admin';



