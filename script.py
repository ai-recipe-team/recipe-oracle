import streamlit as st
from PIL import Image
from NLP_code import preprocess_ingredients
from yolo_detect import detect_objects
from llm_module import generate_dish_options, generate_recipe
import os
from dotenv import load_dotenv
import base64

#  Load Gemini API key from secrets.env
load_dotenv("secrets.env")

#  Background image setup
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)),
                          url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

#  Apply background image
set_background("background.png")

#  Page setup
st.set_page_config(page_title="The Recipe Oracle", layout="wide")

#  Add custom Google font
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Chewy&display=swap" rel="stylesheet">', unsafe_allow_html=True)

#  Heading + subtitle
st.markdown("<h1 style='text-align: center; color: orange;'>🔮 The Recipe Oracle</h1>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center; font-family: "Chewy", cursive; font-size: 20px;'>
    Your AI-powered kitchen companion
</p>
""", unsafe_allow_html=True)
st.markdown("---")

#  Upload image
uploaded_file = st.file_uploader("Upload a food image (optional)", type=["jpg", "jpeg", "png"])

#  Manual ingredients input
manual_input = st.text_input("Add ingredients (comma-separated)")
manual_ingredients = [i.strip().lower() for i in manual_input.split(',') if i.strip()]

#  Allow dish suggestion from manual input
if manual_ingredients and "ingredients" not in st.session_state:
    st.session_state.ingredients = manual_ingredients

#  Show uploaded image and save it
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    with open("uploads/image.jpg", "wb") as f:
        f.write(uploaded_file.read())


#  Run YOLO + NLP filtering
if st.button("🔍 Detect Ingredients") and uploaded_file:
    raw_detected = detect_objects("uploads/image.jpg")
    ingredients = preprocess_ingredients(raw_detected)
    all_ingredients = list(set(ingredients + manual_ingredients))
    st.session_state.ingredients = all_ingredients
    st.success(f"Ingredients: {', '.join(all_ingredients)}")

#  Generate dish suggestions
if "ingredients" in st.session_state and st.button("✨ Suggest Dishes"):
    dishes = generate_dish_options(st.session_state.ingredients)
    st.session_state.dishes = dishes

#  Show recipe
if "dishes" in st.session_state:
    # Style for radio button labels (dish list)
    st.markdown("""
        <style>
        div[role="radiogroup"] label {
            color: #000000 !important;
            font-family: 'Segoe UI', sans-serif;
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)

    dish_titles = [d['title'] for d in st.session_state.dishes]
    selected = st.radio("Pick a dish to cook:", dish_titles)

    if st.button("📜 Show Recipe"):
        recipe = generate_recipe(selected)
        
        if recipe["title"] == "Error":
            st.warning("⚠️ Gemini API is temporarily unavailable. Please wait a minute and try again.")
        else:
            # 🍽️ Recipe title styling
            st.markdown(f"""
                <h3 style='color:#000000; font-family:"Trebuchet MS", sans-serif;'>
                    🍽️ {recipe['title']}
                </h3>
            """, unsafe_allow_html=True)

            # 📄 Recipe steps styling
            for step in recipe['steps']:
                st.markdown(f"""
                    <p style='color:#000000; font-size:1.1rem; font-family:"Segoe UI", sans-serif; margin-bottom:0.5rem;'>
                        • {step}
                    </p>
                """, unsafe_allow_html=True)
