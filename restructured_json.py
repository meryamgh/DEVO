import json

with open("all_items_69486_comp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

categories = {}
for entry in data:
    categories[entry["category_id"]] = entry

processed_categories = set()

def build_hierarchy(category_id, parent_id=None, parent_libelle=None):
    if category_id in processed_categories:
        return None  

    category = categories.get(category_id, {}).copy()  
    processed_categories.add(category_id)  

    if parent_id is not None:
        category["id_parent"] = parent_id
    if parent_libelle is not None:
        category["libelle_parent"] = parent_libelle

    if "final_data" in category:
        return category

    children = []
    if "data" in category and "liste" in category["data"]:
        for sub in category["data"]["liste"]:
            sub_id = sub.get("id")
            if sub_id in categories:
                child = build_hierarchy(sub_id, category_id, sub.get("libelle"))
                if child:
                    children.append(child)

    category["children"] = children
    category.pop("data", None)  
    return category

top_level_categories = [
    build_hierarchy(category_id) for category_id, entry in categories.items()
    if "id_parent" not in entry or entry["id_parent"] not in categories
]

top_level_categories = [item for item in top_level_categories if item]

with open("restructured_data_test.json", "w", encoding="utf-8") as f:
    json.dump(top_level_categories, f, ensure_ascii=False, indent=4)

print("JSON restructuré enregistré dans 'restructured_data.json'")
