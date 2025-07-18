import pandas as pd
import os
import re

# Load all CSV files into a dictionary of DataFrames
def load_csv_files():
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    lookup_tables = {}
    for file in csv_files:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip()
        if 'Code' in df.columns and 'Label' in df.columns:
            df['Code'] = df['Code'].astype(str).str.strip()
            df['Label'] = df['Label'].astype(str).str.strip()
            lookup_tables[file] = df
    return lookup_tables

# Helper function to find label from code using a lookup table
def decode_component(code, df):
    if df is not None and not df.empty:
        match = df[df['Code'] == code]
        if not match.empty:
            return match['Label'].values[0]
    return "Unknown"

# Define decoding logic for each product type
def decode_catalog_number(catalog, lookup_tables):
    result = {"Catalog Number": catalog}
    catalog = catalog.strip().upper()

    # Remove hyphen before circuit code if present
    if '-' in catalog:
        base, circuit = catalog.split('-', 1)
        catalog = base + circuit

    if not catalog.startswith("10250T"):
        result["Product Type"] = "Invalid: Must start with '10250T'"
        return result

    suffix = catalog[6:]

    # Try matching known product types based on suffix length and patterns
    if re.fullmatch(r'[A-Z0-9]{4}', suffix):
        result["Product Type"] = "Non-Illuminated Pushbutton"
        result["Operator"] = decode_component(suffix[0], lookup_tables.get("NonIlluminatedPushbuttonOperator.csv"))
        result["Button Color"] = decode_component(suffix[1], lookup_tables.get("NonIlluminatedPushbuttonButtonColor.csv"))
        result["Circuit"] = decode_component(suffix[2:], lookup_tables.get("Circuit.csv"))

    elif re.fullmatch(r'[A-Z0-9]{6}', suffix):
        result["Product Type"] = "Illuminated Incandescent Pushbutton"
        result["Light Unit"] = decode_component(suffix[:3], lookup_tables.get("IlluminatedPushbuttonIncandescentLightUnit.csv"))
        result["Lens"] = decode_component(suffix[3:5], lookup_tables.get("illuminatedPushbuttonIncandescentLensColor.csv"))
        result["Circuit"] = decode_component(suffix[5:], lookup_tables.get("Circuit.csv"))

    elif re.fullmatch(r'[A-Z0-9]{8}', suffix):
        result["Product Type"] = "Illuminated LED Pushbutton"
        result["Light Unit"] = decode_component(suffix[:3], lookup_tables.get("IlluminatedPushbuttonLEDLightUnit.csv"))
        result["Lens"] = decode_component(suffix[3:5], lookup_tables.get("IlluminatedPushbuttonLEDLensColor.csv"))
        result["Voltage"] = decode_component(suffix[5:7], lookup_tables.get("IlluminatedPushbuttonLEDVoltage.csv"))
        result["Circuit"] = decode_component(suffix[7:], lookup_tables.get("Circuit.csv"))

    elif re.fullmatch(r'[A-Z0-9]{5}', suffix):
        result["Product Type"] = "Non-Illuminated Push-Pull"
        result["Operator"] = decode_component(suffix[0], lookup_tables.get("PushPullOperator.csv"))
        result["Button"] = decode_component(suffix[1:3], lookup_tables.get("NonIlluminatedPushPullButton.csv"))
        result["Circuit"] = decode_component(suffix[3:], lookup_tables.get("Circuit.csv"))

    elif re.fullmatch(r'[A-Z0-9]{6}', suffix):
        result["Product Type"] = "Illuminated Incandescent Push-Pull"
        result["Operator"] = decode_component(suffix[0], lookup_tables.get("PushPullOperator.csv"))
        result["Light Unit"] = decode_component(suffix[1:4], lookup_tables.get("IlluminatedPushPullIncandescentLightUnit.csv"))
        result["Lens"] = decode_component(suffix[4:6], lookup_tables.get("IlluminatedPushPullIncandescentLens.csv"))
        result["Circuit"] = decode_component(suffix[6:], lookup_tables.get("Circuit.csv"))

    elif re.fullmatch(r'[A-Z0-9]{8}', suffix):
        result["Product Type"] = "Illuminated LED Push-Pull"
        result["Operator"] = decode_component(suffix[0], lookup_tables.get("PushPullOperator 6.csv"))
        result["Light Unit"] = decode_component(suffix[1:4], lookup_tables.get("IlluminatedPushPullLEDLightUnit 3.csv"))
        result["Lens"] = decode_component(suffix[4:6], lookup_tables.get("IlluminatedPushPullLEDlens 3.csv"))
        result["Voltage"] = decode_component(suffix[6:8], lookup_tables.get("IlluminatedPushPullLLEDVoltage 3.csv"))
        result["Circuit"] = decode_component(suffix[8:], lookup_tables.get("Circuit 14.csv"))

    elif re.fullmatch(r'[A-Z0-9]{6}', suffix):
        result["Product Type"] = "Standard Incandescent Indicating Light"
        result["Light Unit"] = decode_component(suffix[:3], lookup_tables.get("StandardIndicatingLightIncandescentLightUnit.csv"))
        result["Lens"] = decode_component(suffix[3:], lookup_tables.get("StandardIndicatingIncandescentLens.csv"))

    elif re.fullmatch(r'[A-Z0-9]{7}', suffix):
        result["Product Type"] = "Standard LED Indicating Light"
        result["Light Unit"] = decode_component(suffix[:3], lookup_tables.get("StandardindicatingLightLEDlightUnit.csv"))
        result["Lens"] = decode_component(suffix[3:5], lookup_tables.get("StandardIndicatingLightLEDLens.csv"))
        result["Voltage"] = decode_component(suffix[5:7], lookup_tables.get("IndicatinglightLEDvoltage.csv"))

    else:
        result["Product Type"] = "Unknown or Unsupported Format"

    return result
