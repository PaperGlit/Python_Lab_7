import re
import requests
from GlobalVariables import *


class NetworkRequest:
    @staticmethod
    def get(uow, entity, db_handler):
        prompt = input("1 - GET all\n2 - GET by ID\nYour choice: ")
        try:
            if prompt == "1":
                result = getattr(uow, entity).get_all()
                db_handler.insert_history(entity, "GET", "all")
                return result
            elif prompt == "2":
                entity_id = input("Enter ID: ")
                result = getattr(uow, entity).get_by_id(entity_id)
                db_handler.insert_history(entity, "GET", entity_id)
                return [result]
            else:
                print("Invalid input!")
        except requests.HTTPError as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def post(uow, entity, db_handler):
        try:
            example = getattr(uow, entity).get_by_id(1)  # Fetch example data structure
            request = NetworkRequest.form_request("", example)
            result = getattr(uow, entity).add(request)
            db_handler.insert_history(entity, "POST", result["id"])
            print(f"Created successfully with ID: {result['id']}")
        except ValueError as e:
            print(e)
        except requests.HTTPError as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def patch(uow, entity, db_handler):
        entity_id = input("Enter ID: ")
        try:
            example = getattr(uow, entity).get_by_id(entity_id)
            request = NetworkRequest.form_request("", example, is_post_request=False)
            result = getattr(uow, entity).update(entity_id, request)
            db_handler.insert_history(entity, "PATCH", entity_id)
            print(f"Updated successfully for ID: {entity_id}")
        except ValueError as e:
            print(e)
        except requests.HTTPError as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def delete(uow, entity, db_handler):
        entity_id = input("Enter ID: ")
        try:
            if getattr(uow, entity).delete(entity_id):
                db_handler.insert_history(entity, "DELETE", entity_id)
                print(f"Deleted successfully.")
        except requests.HTTPError as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def form_request(link, data, is_post_request=True):
        request = {}
        for key, item in data.items():
            if isinstance(item, dict):
                request[key] = NetworkRequest.form_request(link, item, is_post_request)
            elif key != "id":
                prompt_1 = input("Enter " + key + ": ")
                if prompt_1.strip() != "":
                    if "id" in key.lower():
                        prompt_1 = int(prompt_1)
                    elif key.lower() == "email" and not re.match(email_regex, prompt_1):
                        raise ValueError("The email value is incorrect!")
                    elif (key.lower() == "url" or key.lower() == "website") and not re.match(link_regex, prompt_1):
                        raise ValueError("The website value is incorrect!")
                    elif key.lower() == "phone" and not re.match(phone_regex, prompt_1):
                        raise ValueError("The phone value is incorrect!")
                    elif key.lower() == "lat" and not (-90 <= int(prompt_1) <= 90):
                        raise ValueError("The latitude value is incorrect!")
                    elif key.lower() == "lng" and  not (-180 <= int(prompt_1) <= 180):
                        raise ValueError("The longitude value is incorrect!")
                    request[key] = prompt_1
                else:
                    if is_post_request:
                        raise ValueError("The value cannot be empty!")
        return request