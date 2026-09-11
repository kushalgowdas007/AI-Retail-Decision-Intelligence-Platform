import requests


# ─────────────────────────────────────────────────────────────────────────────
# DEPLOYED FASTAPI BACKEND
# ─────────────────────────────────────────────────────────────────────────────

API_BASE_URL = "https://ai-retail-decision-intelligence-pla.vercel.app"


# ─────────────────────────────────────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────────────────────────────────────

def get_health():
    try:
        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        response = requests.get(
            f"{API_BASE_URL}/",
            headers={"Accept": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


# ─────────────────────────────────────────────────────────────────────────────
# FORECAST / RETAIL INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────

def get_forecast():
    response = requests.get(
        f"{API_BASE_URL}/forecast",
        timeout=60,
    )

    response.raise_for_status()

    return response.json()


# ─────────────────────────────────────────────────────────────────────────────
# WHAT-IF / DIGITAL TWIN / MARKET SHOCK
# ─────────────────────────────────────────────────────────────────────────────

def run_simulation(
    discount_percent=10,
    supplier_delay_days=10,
    inventory_increase_percent=20,
):

    payload = {
        "discount_percent": discount_percent,
        "supplier_delay_days": supplier_delay_days,
        "inventory_increase_percent": inventory_increase_percent,
    }

    response = requests.post(
        f"{API_BASE_URL}/simulate",
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    return response.json()