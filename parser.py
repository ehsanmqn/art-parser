import os
import json
from html2json import collect

regex2015 = {
    "artist": ["h2", "", ""],
    "work": ["h3", "", ""],
    "price": ["div", "", ["/[GU][BS][PD].*/"]]
}


regex2017 = {
    "h3": ["h3", "", ""],
    "currency": ["span", "", ["/[GU][BS][PD].*/"]],
    "amount": ["span", "", ["/[0-9].*/"]]
}


def to_json_2017(x):
    return {
        "artist": x["h3"].split("|")[0],
        "works": [{
            "title": x["h3"].split("|")[1],
            "currency": x["currency"].split("|")[0],
            "totalLifetimeValue": x["amount"]
        }]
    }


def to_json_2015(x):
    return {
        "artist": x["artist"],
        "works": [{
            "title": x["work"].split("|")[0],
            "currency": x["price"].split(" ")[0],
            "totalLifetimeValue": x["price"].split(" ")[1]
        }]
    }


def add_to_dict_without_duplication(dict, json_data):
    for key, value in dict.items():
        if key == json_data["artist"]:
            dict[key]["works"].append(json_data["works"])
            return dict

    dict[json_data["artist"]] = json_data

    return dict


def parse_html_data_2015(data=None):
    working_directory = "data/2015-03-18/"
    entries = os.listdir(working_directory)

    if data == None:
        data = {}

    for entry in entries:
        html_content = open(working_directory + entry, "r")

        parsed = collect(html_content.read(), regex2015)
        add_to_dict_without_duplication(data, to_json_2015(parsed))

    return data


def parse_html_data_2017(data=None):
    working_directory = "data/2017-12-20/"
    entries = os.listdir(working_directory)

    if data == None:
        data = {}

    for entry in entries:
        html_content = open(working_directory + entry, "r")

        parsed = collect(html_content.read(), regex2017)
        add_to_dict_without_duplication(data, to_json_2017(parsed))

    return data


if __name__ == '__main__':
    parsed_data = parse_html_data_2015()

    # Step 1
    # print(list(dict.fromkeys(parsed_data)))

    # Step 2 to 3
    # print(list(map(lambda x: to_json(x), parsed_data)))

    # Step 4
    # print(list(dict.values(parsed_data)))

    # Step 5
    parsed_data = parse_html_data_2017(parsed_data)
    print(list(dict.values(parsed_data)))