import re
import requests
from tabulate import tabulate
from GlobalVariables import *
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

def get(link):
    prompt_1 = input("1 - GET all\n"
                     "2 - GET by ID\n"
                     "Your choice: ")
    if prompt_1 == "1":
        response = requests.get(f"https://jsonplaceholder.typicode.com/{link}")
        result = response.json()
        print_result(result)
    elif prompt_1 == "2":
        prompt_2 = input("Enter ID: ")
        response = requests.get(f"https://jsonplaceholder.typicode.com/{link}/{prompt_2}")
        result = response.json()
        print_result([result])
    else:
        print("Invalid input!")

def form_request(link, data, is_post_request=True):
    request = {}
    for key, item in data.items():
        if isinstance(item, dict):
            request[key] = form_request(link, item, is_post_request)
        elif key != "id":
            prompt_1 = input("Enter " + key + ": ")
            if prompt_1.strip() != "":
                if "id" in key.lower():
                    prompt_1 = int(prompt_1)
                elif not (key.lower() == "email" and re.match(prompt_1, email_regex)):
                    raise ValueError("The email value is incorrect!")
                elif not ((key.lower() == "url" or key.lower() == "website") and re.match(prompt_1, link_regex)):
                    raise ValueError("The website value is incorrect!")
                elif not (key.lower() == "phone" and re.match(prompt_1, phone_regex)):
                    raise ValueError("The phone value is incorrect!")
                elif not (key.lower() == "lat" and (-90 <= int(prompt_1) <= 90)):
                    raise ValueError("The latitude value is incorrect!")
                elif not (key.lower() == "lng" and (-180 <= int(prompt_1) <= 180)):
                    raise ValueError("The longitude value is incorrect!")
                request[key] = prompt_1
            else:
                if is_post_request:
                    raise ValueError("The value cannot be empty!")
    return request

def post(link):
    response = requests.get(f"https://jsonplaceholder.typicode.com/{link}/1")
    data = response.json()
    try:
        request = form_request(link, data)
    except ValueError as e:
        print(e)
        return
    response = requests.post(f"https://jsonplaceholder.typicode.com/{link}", request)
    if response.ok:
        print(f"The post with id {response.json().get('id')} has been added successfully.")
    else:
        print(f"An error occurred: {response.text}")

def patch(link):
    prompt_1 = input("Enter ID: ")
    response = requests.get(f"https://jsonplaceholder.typicode.com/{link}/{prompt_1}")
    data = response.json()
    try:
        request = form_request(link, data, False)
    except ValueError as e:
        print(e)
        return
    response = requests.patch(f"https://jsonplaceholder.typicode.com/{link}/{data["id"]}", request)
    if response.ok:
        print(f"The post's data with id {data["id"]} has been changed successfully.")
    else:
        print(f"An error occurred: {response.text}")

def delete(link):
    prompt_1 = input("Enter ID: ")
    response = requests.delete(f"https://jsonplaceholder.typicode.com/{link}/{prompt_1}")
    if response.ok:
        print(f"The post with id {prompt_1} has been deleted successfully.")
    else:
        print(f"An error occurred: {response.text}")

def main():
    while True:
        prompt = input("\n1 - Posts\n"
                         "2 - Comments\n"
                         "3 - Albums\n"
                         "4 - Photos\n"
                         "5 - Todos\n"
                         "6 - Users\n"
                         "Your choice: ")
        match prompt:
            case "1":
                link = "posts"
            case "2":
                link = "comments"
            case "3":
                link = "albums"
            case "4":
                link = "photos"
            case "5":
                link = "todos"
            case "6":
                link = "users"
            case _:
                print("Invalid input!")
                break

        prompt_1 = input("1 - GET\n"
                         "2 - POST\n"
                         "3 - PATCH\n"
                         "4 - DELETE\n"
                         "Your choice: ")
        match prompt_1:
            case "1":
                get(link)
            case "2":
                post(link)
            case "3":
                patch(link)
            case "4":
                delete(link)
            case _:
                break
main()