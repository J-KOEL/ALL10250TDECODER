import streamlit as st
from decoder import load_csv_files, decode_catalog_number

st.set_page_config(page_title="10250T Catalog Decoder", layout="centered")

st.title("🔍 10250T Catalog Number Decoder")
st.markdown("Enter a full catalog number (e.g., `10250T411C21-C1`) to decode it into its components.")

catalog_input = st.text_input("Catalog Number", placeholder="e.g., 10250T411C21-C1")

if catalog_input:
    lookup_tables = load_csv_files()
    decoded = decode_catalog_number(catalog_input.strip(), lookup_tables)

    st.subheader("🧩 Decoded Components")
    for key, value in decoded.items():
        st.markdown(f"**{key}**: {value}")
