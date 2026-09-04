from datetime import date
import re

import pandas as pd
import streamlit as st
from supabase import create_client


st.set_page_config(
    page_title="Mamma's Happy Health Tracker",
    page_icon="💜",
    layout="centered",
)


# -----------------------------
# SUPABASE CONNECTION
# -----------------------------

@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )


supabase = get_supabase()

st.write("DEBUG: Supabase connection loaded")

import base64
import json

try:
    token = st.secrets["SUPABASE_KEY"]
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    decoded = json.loads(
        base64.urlsafe_b64decode(payload)
    )
    st.write("DEBUG: Supabase key role:", decoded.get("role"))
except Exception as e:
    st.write("DEBUG: Could not inspect key role:", e)

# -----------------------------
# FREE FOOD DATABASE
# Calories and protein are
# approximate per serving.
# -----------------------------

FOODS = {
    "roti": {"calories": 100, "protein": 3},
    "chapati": {"calories": 100, "protein": 3},
    "paratha": {"calories": 180, "protein": 4},
    "rice": {"calories": 200, "protein": 4},
    "dal": {"calories": 180, "protein": 9},
    "curd": {"calories": 100, "protein": 5},
    "yogurt": {"calories": 100, "protein": 5},
    "paneer": {"calories": 265, "protein": 18},
    "milk": {"calories": 120, "protein": 6},
    "bread": {"calories": 70, "protein": 3},
    "banana": {"calories": 105, "protein": 1.3},
    "apple": {"calories": 95, "protein": 0.5},
    "mango": {"calories": 100, "protein": 1},
    "egg": {"calories": 75, "protein": 6},
    "chicken": {"calories": 240, "protein": 27},
    "vegetables": {"calories": 120, "protein": 4},
    "sabzi": {"calories": 120, "protein": 4},
    "salad": {"calories": 50, "protein": 2},
    "pickle": {"calories": 20, "protein": 0},
    "tea": {"calories": 60, "protein": 2},
    "coffee": {"calories": 60, "protein": 2},
}


# -----------------------------
# FOOD CALCULATOR
# -----------------------------

def analyze_food(food_description):
    text = food_description.lower()

    total_calories = 0
    total_protein = 0
    found_foods = []

    for food, nutrition in FOODS.items():

        if food in text:

            # Look for a number immediately before the food.
            pattern = rf"(\d+(?:\.\d+)?)\s*(?:x\s*)?{re.escape(food)}"
            match = re.search(pattern, text)

            if match:
                quantity = float(match.group(1))
            else:
                quantity = 1

            total_calories += nutrition["calories"] * quantity
            total_protein += nutrition["protein"] * quantity

            found_foods.append(
                f"{quantity:g} × {food}"
            )

    if not found_foods:
        raise ValueError(
            "I couldn't recognize any foods in that description. "
            "Try foods such as roti, rice, dal, curd, paneer, "
            "banana, apple, mango, milk, bread, egg, or vegetables."
        )

    summary = "Recognized: " + ", ".join(found_foods)

    assumptions = (
        "Values are approximate and use the app's built-in "
        "serving estimates."
    )

    return {
        "calories": total_calories,
        "protein_g": total_protein,
        "summary": summary,
        "assumptions": assumptions,
    }


# -----------------------------
# SAVE RECORD
# -----------------------------

def save_record(record):
    supabase.table("food_records").insert(record).execute()


# -----------------------------
# LOAD HISTORY
# -----------------------------

def load_history():
    response = (
        supabase
        .table("food_records")
        .select("*")
        .order("entry_date", desc=True)
        .execute()
    )

    return response.data or []


# -----------------------------
# APP UI
# -----------------------------

st.title("💜 Mamma's Happy Health Tracker")

today = date.today()

st.subheader(today.strftime("%A, %d %B %Y"))

st.write(
    "Type what Mumma ate today. The app will estimate "
    "calories and protein using its free built-in food database."
)


food = st.text_area(
    "🍽️ What did Mumma eat today?",
    placeholder=(
        "Example: 2 roti, 1 bowl dal, 1 mango, "
        "1 cup curd"
    ),
    height=150,
)


if st.button("✨ Calculate & Save", use_container_width=True):

    if not food.strip():

        st.warning("Please describe what Mumma ate first.")

    else:

        with st.spinner("🧮 Calculating nutrition..."):

            try:

                result = analyze_food(food)

                calories = float(result["calories"])
                protein = float(result["protein_g"])

                record = {
                    "entry_date": str(today),
                    "food_description": food.strip(),
                    "calories": calories,
                    "protein_g": protein,
                    "summary": result.get("summary", ""),
                    "assumptions": result.get("assumptions", ""),
                }

                save_record(record)

                st.success("✅ Today's food has been saved!")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "🔥 Estimated calories",
                        f"{calories:.0f} kcal"
                    )

                with col2:
                    st.metric(
                        "💪 Estimated protein",
                        f"{protein:.1f} g"
                    )

                if result.get("summary"):
                    st.info(result["summary"])

                if result.get("assumptions"):
                    st.caption(
                        "Assumptions: "
                        + result["assumptions"]
                    )

            except Exception as e:

                st.error(
                    "Something went wrong while calculating or saving."
                )

                st.caption(str(e))


# -----------------------------
# HISTORY
# -----------------------------

st.divider()

st.header("📚 Your History")


try:

    history = load_history()

    if history:

        df = pd.DataFrame(history)

        if "entry_date" in df.columns:

            df["entry_date"] = pd.to_datetime(
                df["entry_date"]
            )

            df = df.sort_values(
                "entry_date",
                ascending=False
            )

        display_columns = [
            "entry_date",
            "food_description",
            "calories",
            "protein_g",
        ]

        available_columns = [
            column
            for column in display_columns
            if column in df.columns
        ]

        st.dataframe(
            df[available_columns],
            use_container_width=True,
            hide_index=True,
        )

        st.header("📊 Summary")

        average_calories = df["calories"].mean()
        average_protein = df["protein_g"].mean()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Days recorded",
                len(df)
            )

        with col2:

            st.metric(
                "Average calories",
                f"{average_calories:.0f} kcal"
            )

        st.metric(
            "Average protein",
            f"{average_protein:.1f} g"
        )

    else:

        st.info("No saved food records yet.")


except Exception as e:

    st.error("Couldn't load the saved history.")
    st.caption(str(e))


st.divider()

st.caption(
    "Nutrition values are estimates and should not be treated "
    "as medical advice."
)
