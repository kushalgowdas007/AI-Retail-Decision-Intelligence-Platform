"""
simulation_panel.py — What-If Simulator with Streamlit sliders.

Calls the deployed Vercel FastAPI /simulate POST endpoint
through the shared api_client.py module.
"""

import streamlit as st

from api_client import run_simulation


# ─────────────────────────────────────────────────────────────────────────────
# SIMULATION PANEL
# ─────────────────────────────────────────────────────────────────────────────

def render_simulation_panel(data: dict) -> None:
    """
    What-If Simulator.

    Interactive sliders send the selected parameters to the deployed
    FastAPI /simulate endpoint and display the returned simulation outcome.
    """

    # ─────────────────────────────────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────────────────────────────────

    header_html = (
        '<div class="dash-card-header" style="margin-bottom:0.75rem">'
        '<span class="dash-card-icon">◇</span>'
        '<span class="dash-card-title">WHAT-IF SIMULATOR</span>'
        '<span style="margin-left:auto">'
        '<span class="badge badge-ai">Live API</span>'
        '</span>'
        '</div>'

        '<div style="font-size:0.76rem;'
        'color:var(--text-secondary);'
        'margin-bottom:0.85rem">'
        'Adjust parameters and run a simulation to see projected outcomes '
        'from the AI Retail Decision Intelligence engine.'
        '</div>'
    )

    st.markdown(
        header_html,
        unsafe_allow_html=True,
    )


    # ─────────────────────────────────────────────────────────────────────────
    # COLUMNS
    # ─────────────────────────────────────────────────────────────────────────

    col_sliders, col_result = st.columns(
        [1, 1]
    )


    # ─────────────────────────────────────────────────────────────────────────
    # SLIDERS
    # ─────────────────────────────────────────────────────────────────────────

    with col_sliders:

        discount = st.slider(
            "💰 Price Discount (%)",
            min_value=0,
            max_value=50,
            value=10,
            step=5,
            help=(
                "Percentage price discount applied "
                "to the base product price."
            ),
        )


        supplier_delay = st.slider(
            "🚚 Supplier Delay (days)",
            min_value=0,
            max_value=30,
            value=10,
            step=1,
            help=(
                "Simulated supplier delay in days "
                "for supply-chain risk analysis."
            ),
        )


        inv_increase = st.slider(
            "📦 Inventory Increase (%)",
            min_value=0,
            max_value=100,
            value=20,
            step=10,
            help=(
                "Simulated percentage increase in inventory "
                "for Digital Twin analysis."
            ),
        )


        st.markdown(
            "<div style='margin-top:0.5rem'></div>",
            unsafe_allow_html=True,
        )


        run_btn = st.button(
            "▶ Run Simulation",
            use_container_width=True,
            type="primary",
        )


    # ─────────────────────────────────────────────────────────────────────────
    # RESULT
    # ─────────────────────────────────────────────────────────────────────────

    with col_result:

        if run_btn:

            try:

                # Show progress while contacting Vercel
                with st.spinner(
                    "Running AI simulation..."
                ):

                    result = run_simulation(
                        discount_percent=float(discount),
                        supplier_delay_days=int(supplier_delay),
                        inventory_increase_percent=float(inv_increase),
                    )


                # ─────────────────────────────────────────────────────────────
                # EXTRACT RESULT
                # ─────────────────────────────────────────────────────────────

                proj_demand = result.get(
                    "projected_demand",
                    0,
                )


                exp_revenue = result.get(
                    "expected_revenue",
                    0,
                )


                exp_profit = result.get(
                    "expected_profit",
                    0,
                )


                disc_price = result.get(
                    "discounted_price",
                    0,
                )


                stockout_risk = result.get(
                    "stockout_risk",
                    "LOW",
                )


                digital_twin = result.get(
                    "digital_twin",
                    {},
                )


                supply_chain = result.get(
                    "supply_chain",
                    {},
                )


                # ─────────────────────────────────────────────────────────────
                # DIGITAL TWIN DATA
                # ─────────────────────────────────────────────────────────────

                inventory_before = digital_twin.get(
                    "inventory_before",
                    0,
                )


                inventory_after = digital_twin.get(
                    "inventory_after",
                    0,
                )


                stockout_before = digital_twin.get(
                    "stockout_before",
                    False,
                )


                stockout_after = digital_twin.get(
                    "stockout_after",
                    False,
                )


                inventory_cost_before = digital_twin.get(
                    "inventory_cost_before",
                    0,
                )


                inventory_cost_after = digital_twin.get(
                    "inventory_cost_after",
                    0,
                )


                # ─────────────────────────────────────────────────────────────
                # SUPPLY CHAIN DATA
                # ─────────────────────────────────────────────────────────────

                supplier_delay_result = supply_chain.get(
                    "supplier_delay",
                    supplier_delay,
                )


                supply_chain_risk = supply_chain.get(
                    "risk",
                    "LOW",
                )


                recommended_safety_stock = supply_chain.get(
                    "recommended_safety_stock",
                    0,
                )


                # ─────────────────────────────────────────────────────────────
                # RISK STYLES
                # ─────────────────────────────────────────────────────────────

                stockout_style = _risk_style(
                    stockout_risk
                )


                supply_chain_style = _risk_style(
                    supply_chain_risk
                )


                # ─────────────────────────────────────────────────────────────
                # MAIN OUTCOME CARD
                # ─────────────────────────────────────────────────────────────

                outcome_html = (
                    '<div class="outcome-card">'

                    '<div class="outcome-card-title">'
                    '◇ SIMULATION RESULT'
                    '</div>'


                    # Projected Demand
                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Projected Demand'
                    '</span>'
                    '<span class="metric-row-value" '
                    'style="color:#3B82F6">'
                    f'{proj_demand} units'
                    '</span>'
                    '</div>'


                    # Discounted Price
                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Discounted Price'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'₹{disc_price:,.2f}'
                    '</span>'
                    '</div>'


                    # Expected Revenue
                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Expected Revenue'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'₹{exp_revenue:,.0f}'
                    '</span>'
                    '</div>'


                    # Expected Profit
                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Expected Profit'
                    '</span>'
                    '<span class="metric-row-value" '
                    'style="color:#22C55E">'
                    f'₹{exp_profit:,.0f}'
                    '</span>'
                    '</div>'


                    # Stockout Risk
                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Stockout Risk'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'<span class="badge badge-{stockout_style}">'
                    f'{stockout_risk}'
                    '</span>'
                    '</span>'
                    '</div>'


                    # Supply Chain Risk
                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Supply Chain Risk'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'<span class="badge badge-{supply_chain_style}">'
                    f'{supply_chain_risk}'
                    '</span>'
                    '</span>'
                    '</div>'


                    '</div>'
                )


                st.markdown(
                    outcome_html,
                    unsafe_allow_html=True,
                )


                # ─────────────────────────────────────────────────────────────
                # DIGITAL TWIN CARD
                # ─────────────────────────────────────────────────────────────

                st.markdown(
                    "<div style='margin-top:0.75rem'></div>",
                    unsafe_allow_html=True,
                )


                digital_twin_html = (
                    '<div class="outcome-card">'

                    '<div class="outcome-card-title">'
                    '◇ DIGITAL TWIN'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Inventory Before'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'{inventory_before} units'
                    '</span>'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Inventory After'
                    '</span>'
                    '<span class="metric-row-value" '
                    'style="color:#3B82F6">'
                    f'{inventory_after} units'
                    '</span>'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Stockout Before'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'{"YES" if stockout_before else "NO"}'
                    '</span>'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Stockout After'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'{"YES" if stockout_after else "NO"}'
                    '</span>'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Inventory Cost Before'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'₹{inventory_cost_before:,.2f}'
                    '</span>'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Inventory Cost After'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'₹{inventory_cost_after:,.2f}'
                    '</span>'
                    '</div>'


                    '</div>'
                )


                st.markdown(
                    digital_twin_html,
                    unsafe_allow_html=True,
                )


                # ─────────────────────────────────────────────────────────────
                # SUPPLY CHAIN CARD
                # ─────────────────────────────────────────────────────────────

                st.markdown(
                    "<div style='margin-top:0.75rem'></div>",
                    unsafe_allow_html=True,
                )


                supply_chain_html = (
                    '<div class="outcome-card">'

                    '<div class="outcome-card-title">'
                    '◇ SUPPLY CHAIN IMPACT'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Supplier Delay'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'{supplier_delay_result} days'
                    '</span>'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Supply Risk'
                    '</span>'
                    '<span class="metric-row-value">'
                    f'<span class="badge badge-{supply_chain_style}">'
                    f'{supply_chain_risk}'
                    '</span>'
                    '</span>'
                    '</div>'


                    '<div class="metric-row">'
                    '<span class="metric-row-label">'
                    'Recommended Safety Stock'
                    '</span>'
                    '<span class="metric-row-value" '
                    'style="color:#F59E0B">'
                    f'{recommended_safety_stock} units'
                    '</span>'
                    '</div>'


                    '</div>'
                )


                st.markdown(
                    supply_chain_html,
                    unsafe_allow_html=True,
                )


            except Exception as e:

                st.error(
                    f"Simulation failed: {e}"
                )

                st.caption(
                    "The dashboard could not reach the deployed "
                    "FastAPI simulation endpoint."
                )


        else:

            # ─────────────────────────────────────────────────────────────────
            # PLACEHOLDER
            # ─────────────────────────────────────────────────────────────────

            placeholder_html = (
                '<div class="dash-card" '
                'style="text-align:center;'
                'padding:2rem 1rem">'

                '<div style="font-size:2rem;'
                'margin-bottom:0.5rem">'
                '◇'
                '</div>'

                '<div style="font-size:0.8rem;'
                'color:var(--text-secondary)">'

                'Adjust the sliders and click<br>'

                '<strong>Run Simulation</strong>'

                ' to see real-time simulation results.'

                '</div>'

                '</div>'
            )


            st.markdown(
                placeholder_html,
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# RISK STYLE HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _risk_style(category: str) -> str:

    return {
        "LOW": "success",
        "MEDIUM": "warning",
        "HIGH": "critical",
    }.get(
        category,
        "neutral",
    )