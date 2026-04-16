"""Streamlit frontend for the Crash Analysis & Injury Prediction System."""

import streamlit as st
from main import analyze_crash


def render_app():
    st.set_page_config(page_title="Crash Analysis & Injury Prediction", layout="centered")
    st.markdown("## Crash Analysis & Injury Prediction System")
    st.markdown("Evaluate collision severity, injury risk, and safety recommendations using a clean and professional interface.")

    st.sidebar.header("Crash Input")
    speed = st.sidebar.slider("Speed (km/h)", min_value=0, max_value=200, value=50, step=5)
    collision_type = st.sidebar.selectbox("Collision type", ["frontal", "rear", "side", "rollover"])
    seatbelt = st.sidebar.checkbox("Seatbelt worn", value=True)
    airbags = st.sidebar.checkbox("Airbags present", value=True)
    analyze = st.sidebar.button("Analyze Crash")

    if analyze:
        report = analyze_crash(speed, collision_type, seatbelt, airbags)
        summary = report["summary"]

        risk_colors = {
            "Low": "#2E7D32",
            "Medium": "#F9A825",
            "High": "#C62828",
        }
        st.metric("Risk level", summary["risk_level"], delta=None)
        st.markdown(f"<div style='padding: 14px; border-radius: 10px; background: {risk_colors.get(summary['risk_level'], '#E0E0E0')}; color: white;'>**Current risk assessment:** {summary['risk_level']}</div>", unsafe_allow_html=True)

        st.write("### Impact metrics")
        st.write(f"- Impact force: **{summary['impact_force_kN']} kN**")
        st.write(f"- Impact energy: **{summary['impact_energy_kJ']} kJ**")

        st.write("### Injury scenarios")
        for category, injuries in report["injuries"].items():
            if injuries:
                st.write(f"**{category}**")
                for injury in injuries:
                    st.write(f"- {injury}")

        st.write("### Safety suggestions")
        for suggestion in report["safety_suggestions"]:
            st.write(f"- {suggestion}")

        st.info("Use the sidebar controls to model different crash conditions and inspect how safety measures change the outcome.")


if __name__ == "__main__":
    render_app()
