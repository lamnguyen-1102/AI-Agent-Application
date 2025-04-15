import json



with open('notes_db.json') as f:
    notes_collection = json.load(f)

def get_values(_id):
    return {
        "_id": _id,
        "general": {
            "name":"",
            "age":30,
            "weight":60,
            "height":165,
            "activity_level":"Moderately Active",
            "gender":"Male"
            },
        "goals": ["Muscle Gain"],
        "nutrition": {
            "calories":2000,
            "protein":140,
            "fat": 20,
            "carbs": 100
            }
        }

def create_profile(_id):
    # Load current db
    with open('personal_data_db.json') as f:
        personal_data_collection = json.load(f)

    profile_values = get_values(_id)
    personal_data_collection[f"{_id}"] = profile_values

    # Write to db
    with open('personal_data_db.json', "w") as f:
        json.dump(personal_data_collection , f)

    return _id, profile_values

def get_profile(_id):
    # Load current db
    with open('personal_data_db.json') as f:
        personal_data_collection = json.load(f)

    return personal_data_collection[f"{_id}"]

def get_notes(_id):
    with open('notes_db.json') as f:
        notes_collection = json.load(f)
    
    return notes_collection[f"{_id}"].get("notes")