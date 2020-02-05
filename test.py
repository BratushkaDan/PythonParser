import re

def process_raw_line_for_cli(line):
    processed_line = ""
    #if search doesn't find 1) ... 10)
    #else:
    #search finds 1) ... 10)
    return processed_line

def request_for_translations(line):
    text = process_raw_line_for_cli(line)
    # if processed line doesn't find numbers, don't disturb user(rethink dependencies)

    # map(int, input.split())
    # use dict with retrieved data and put it together in order to pass to dis_user_input()
    return []

def dismember_user_input(data):
    # algorithms that put first word separated with comma and the other ones separated like numbered list 1)
    return []

def begin_writing_from(position):
    table = open("table.csv", "r").read().splitlines()
    result = []
    for current_position in range(position-1, len(table)):
        for i in range(len(table[current_position])):
            if re.match("[a-zA-Z]", table[current_position][i]):
                value = table[current_position][i:].replace("\"", "")
                semicolon_position = re.search(";", value).span()[0]
                # value = value.replace(",", "") # replaces all commas with blank space
                value = value.replace(";", "")
                value = value[:semicolon_position] + "," + value[semicolon_position:]
                # print(value[:semicolon_position]) # prints first word!
                value = re.sub(r"\(.*?\)", "", value)
                ten = re.search(r"10\)", value)
                if ten:
                    index_ten_ends = ten.span()[0] - 1
                    value = value[0:index_ten_ends]
                request_for_translations(value)
                result.append(value)
                break

    f = open("AnkiDeck.csv", "w")
    for line in result:
        print(line)
        # line = re.sub(r"\d\)", "", line)
        f.writelines(line + "\n")
    f.close()
