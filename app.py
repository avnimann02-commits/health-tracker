import json
from datetime import date

import pandas as pd
import streamlit as st
from openai import OpenAI
from supabase import create_client

st.set_page_config(
    page_title="Mamma's Happy Health Tracker",
    page_icon="💜",
    layout="centered",
)

st.success("NEW CODE IS RUNNING")

@st.cache_resource
def get_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )

@st.cache_resource
def get_openai():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


supabase = get_supabase()
client = get_openai()


def analyze_food(food_description):
    prompt = f"""
You are a careful nutrition-estimation assistant.

Estimate the calories and protein for the food described below.

Food eaten:
{food_description}

Important:
- Use reasonable typical Indian serving sizes when quantities are not given.
- If quantities are given, use them.
- Give an estimate, not a laboratory measurement.
- If something is unclear, make a reasonable assumption and mention it.
- Do not encourage crash dieting or extremely low calorie intake.

Return ONLY valid JSON in exactly this format:

{{
  "calories": number,
  "protein_g": number,
  "summary": "short explanation",
  "assumptions": "important assumptions"
}}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
    )

    text = response.output_text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)


def save_record(record):
    supabase.table("food_records").insert(record).execute()


def load_history():
    response = (
        supabase
        .table("food_records")
        .select("*")
        .order("entry_date", desc=True)
        .execute()
    )
    return response.data or []


st.title("💜 Mamma's Happy Health Tracker")

today = date.today()

st.subheader(today.strftime("%A, %d %B %Y"))

st.write(
    "Type what Mumma ate today. The app will estimate calories "
    "and protein automatically."
)

food = st.text_area(
    "🍽️ What did Mumma eat today?",
    placeholder=(
        "Example: Breakfast - 2 parathas and curd. "
        "Lunch - dal, rice and salad. "
        "Snack - mango. Dinner - 2 rotis and paneer."
    ),
    height=150,
)

if st.button("✨ Calculate & Save", use_container_width=True):

    if not food.strip():
        st.warning("Please describe what Mumma ate first.")

    else:
        with st.spinner("🧠 Calculating nutrition..."):

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
                        "Assumptions: " + result["assumptions"]
                    )

            except Exception as e:
                st.error(
                    "Something went wrong while calculating or saving."
                )
                st.caption(str(e))


st.divider()

st.header("📚 Your History")

try:
    history = load_history()

    if history:

        df = pd.DataFrame(history)

        if "entry_date" in df.columns:
            df["entry_date"] = pd.to_datetime(df["entry_date"])
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
    "Nutrition values are estimates and should not be treated as medical advice."
)
