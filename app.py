from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    skin_type = request.form['skin_type']
    hair_type = request.form['hair_type']
    diet = request.form['diet']
    concerns = request.form.getlist('concerns')

    bmi = weight / ((height / 100) ** 2)
    bmi_category = (
        "Underweight" if bmi < 18.5 else
        "Normal" if bmi < 24.9 else
        "Overweight" if bmi < 29.9 else
        "Obese"
    )

    suggestion_dict = {
        "acne": "Use salicylic acid or tea tree oil. Avoid oily food and wash your face twice daily.",
        "tanning": "Apply sunscreen daily, use aloe vera or tomato juice as a natural remedy.",
        "dryness": "Moisturize frequently, use hyaluronic acid, and avoid hot showers.",
        "pigmentation": "Use vitamin C serum, wear SPF daily, and try licorice root extract.",
        "hairfall": "Include biotin-rich foods, avoid tight hairstyles, and massage your scalp with coconut oil.",
        "frizziness": "Use leave-in conditioner, avoid heat, and deep condition weekly.",
        "dandruff": "Use anti-dandruff shampoos with ketoconazole or neem extracts.",
        "hair maintenance": "Trim hair regularly, avoid harsh chemicals, and use suitable shampoo.",
        "fatigue": "Improve sleep habits, eat iron-rich foods, and reduce screen time.",
        "weak immunity": "Eat citrus fruits, exercise, and stay hydrated.",
        "stress": "Practice yoga/meditation, reduce caffeine, and take breaks.",
        "dehydration": "Drink at least 3L of water daily. Include cucumbers, watermelon, and coconut water."
    }
    food_suggestions = {
        "acne": [
        {"name": "Pumpkin seeds", "type": "vegan"},
        {"name": "Fish", "type": "nonveg"},
        {"name": "Green tea", "type": "vegan"}
    ],
    "hairfall": [
        {"name": "Eggs", "type": "nonveg"},
        {"name": "Spinach", "type": "vegan"},
        {"name": "Almonds", "type": "vegan"}
    ],
    "fatigue": [
        {"name": "Dates", "type": "vegan"},
        {"name": "Banana", "type": "vegan"},
        {"name": "Leafy greens", "type": "vegan"}
    ],
    "tanning": [
        {"name": "Tomatoes", "type": "vegan"},
        {"name": "Carrot juice", "type": "vegan"},
        {"name": "Green tea", "type": "vegan"}
    ],
    "dryness": [
        {"name": "Avocado", "type": "vegan"},
        {"name": "Coconut", "type": "vegan"},
        {"name": "Milk", "type": "nonveg"}
    ],
    "pigmentation": [
        {"name": "Berries", "type": "vegan"},
        {"name": "Spinach", "type": "vegan"},
        {"name": "Citrus fruits", "type": "vegan"}
    ],
    "frizziness": [
        {"name": "Walnuts", "type": "vegan"},
        {"name": "Sunflower seeds", "type": "vegan"},
        {"name": "Salmon", "type": "nonveg"}
    ],
    "dandruff": [
        {"name": "Yogurt", "type": "nonveg"},
        {"name": "Neem leaves", "type": "vegan"},
        {"name": "Coconut water", "type": "vegan"}
    ],
    "hair maintenance": [
        {"name": "Pumpkin seeds", "type": "vegan"},
        {"name": "Eggs", "type": "nonveg"},
        {"name": "Greek yogurt", "type": "nonveg"}
    ],
    "weak immunity": [
        {"name": "Citrus fruits", "type": "vegan"},
        {"name": "Garlic", "type": "vegan"},
        {"name": "Yogurt", "type": "nonveg"}
    ],
    "stress": [
        {"name": "Chamomile tea", "type": "vegan"},
        {"name": "Dark chocolate", "type": "vegan"},
        {"name": "Ashwagandha", "type": "vegan"}
    ],
    "dehydration": [
        {"name": "Coconut water", "type": "vegan"},
        {"name": "Watermelon", "type": "vegan"},
        {"name": "Cucumber", "type": "vegan"}
    ]
    }

    product_suggestions = {
        "acne": ["Salicylic Acid Face Wash (Minimalist)", "Tea Tree Serum (The Body Shop)"],
        "tanning": ["Sunscreen SPF 50+ (Fixderma)", "De-Tan Pack (Mamaearth)"],
        "dryness": ["Cetaphil Moisturizer", "Bio Oil"],
        "pigmentation": ["Vitamin C Serum (Plum)", "Licorice Face Cream (Dot & Key)"],
        "hairfall": ["Indulekha Bringha Oil", "Biotin Tablets (HealthKart)"],
        "frizziness": ["Streax Hair Serum", "Argan Oil (WOW Skin Science)"],
        "dandruff": ["Nizoral Anti-Dandruff Shampoo", "Mamaearth Tea Tree Shampoo"],
        "hair maintenance": ["L'Oreal Hair Spa", "TRESemmé Keratin Shampoo"],
        "fatigue": ["Ashwagandha Capsules", "NutriMix Energy Drink"],
        "weak immunity": ["Chyawanprash", "Multivitamins (Zincovit)"],
        "stress": ["Essential Oil Roll-on (Aroma Magic)", "Chamomile Tea"],
        "dehydration": ["ORS Sachets", "Electrolyte Drinks (Enerzal)"]
    }

    routine = {
        "morning": {
            "dry": [
                "Hydrating cleanser", "Hyaluronic acid serum", "Moisturizer", "SPF 50+"
            ],
            "oily": [
                "Salicylic acid face wash", "Oil-free moisturizer", "Niacinamide serum", "Gel-based sunscreen"
            ],
            "sensitive": [
                "Fragrance-free cleanser", "Aloe vera gel", "Barrier-repair moisturizer", "Mineral sunscreen"
            ],
            "combination": [
                "Foam cleanser", "Light moisturizer", "SPF 30+"
            ]
        },
        "night": {
            "dry": [
                "Gentle cleanse", "Night cream", "Facial oil", "Use humidifier"
            ],
            "oily": [
                "Cleanse with face wash", "Retinol (2–3 times/week)", "Clay mask (weekly)"
            ],
            "sensitive": [
                "Lukewarm water rinse", "Calming serum", "Non-comedogenic moisturizer"
            ],
            "combination": [
                "Double cleanse", "Hydrating toner", "Night cream"
            ]
        }
    }

    collected_suggestions = []
    foods_for_user = []
    products_for_user = []

    for c in concerns:
        if c in suggestion_dict:
            collected_suggestions.append(f"• {c.title()}: {suggestion_dict[c]}")

        if c in food_suggestions:
            for item in food_suggestions[c]:
                if diet == "any" or item["type"] == diet:
                    foods_for_user.append(item["name"])

        if c in product_suggestions:
            products_for_user += product_suggestions[c]

    return render_template(
        'result.html',
        name=name,
        bmi=round(bmi, 2),
        bmi_category=bmi_category,
        skin_type=skin_type,
        hair_type=hair_type,
        concerns=concerns,
        collected_suggestions=collected_suggestions,
        foods_for_user=list(set(foods_for_user)),
        products_for_user=list(set(products_for_user)),
        morning_routine=routine["morning"].get(skin_type, []),
        night_routine=routine["night"].get(skin_type, [])
    )

if __name__ == '__main__':
    app.run(debug=True)