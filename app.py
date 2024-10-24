import streamlit as st
from PIL import Image
import os

# Title of the app
st.title("Chlorine, HCl, Hydrogen Production Calculator")
st.markdown("### Developed by [Your Name or Company]")

# Load NIMIR logo
logo_path = 'images/nimir_logo.png'  # Change this path if needed
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    # Display logo on the top right
    st.image(logo, use_column_width=False, width=150)
else:
    st.warning("NIMIR logo not found. Please ensure the image file is in the correct folder.")

# Function to calculate chlorine, HCl, hydrogen production, power consumption, and CS ELZ load
def calculate_chlorine_hcl_hydrogen(caustic_soda_prod, sodium_hypo_prod, liquid_chlorine_prod, stearic_batches, hcl_hydrogen_usage):
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
    hydrogen_used_in_stearic = stearic_batches * 600  # Hydrogen used in Stearic Acid batches (No of batches * 600 NM3)
    total_hydrogen_usage = hydrogen_used_in_hcl + hydrogen_used_in_stearic  # Total hydrogen used
    balance_hydrogen_nm3 = hydrogen_prod_nm3 - total_hydrogen_usage  # Remaining hydrogen after usage
    balance_waste_percentage = (balance_hydrogen_nm3 / hydrogen_prod_nm3) * 100 if hydrogen_prod_nm3 > 0 else 0  # Percentage of hydrogen wasted

    # ---- Power consumption calculations ----
    total_power_used = power_rate_per_ton * caustic_soda_prod  # Total power used based on production
    power_per_ton_caustic_soda = total_power_used / caustic_soda_prod if caustic_soda_prod > 0 else 0  # Power used per ton of caustic soda

    # ---- CS ELZ Load calculation ----
    cs_elz_load = caustic_soda_prod / 3.5 if caustic_soda_prod > 0 else 0  # CS ELZ Load calculation

    # Return results
    return {
        'chlorine_production': chlorine_production,
        'chlorine_used_in_hypo': chlorine_used_in_hypo,
        'chlorine_neutralized': chlorine_neutralized,
        'net_chlorine_available': net_chlorine_available,
        'hcl_prod': hcl_prod,
        'hcl_in_house': hcl_in_house,
        'net_hcl_for_sale': net_hcl_for_sale,
        'hydrogen_prod_mt': hydrogen_prod_mt,
        'hydrogen_prod_nm3': hydrogen_prod_nm3,
        'hydrogen_used_in_stearic': hydrogen_used_in_stearic,
        'balance_hydrogen_nm3': balance_hydrogen_nm3,
        'balance_waste_percentage': balance_waste_percentage,
        'total_power_used': total_power_used,
        'power_per_ton_caustic_soda': power_per_ton_caustic_soda,
        'cs_elz_load': cs_elz_load
    }

# Streamlit inputs for user data
caustic_soda_prod = st.number_input("Enter Caustic Soda production in tons (TPD):", min_value=0.0, step=0.1)
sodium_hypo_prod = st.number_input("Enter Sodium Hypochlorite production in tons:", min_value=0.0, step=0.1)
liquid_chlorine_prod = st.number_input("Enter Liquid Chlorine production in tons:", min_value=0.0, step=0.1)
stearic_batches = st.number_input("Enter number of Stearic Acid Batches:", min_value=0, step=1)

# Fixed hydrogen usage data for HCl production
hcl_hydrogen_usage = 17228  # Hydrogen used in HCl production (NM3)

# Perform calculations when the user clicks the button
if st.button('Calculate'):
    results = calculate_chlorine_hcl_hydrogen(caustic_soda_prod, sodium_hypo_prod, liquid_chlorine_prod, stearic_batches, hcl_hydrogen_usage)

    # Display the results
    st.subheader("Results")
    st.write(f"**Chlorine Production:** {results['chlorine_production']:.2f} tons/day")
    st.write(f"**Chlorine Used in Hypo Production:** {results['chlorine_used_in_hypo']:.2f} tons")
    st.write(f"**Neutralized Chlorine:** {results['chlorine_neutralized']:.2f} tons")
    st.write(f"**Net Chlorine Available for HCl Production:** {results['net_chlorine_available']:.2f} tons")
    st.write(f"**Total HCl Production:** {results['hcl_prod']:.2f} tons")
    st.write(f"**HCl Used In-House:** {results['hcl_in_house']:.2f} tons")
    st.write(f"**Net HCl Available for Sale:** {results['net_hcl_for_sale']:.2f} tons")
    
    st.write(f"**Hydrogen Production:** {results['hydrogen_prod_mt']:.2f} MT or {results['hydrogen_prod_nm3']:.2f} NM3")
    st.write(f"**Hydrogen Used in Stearic Acid Batches:** {results['hydrogen_used_in_stearic']:.2f} NM3")
    st.write(f"**Balance Hydrogen Waste:** {results['balance_hydrogen_nm3']:.2f} NM3")
    st.write(f"**Balance Hydrogen Waste Percentage:** {results['balance_waste_percentage']:.2f}%")
    
    st.write(f"**Total Power Consumption:** {results['total_power_used']:.2f} KWH")
    st.write(f"**Power Consumption per Ton of Caustic Soda:** {results['power_per_ton_caustic_soda']:.2f} KWH/ton")
    
    st.write(f"**CS ELZ Load:** {results['cs_elz_load']:.4f}")

# Footer with attribution
st.markdown("---")
st.markdown("Developed by [Your Name or Company]")
