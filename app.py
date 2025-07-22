import streamlit as st
from decoder import load_csv_files, load_catalog_reference, decode_catalog_number

# Set up the Streamlit app
st.set_page_config(page_title="10250T Catalog Decoder", layout="centered")

st.title("🔍 10250T Catalog Number Decoder")
st.markdown("Enter a full catalog number (e.g., `10250T411C21-C1`) to decode it into its components.")

# Input field for catalog number
catalog_input = st.text_input("Catalog Number", placeholder="e.g., 10250T411C21-51")

if catalog_input:
    try:
        # Normalize input
        normalized_input = catalog_input.strip().replace("-", "").upper()

        # Load lookup tables and catalog reference
        lookup_tables = load_csv_files()
        catalog_reference = load_catalog_reference()

        # Decode the catalog number
        decoded = decode_catalog_number(normalized_input, lookup_tables, catalog_reference)

        # Display decoded components
        st.subheader("🧩 Decoded Components")
        for key, value in decoded.items():
            st.markdown(f"**{key}**: {value}")

    except Exception as e:
        st.error(f"An error occurred during decoding: {e}")

