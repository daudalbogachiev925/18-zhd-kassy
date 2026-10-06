SELECT c.id AS car_id, c.number AS car_num, c.car_type, c.seats,
       COUNT(t.id) AS booked,
       c.seats - COUNT(t.id) AS free,
       ROUND(100.0 * COUNT(t.id) / c.seats, 1) AS load_pct
FROM cars c
LEFT JOIN tickets t ON t.car_id = c.id AND t.status='booked'
WHERE c.route_id = :route_id
GROUP BY c.id
ORDER BY load_pct DESC;
