from fastapi import FastAPI
from routes import stations, trains, routes, cars, passengers, tickets, reports

app = FastAPI(title="Railway API")
app.include_router(stations.router, prefix="/stations", tags=["stations"])
app.include_router(trains.router, prefix="/trains", tags=["trains"])
app.include_router(routes.router, prefix="/routes", tags=["routes"])
app.include_router(cars.router, prefix="/cars", tags=["cars"])
app.include_router(passengers.router, prefix="/passengers", tags=["passengers"])
app.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/health")
def health(): return {"status": "ok"}
