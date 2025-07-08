import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv("secrets.env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

chat = genai.GenerativeModel("gemini-1.5-flash").start_chat()

def generate_dish_options(ingredients):
    ingredient_str = ", ".join(ingredients)
    prompt = f"I have {ingredient_str}. Suggest some Indian dishes using some of these ingredients (just names, no recipes)."
    
    try:
        response = chat.send_message(prompt)
        dishes = response.text.strip().split("\n")
        return [{"title": dish.strip("1234567890. ").strip()} for dish in dishes if dish.strip()]
    except Exception as e:
        print("❌ Gemini API error (dish generation):", e)
        return [{"title": "⚠️ Unable to fetch dish options. Please try again shortly."}]

def generate_recipe(dish_name):
    prompt = f"Give me a detailed recipe for {dish_name}"
    
    try:
        response = chat.send_message(prompt)
        steps = response.text.strip().split("\n")
        return {
            "title": dish_name,
            "steps": [step.strip("1234567890. ").strip() for step in steps if step.strip()]
        }
    except Exception as e:
        print("❌ Gemini API error (recipe generation):", e)
        return {
            "title": "Error",
            "steps": ["⚠️ Unable to fetch recipe at the moment. Please wait and try again."]
        }

