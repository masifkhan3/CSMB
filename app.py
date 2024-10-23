import streamlit as st

# Function to calculate the production of chlorine, HCl, hydrogen, power consumption, and CS ELZ Load
def calculate_chlorine_hcl_hydrogen(caustic_soda_prod, sodium_hypo_prod, liquid_chlorine_prod, stearic_batches, hcl_hydrogen_usage, stearic_hydrogen_usage):
    # Constants for calculations
    chlorine_factor = 0.889  # Chlorine production as a fraction of Caustic Soda production
    hypo_chlorine_usage = 0.22  # 22% of Hypo production uses Chlorine
    chlorine_neutralization = 0.017  # 1.7% of Chlorine is neutralized
    hcl_chlorine_usage = 0.32  # 32% of Chlorine is used to produce HCl
    in_house_hcl = 0.05  # 5% of Caustic Soda used in-house for HCl production
    power_rate_per_ton = 2150.0  # Power consumption per ton of Caustic Soda in KWH
    hydrogen_production_percentage = 0.026  # Hydrogen production as 2.6% of Caustic Soda production

    # ---- Chlorine and HCl calculations ----
    chlorine_production = caustic_soda_prod * chlorine_factor  # Chlorine production based on Caustic Soda
    chlorine_used_in_hypo = sodium_hypo_prod * hypo_chlorine_usage  # Chlorine used in Hypo production
    chlorine_neutralized = chlorine_production * chlorine_neutralization  # Chlorine neutralized
    net_chlorine_available = chlorine_production - chlorine_used_in_hypo - chlorine_neutralized - liquid_chlorine_prod  # Chlorine left for HCl production
    
    hcl_prod = net_chlorine_available / hcl_chlorine_usage  # HCl production
    hcl_in_house = caustic_soda_prod * in_house_hcl  # HCl used in-house
    net_hcl_for_sale = hcl_prod - hcl_in_house  # HCl available for sale

    # ---- Hydrogen calculations ----
    hydrogen_prod_mt = caustic_soda_prod * hydrogen_production_percentage  # Hydrogen production in metric tons (MT)
    hydrogen_prod_nm3 = hydrogen_prod_mt * 34819 / 3.12  # Convert to normal cubic meters (NM3) based on 3.12 MT

    hydrogen_used_in_hcl = hcl_hydrogen_usage  # Hydrogen used in HCl production
    hydrogen_used_in_stearic = stearic_hydrogen_usage  # Hydrogen used in Stearic Acid batches
    total_hydrogen_usage = hydrogen_used_in_hcl + hydrogen_used_in_stearic  # Total hydrogen used
    balance_hydrogen_nm3 = hydrogen_prod_nm3 - total_hydrogen_usage  # Remaining hydrogen after usage
    balance_waste_percentage = (balance_hydrogen_nm3 / hydrogen_prod_nm3) * 100 if hydrogen_prod_nm3 > 0 else 0  # Percentage of hydrogen wasted

    # ---- Power consumption calculations ----
    total_power_used = power_rate_per_ton * caustic_soda_prod  # Total power used based on production
    power_per_ton_caustic_soda = total_power_used / caustic_soda_prod if caustic_soda_prod > 0 else 0  # Power used per ton of caustic soda

    # ---- CS ELZ Load calculation ----
    cs_elz_load = 3.5 / caustic_soda_prod if caustic_soda_prod > 0 else 0  # CS ELZ Load calculation

    return {
        "Chlorine Production": chlorine_production,
        "Chlorine Used in Hypo Production": chlorine_used_in_hypo,
        "Neutralized Chlorine": chlorine_neutralized,
        "Liquid Chlorine Production": liquid_chlorine_prod,
        "Net Chlorine Available for HCl": net_chlorine_available,
        "Total HCl Production": hcl_prod,
        "HCl Used In-House": hcl_in_house,
        "Net HCl Available for Sale": net_hcl_for_sale,
        "Hydrogen Production (MT)": hydrogen_prod_mt,
        "Hydrogen Production (NM3)": hydrogen_prod_nm3,
        "Hydrogen Used in HCl Production (NM3)": hydrogen_used_in_hcl,
        "Hydrogen Used in Stearic Acid Batches (NM3)": hydrogen_used_in_stearic,
        "Balance Hydrogen Waste (NM3)": balance_hydrogen_nm3,
        "Balance Hydrogen Waste Percentage": balance_waste_percentage,
        "Total Power Consumption (KWH)": total_power_used,
        "Power Consumption per Ton of Caustic Soda (KWH/ton)": power_per_ton_caustic_soda,
        "CS ELZ Load": cs_elz_load,
    }

# Streamlit App
st.title("🌈 Caustic Soda Production Calculator 🌈")
st.markdown(
    """
    Welcome to the **Caustic Soda Production Calculator**! 
    This application allows you to input your production data and calculate key outputs related to chlorine, HCl, hydrogen production, power consumption, and more.
    """
)

# Input fields
caustic_soda_prod = st.number_input("Enter Caustic Soda production in tons (TPD):", min_value=0.0)
sodium_hypo_prod = st.number_input("Enter Sodium Hypochlorite production in tons:", min_value=0.0)
liquid_chlorine_prod = st.number_input("Enter Liquid Chlorine production in tons:", min_value=0.0)
stearic_batches = st.number_input("Enter number of Stearic Acid Batches:", min_value=0)
hcl_hydrogen_usage = st.number_input("Enter Hydrogen used in HCl production (NM3):", min_value=0.0)
stearic_hydrogen_usage = st.number_input("Enter Hydrogen used in Stearic Acid production (NM3):", min_value=0.0)

# Calculate button
if st.button("Calculate"):
    results = calculate_chlorine_hcl_hydrogen(caustic_soda_prod, sodium_hypo_prod, liquid_chlorine_prod, stearic_batches, hcl_hydrogen_usage, stearic_hydrogen_usage)

    # Display results
    st.subheader("📊 Results")
    for key, value in results.items():
        st.write(f"**{key}:** {value:.2f}")

# Developed By Section
st.markdown(
    """
    <h3 style='color:blue;'>Developed by: mak3.8</h3>
    <p style='color:gray;'>This application is designed for educational and practical purposes in chemical production analysis.</p>
    """,
    unsafe_allow_html=True
)

# Adding some colorful style to the dashboard
st.markdown(
    """
    <style>
    .css-1lcbmhc {
        background-color: #f0f8ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)
