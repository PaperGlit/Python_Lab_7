import requests
from tabulate import tabulate
from collections import defaultdict


def to_table(result):
    data = defaultdict(list)
    for i in result:
        for key, value in i.items():
            data[key].append(value)
    data = dict(data)
    headers = data.keys()
    rows = zip(*data.values())
    # noinspection PyTypeChecker
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def to_list(result):
    for i in result:
        print()
        for key, value in i.items():
            print(f"{str(key)}: {value}")

def print_result(result):
    prompt_2 = input("1 - Print a table\n"
                     "2 - Print a list\n"
                     "Your choice: ")
    if prompt_2 == "1":
        to_table(result)
    elif prompt_2 == "2":
        to_list(result)
    else:
        print("Invalid input!")

def get_keys():
    response = requests.get("https://jsonplaceholder.org/posts/1")
    result = response.json()
    keys = result.keys()
    return keys

def main():
    while True:
        prompt = input("\n1 - GET\n"
                         "2 - POST\n"
                         "3 - PATCH\n"
                         "4 - DELETE\n"
                         "Your choice: ")
        match prompt:
            case "1":
                prompt_1 = input("1 - GET all\n"
                                 "2 - GET by ID\n"
                                 "Your choice: ")
                if prompt_1 == "1":
                    response = requests.get("https://jsonplaceholder.org/posts")
                    result = response.json()
                    print_result(result)
                elif prompt_1 == "2":
                    post_id = input("Enter ID: ")
                    response = requests.get("https://jsonplaceholder.org/posts/" + post_id)
                    result = response.json()
                    print_result([result])
                else:
                    print("Invalid input!")
            case "2":
                request = {}
                keys = get_keys()
                for key in keys:
                    # if key == "url":
                    #     request[key] = f"https://jsonplaceholder.org/posts/{request["slug"]}"
                    if key != "id":
                        prompt_2 = input("Enter " + key + ": ")
                        if prompt_2.strip() != "":
                            request[key] = prompt_2
                        else:
                            print("The value cannot be empty!")
                            break
                response = requests.post("https://jsonplaceholder.org/posts", request)
                print(response.text)
            case "3":
                pass
            case _:
                break
main()