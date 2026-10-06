SELECT date_trunc('day', s.sold_at) AS day,
       COUNT(*) AS sales_count,
       SUM(s.qty) AS units,
       SUM(s.qty * s.price) AS revenue
FROM sales s
WHERE s.sold_at >= NOW() - INTERVAL '30 days'
GROUP BY day
ORDER BY day DESC;
