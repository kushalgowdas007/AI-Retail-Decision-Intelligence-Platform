"""
executive_dashboard.py
AI Retail Decision Intelligence Platform — Enterprise SaaS Dashboard v2.0

Run with:
    streamlit run app/executive_dashboard.py
    (from the AI-Retail-Decision-Intelligence-Platform/ directory)

FastAPI backend:
    Deployed on Vercel
"""

import sys
import os
from datetime import datetime

import streamlit as st

# ── Path setup: allow imports from app and project root ───────────────────────

APP_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(APP_DIR)

if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


# ── API Client ────────────────────────────────────────────────────────────────

from api_client import get_forecast


# ── Component imports ─────────────────────────────────────────────────────────

from components.sidebar import render_sidebar
from components.kpi_cards import (
    render_kpi_cards,
    render_business_health,
)
from components.forecast_chart import render_forecast_chart
from components.inventory_card import render_inventory_card
from components.risk_card import (
    render_risk_card,
    render_supply_chain_card,
    render_demand_intel_card,
)
from components.replenishment_card import render_replenishment_card
from components.copilot_panel import render_copilot_panel
from components.simulation_panel import render_simulation_panel
from components.digital_twin import render_digital_twin
from components.mlops_panel import render_mlops_panel


# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Retail Decision Intelligence Platform",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# INJECT CSS
# ─────────────────────────────────────────────────────────────────────────────

_css_path = os.path.join(
    os.path.dirname(__file__),
    "styles",
    "dashboard.css",
)

if os.path.exists(_css_path):
    with open(_css_path, "r", encoding="utf-8") as _f:
        st.markdown(
            f"<style>{_f.read()}</style>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# DATA FETCH
# ─────────────────────────────────────────────────────────────────────────────

# Deployed FastAPI backend on Vercel
API_URL = "https://ai-retail-decision-intelligence-pla.vercel.app/forecast"


@st.cache_data(ttl=30)
def fetch_data() -> dict | None:
    """
    Fetch retail intelligence data from the deployed
    Vercel FastAPI backend.

    Data is cached for 30 seconds to reduce unnecessary
    API requests.
    """

    try:
        data = get_forecast()

        if not isinstance(data, dict):
            return None

        return data

    except Exception:
        return None


def _api_error_banner():
    """
    Display an API connection error banner.
    """

    banner_html = (
        '<div class="alert-banner critical" '
        'style="margin-bottom:1.25rem">'
        '⚡ <strong>Cannot reach Retail AI API</strong><br>'
        '<span style="font-size:0.72rem;opacity:0.85">'
        f'Backend: <code>{API_URL}</code>'
        '</span>'
        '</div>'
    )

    st.markdown(
        banner_html,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────

page = render_sidebar()


# ─────────────────────────────────────────────────────────────────────────────
# TOP HEADER
# ─────────────────────────────────────────────────────────────────────────────

now_str = datetime.now().strftime(
    "%b %d, %Y   %I:%M %p"
)

# Determine model status label from data
_header_model_status = "ARIMA/SARIMA"

header_html = (
    '<div class="dash-header">'
    
    '<div class="dash-header-brand">'
    
    '<div class="dash-header-title">'
    'AI Retail Decision Intelligence Platform'
    '</div>'
    
    '<div class="dash-header-sub">'
    'Forecast · Optimize · Predict · Decide'
    '</div>'
    
    '</div>'
    
    '<div class="dash-header-right">'
    
    '<div class="header-meta">'
    
    f'<div class="header-datetime">{now_str}</div>'
    
    '<div class="status-dot">'
    'System Operational'
    '</div>'
    
    '</div>'
    
    f'<span class="badge badge-ai" '
    f'style="font-size:0.6rem">'
    f'{_header_model_status}'
    '</span>'
    
    '</div>'
    
    '</div>'
)

st.markdown(
    header_html,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# FETCH DATA
# ─────────────────────────────────────────────────────────────────────────────

data = fetch_data()


# ─────────────────────────────────────────────────────────────────────────────
# REFRESH BUTTON ROW
# ─────────────────────────────────────────────────────────────────────────────

col_spacer, col_last, col_refresh = st.columns(
    [5, 2, 1]
)


with col_last:

    last_upd = datetime.now().strftime(
        "Last updated: %I:%M %p"
    )

    st.markdown(
        f'<div style="font-size:0.68rem;'
        f'color:var(--text-muted);'
        f'text-align:right;'
        f'padding-top:0.4rem">'
        f'{last_upd}'
        f'</div>',
        unsafe_allow_html=True,
    )


with col_refresh:

    if st.button(
        "↻ Refresh",
        help="Reload all data from FastAPI backend",
        type="secondary",
    ):
        st.cache_data.clear()
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# API ERROR HANDLING
# ─────────────────────────────────────────────────────────────────────────────

if data is None:

    _api_error_banner()

    st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# VERTICAL KPI LIST
# ─────────────────────────────────────────────────────────────────────────────

def _render_kpi_vertical(data: dict) -> None:
    """
    Compact vertical key-metric list for secondary columns.
    """

    forecast = data.get(
        "forecast",
        0,
    )

    revenue = data.get(
        "revenue",
        0,
    )

    profit = data.get(
        "profit",
        0,
    )

    inventory = data.get(
        "inventory",
        0,
    )

    risk_cat = data.get(
        "risk_category",
        "LOW",
    )


    risk_style = {
        "LOW": "success",
        "MEDIUM": "warning",
        "HIGH": "critical",
    }.get(
        risk_cat,
        "neutral",
    )


    if risk_style == "critical":
        risk_color = "var(--color-critical)"

    elif risk_style == "success":
        risk_color = "var(--color-success)"

    elif risk_style == "warning":
        risk_color = "var(--color-warning)"

    else:
        risk_color = "var(--text-secondary)"


    rows = [
        (
            "FORECAST",
            f"{forecast} units",
            "var(--color-primary)",
        ),
        (
            "REVENUE",
            f"₹{revenue:,}",
            "var(--color-ai)",
        ),
        (
            "PROFIT",
            f"₹{profit:,}",
            "var(--color-success)",
        ),
        (
            "INVENTORY",
            f"{inventory} units",
            "var(--text-primary)",
        ),
        (
            "RISK",
            risk_cat,
            risk_color,
        ),
    ]


    rows_html = "".join(
        f'<div class="metric-row">'
        f'<span class="metric-row-label">'
        f'{lbl}'
        f'</span>'
        f'<span class="metric-row-value" '
        f'style="color:{clr}">'
        f'{val}'
        f'</span>'
        f'</div>'
        for lbl, val, clr in rows
    )


    st.markdown(
        f'<div class="dash-card">'
        f'{rows_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════

if page == "overview":

    st.markdown(
        '<div class="section-header">'
        'EXECUTIVE KPIs'
        '</div>',
        unsafe_allow_html=True,
    )

    render_kpi_cards(data)


    st.markdown(
        "<div style='margin-top:0.85rem'></div>",
        unsafe_allow_html=True,
    )


    # ── Row 2: Business Health + Demand Intelligence | Forecast Chart ────────

    col_left, col_forecast = st.columns(
        [1, 2]
    )


    with col_left:

        render_business_health(data)

        st.markdown(
            "<div style='margin-top:0.65rem'></div>",
            unsafe_allow_html=True,
        )

        render_demand_intel_card(data)


    with col_forecast:

        st.markdown(
            '<div class="dash-card">',
            unsafe_allow_html=True,
        )

        render_forecast_chart(data)

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


    st.markdown(
        "<div style='margin-top:0.75rem'></div>",
        unsafe_allow_html=True,
    )


    # ── Row 3: Inventory | Risk | Replenishment ──────────────────────────────

    col_inv, col_risk, col_rep = st.columns(3)


    with col_inv:

        render_inventory_card(data)


    with col_risk:

        st.markdown(
            '<div class="dash-card">',
            unsafe_allow_html=True,
        )

        render_risk_card(data)

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


    with col_rep:

        render_replenishment_card(data)


    st.markdown(
        "<div style='margin-top:0.75rem'></div>",
        unsafe_allow_html=True,
    )


    # ── Row 4: AI Copilot | Supply Chain ─────────────────────────────────────

    col_cop, col_sc = st.columns(
        [2, 1]
    )


    with col_cop:

        st.markdown(
            '<div class="dash-card">',
            unsafe_allow_html=True,
        )

        render_copilot_panel(data)

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


    with col_sc:

        render_supply_chain_card(data)


# ══════════════════════════════════════════════════════════════════════════════
# FORECAST
# ══════════════════════════════════════════════════════════════════════════════

elif page == "forecast":

    st.markdown(
        '<div class="section-header">'
        'DEMAND FORECAST'
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="dash-card">',
        unsafe_allow_html=True,
    )

    render_forecast_chart(data)

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        "<div style='margin-top:0.75rem'></div>",
        unsafe_allow_html=True,
    )


    with st.expander(
        "📋 Forecast Series Data",
        expanded=False,
    ):

        import pandas as pd

        fs = data.get(
            "forecast_series",
            {},
        )


        if fs:

            df_fc = pd.DataFrame(
                {
                    "Date": list(fs.keys()),
                    "Forecast (units)": [
                        round(v, 2)
                        for v in fs.values()
                    ],
                }
            )


            st.dataframe(
                df_fc,
                use_container_width=True,
                hide_index=True,
            )


    st.markdown(
        "<div style='margin-top:0.65rem'></div>",
        unsafe_allow_html=True,
    )


    col_a, col_b = st.columns(2)


    with col_a:

        render_demand_intel_card(data)


    with col_b:

        render_replenishment_card(data)


# ══════════════════════════════════════════════════════════════════════════════
# INVENTORY
# ══════════════════════════════════════════════════════════════════════════════

elif page == "inventory":

    st.markdown(
        '<div class="section-header">'
        'INVENTORY HEALTH'
        '</div>',
        unsafe_allow_html=True,
    )


    col_a, col_b = st.columns(2)


    with col_a:

        render_inventory_card(data)


    with col_b:

        render_replenishment_card(data)


# ══════════════════════════════════════════════════════════════════════════════
# REPLENISHMENT
# ══════════════════════════════════════════════════════════════════════════════

elif page == "replenishment":

    st.markdown(
        '<div class="section-header">'
        'AUTONOMOUS REPLENISHMENT'
        '</div>',
        unsafe_allow_html=True,
    )


    render_replenishment_card(data)


    st.markdown(
        "<div style='margin-top:0.65rem'></div>",
        unsafe_allow_html=True,
    )


    col_a, col_b = st.columns(2)


    with col_a:

        render_inventory_card(data)


    with col_b:

        render_supply_chain_card(data)


# ══════════════════════════════════════════════════════════════════════════════
# RISK
# ══════════════════════════════════════════════════════════════════════════════

elif page == "risk":

    st.markdown(
        '<div class="section-header">'
        'RISK INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="dash-card">',
        unsafe_allow_html=True,
    )

    render_risk_card(data)

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        "<div style='margin-top:0.65rem'></div>",
        unsafe_allow_html=True,
    )


    col_a, col_b = st.columns(2)


    with col_a:

        render_supply_chain_card(data)


    with col_b:

        render_demand_intel_card(data)


# ══════════════════════════════════════════════════════════════════════════════
# AI COPILOT
# ══════════════════════════════════════════════════════════════════════════════

elif page == "copilot":

    st.markdown(
        '<div class="section-header">'
        'AI BUSINESS COPILOT'
        '</div>',
        unsafe_allow_html=True,
    )


    col_cop, col_kpi = st.columns(
        [2, 1]
    )


    with col_cop:

        st.markdown(
            '<div class="dash-card">',
            unsafe_allow_html=True,
        )

        render_copilot_panel(data)

        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )


    with col_kpi:

        _render_kpi_vertical(data)

        st.markdown(
            "<div style='margin-top:0.65rem'></div>",
            unsafe_allow_html=True,
        )

        render_business_health(data)


# ══════════════════════════════════════════════════════════════════════════════
# DIGITAL TWIN
# ══════════════════════════════════════════════════════════════════════════════

elif page == "digital_twin":

    st.markdown(
        '<div class="section-header">'
        'DIGITAL TWIN — STATE COMPARISON'
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="dash-card">',
        unsafe_allow_html=True,
    )

    render_digital_twin(data)

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════

elif page == "simulator":

    st.markdown(
        '<div class="section-header">'
        'WHAT-IF SIMULATOR'
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        '<div class="dash-card">',
        unsafe_allow_html=True,
    )

    render_simulation_panel(data)

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# MLOPS
# ══════════════════════════════════════════════════════════════════════════════

elif page == "mlops":

    st.markdown(
        '<div class="section-header">'
        'MLOPS MONITORING'
        '</div>',
        unsafe_allow_html=True,
    )


    render_mlops_panel(data)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

footer_html = (
    '<div class="dash-footer">'
    '<strong>'
    'AI Retail Decision Intelligence Platform'
    '</strong><br>'
    'Built with Python &bull; FastAPI &bull; Streamlit &bull; ARIMA/SARIMA'
    '&nbsp;&nbsp;|&nbsp;&nbsp;'
    'v1.0.0'
    '</div>'
)

st.markdown(
    footer_html,
    unsafe_allow_html=True,
)