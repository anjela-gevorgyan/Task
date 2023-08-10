#!/usr/bin/env python3

import sys
import json
import requests
import urllib3
import netifaces
import urllib.parse
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
COMMANDS : list = ["add-task", "delete-task", "mark-as-completed", "show-tasks-list", "show-pending", "show-completed"]

class CloudInterface:
    '''
    Cloud interface.
    '''
    def __init__(self):
        self.base_url : str = f"http://192.168.1.5:5000"
        self.session : requests.Session = requests.Session()
        self.session.headers : dict = {"Content-type": "application/json"}
        self.session.verify : bool = False
        self.session.timeout : int = 20
        self.error_flag : bool = False
        self.my_ip : str = ""
        self.__search_info : list = ["Name", "Last name", "Comment"]
        try:
            active_interface : list = netifaces.gateways()['default'][netifaces.AF_INET][1]
        except KeyError:
            self.error_flag = True
            return

    def __parse_and_validate_response(self, response : requests.models.Response) -> (any, bool):
        '''
        Functionality that parses and validates a response from the Cloud.
        First argument - Cloud response object.
        '''
        body : str = response.text
        try:
            body : dict = json.loads(body)
        except json.decoder.JSONDecodeError:
            pass
        status_code : int = response.status_code
        if status_code in [405, 404, 502]:
            return body, False
        return body, True

    def send_request(self, method : str, data : dict, endpoint : str="") -> (any, bool):
        '''
        Functionality that sends request to the Cloud.
        First argument - request method.
        Second argument - request body.
        Third argument - URL endpoint.
        '''
        try:
            response_data : requests.models.Response = self.session.request(method=method,
                                                                            url=f"{self.base_url}/{endpoint}",
                                                                            data=json.dumps(data))
            return self.__parse_and_validate_response(response_data)
        except requests.ConnectTimeout:
            return "Connection timeout.", False
        except:
            return "Error on the Cloud side.", False

    def add_task(self) -> bool:
        data : dict = {}
        data['name'] : str = "add-task"
        data['title'] : str = input("Enter task title: ")
        data['description'] : str = input("Enter some description: ")
        data['status'] : str = input("Enter current status, e.g. pending or completed: ")
        body , flag = self.send_request("post", data, endpoint='/add-task')
        return flag
    
    def delete_task(self) -> bool:
        data : dict = {}
        data['name'] : str = "delete-task"
        data['title'] : str = input("Enter the title of task you want to delete: ")
        body, flag = self.send_request("post", data, endpoint='/delete-task')
        return flag

    def mark_as_completed(self) -> bool:
        data : dict = {}
        data['name'] = "mark-as-completed"
        data['title'] = input("Enter the title of task you completed: ")
        body, flag = self.send_request("post", data, endpoint='/mark-as-completed')
        return flag

    def show_tasks_list(self) -> bool:
        data : dict = {}
        data['name'] : str = "show-tasks-list"
        body, flag = self.send_request("get", data, endpoint='/show-tasks-list')
        print(*(title for title in body), sep='\n')
        return flag

    def show_pending(self) -> bool:
        data : dict = {}
        data['name'] : str = "show-pending"
        body, flag = self.send_request("get", data, endpoint='/show-pending')
        print(*(title for title in body), sep='\n')
        return flag

    def show_completed(self) -> bool:
        data : dict = {}
        data['name'] : str = "show-completed"
        body, flag = self.send_request("get", data, endpoint='/show-completed')
        print(*(title for title in body), sep='\n')
        return flag

def main() -> int:
    cloud = CloudInterface()
    print("Here are the features you can use:")
    for index, command in enumerate(COMMANDS):
        print(f"{index}: {command}")
    while True:
        number = input("Enter feature number: ")
        if number == "0":
            cloud.add_task()
        elif number == "1":
            cloud.delete_task()
        elif number == "2":
            cloud.mark_as_completed()
        elif number == "3":
            cloud.show_tasks_list()
        elif number == "4":
            cloud.show_pending()
        elif number == "5":
            cloud.show_completed()
        else:
            print("Unknown command.")
    return 0

if '__main__' == __name__:
    sys.exit(main())
