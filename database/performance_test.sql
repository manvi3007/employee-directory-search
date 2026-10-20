USE employee_directory;

-- Verify indexes
SHOW INDEX FROM employees;

-- Test prefix-based employee search
EXPLAIN
SELECT *
FROM employees
WHERE name LIKE 'Rah%'
   OR department LIKE 'Eng%'
ORDER BY id
LIMIT 50;