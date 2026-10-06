SELECT date_trunc('day', bought_at) AS day,
       COUNT(*) AS tickets,
       SUM(price) AS revenue,
       AVG(price) AS avg_price
FROM tickets
WHERE status='booked' AND bought_at >= NOW() - INTERVAL '30 days'
GROUP BY day
ORDER BY day DESC;
