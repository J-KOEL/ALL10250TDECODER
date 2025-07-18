import streamlit as st
import pandas as pd
import os

# Load all CSV files into a dictionary of DataFrames
def load_csv_files():
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    lookup_tables = {}
    for file in csv_files:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        df['Code'] = df['Code'].astype(str).str.strip()
        df['Label'] = df['Label'].astype(str).str.strip()
        lookup_tables[file] = df
    return lookup_tables

# Helper function to find label from code using a lookup table
def decode_component(code, df):
    match = df[df['Code'] == code]
    if not match.empty:
        return match['Label'].values[0]
    return "Unknown"

# Define decoding logic for each product type
def decode_catalog_number(catalog, lookup_tables):
    result = {"Catalog Number": catalog}
    if catalog.startswith("10250T"):
        suffix = catalog[6:]
        if len(suffix) == 4:
            # Non-Illuminated Pushbutton
            operator = suffix[0]
            color = suffix[1]
            circuit = suffix[2:]
            result["Product Type"] = "Non-Illuminated Pushbutton"
            result["Operator"] = decode_component(operator, lookup_tables.get("NonIlluminatedPushbuttonOperator .csv", pd.DataFrame()))
            result["Button Color"] = decode_component(color, lookup_tables.get("NonIlluminatedPushbuttonButtonColor .csv", pd.DataFrame()))
            result["Circuit"] = decode_component(circuit, lookup_tables.get("Circuit.csv", pd.DataFrame()))
        elif len(suffix) == 6:
            # Illuminated Incandescent Pushbutton
            light = suffix[:3]
            lens = suffix[3:5]
            circuit = suffix[5:]
            result["Product Type"] = "Illuminated Incandescent Pushbutton"
            result["Light Unit"] = decode_component(light, lookup_tables.get("IlluminatedPushbuttonIncandescentLightUnit.csv", pd.DataFrame()))
            result["Lens"] = decode_component(lens, lookup_tables.get("illuminatedPushbuttonIncandescentLensColor.csv", pd.DataFrame()))
            result["Circuit"] = decode_component(circuit, lookup_tables.get("Circuit.csv", pd.DataFrame()))
        elif len(suffix) == 7:
            # Illuminated LED Pushbutton
            light = suffix[:3]
            lens = suffix[3:5]
            voltage = suffix[5:7]
            circuit = suffix[7:]
            result["Product Type"] = "Illuminated LED Pushbutton"
            result["Light Unit"] = decode_component(light, lookup_tables.get("IlluminatedPushbuttonLEDLightUnit.csv", pd.DataFrame()))
            result["Lens"] = decode_component(lens, lookup_tables.get("IlluminatedPushbuttonLEDLensColor.csv", pd.DataFrame()))
            result["Voltage"] = decode_component(voltage, lookup_tables.get("IlluminatedPushbuttonLEDVoltage.csv", pd.DataFrame()))
            result["Circuit"] = decode_component(circuit, lookup_tables.get("Circuit.csv", pd.DataFrame()))
        else:
            result["Product Type"] = "Unknown 10250T Format"
    else:
        # Handle non-10250T formats
        if len(catalog) == 6:
            # Master Test
            light = catalog[:3]
            lens = catalog[3:]
            result["Product Type"] = "Master Test"
            result["Light Unit"] = decode_component(light, lookup_tables.get("MasterTestIncandescentLightUnit.csv", pd.DataFrame()))
            result["Lens"] = decode_component(lens, lookup_tables.get("MasterTestIncandescentLens.csv", pd.DataFrame()))
        else:
            result["Product Type"] = "Unknown Format"
    return result

# Streamlit UI
st.title("🔍 10250T Catalog Number Decoder")
st.write("Enter a full catalog number to decode it into its components.")

catalog_input = st.text_input("Catalog Number", "")

if catalog_input:
    lookup_tables = load_csv_files()
    decoded = decode_catalog_number(catalog_input.strip(), lookup_tables)
    st.subheader("🧩 Decoded Components")
    for key, value in decoded.items():
        st.write(f"**{key}**: {value}")
