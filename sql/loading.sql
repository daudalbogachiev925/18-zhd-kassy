SELECT r.id AS route_id, t.number AS train, t.name,
       s1.name AS from_st, s2.name AS to_st,
       r.depart,
       (SELECT SUM(c.seats) FROM cars c WHERE c.route_id = r.id) AS total_seats,
       COUNT(tk.id) AS booked,
       ROUND(100.0 * COUNT(tk.id) / (SELECT SUM(c.seats) FROM cars c WHERE c.route_id = r.id), 1) AS load_pct
FROM routes r
JOIN trains t ON t.id = r.train_id
JOIN stations s1 ON s1.id = r.from_station_id
JOIN stations s2 ON s2.id = r.to_station_id
LEFT JOIN tickets tk ON tk.route_id = r.id AND tk.status='booked'
GROUP BY r.id, t.number, t.name, s1.name, s2.name, r.depart
ORDER BY r.depart DESC;
