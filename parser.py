import os
from html2json import collect

regex = {
    "artist": ["h2", "", ""],
    "work": ["h3", "", ""],
    "price": ["div", "", ["/[GU][BS][PD].*/"]]
}

def to_json(x):
    return {
        "artist": x["artist"],
        "works": {
            "title": x["work"].split("|")[0],
            "price": x["price"]
        }
    }

def parse_html_data_2015():
    working_directory = "data/2015-03-18/"
    entries = os.listdir(working_directory)

    data = []
    for entry in entries:
        html_content = open(working_directory + entry, "r")

        parsed = collect(html_content.read(), regex)
        data.append(parsed)

    return data


if __name__ == '__main__':
    parsed_data = parse_html_data_2015()

    # Step 1
    # print(list(dict.fromkeys(parsed_data)))

    # Step 2 to 3
    print(list(map(lambda x: to_json(x), parsed_data)))