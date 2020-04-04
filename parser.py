import os
from html2json import collect

regex = {
    "artist": ["h2", "", ""],
}


def parse_html_data_2015():
    working_directory = "data/2015-03-18/"
    entries = os.listdir(working_directory)

    data = []
    for entry in entries:
        html_content = open(working_directory + entry, "r")

        parsed = collect(html_content.read(), regex)
        data.append(parsed["artist"])

    return data


if __name__ == '__main__':
    parsed_data = parse_html_data_2015()
    # print(list(dict.fromkeys(parsed_data)))