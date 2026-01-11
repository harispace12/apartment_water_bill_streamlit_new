import streamlit as st
import pandas as pd
import json
from validations import *
from billing import *
from ocr_utils import *

st.set_page_config(page_title="Apartment Water Bill", layout="wide")
st.title("🚰 Apartment Water Bill Calculator")

with open("data/master_flats.json") as f:
    MASTER_FLATS = json.load(f)

st.header("1️⃣ Upload Meter Readings")

input_mode = st.radio(
    "Choose input method",
    ["Excel Upload", "Image Upload", "Manual Entry"]
)

readings = []

if input_mode == "Image Upload":
    img = st.file_uploader("Upload meter reading image", type=["jpg", "png"])
    if img:
        with open("temp.png", "wb") as f:
            f.write(img.getbuffer())

        extracted = extract_readings_from_image("temp.png")

        if not extracted:
            st.error("No valid meter readings detected. Please upload a clearer image.")
        else:
            df = pd.DataFrame(extracted)
            st.info("Please verify OCR results before proceeding")
            st.dataframe(df)



elif input_mode == "Manual Entry":
    flat = normalize_flat(st.text_input("Flat Number"))
    prev = st.number_input("Previous Reading", min_value=0)
    curr = st.number_input("Current Reading", min_value=0)

    if st.button("Add"):
        valid, msg = is_valid_flat(flat, MASTER_FLATS)
        if not valid:
            st.error(msg)
        else:
            readings.append({
                "flat": flat,
                "previous": prev,
                "current": curr,
                "usage": curr - prev
            })

st.header("2️⃣ Tanker Details")
tankers = st.number_input("Number of tankers", min_value=1)
total_cost = st.number_input("Total tanker cost (₹)", min_value=1)

if st.button("Calculate Bill"):
    billed, cpu = calculate_bills(readings, total_cost)
    df = pd.DataFrame(billed)
    st.success(f"Cost per unit: ₹{cpu}")
    st.dataframe(df)
