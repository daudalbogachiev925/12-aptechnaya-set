SELECT p.name AS pharmacy, m.name AS medicine,
       SUM(b.qty) - COALESCE(SUM(s.qty),0) AS stock
FROM batches b
JOIN pharmacies p ON p.id = b.pharmacy_id
JOIN medicines m ON m.id = b.medicine_id
LEFT JOIN sales s ON s.batch_id = b.id
GROUP BY p.name, m.name
HAVING SUM(b.qty) - COALESCE(SUM(s.qty),0) > 0
ORDER BY p.name, m.name;
