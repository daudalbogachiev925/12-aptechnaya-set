SELECT m.id, m.name, m.form,
       SUM(s.qty) AS sold,
       SUM(s.qty * s.price) AS revenue,
       SUM(s.qty * (s.price - COALESCE(b.purchase_price,0))) AS margin
FROM sales s
JOIN batches b ON b.id = s.batch_id
JOIN medicines m ON m.id = b.medicine_id
GROUP BY m.id
ORDER BY revenue DESC
LIMIT 20;
