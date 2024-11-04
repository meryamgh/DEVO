from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

# Charger les données JSON
with open("restructured_data_test.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

@app.route("/")
def index():
    # Retourner la page HTML
    return render_template("index.html")

@app.route("/api/categories/<int:category_id>", methods=["GET"])
def get_category(category_id):
    # Fonction récursive pour trouver la catégorie avec tous ses sous-enfants
    def find_category(categories, cat_id):
        for category in categories:
            if category.get("category_id") == cat_id:
                return category
            elif "children" in category:
                found = find_category(category["children"], cat_id)
                if found:
                    return found
        return None

    # Trouver la catégorie à partir du JSON principal
    category_data = find_category(json_data, category_id)
    if category_data:
        return jsonify(category_data)
    else:
        return jsonify({"error": "Category not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
