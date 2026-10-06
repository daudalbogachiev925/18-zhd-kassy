CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    code TEXT UNIQUE
);

CREATE TABLE trains (
    id SERIAL PRIMARY KEY,
    number TEXT UNIQUE NOT NULL,
    name TEXT,
    train_type TEXT
);

CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    train_id INT REFERENCES trains(id),
    from_station_id INT REFERENCES stations(id),
    to_station_id INT REFERENCES stations(id),
    depart TIMESTAMP NOT NULL,
    arrive TIMESTAMP NOT NULL,
    base_price NUMERIC(10,2)
);

CREATE TABLE cars (
    id SERIAL PRIMARY KEY,
    route_id INT REFERENCES routes(id),
    number TEXT NOT NULL,
    car_type TEXT CHECK (car_type IN ('купе','плацкарт','СВ','сидячий')),
    seats INT NOT NULL,
    price NUMERIC(10,2) NOT NULL
);

CREATE TABLE passengers (
    id BIGSERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    passport TEXT UNIQUE,
    birth DATE,
    phone TEXT
);

CREATE TABLE tickets (
    id BIGSERIAL PRIMARY KEY,
    car_id INT REFERENCES cars(id),
    route_id INT REFERENCES routes(id),
    passenger_id BIGINT REFERENCES passengers(id),
    seat INT NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    status TEXT DEFAULT 'booked',
    bought_at TIMESTAMP DEFAULT NOW(),
    refunded_at TIMESTAMP,
    UNIQUE(route_id, car_id, seat)
);

CREATE INDEX idx_routes_train ON routes(train_id);
CREATE INDEX idx_routes_depart ON routes(depart);
CREATE INDEX idx_tickets_route ON tickets(route_id);
CREATE INDEX idx_tickets_passenger ON tickets(passenger_id);
