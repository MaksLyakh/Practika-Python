-- 1 SELECT
SELECT * FROM doctors;
-- 2 WHERE
SELECT * FROM appointments WHERE status='scheduled';
-- 3 ORDER BY
SELECT * FROM appointments ORDER BY price DESC;
-- 4 JOIN
SELECT a.id, d.name FROM appointments a JOIN doctors d ON a.doctor_id=d.id;
-- 5 LEFT JOIN
SELECT d.name, a.id FROM doctors d LEFT JOIN appointments a ON a.doctor_id=d.id;
-- 6 GROUP BY
SELECT doctor_id, COUNT(*) FROM appointments GROUP BY doctor_id;
-- 7 HAVING
SELECT doctor_id, COUNT(*) FROM appointments GROUP BY doctor_id HAVING COUNT(*)>=2;
-- 8 COUNT
SELECT COUNT(*) FROM appointments;
-- 9 AVG
SELECT AVG(price) FROM appointments;
-- 10 INSERT (демонстрационный запрос, выполняется отдельно)
INSERT INTO patients(name,phone) VALUES ('Тестовый пациент','+79999999999');
-- 11 UPDATE
UPDATE appointments SET price=price+100 WHERE id=1;
-- 12 DELETE (удаляем только тестового пациента)
DELETE FROM patients WHERE phone='+79999999999';
-- 13 подзапрос
SELECT * FROM appointments WHERE price>(SELECT AVG(price) FROM appointments);
-- 14 несколько условий
SELECT * FROM appointments WHERE price>=1200 AND status='scheduled';
-- 15 несколько таблиц
SELECT a.id,d.name,p.name FROM appointments a JOIN doctors d ON a.doctor_id=d.id JOIN patients p ON a.patient_id=p.id;
-- 16 N:M
SELECT d.name,dep.name FROM doctor_departments dd JOIN doctors d ON d.id=dd.doctor_id JOIN departments dep ON dep.id=dd.department_id;
