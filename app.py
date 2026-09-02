import streamlit as st
from datetime import datetime
import json
from pathlib import Path

# ============================================================
# 💜 MOM'S HAPPY HEALTH TRACKER
# ============================================================

st.set_page_config(
    page_title="Mamma's Happy Health Tracker 💜",
    page_icon="💜",
    layout="centered"
)

# ============================================================
# SETTINGS
# ============================================================

CALORIE_TARGET = 1800
PROTEIN_TARGET = 100

DATA_FILE = Path("mom_data.json")

# ============================================================
# COLORS / STYLE
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg, #F8EEFF 0%, #FFF5FA 100%);
}

.main-title {
    text-align: center;
    color: #7B2CBF;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #6B6570;
    font-size: 17px;
    margin-bottom: 25px;
}

.date-box {
    background: white;
    padding: 12px;
    border-radius: 15px;
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-top: 15px;
    margin-bottom: 15px;
}

.good {
    background: #E8F7EE;
    padding: 18px;
    border-radius: 18px;
    border-left: 7px solid #2E9D62;
}

.warning {
    background: #FFF8D9;
    padding: 18px;
    border-radius: 18px;
    border-left: 7px solid #F4B400;
}

.high {
    background: #FFE8E8;
    padding: 18px;
    border-radius: 18px;
    border-left: 7px solid #D64545;
}

.big-button {
    font-size: 20px !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LANGUAGE
# ============================================================

language = st.sidebar.radio(
    "🌐 Language / भाषा",
    ["English", "हिन्दी"]
)

if language == "English":

    TEXT = {
        "title": "💜 Mamma's Happy Health Tracker",
        "subtitle": "A simple little place to check in every day 🌸",
        "food": "🍽️ What did you eat today?",
        "food_hint": "Example: roti, dal, curd, fruit...",
        "calories": "🔥 Approximate calories",
        "protein": "💪 Protein (grams)",
        "save": "💜 SAVE TODAY",
        "history": "📊 Your History",
        "recommendation": "💡 Today's Recommendation",
        "balanced": "🌟 BALANCED DAY",
        "lower": "💚 LOWER THAN USUAL",
        "higher": "🌼 A LITTLE HIGHER TODAY",
        "saved": "Your day has been saved! 💜",
        "empty": "Please enter your calories.",
        "lowest": "Lowest recorded day",
        "highest": "Highest recorded day",
        "average": "Average calories",
        "days": "Days recorded",
        "protein_tip": "Protein check",
        "good_protein": "Great protein intake today! 💪",
        "more_protein": "Try including a little more protein in your meals.",
        "balanced_tip":
            "Nice! Your calories are close to your usual target. "
            "Keep meals balanced with protein, vegetables, fruit and enough water.",
        "lower_tip":
            "Today's calories are lower than your usual target. "
            "Make sure you're still getting enough nutritious food.",
        "higher_tip":
            "Today's calories are a little above your usual target. "
            "No need to panic—just aim for balanced portions at your next meal.",
        "food_note": "🍽️ Food note",
        "no_food": "No food details entered.",
        "no_history": "Your history will appear here after your first entry.",
    }

else:

    TEXT = {
        "title": "💜 मम्मा का हैप्पी हेल्थ ट्रैकर",
        "subtitle": "हर दिन का आसान और प्यारा चेक-इन 🌸",
        "food": "🍽️ आज आपने क्या खाया?",
        "food_hint": "जैसे: रोटी, दाल, दही, फल...",
        "calories": "🔥 लगभग कितनी कैलोरी?",
        "protein": "💪 प्रोटीन (ग्राम)",
        "save": "💜 आज सेव करें",
        "history": "📊 आपका रिकॉर्ड",
        "recommendation": "💡 आज की सलाह",
        "balanced": "🌟 संतुलित दिन",
        "lower": "💚 आज सामान्य से कम",
        "higher": "🌼 आज थोड़ी ज़्यादा",
        "saved": "आज का रिकॉर्ड सेव हो गया! 💜",
        "empty": "कृपया कैलोरी लिखें।",
        "lowest": "सबसे कम रिकॉर्ड",
        "highest": "सबसे ज़्यादा रिकॉर्ड",
        "average": "औसत कैलोरी",
        "days": "कुल दिन",
        "protein_tip": "प्रोटीन चेक",
        "good_protein": "आज प्रोटीन की मात्रा अच्छी है! 💪",
        "more_protein": "अपने भोजन में थोड़ा और प्रोटीन शामिल करने की कोशिश करें।",
        "balanced_tip":
            "बहुत अच्छा! आज की कैलोरी आपके सामान्य लक्ष्य के करीब है। "
            "प्रोटीन, सब्ज़ियाँ, फल और पर्याप्त पानी लेते रहें।",
        "lower_tip":
            "आज की कैलोरी आपके सामान्य लक्ष्य से कम है। "
            "यह ध्यान रखें कि आपको पर्याप्त पौष्टिक भोजन मिलता रहे।",
        "higher_tip":
            "आज की कैलोरी आपके सामान्य लक्ष्य से थोड़ी ज़्यादा है। "
            "चिंता की जरूरत नहीं—अगले भोजन में संतुलित मात्रा रखें।",
        "food_note": "🍽️ खाने की जानकारी",
        "no_food": "खाने की जानकारी नहीं दी गई।",
        "no_history": "पहली एंट्री के बाद आपका रिकॉर्ड यहाँ दिखाई देगा।",
    }

# ============================================================
# DATA FUNCTIONS
# ============================================================

def load_data():

    if DATA_FILE.exists():

        try:

            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)

        except:
            return []

    return []


def save_data(data):

    with open(DATA_FILE, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


data = load_data()

# ============================================================
# HEADER
# ============================================================

st.markdown(
    f'<div class="main-title">{TEXT["title"]}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{TEXT["subtitle"]}</div>',
    unsafe_allow_html=True
)

today = datetime.now()

st.markdown(
    f"""
    <div class="date-box">
    📅 {today.strftime("%A")} • {today.strftime("%d %B %Y")}
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# INPUT FORM
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

food = st.text_area(
    TEXT["food"],
    placeholder=TEXT["food_hint"],
    height=100
)

calories = st.number_input(
    TEXT["calories"],
    min_value=0,
    max_value=10000,
    value=0,
    step=50
)

protein = st.number_input(
    TEXT["protein"],
    min_value=0,
    max_value=500,
    value=0,
    step=5
)

save_button = st.button(
    TEXT["save"],
    use_container_width=True,
    type="primary"
)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# SAVE ENTRY
# ============================================================

if save_button:

    if calories <= 0:

        st.error(TEXT["empty"])

    else:

        date_string = today.strftime("%d %B %Y")

        new_entry = {
            "date": date_string,
            "day": today.strftime("%A"),
            "calories": int(calories),
            "protein": int(protein),
            "food": food
        }

        # Replace today's entry if it already exists
        data = [
            entry for entry in data
            if entry["date"] != date_string
        ]

        data.append(new_entry)

        save_data(data)

        st.success(TEXT["saved"])

# ============================================================
# CURRENT STATUS
# ============================================================

if calories > 0:

    difference = calories - CALORIE_TARGET

    if abs(difference) <= CALORIE_TARGET * 0.10:

        status = "balanced"

        st.markdown(
            f"""
            <div class="good">
            <h3>{TEXT["balanced"]}</h3>
            <p>{TEXT["balanced_tip"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    elif calories < CALORIE_TARGET:

        status = "lower"

        st.markdown(
            f"""
            <div class="good">
            <h3>{TEXT["lower"]}</h3>
            <p>{TEXT["lower_tip"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        status = "higher"

        st.markdown(
            f"""
            <div class="warning">
            <h3>{TEXT["higher"]}</h3>
            <p>{TEXT["higher_tip"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# PROTEIN CHECK
# ============================================================

if protein > 0:

    st.markdown(
        f'<div class="card"><h3>💪 {TEXT["protein_tip"]}</h3>',
        unsafe_allow_html=True
    )

    if protein >= PROTEIN_TARGET:

        st.success(TEXT["good_protein"])

    else:

        st.info(TEXT["more_protein"])

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# HISTORY
# ============================================================

st.markdown(
    f"## {TEXT['history']}"
)

if len(data) == 0:

    st.info(TEXT["no_history"])

else:

    calorie_values = [
        entry["calories"]
        for entry in data
    ]

    lowest_entry = min(
        data,
        key=lambda x: x["calories"]
    )

    highest_entry = max(
        data,
        key=lambda x: x["calories"]
    )

    average_calories = sum(calorie_values) / len(calorie_values)

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            TEXT["lowest"],
            f"{lowest_entry['calories']} kcal"
        )

    with col2:

        st.metric(
            TEXT["highest"],
            f"{highest_entry['calories']} kcal"
        )

    col3, col4 = st.columns(2)

    with col3:

        st.metric(
            TEXT["average"],
            f"{average_calories:.0f} kcal"
        )

    with col4:

        st.metric(
            TEXT["days"],
            len(data)
        )

    # ========================================================
    # DAILY RECORDS
    # ========================================================

    st.markdown("### 📅 Daily Records")

    for entry in reversed(data):

        with st.expander(
            f"📅 {entry['day']} • {entry['date']}"
        ):

            st.write(
                f"🔥 **{TEXT['calories']}:** "
                f"{entry['calories']} kcal"
            )

            st.write(
                f"💪 **{TEXT['protein']}:** "
                f"{entry['protein']} g"
            )

            st.write(
                f"🍽️ **{TEXT['food_note']}:** "
                f"{entry['food'] or TEXT['no_food']}"
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "💜 Made with love for Mamma • "
    "This tracker is for general tracking and is not medical advice."
)
