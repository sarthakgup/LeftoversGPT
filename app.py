from flask import Flask, request, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv
import traceback

print("🔧 Loading environment variables...")
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("🔐 Loaded API Key:", "Found" if api_key else "NOT FOUND")

client = OpenAI(api_key=api_key)
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recipes = None

    print("📡 Received request:", request.method)

    if request.method == "POST":
        ingredients = request.form.get("ingredients", "")
        print("🧾 Received ingredients:", ingredients)

        if ingredients.strip():
            prompt = f"I have the following leftovers: {ingredients}. Suggest 3 simple and creative meals using common pantry items."
            print("✉️ Sending prompt to OpenAI:", prompt)

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful recipe assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=400
                )
                recipes = response.choices[0].message.content
                print("✅ Received response from OpenAI")

            except Exception as e:
                print("❌ OpenAI API error:", e)
                traceback.print_exc()
                recipes = "There was an error contacting OpenAI. Please check your API key and try again."
        else:
            print("⚠️ No ingredients submitted.")

    return render_template("index.html", recipes=recipes)
