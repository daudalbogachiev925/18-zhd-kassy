SELECT tk.id, p.full_name, t.number AS train, s1.name AS from_st, s2.name AS to_st,
       tk.price, tk.bought_at, tk.refunded_at,
       tk.price - tk.price * 0.30 AS refund_amount
FROM tickets tk
JOIN passengers p ON p.id = tk.passenger_id
JOIN routes r ON r.id = tk.route_id
JOIN trains t ON t.id = r.train_id
JOIN stations s1 ON s1.id = r.from_station_id
JOIN stations s2 ON s2.id = r.to_station_id
WHERE tk.status='refunded'
ORDER BY tk.refunded_at DESC;
