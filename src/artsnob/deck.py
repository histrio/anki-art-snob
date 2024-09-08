import os
import json
import zipfile

import re
import uuid
import requests
import requests_cache

from urllib.parse import urljoin
from bs4 import BeautifulSoup


requests_cache.install_cache("cache")

NAMESPACE = uuid.UUID(
    "1b671a64-40d5-491e-99b0-da01ff1f3341"
)  # Arbitrary but constant namespace UUID

TEMPLATE = {
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
                "delays": [10.0],
                "leechAction": 1,
                "leechFails": 8,
                "minInt": 1,
                "mult": 0.0,
            },
            "maxTaken": 60,
            "name": "Default",
            "new": {
                "bury": False,
                "delays": [1.0, 10.0],
                "initialFactor": 2500,
                "ints": [1, 4, 0],
                "order": 1,
                "perDay": 20,
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
                "perDay": 200,
            },
            "reviewOrder": 0,
            "secondsToShowAnswer": 0.0,
            "secondsToShowQuestion": 0.0,
            "sm2Retention": 0.9,
            "stopTimerOnAnswer": False,
            "timer": 0,
            "waitForAudio": False,
            "weightSearch": "",
        }
    ],
    "desc": '<a href="https://github.com/histrio/anki-art-snob/"><b>FULL DESCRIPTION</b></a> |\n<a href="https://github.com/histrio/anki-art-snob/blob/master/CHANGELOG.md"><b>RELEASE NOTES</b></a> \n\n<b>Art Snob</b> features:\n\n- the world\'s most famous <a href="https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"><b>3k+ paintings</b></a> \n\nThis deck is <a href="https://github.com/histrio/anki-art-snob"><b>maintained on GitHub</b></a>. If you spot a mistake, have a suggestion or want to help, please don\'t hesitate to <a href="https://github.com/histrio/anki-art-snob/issues">open an issue</a>. Want to <b>stay informed of new releases</b>? Watch the GitHub repository or subscribe to the <a href="https://github.com/histrio/anki-art-snob/releases.atom">releases feed</a>!\n',
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
                    "tag": None,
                },
                {
                    "collapsed": False,
                    "description": "",
                    "excludeFromSearch": False,
                    "font": "Arial",
                    "id": 8123297495127658195,
                    "name": "Author",
                    "ord": 1,
                    "plainText": False,
                    "preventDeletion": False,
                    "rtl": False,
                    "size": 20,
                    "sticky": False,
                    "tag": None,
                },
                {
                    "collapsed": False,
                    "description": "",
                    "excludeFromSearch": False,
                    "font": "Arial",
                    "id": 8123297495127658195,
                    "name": "Name",
                    "ord": 1,
                    "plainText": False,
                    "preventDeletion": False,
                    "rtl": False,
                    "size": 20,
                    "sticky": False,
                    "tag": None,
                },
                {
                    "collapsed": False,
                    "description": "",
                    "excludeFromSearch": False,
                    "font": "Arial",
                    "id": 8123297495127658194,
                    "name": "Description",
                    "ord": 3,
                    "plainText": False,
                    "preventDeletion": False,
                    "rtl": False,
                    "size": 20,
                    "sticky": False,
                    "tag": None,
                },
            ],
            "latexPost": "\\end{document}",
            "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
            "latexsvg": False,
            "name": "ArtSnobRu",
            "originalStockKind": 1,
            "req": [[0, "any", [0]]],
            "sortf": 0,
            "tmpls": [
                {
                    "afmt": "{{FrontSide}} <hr id=answer> <b>{{Name}}</b> </br> {{Author}} </br> <i>{{Description}}</i>",
                    "bafmt": "",
                    "bfont": "",
                    "bqfmt": "",
                    "bsize": 0,
                    "did": None,
                    "id": 7676649678896259095,
                    "name": "Card 1",
                    "ord": 0,
                    "qfmt": '<img src="{{Image}}">',
                }
            ],
            "type": 0,
        }
    ],
    "notes": [],
    "reviewLimit": None,
    "reviewLimitToday": None,
}


def generate_json(data):
    # Template for the JSON structure
    json_data = TEMPLATE.copy()

    # Added to generate consistent crowdanki_uuid for deck configurations and note models
    json_data["crowdanki_uuid"] = str(uuid.uuid5(NAMESPACE, "deck"))

    deck_config_uuid = str(uuid.uuid5(NAMESPACE, "deck_config_default"))
    json_data["deck_config_uuid"] = deck_config_uuid
    json_data["deck_configurations"][0]["crowdanki_uuid"] = deck_config_uuid

    note_model_uuid = str(uuid.uuid5(NAMESPACE, "note_model_art_snob"))
    json_data["note_models"][0]["crowdanki_uuid"] = note_model_uuid

    for image_url, author, name, description in data:
        unique_identifier = image_url  # Use the image URL as the unique identifier
        note_uuid = str(uuid.uuid5(NAMESPACE, unique_identifier))
        note = {
            "__type__": "Note",
            "fields": [image_url, author, name, description],
            "guid": note_uuid[:10],  # Use the first 10 characters of the UUID
            "note_model_uuid": note_model_uuid,
            "tags": [],
        }
        json_data["notes"].append(note)
    return json_data


def zip_json_as_folder(json_file_path, zip_file_path):
    # Define the folder name and the new file name inside the ZIP
    folder_name = "ArtSnobRu"
    inside_zip_path = os.path.join(folder_name, "deck.json")

    # Create a ZIP file and add the JSON file with the specified folder structure
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(json_file_path, inside_zip_path)


def get_deck():
    deck_dst = "deck.json"
    data = get_data()
    json_data = generate_json(data)
    # Write the structured data to a JSON file
    with open(deck_dst, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)


def iter_next_page(url):
    """
    Generator to iterate over pages starting from a given URL.
    Yields BeautifulSoup objects for each page with a 'Next page' link.
    """
    while url:
        response = requests.get(url)
        if response.status_code != 200:
            break  # Exit if there's an error loading the page
        soup = BeautifulSoup(response.content, "lxml")
        yield soup
        next_link = soup.find("a", text="Следующая страница")
        url = urljoin(url, next_link.get("href")) if next_link else None


def art_list():
    """
    Generator that yields URLs of Wikipedia articles in a specific category.
    Filters out non-article links using a pre-compiled regular expression.
    """
    base_url = "https://ru.wikipedia.org"
    start_path = "/w/index.php?title=Категория:Картины_по_алфавиту"
    full_url = urljoin(base_url, start_path)

    exlude_list = "|".join(
        [
            "%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:",
            "%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:",
            "%D0%A1%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B0:",
            "%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:",
            "%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB:",
            "%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0",
        ]
    )

    exclude_pattern = re.compile(rf"^/wiki/(?!{exlude_list})")
    for soup in iter_next_page(full_url):
        for li in soup.find_all("li"):
            a = li.find("a", href=exclude_pattern)
            if a:
                yield urljoin(base_url, a.get("href"))


def get_data():
    for link in art_list():
        print(link)
        w_resp = requests.get(link, stream=False)
        w_soup = BeautifulSoup(w_resp.content, "lxml")
        box = w_soup.find("table", {"class": "infobox"})
        if box:
            data = [t.text.strip() for t in box.find_all("tr") or []]
            if len(data) > 2:
                _, author, name_ru = data[:3]
                desc = " ".join(data[3:])
                img_tag = box.find("img")
                if img_tag:
                    img_url = "https:" + img_tag["src"]
                    yield img_url, author, name_ru, desc
                else:
                    print("No image tag found")
