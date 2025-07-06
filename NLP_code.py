import nltk
from nltk.corpus import stopwords, wordnet as wn
from nltk.stem import WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

FOOD_WHITELIST = {
    'apple', 'banana', 'orange', 'milk', 'bread', 'butter', 'cheese', 'egg', 'carrot',
    'broccoli', 'onion', 'potato', 'tomato', 'rice', 'pasta', 'chicken', 'fish', 'meat',
    'pizza', 'cake', 'cucumber', 'corn', 'lettuce', 'mushroom', 'yogurt', 'flour',
    'spinach', 'garlic', 'pepper', 'beans', 'peas', 'chili', 'tomatoes'
}

def is_food_word(word):
    for syn in wn.synsets(word, pos=wn.NOUN):
        if 'food' in syn.lexname():
            return True
    return False

def preprocess_ingredients(yolo_output):
    raw_ingredients = [item['class'] for item in yolo_output]
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    cleaned = []

    for ingredient in raw_ingredients:
        ingredient = re.sub(r'[^a-zA-Z\s]', '', ingredient.lower())
        tokens = nltk.word_tokenize(ingredient)
        tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
        for token in tokens:
            if token in FOOD_WHITELIST or is_food_word(token):
                cleaned.append(token)
    return list(set(cleaned))
