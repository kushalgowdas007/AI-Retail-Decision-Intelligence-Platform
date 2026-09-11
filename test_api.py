from app.api_client import get_health, get_forecast, run_simulation


print("===== API HEALTH =====")

health = get_health()

print(health)


print("\n===== FORECAST =====")

forecast = get_forecast()

print(forecast)


print("\n===== SIMULATION =====")

simulation = run_simulation(
    discount_percent=10,
    supplier_delay_days=10,
    inventory_increase_percent=20,
)

print(simulation)