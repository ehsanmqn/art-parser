import os
import json
import re
from html2json import collect

GBP_EXCHANGE_RATE = 1.34
DIRECTORY_2015 = "data/2015-03-18/"
DIRECTORY_2017 = "data/2017-12-20/"

##
# Regular expression
# The regular expression for extracting data from category 2015
#
regex2015 = {
    "artist": ["h2", "", ""],
    "work": ["h3", "", ""],
    "price": ["div", "", ["/[GU][BS][PD].*/"]]
}

##
# Function: to_json_2017(x)
# This function jsonify an input data for category 2015
#
def to_json_2015(x):
    return {
        "artist": re.sub(" \([1-9]{4}-[1-9]{4}\)", "", x["artist"]),
        "works": [{
            "title": x["work"].split("|")[0],
            "currency": x["price"].split(" ")[0],
            "totalLifetimeValue": x["price"].split(" ")[1].replace(",", "")
        }]
    }

##
# Regular expression
# The regular expression for extracting data from category 2017
#
regex2017 = {
    "h3": ["h3", "", ""],
    "currency": ["span", "", ["/[GU][BS][PD].*/"]],
    "amount": ["span", "", ["/[0-9].*/"]]
}

##
# Function: to_json_2017(x)
# This function jsonify an input data for category 2017
#
def to_json_2017(x):
    return {
        "artist": re.sub(" \([1-9]{4}-[1-9]{4}\)", "", x["h3"].split("|")[0]),
        "works": [{
            "title": x["h3"].split("|")[1],
            "currency": x["currency"].split("|")[0],
            "totalLifetimeValue": x["amount"].replace(",", "")
        }]
    }

##
# Function: add_to_dict_without_duplication(dict, json_data)
# This function insert a json data into a dict with respect to redundancy
#
def add_to_dict_without_duplication(dict, json_data):
    for key, value in dict.items():
        if key == json_data["artist"]:
            dict[key]["works"].append(json_data["works"][0])
            dict[key]["totalValue"] = str(float(dict[key]["totalValue"]) + float(json_data["works"][0]["totalLifetimeValue"]))

            return dict

    dict[json_data["artist"]] = json_data

    return dict

##
# Function: change_to_dollar(json)
# This function change GBP currency to dollar in a provided json object
#
def change_to_dollar(json):
    if json["works"][0]["currency"] == "GBP":
        json["works"][0]["totalLifetimeValue"] = str(float(json["works"][0]["totalLifetimeValue"]) * GBP_EXCHANGE_RATE)
        json["works"][0]["currency"] = "USD"
        json["totalValue"] = json["works"][0]["totalLifetimeValue"]

    else:
        json["totalValue"] = json["works"][0]["totalLifetimeValue"]

    return json


##
# Function: parse_html_data_2015(data=None):
# This function parse category 2015 data
#
def parse_html_data_2015(data=None):
    working_directory = DIRECTORY_2015

    entries = os.listdir(working_directory)

    if data == None:
        data = {}

    for entry in entries:
        html_content = open(working_directory + entry, "r")

        # Convert data from HTML to json
        parsed = collect(html_content.read(), regex2015)
        parsed_json = to_json_2015(parsed)

        # Change currency
        parsed_json = change_to_dollar(parsed_json)

        # Add data to dictionary regarding to data duplication
        add_to_dict_without_duplication(data, parsed_json)

    return data

##
# Function: parse_html_data_2017(data=None):
# This function parse category 2017 data
#
def parse_html_data_2017(data=None):
    working_directory = DIRECTORY_2017

    entries = os.listdir(working_directory)

    if data == None:
        data = {}

    for entry in entries:
        html_content = open(working_directory + entry, "r")

        # Convert data from HTML to json
        parsed = collect(html_content.read(), regex2017)
        parsed_json = to_json_2017(parsed)

        # Change currency
        parsed_json = change_to_dollar(parsed_json)

        # Add data to dictionary regarding to data duplication
        add_to_dict_without_duplication(data, parsed_json)

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
