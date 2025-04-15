import json

def update_personal_info(existing, update_type, **kwargs):
    if update_type == "goals":
        existing["goals"] = kwargs.get("goals",[])
        update_field = {"goals":existing["goals"]}
    else:
        existing[update_type] = kwargs
        update_field = {update_type:existing[update_type]}

    # Load current db
    with open('personal_data_db.json') as f:
        personal_data_collection = json.load(f)

    personal_data_collection[f"{existing["_id"]}"].update(update_field)

    # Write to db
    with open('personal_data_db.json', "w") as f:
        json.dump(personal_data_collection , f)

    return existing

def add_note(note, profile_id):
    # Load current db
    with open('notes_db.json') as f:
        notes_collection = json.load(f)
    
    try:
        notes_collection[f"{profile_id}"].get("notes").append(note)
    except:
        notes_collection[f"{profile_id}"] = {
            "_id": profile_id,
            "notes": [note]
        }

    # Write to db
    with open('notes_db.json', "w") as f:
        json.dump(notes_collection , f)
    
    return note

def delete_note(note_index, _id):
    # Load current db
    with open('notes_db.json') as f:
        notes_collection = json.load(f)
    
    notes_collection[f"{_id}"].get("notes").pop(note_index)

    # Write to db
    with open('notes_db.json', "w") as f:
        json.dump(notes_collection , f)