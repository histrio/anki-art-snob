import uuid
import os
import csv
import json
import zipfile

NAMESPACE = uuid.UUID('1b671a64-40d5-491e-99b0-da01ff1f3341')  # Arbitrary but constant namespace UUID

def generate_json_from_csv(csv_file_path, json_file_path):
    # Template for the JSON structure
    json_data = {
        "__type__": "Deck",
        "children": [],
        "crowdanki_uuid": "3c9b598a-c72d-11ee-bdb4-b7b23cdf7638",
        "deck_config_uuid": "eed25086-d07a-11ed-ab48-103d1c4cae55",
        "deck_configurations": [
            {
                "__type__": "DeckConfig",
                "answerAction": 0,
                "autoplay": True,
                "buryInterdayLearning": False,
                "crowdanki_uuid": "eed25086-d07a-11ed-ab48-103d1c4cae55",
                "desiredRetention": 0.9,
                "dyn": False,
                "fsrsWeights": [],
                "interdayLearningMix": 0,
                "lapse": {
                    "delays": [
                        10.0
                    ],
                    "leechAction": 1,
                    "leechFails": 8,
                    "minInt": 1,
                    "mult": 0.0
                },
                "maxTaken": 60,
                "name": "Default",
                "new": {
                    "bury": False,
                    "delays": [
                        1.0,
                        10.0
                    ],
                    "initialFactor": 2500,
                    "ints": [
                        1,
                        4,
                        0
                    ],
                    "order": 1,
                    "perDay": 20
                },
                "newGatherPriority": 0,
                "newMix": 0,
                "newPerDayMinimum": 0,
                "newSortOrder": 0,
                "replayq": True,
                "rev": {
                    "bury": False,
                    "ease4": 1.3,
                    "hardFactor": 1.2,
                    "ivlFct": 1.0,
                    "maxIvl": 36500,
                    "perDay": 200
                },
                "reviewOrder": 0,
                "secondsToShowAnswer": 0.0,
                "secondsToShowQuestion": 0.0,
                "sm2Retention": 0.9,
                "stopTimerOnAnswer": False,
                "timer": 0,
                "waitForAudio": False,
                "weightSearch": ""
            }
        ],
        "desc": "",
        "dyn": 0,
        "extendNew": 0,
        "extendRev": 0,
        "media_files": [],
        "name": "ArtSnob (ru)",
        "newLimit": None,
        "newLimitToday": None,
        "note_models": [
            {
                "__type__": "NoteModel",
                "crowdanki_uuid": "3c9b8108-c72d-11ee-bdb4-b7b23cdf7638",
                "css": ".card {\n    font-family: arial;\n    font-size: 20px;\n    text-align: center;\n    color: black;\n    background-color: white;\n}\n",
                "flds": [
                    {
                        "collapsed": False,
                        "description": "",
                        "excludeFromSearch": False,
                        "font": "Liberation Sans",
                        "id": 8562905359002828277,
                        "name": "Image",
                        "ord": 0,
                        "plainText": False,
                        "preventDeletion": False,
                        "rtl": False,
                        "size": 20,
                        "sticky": False,
                        "tag": None
                    },
                    {
                        "collapsed": False,
                        "description": "",
                        "excludeFromSearch": False,
                        "font": "Arial",
                        "id": 8123297495127658194,
                        "name": "Description",
                        "ord": 1,
                        "plainText": False,
                        "preventDeletion": False,
                        "rtl": False,
                        "size": 20,
                        "sticky": False,
                        "tag": None
                    }
                ],
                "latexPost": "\\end{document}",
                "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
                "latexsvg": False,
                "name": "ArtSnobRu",
                "originalStockKind": 1,
                "req": [
                    [
                        0,
                        "any",
                        [
                            0
                        ]
                    ]
                ],
                "sortf": 0,
                "tmpls": [
                    {
                        "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Description}}",
                        "bafmt": "",
                        "bfont": "",
                        "bqfmt": "",
                        "bsize": 0,
                        "did": None,
                        "id": 7676649678896259095,
                        "name": "Card 1",
                        "ord": 0,
                        "qfmt": "<img src=\"{{Image}}\">"
                    }
                ],
                "type": 0
            }
        ],
        "notes": [],
        "reviewLimit": None,
        "reviewLimitToday": None
    }

    # Added to generate consistent crowdanki_uuid for deck configurations and note models
    json_data["deck_configurations"][0]["crowdanki_uuid"] = str(uuid.uuid5(NAMESPACE, "deck_config_default"))
    json_data["note_models"][0]["crowdanki_uuid"] = str(uuid.uuid5(NAMESPACE, "note_model_art_snob"))

    # Read the CSV file and populate the "notes" list
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            # Assuming the first column of the CSV (article URL) is unique for each note

            image_url, description = row
            unique_identifier = image_url  # Use the image URL as the unique identifier
            note_uuid = str(uuid.uuid5(NAMESPACE, unique_identifier))
            note = {
                "__type__": "Note",
                "fields": [image_url, description],
                "guid": note_uuid[:10],  # Use the first 10 characters of the UUID
                "note_model_uuid": json_data["note_models"][0]["crowdanki_uuid"],
                "tags": []
            }
            json_data["notes"].append(note)

    # Write the structured data to a JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

def zip_json_as_folder(json_file_path, zip_file_path):
    # Define the folder name and the new file name inside the ZIP
    folder_name = "ArtSnobRu"
    inside_zip_path = os.path.join(folder_name, "deck.json")
    
    # Create a ZIP file and add the JSON file with the specified folder structure
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(json_file_path, inside_zip_path)

# Specify the paths for the CSV input and JSON output
csv_file_path = 'wikipedia_art_links.csv'
json_file_path = 'deck.json'
#zip_file_path = 'ArtSnobRu.zip'

generate_json_from_csv(csv_file_path, json_file_path)
#zip_json_as_folder(json_file_path, zip_file_path)
