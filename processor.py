import re
import json
import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def start():
    cls()
    contents = open("cfg.txt", "r", encoding="utf-8").readline()
    try:
        config = json.loads(contents)
    except json.JSONDecodeError:
        write_to_config()
    contents = open("cfg.txt", "r", encoding="utf-8").readline()
    config = json.loads(contents)
    print("Текущая позиция - " + str(config["pos"]) + ". Слово - " + find_word_at_position(int(config["pos"])) + ".")
    if config["ask_position_on_every_start"]:
        pos = input("Изменить позицию? (Да/нет)\n").lower()
        ask = config["ask_position_on_every_start"]
        while not (pos == "нет" or pos == "да"):
            cls()
            pos = input("Изменить позицию? (Да/нет)\n").lower()
        if pos == "да":
            pos = ""
            while not (type(pos) == int and find_word_at_position(pos)):
                try:
                    cls()
                    pos = int(input("Введите номер позиции: "))
                except ValueError:
                    pass
            cls()
            ask = input("Спрашивать позицию впоследствии?\n").lower()
            while not (ask == "нет" or ask == "да"):
                cls()
                ask = input("Спрашивать позицию впоследствии?\n").lower()
            ask = True if ask == "да" else False
        else:
            pos = config["pos"]
        cls()
        write_to_config(pos)
    begin_writing_from(json.loads(open("cfg.txt", "r", encoding="utf-8").readline())["pos"])


def write_to_config(pos=1):
    ask = True
    try:
        ask = json.loads(open("cfg.txt", "r", encoding="utf-8").readline())["ask_position_on_every_start"]
    except json.JSONDecodeError:
        pass
    f = open("cfg.txt", "w", encoding="utf-8")
    d = {"pos": pos, "ask_position_on_every_start": ask}
    f.write(json.dumps(d))
    f.close()


def find_word_at_position(pos):
    table = open("table.csv", "r", encoding="utf-8")
    for i, line in enumerate(table):
        if i + 1 == pos:
            res = re.search(r";[\w;][^\d;]+", line)
            if res:
                return line[res.span()[0]:res.span()[1]].replace(";", "")
            return ""


def process_raw_line_for_cli(line, semicolon_position, line_num):
    data = {
        "word": line[:semicolon_position]
    }
    translations = line[semicolon_position:]
    matches = re.findall(r"\d+?\)[\s\W][^\d\)]+", translations)
    if matches:
        translations_to_show = []
        for match in range(len(matches)):
            words_after_digit = re.sub(r"\d+?\)+", "", matches[match]).lstrip().rstrip()
            for translation in words_after_digit.split(","):
                translations_to_show.append(translation.lstrip().rstrip())
        data["translations"] = translations_to_show
        request_for_translations(data, line_num)
    else:
        data["translations"] = list(map(str.lstrip, translations.split(",")))
        if len(data["translations"]) > 2:
            request_for_translations(data, line_num)
        else:
            write_to_file(data, line_num)


def request_for_translations(data, line_num):
    initial_translations = data["translations"]
    data["translations"] = []

    out_of_range_index_is_present = True
    while out_of_range_index_is_present:
        print(data["word"], end=": \n")
        for tr_idx in range(len(initial_translations)):
            if (tr_idx + 1) % 5 == 0:
                print(str(tr_idx + 1) + ". " + initial_translations[tr_idx])
            else:
                print(str(tr_idx + 1) + ". " + initial_translations[tr_idx], end=" ")
        print("\n")
        out_of_range_index_is_present = False
        user_input = list(map(int, input("Введите номера необходимых переводов: ").split()))
        for idx in user_input:
            if idx > len(initial_translations) or idx == 0:
                cls()
                out_of_range_index_is_present = True
                break

    cls()
    for index in user_input:
        data["translations"].append(initial_translations[index - 1])
    write_to_file(data, line_num)


def write_to_file(data, line_num):
    num = line_num // 100 + 1
    f = open("AnkiDeck{}.tsv".format(num), "a", encoding="utf-8")
    f.write(numerate_list(data["translations"]) + "\t" + data["word"] + "\n")
    f.close()
    write_to_config(line_num + 1)


def numerate_list(translations):
    string = ""
    for i in range(len(translations)):
        if len(translations) == 1:
            return translations[i]
        string += str(i + 1) + ". {}".format(translations[i]) + " "
    return string


def begin_writing_from(position):
    table = open("table.csv", "r", encoding="utf-8").read().splitlines()
    for current_position in range(position - 1, len(table)):
        for i in range(len(table[current_position])):
            if re.match("[a-zA-Z]", table[current_position][i]):
                value = table[current_position][i:].replace("\"", "")
                semicolon_position = re.search(";", value).span()[0]
                value = value.replace(";", ",")
                value = value[:semicolon_position] + "" + value[semicolon_position + 1:]
                value = re.sub(r"\(.*?\)", "", value)
                ten = re.search(r"10\)", value)
                if ten:
                    index_ten_begins = ten.span()[0] - 1
                    value = value[0:index_ten_begins]
                current_position += 1
                process_raw_line_for_cli(value, semicolon_position, current_position)
                break


try:
    start()
except:
    cls()
    print("Interrupted.")
