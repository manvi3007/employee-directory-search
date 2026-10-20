
CREATE DATABASE IF NOT EXISTS employee_directory;
USE employee_directory;

CREATE TABLE IF NOT EXISTS employees (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    date_of_joining DATE NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email),
    KEY idx_employees_name (name),
    KEY idx_employees_department (department)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO employees
    (name, email, department, designation, date_of_joining)
VALUES
    ('Rahul Sharma', 'rahul@company.com', 'Engineering',
     'Software Engineer', '2024-01-15'),
    ('Priya Singh', 'priya@company.com', 'HR',
     'HR Executive', '2023-06-10'),
    ('Rahul Verma', 'rahulv@company.com', 'Marketing',
     'Marketing Manager', '2022-11-20'),
    ('Aman Kumar', 'aman@company.com', 'Engineering',
     'Developer', '2024-03-05'),
    ('Neha Gupta', 'neha@company.com', 'Finance',
     'Financial Analyst', '2023-09-12');
