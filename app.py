import streamlit as st
from datetime import date
from supabase import create_client

st.set_page_config(page_title="Health Tracker", page_icon="🥗")

# Supabase connection
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_SECRET_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🥗 Health Tracker")

food = st.text_input("What did you eat?", placeholder="Example: 2 rotis and dal")

calories = st.number_input("Calories", min_value=0.0, value=100.0)
protein = st.number_input("Protein (g)", min_value=0.0, value=5.0)

if st.button("Save Food"):

    try:
        record = {
            "entry_date": str(date.today()),
            "food_description": food,
            "calories": calories,
            "protein_g": protein,
            "summary": "Food entry",
            "assumptions": ""
        }

        response = supabase.table("food_records").insert(record).execute()

        st.success("✅ SAVED SUCCESSFULLY!")
        st.write(response.data)

    except Exception as e:
        st.error("❌ Save failed")
        st.write(e)

st.divider()

st.subheader("History")

try:
    history = (
        supabase
        .table("food_records")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    if history.data:
        st.dataframe(history.data)
    else:
        st.info("No saved food records yet.")

except Exception as e:
    st.error("Could not load history.")
    st.write(e)
