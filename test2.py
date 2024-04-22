import openai
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Setting up the API key for OpenAI
openai.api_key = "api-key"

# Function to generate a GPT-3 prompt based on client answers
def generate_prompt(answers):
    prompt = "Given the following rules:\n\n"
    prompt += "1. If you go out to party on weekends, you are allowed to choose from apples, pears, grapes, and watermelon.\n"
    prompt += "2. If you like cider, you can choose from apples, oranges, lemon, and lime.\n"
    prompt += "3. If you like sweet flavors, you can choose from watermelon and oranges.\n"
    prompt += "4. If you like waterlike drinks, you can choose watermelon.\n"
    prompt += "5. If grapes are chosen, watermelon is removed from the list.\n"
    prompt += "6. If you don't like smooth texture, pears are removed.\n"
    prompt += "7. If you don't like slimy texture, watermelon, lime, and grapes are removed.\n"
    prompt += "8. If you don't like waterlike texture, watermelon is removed.\n"
    prompt += "9. If the price is less than $3, lime and watermelon are removed.\n"
    prompt += "10. If the price is between $4 and $7, pears and apples are removed.\n\n"
    prompt += "Based on your answers, here are the recommended fruits:\n"

    # Determine which fruits are allowed based on the answers
    allowed_fruits = []
    if answers["weekend_party"] == "yes":
        allowed_fruits.extend(["apples", "pears", "grapes", "watermelon"])
    if answers["flavor"] == "cider":
        allowed_fruits.extend(["apples", "oranges", "lemon", "lime"])
    elif answers["flavor"] == "sweet":
        allowed_fruits.extend(["watermelon", "oranges"])
    elif answers["flavor"] == "waterlike":
        allowed_fruits.append("watermelon")

    # Handle removal of fruits based on texture preference
    if answers["texture"] == "smooth":
        allowed_fruits = [fruit for fruit in allowed_fruits if fruit != "pears"]
    elif answers["texture"] == "slimy":
        allowed_fruits = [fruit for fruit in allowed_fruits if fruit not in ["watermelon", "lime", "grapes"]]
    elif answers["texture"] == "waterlike":
        allowed_fruits = [fruit for fruit in allowed_fruits if fruit != "watermelon"]

    # Handle removal of fruits based on price range
    price_range = answers["price"]
    if price_range < 3:
        allowed_fruits = [fruit for fruit in allowed_fruits if fruit not in ["lime", "watermelon"]]
    elif 4 <= price_range <= 7:
        allowed_fruits = [fruit for fruit in allowed_fruits if fruit not in ["pears", "apples"]]

    prompt += ", ".join(allowed_fruits)
    return prompt

@app.route('/recommend_fruits', methods=['POST'])
def recommend_fruits():
    data = request.get_json()
    answers = data["answers"]
    prompt = generate_prompt(answers)

    # Generate an answer using GPT-3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    # Extract the generated text from the response
    recommended_fruits = response.choices[0].message['content'].strip()

    return jsonify({"recommended_fruits": recommended_fruits})


if __name__ == '__main__':
    app.run(debug=True)
