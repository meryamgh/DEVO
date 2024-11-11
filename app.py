from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)


json_data = {
    48659: json.load(open("data/restructured_data_48659_test.json", "r", encoding="utf-8")),
    48629: json.load(open("data/restructured_data_48629_test.json", "r", encoding="utf-8")),
    48646: json.load(open("data/restructured_data_48646_test.json", "r", encoding="utf-8")),
    66719: json.load(open("data/restructured_data_66719_test.json", "r", encoding="utf-8")),
    69486: json.load(open("data/restructured_data_69486_test.json", "r", encoding="utf-8")),
    141175: json.load(open("data/restructured_data_141175_test.json", "r", encoding="utf-8"))
}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/categories/<int:category_id>", methods=["GET"])
def get_category(category_id):
    def find_category(categories, cat_id):
        for category in categories:
            if category.get("category_id") == cat_id:
                return category
            elif "children" in category:
                found = find_category(category["children"], cat_id)
                if found:
                    return found
        return None

    if category_id in json_data:
        category_data = find_category(json_data[category_id], category_id)
        if category_data:
            return jsonify(category_data)
        else:
            return jsonify({"error": "Category not found"}), 404
    else:
        return jsonify({"error": "Category ID not recognized"}), 404

if __name__ == "__main__":
    app.run(debug=True)
