import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the .env file
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Start the Gemini model (flash version)
llm = genai.GenerativeModel('gemini-1.5-flash').start_chat()
def generate_dish_options(ingredients):
    ing = ", ".join(ingredients)
    prompt = f"I have {ing}. Suggest 3 Indian dishes I can make (just names)."
    res = llm.send_message(prompt)
    titles = res.text.split("\n")
    return [{"title": t.strip()} for t in titles if t.strip()]

def generate_recipe(dish_name):
    prompt = f"Give me a recipe for {dish_name}"
    res = llm.send_message(prompt)
    steps = res.text.split("\n")
    return {"title": dish_name, "steps": [s for s in steps if s.strip()]}