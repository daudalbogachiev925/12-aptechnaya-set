SELECT m.name AS medicine, b.expiry, p.name AS pharmacy,
       b.qty, b.expiry - CURRENT_DATE AS days_left
FROM batches b
JOIN medicines m ON m.id = b.medicine_id
JOIN pharmacies p ON p.id = b.pharmacy_id
WHERE b.expiry < CURRENT_DATE + INTERVAL '90 days'
  AND b.qty > 0
ORDER BY b.expiry;
