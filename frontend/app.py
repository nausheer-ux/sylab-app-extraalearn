import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Page title
st.title("ExtraaLearn Lead Conversion Prediction App")
st.write(
    "Enter the lead's details below to predict whether the lead is likely to be converted."
)

# Collect lead details
age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=30
)

current_occupation = st.selectbox(
    "Current Occupation",
    ["Unemployed", "Professional", "Student"]
)

first_interaction = st.selectbox(
    "First Interaction Channel",
    ["Website", "Mobile App"]
)

profile_completed = st.selectbox(
    "Profile Completed Status",
    ["High", "Medium", "Low"]
)

website_visits = st.number_input(
    "Website Visits",
    min_value=0,
    value=3
)

time_spent_on_website = st.number_input(
    "Time Spent on Website (seconds)",
    min_value=0.0,
    value=300.0
)

page_views_per_visit = st.number_input(
    "Page Views Per Visit",
    min_value=0.0,
    value=2.0
)

last_activity = st.selectbox(
    "Last Activity",
    ["Website Activity", "Email Activity", "Phone Activity"]
)

print_media_type1 = st.selectbox(
    "Print Media Type 1",
    ["Yes", "No"]
)

print_media_type2 = st.selectbox(
    "Print Media Type 2",
    ["Yes", "No"]
)

digital_media = st.selectbox(
    "Digital Media",
    ["Yes", "No"]
)

educational_channels = st.selectbox(
    "Educational Channels",
    ["Yes", "No"]
)

referral = st.selectbox(
    "Referral",
    ["Yes", "No"]
)

# Create JSON payload
lead_data = {
    "age": age,
    "current_occupation": current_occupation,
    "first_interaction": first_interaction,
    "profile_completed": profile_completed,
    "website_visits": website_visits,
    "time_spent_on_website": time_spent_on_website,
    "page_views_per_visit": page_views_per_visit,
    "last_activity": last_activity,
    "print_media_type1": print_media_type1,
    "print_media_type2": print_media_type2,
    "digital_media": digital_media,
    "educational_channels": educational_channels,
    "referral": referral
}

# Single Prediction
if st.button("Predict Lead Conversion", type="primary"):

    response = requests.post(
        f"{BACKEND_URL}/v1/lead",
        json=lead_data
    )

    if response.status_code == 200:
        result = response.json()

        if result["Prediction"] == "Converted":
            st.success("✅ The lead is likely to be converted!")
        else:
            st.warning("⚠️ The lead is unlikely to be converted.")

    else:
        st.error("Unable to connect to the prediction API.")

# Batch Prediction
st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict for Batch", type="primary"):

        response = requests.post(
            f"{BACKEND_URL}/v1/leadbatch",
            files={"file": uploaded_file}
        )

        if response.status_code == 200:
            results = response.json()

            st.success("Predictions completed successfully!")

            try:
                if isinstance(results, list):
                    df = pd.DataFrame(results)
                elif isinstance(results, dict):
                    # Check if all values are scalars
                    if all(not isinstance(v, (list, dict)) for v in results.values()):
                        df = pd.DataFrame([results])
                    else:
                        df = pd.DataFrame(results)
                else:
                    df = pd.DataFrame({"Result": [results]})

                st.dataframe(df, use_container_width=True)

            except Exception as e:
                st.error(f"Unable to display results as a table: {e}")
                st.json(results)

        else:
            st.error("Unable to connect to the prediction API.")
