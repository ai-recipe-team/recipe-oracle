import streamlit as st
from PIL import Image
from NLP_code import preprocess_ingredients
from yolo_detect import detect_objects
from llm_module import generate_dish_options, generate_recipe
import os
from dotenv import load_dotenv
import base64

# 🔑 Load API keys from .env
load_dotenv()

# 🎨 Set background image function
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

# 🌄 Apply background image
set_background("background.png")

# 🧠 Page config
st.set_page_config(page_title="The Recipe Oracle", layout="wide")
st.markdown("<h1 style='text-align: center; color: orange;'>🔮 The Recipe Oracle</h1>", unsafe_allow_html=True)

# 📸 Upload image
uploaded_file = st.file_uploader("Upload a food image (optional)", type=["jpg", "jpeg", "png"])

# ✍️ Manual ingredients input
manual_input = st.text_input("Add ingredients (comma-separated)")
manual_ingredients = [i.strip().lower() for i in manual_input.split(',') if i.strip()]

# 🖼️ Show image and save it locally
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    with open("uploads/image.jpg", "wb") as f:
        f.write(uploaded_file.read())

# 🔍 Ingredient detection button
if st.button("🔍 Detect Ingredients") and uploaded_file:
    raw_detected = detect_objects("uploads/image.jpg")
    ingredients = preprocess_ingredients(raw_detected)
    all_ingredients = list(set(ingredients + manual_ingredients))
    st.session_state.ingredients = all_ingredients
    st.success(f"Ingredients: {', '.join(all_ingredients)}")

# ✨ Suggest dishes
if "ingredients" in st.session_state and st.button("✨ Suggest Dishes"):
    dishes = generate_dish_options(st.session_state.ingredients)
    st.session_state.dishes = dishes

# 📜 Show recipe
if "dishes" in st.session_state:
    dish_titles = [d['title'] for d in st.session_state.dishes]
    selected = st.radio("Pick a dish to cook:", dish_titles)

    if st.button("📜 Show Recipe"):
        recipe = generate_recipe(selected)
        st.markdown(f"### 🍽️ {recipe['title']}")
        for step in recipe['steps']:
            st.markdown(f"- {step}")
