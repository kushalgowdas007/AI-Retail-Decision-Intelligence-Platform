"""
AI Retail Decision Intelligence Platform — FastAPI Backend
Serves all computed metrics to the Streamlit dashboard.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
    
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from api.dashboard_ui import get_dashboard_html


# ---------------------------------------------------------------------------
# Ensure project root is available for src.* imports
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------------------------
# Existing business logic
# ---------------------------------------------------------------------------

from src.forecasting.forecast import get_forecast

from src.inventory.stockout_predictor import (
    predict_stockout
)

from src.inventory.inventory_optimizer import (
    optimize_inventory
)

from src.inventory.safety_stock_optimizer import (
    calculate_safety_stock
)

from src.inventory.replenishment_engine import (
    recommend_replenishment
)

from src.finance.revenue_forecast import (
    forecast_revenue
)

from src.intelligence.demand_spike_detector import (
    detect_spike
)

from src.intelligence.product_risk_classifier import (
    classify_risk
)

from src.agents.autonomous_replenishment_agent import (
    run_autonomous_replenishment
)

from src.agents.executive_agent import (
    run_executive_agent
)

from src.simulation.what_if_simulator import (
    run_what_if
)

from src.simulation.digital_twin import (
    run_digital_twin
)

from src.simulation.market_shock_simulator import (
    simulate_market_shock
)

from src.mlops.model_monitor import (
    monitor_model
)

from src.mlops.drift_detector import (
    detect_drift
)

from src.mlops.retraining_agent import (
    retraining_decision
)


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI Retail Decision Intelligence Platform",
    version="1.0.0",
    description=(
        "Enterprise Retail AI — "
        "Forecast, Optimize, Predict, Decide."
    )
)


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Shared configuration
# ---------------------------------------------------------------------------

INVENTORY = 100

PRICE = 120

PROFIT_MARGIN = 0.25

SALES_HISTORY = [
    30,
    32,
    31,
    34,
    33,
    80,
    90,
    100,
    95,
    110
]

HISTORICAL_SALES = [
    30,
    32,
    35,
    31,
    33
]

RECENT_SALES = [
    70,
    75,
    80,
    72,
    78
]

MAE = 4.2

RMSE = 5.8

SUPPLIER_DELAY_DAYS = 10


# ---------------------------------------------------------------------------
# Dashboard UI / Health endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def home(request: Request):
    """
    Serves the AI Retail Decision Intelligence interactive dashboard UI.
    If explicitly requested with Accept: application/json, returns API health JSON.
    """
    accept = request.headers.get("accept", "")
    if "application/json" in accept and "text/html" not in accept:
        return JSONResponse(
            content={
                "message": (
                    "AI Retail Decision Intelligence "
                    "Platform API Running"
                ),
                "version": "1.0.0"
            }
        )

    return HTMLResponse(
        content=get_dashboard_html(),
        status_code=200
    )


@app.get("/health")
def health():
    """
    Basic API health endpoint.
    """
    return {
        "message": (
            "AI Retail Decision Intelligence "
            "Platform API Running"
        ),
        "version": "1.0.0"
    }


# ---------------------------------------------------------------------------
# Main Forecast + Retail Intelligence endpoint
# ---------------------------------------------------------------------------

@app.get("/forecast")
def forecast_endpoint():
    """
    Full retail intelligence pipeline.

    Returns:
        - Forecast
        - Revenue
        - Profit
        - Inventory
        - Safety stock
        - Stockout risk
        - Replenishment
        - Risk intelligence
        - Supply-chain risk
        - Executive recommendations
        - MLOps information
    """

    # -----------------------------------------------------------------------
    # Forecasting
    # -----------------------------------------------------------------------

    raw_forecast = get_forecast()

    forecast_value = int(
        raw_forecast.iloc[0]
    )

    forecast_series = {
        str(index): float(
            round(value, 6)
        )
        for index, value in raw_forecast.items()
    }


    # -----------------------------------------------------------------------
    # Inventory
    # -----------------------------------------------------------------------

    stockout = predict_stockout(
        INVENTORY,
        forecast_value
    )

    optimization = optimize_inventory(
        INVENTORY,
        forecast_value
    )

    replenishment_basic = recommend_replenishment(
        INVENTORY,
        forecast_value
    )


    # -----------------------------------------------------------------------
    # Safety Stock + Risk Intelligence
    # -----------------------------------------------------------------------

    sales_series = pd.Series(
        SALES_HISTORY
    )

    safety = calculate_safety_stock(
        sales_series
    )

    safety_stock_value = safety[
        "safety_stock"
    ]

    spike = detect_spike(
        sales_series
    )

    risk = classify_risk(
        INVENTORY,
        forecast_value,
        confidence=99
    )


    # -----------------------------------------------------------------------
    # Finance
    # -----------------------------------------------------------------------

    finance = forecast_revenue(
        forecast_value,
        PRICE,
        PROFIT_MARGIN
    )


    # -----------------------------------------------------------------------
    # Autonomous Replenishment
    # -----------------------------------------------------------------------

    auto_rep = run_autonomous_replenishment(
        inventory=INVENTORY,
        forecast=forecast_value,
        safety_stock=int(
            safety_stock_value
        )
    )


    # -----------------------------------------------------------------------
    # Executive Agent
    # -----------------------------------------------------------------------

    inventory_result_for_exec = {
        "stockout": stockout,
        "optimization": optimization,
        "replenishment": replenishment_basic
    }

    risk_result_for_exec = {
        "spike": {
            "spike_detected": bool(
                spike["spike_detected"]
            ),
            "spike_ratio": float(
                spike["spike_ratio"]
            )
        },
        "safety_stock": safety,
        "risk": risk
    }

    finance_result_for_exec = {
        "revenue": finance["revenue"],
        "profit": finance["profit"]
    }

    executive = run_executive_agent(
        inventory_result_for_exec,
        risk_result_for_exec,
        finance_result_for_exec
    )


    # -----------------------------------------------------------------------
    # Supply Chain / Market Shock
    # -----------------------------------------------------------------------

    supply_chain = simulate_market_shock(
        forecast_value,
        SUPPLIER_DELAY_DAYS
    )


    # -----------------------------------------------------------------------
    # MLOps
    # -----------------------------------------------------------------------

    model_health = monitor_model(
        MAE,
        RMSE
    )

    drift = detect_drift(
        HISTORICAL_SALES,
        RECENT_SALES
    )

    retrain = retraining_decision(
        bool(
            drift["drift_detected"]
        )
    )


    # -----------------------------------------------------------------------
    # API Response
    # -----------------------------------------------------------------------

    return {

        # ===================================================================
        # Core KPIs
        # ===================================================================

        "forecast": int(
            forecast_value
        ),

        "revenue": int(
            finance["revenue"]
        ),

        "profit": int(
            finance["profit"]
        ),

        "margin": float(
            PROFIT_MARGIN
        ),

        "risk": str(
            risk["category"]
        ),

        "status": str(
            executive["status"]
        ),


        # ===================================================================
        # Forecast Series
        # ===================================================================

        "forecast_series": forecast_series,


        # ===================================================================
        # Inventory
        # ===================================================================

        "inventory": int(
            INVENTORY
        ),

        "recommended_stock": int(
            optimization["recommended_stock"]
        ),

        "safety_stock": int(
            safety_stock_value
        ),

        "excess_inventory": int(
            optimization["excess_inventory"]
        ),

        "stockout_risk": str(
            stockout["risk"]
        ),

        "stockout_shortage": int(
            stockout["shortage"]
        ),


        # ===================================================================
        # Autonomous Replenishment
        # ===================================================================

        "replenishment": {

            "action": str(
                auto_rep["action"]
            ),

            "required_stock": int(
                auto_rep["required_stock"]
            ),

            "current_inventory": int(
                auto_rep["current_inventory"]
            ),

            "reorder_quantity": int(
                auto_rep["reorder_quantity"]
            ),

            "recommended_order_date": str(
                auto_rep["recommended_order_date"]
            ),

            "lead_time_days": int(
                auto_rep["lead_time_days"]
            ),

            "confidence": int(
                auto_rep["confidence"]
            )
        },


        # ===================================================================
        # Risk Intelligence
        # ===================================================================

        "risk_score": int(
            risk["score"]
        ),

        "risk_category": str(
            risk["category"]
        ),

        "spike_detected": bool(
            spike["spike_detected"]
        ),

        "spike_ratio": float(
            spike["spike_ratio"]
        ),


        # ===================================================================
        # Supply Chain
        # ===================================================================

        "supply_chain": {

            "supplier_delay": int(
                supply_chain["supplier_delay"]
            ),

            "risk": str(
                supply_chain["risk"]
            ),

            "recommended_safety_stock": int(
                supply_chain[
                    "recommended_safety_stock"
                ]
            )
        },


        # ===================================================================
        # Executive Recommendations
        # ===================================================================

        "recommendations": list(
            executive["recommendations"]
        ),


        # ===================================================================
        # MLOps
        # ===================================================================

        "mlops": {

            "model_status": str(
                model_health["status"]
            ),

            "mae": float(
                model_health["mae"]
            ),

            "rmse": float(
                model_health["rmse"]
            ),

            "drift_detected": bool(
                drift["drift_detected"]
            ),

            "drift_score": float(
                drift["drift_score"]
            ),

            # FIX:
            # Previously this was str(retrain), which returned
            # "{'action': 'RETRAIN_MODEL'}".
            # Now it returns only "RETRAIN_MODEL".
            "retrain_action": str(
                retrain
            )
        }
    }


# ---------------------------------------------------------------------------
# Simulation request model
# ---------------------------------------------------------------------------

class SimulateRequest(BaseModel):

    discount_percent: float = 10.0

    supplier_delay_days: int = 10

    inventory_increase_percent: float = 20.0


# ---------------------------------------------------------------------------
# What-If + Digital Twin Simulation
# ---------------------------------------------------------------------------

@app.post("/simulate")
def simulate_endpoint(
    req: SimulateRequest
):
    """
    Runs:

    - What-If simulation
    - Digital Twin simulation
    - Market shock simulation
    - Revenue/profit estimation
    - Stockout risk estimation
    """

    # -----------------------------------------------------------------------
    # Forecast
    # -----------------------------------------------------------------------

    raw_forecast = get_forecast()

    forecast_value = int(
        raw_forecast.iloc[0]
    )


    # -----------------------------------------------------------------------
    # What-If Simulation
    # -----------------------------------------------------------------------

    what_if = run_what_if(
        forecast=forecast_value,
        price=PRICE,
        discount_percent=req.discount_percent
    )


    # -----------------------------------------------------------------------
    # Digital Twin
    # -----------------------------------------------------------------------

    twin = run_digital_twin(
        current_inventory=INVENTORY,
        forecast=forecast_value,
        increase_percent=req.inventory_increase_percent
    )


    # -----------------------------------------------------------------------
    # Market Shock
    # -----------------------------------------------------------------------

    supply = simulate_market_shock(
        forecast_value,
        req.supplier_delay_days
    )


    # -----------------------------------------------------------------------
    # Simulated Financials
    # -----------------------------------------------------------------------

    sim_revenue = what_if[
        "expected_revenue"
    ]

    sim_profit = (
        sim_revenue *
        PROFIT_MARGIN
    )


    # -----------------------------------------------------------------------
    # Simulated Stockout Risk
    # -----------------------------------------------------------------------

    stockout_risk_sim = (
        "HIGH"
        if what_if["new_forecast"]
        > twin["inventory_after"]
        else "LOW"
    )


    # -----------------------------------------------------------------------
    # Simulation Response
    # -----------------------------------------------------------------------

    return {

        "projected_demand": what_if[
            "new_forecast"
        ],

        "discounted_price": round(
            what_if["discounted_price"],
            2
        ),

        "expected_revenue": round(
            sim_revenue,
            2
        ),

        "expected_profit": round(
            sim_profit,
            2
        ),

        "stockout_risk": stockout_risk_sim,

        "digital_twin": twin,

        "supply_chain": supply
    }