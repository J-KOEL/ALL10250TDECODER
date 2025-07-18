import pandas as pd
import os

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
    if catalog.startswith("10250T"):
        suffix = catalog[6:]
        if len(suffix) == 4:
            result["Product Type"] = "Non-Illuminated Pushbutton"
            result["Operator"] = decode_component(suffix[0], lookup_tables.get("NonIlluminatedPushbuttonOperator 4.csv"))
            result["Button Color"] = decode_component(suffix[1], lookup_tables.get("NonIlluminatedPushbuttonButtonColor 4.csv"))
            result["Circuit"] = decode_component(suffix[2:], lookup_tables.get("Circuit 14.csv"))
        elif len(suffix) == 6:
            result["Product Type"] = "Illuminated Incandescent Pushbutton"
            result["Light Unit"] = decode_component(suffix[:3], lookup_tables.get("IlluminatedPushbuttonIncandescentLightUnit 5.csv"))
            result["Lens"] = decode_component(suffix[3:5], lookup_tables.get("illuminatedPushbuttonIncandescentLensColor 5.csv"))
            result["Circuit"] = decode_component(suffix[5:], lookup_tables.get("Circuit 14.csv"))
        elif len(suffix) == 7:
            result["Product Type"] = "Illuminated LED Pushbutton"
            result["Light Unit"] = decode_component(suffix[:3], lookup_tables.get("IlluminatedPushbuttonLEDLightUnit 7.csv"))
            result["Lens"] = decode_component(suffix[3:5], lookup_tables.get("IlluminatedPushbuttonLEDLensColor 7.csv"))
            result["Voltage"] = decode_component(suffix[5:7], lookup_tables.get("IlluminatedPushbuttonLEDVoltage 8.csv"))
            result["Circuit"] = decode_component(suffix[7:], lookup_tables.get("Circuit 14.csv"))
        elif len(suffix) == 5:
            result["Product Type"] = "Non-Illuminated Push-Pull"
            result["Operator"] = decode_component(suffix[0], lookup_tables.get("PushPullOperator 6.csv"))
            result["Button"] = decode_component(suffix[1:3], lookup_tables.get("NonIlluminatedPushPullButton 3.csv"))
            result["Circuit"] = decode_component(suffix[3:], lookup_tables.get("Circuit 14.csv"))
        elif len(suffix) == 6:
            result["Product Type"] = "Illuminated Incandescent Push-Pull"
            result["Operator"] = decode_component(suffix[0], lookup_tables.get("PushPullOperator 6.csv"))
            result["Light Unit"] = decode_component(suffix[1:4], lookup_tables.get("IlluminatedPushPullIncandescentLightUnit 3.csv"))
            result["Lens"] = decode_component(suffix[4:6], lookup_tables.get("IlluminatedPushPullIncandescentLens 3.csv"))
            result["Circuit"] = decode_component(suffix[6:], lookup_tables.get("Circuit 14.csv"))
        elif len(suffix) == 8:
            result["Product Type"] = "Illuminated LED Push-Pull"
            result["Operator"] = decode_component(suffix[0], lookup_tables.get("PushPullOperator 6.csv"))
            result["Light Unit"] = decode_component(suffix[1:4], lookup_tables.get("IlluminatedPushPullLEDLightUnit 3.csv"))
            result["Lens"] = decode_component(suffix[4:6], lookup_tables.get("IlluminatedPushPullLEDlens 3.csv"))
            result["Voltage"] = decode_component(suffix[6:8], lookup_tables.get("IlluminatedPushPullLLEDVoltage 3.csv"))
            result["Circuit"] = decode_component(suffix[8:], lookup_tables.get("Circuit 14.csv"))
        elif len(suffix) == 6:
            result["Product Type"] = "Standard Incandescent Indicating Light"
            result["Light Unit"] = decode_component(suffix[:3], lookup_tables.get("StandardIndicatingLightIncandescentLightUnit 1.csv"))
            result["Lens"] = decode_component(suffix[3:], lookup_tables.get("StandardIndicatingIncandescentLens 1.csv"))
        elif len(suffix) == 7:
            result["Product Type"] = "Standard LED Indicating Light"
            result["Light Unit"] = decode_component(suffix[:3], lookup_tables.get("StandardindicatingLightLEDlightUnit 1.csv"))
            result["Lens"] = decode_component(suffix[3:5], lookup_tables.get("StandardIndicatingLightLEDLens 1.csv"))
            result["Voltage"] = decode_component(suffix[5:7], lookup_tables.get("IndicatinglightLEDvoltage 2.csv"))
        else:
            result["Product Type"] = "Unknown 10250T Format"
    else:
        if len(catalog) == 6:
            result["Product Type"] = "Incandescent PresTest"
            result["Light Unit"] = decode_component(catalog[:3], lookup_tables.get("PrestTestIncandescentLightUnit 1.csv"))
            result["Lens"] = decode_component(catalog[3:], lookup_tables.get("PrestTestIncandescentLens 1.csv"))
        elif len(catalog) == 7:
            result["Product Type"] = "LED PresTest"
            result["Light Unit"] = decode_component(catalog[:3], lookup_tables.get("PrestTestLEDLightunit 1.csv"))
            result["Lens"] = decode_component(catalog[3:5], lookup_tables.get("PrestTestLEDLens 1.csv"))
            result["Voltage"] = decode_component(catalog[5:7], lookup_tables.get("IndicatinglightLEDvoltage 2.csv"))
        elif len(catalog) == 6:
            result["Product Type"] = "Master Test"
            result["Light Unit"] = decode_component(catalog[:3], lookup_tables.get("MasterTestIncandescentLightUnit 1.csv"))
            result["Lens"] = decode_component(catalog[3:], lookup_tables.get("MasterTestIncandescentLens 1.csv"))
        else:
            result["Product Type"] = "Unknown Format"
    return result
