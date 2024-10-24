import streamlit as st
logo = Image.open('images/nimir_logo.png')
logo = Image.open('/full/path/to/nimir_logo.png')
import os
from PIL import Image

logo_path = 'nimir_logo.png'
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
else:
    st.warning("NIMIR logo not found. Please ensure the file is in the correct directory.")
    logo = None

from PIL import Image

# Load NIMIR logo
logo = Image.open('nimir_logo.png')  # Ensure the image is saved in the same folder or provide a full path

# Display NIMIR logo and Developed By message
col1, col2 = st.columns([8, 1])
col1.title("Chlorine, HCl, Hydrogen, and Power Consumption Calculator")
col2.image(logo, use_column_width=True)  # NIMIR logo on the right-hand side

st.write("Developed by mak3.7")

# Function to calculate the production of chlorine, HCl, hydrogen, power consumption, and CS ELZ Load
def calculate_chlorine_hcl_hydrogen(caustic_soda_prod, sodium_hypo_prod, liquid_chlorine_prod, stearic_batches, hcl_hydrogen_usage, stearic_hydrogen_usage):
    chlorine_factor = 0.889
    hypo_chlorine_usage = 0.22
    chlorine_neutralization = 0.017
    hcl_chlorine_usage = 0.32
    in_house_hcl = 0.05
    power_rate_per_ton = 2150.0
    hydrogen_production_percentage = 0.026

    # ---- Chlorine and HCl calculations ----
    chlorine_production = caustic_soda_prod * chlorine_factor
    chlorine_used_in_hypo = sodium_hypo_prod * hypo_chlorine_usage
    chlorine_neutralized = chlorine_production * chlorine_neutralization
    net_chlorine_available = chlorine_production - chlorine_used_in_hypo - chlorine_neutralized - liquid_chlorine_prod

    hcl_prod = net_chlorine_available / hcl_chlorine_usage
    hcl_in_house = caustic_soda_prod * in_house_hcl
    net_hcl_for_sale = hcl_prod - hcl_in_house

    # ---- Hydrogen calculations ----
    hydrogen_prod_mt = caustic_soda_prod * hydrogen_production_percentage
    hydrogen_prod_nm3 = hydrogen_prod_mt * 34819 / 3.12

    hydrogen_used_in_hcl = hcl_hydrogen_usage
    hydrogen_used_in_stearic = stearic_hydrogen_usage
    total_hydrogen_usage = hydrogen_used_in_hcl + hydrogen_used_in_stearic
    balance_hydrogen_nm3 = hydrogen_prod_nm3 - total_hydrogen_usage
    balance_waste_percentage = (balance_hydrogen_nm3 / hydrogen_prod_nm3) * 100 if hydrogen_prod_nm3 > 0 else 0

    # ---- Power consumption calculations ----
    total_power_used = power_rate_per_ton * caustic_soda_prod
    power_per_ton_caustic_soda = total_power_used / caustic_soda_prod if caustic_soda_prod > 0 else 0

    # ---- CS ELZ Load calculation ----
    cs_elz_load = caustic_soda_prod / 3.5 if caustic_soda_prod > 0 else 0

    return {
        "chlorine_production": chlorine_production,
        "chlorine_used_in_hypo": chlorine_used_in_hypo,
        "chlorine_neutralized": chlorine_neutralized,
        "net_chlorine_available": net_chlorine_available,
        "hcl_prod": hcl_prod,
        "hcl_in_house": hcl_in_house,
        "net_hcl_for_sale": net_hcl_for_sale,
        "hydrogen_prod_nm3": hydrogen_prod_nm3,
        "balance_hydrogen_nm3": balance_hydrogen_nm3,
        "balance_waste_percentage": balance_waste_percentage,
        "total_power_used": total_power_used,
        "power_per_ton_caustic_soda": power_per_ton_caustic_soda,
        "cs_elz_load": cs_elz_load
    }

# Input Fields
caustic_soda_prod = st.number_input("Enter Caustic Soda production in tons (TPD):", min_value=0.0, step=0.1)
sodium_hypo_prod = st.number_input("Enter Sodium Hypochlorite production in tons:", min_value=0.0, step=0.1)
stearic_batches = st.number_input("Enter number of Stearic Acid Batches:", min_value=0, step=1)
liquid_chlorine_prod = st.number_input("Enter Liquid Chlorine production in tons:", min_value=0.0, step=0.1)

# Fixed Hydrogen usage (as per your request)
hcl_hydrogen_usage = 17228  # Hydrogen used in HCl production (NM3)
stearic_hydrogen_usage = 5400  # Hydrogen used in Stearic Acid production (NM3)

# Calculate results when the button is clicked
if st.button("Calculate"):
    result = calculate_chlorine_hcl_hydrogen(caustic_soda_prod, sodium_hypo_prod, liquid_chlorine_prod, stearic_batches, hcl_hydrogen_usage, stearic_hydrogen_usage)

    # Display results
    st.subheader("Chlorine and HCl Production:")
    st.write(f"Chlorine Production: {result['chlorine_production']:.2f} tons/day")
    st.write(f"Chlorine Used in Hypo Production: {result['chlorine_used_in_hypo']:.2f} tons")
    st.write(f"Neutralized Chlorine: {result['chlorine_neutralized']:.2f} tons")
    st.write(f"Net Chlorine Available for HCl: {result['net_chlorine_available']:.2f} tons")
    st.write(f"Total HCl Production: {result['hcl_prod']:.2f} tons")
    st.write(f"HCl Used In-House: {result['hcl_in_house']:.2f} tons")
    st.write(f"Net HCl Available for Sale: {result['net_hcl_for_sale']:.2f} tons")

    st.subheader("Hydrogen Production and Usage:")
    st.write(f"Hydrogen Production: {result['hydrogen_prod_nm3']:.2f} NM3")
    st.write(f"Balance Hydrogen Waste: {result['balance_hydrogen_nm3']:.2f} NM3")
    st.write(f"Balance Hydrogen Waste Percentage: {result['balance_waste_percentage']:.2f}%")

    st.subheader("Power Consumption:")
    st.write(f"Total Power Consumption: {result['total_power_used']:.2f} KWH")
    st.write(f"Power Consumption per Ton of Caustic Soda: {result['power_per_ton_caustic_soda']:.2f} KWH/ton")

    st.subheader("CS ELZ Load:")
    st.write(f"CS ELZ Load: {result['cs_elz_load']:.4f}")
