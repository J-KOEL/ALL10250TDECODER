import streamlit as st
from decoder import load_csv_files, decode_catalog_number

st.title("🔍 10250T Catalog Number Decoder")
st.write("Enter a full catalog number to decode it into its components.")

catalog_input = st.text_input("Catalog Number", "")

if catalog_input:
    lookup_tables = load_csv_files()
    decoded = decode_catalog_number(catalog_input.strip(), lookup_tables)
    st.subheader("🧩 Decoded Components")
    for key, value in decoded.items():
        st.write(f"**{key}**: {value}")
