#!/usr/bin/env python3
'''
Copyright(c) 2018 Kampr Corporation.
'''

import sys
import socket
from flask import request, jsonify
from flask_restful import Resource, reqparse
import utils

LOGGING = None
NAME = "SERVER"

@utils.REG_APP.route("/add-task", methods=["post"])
def add_task():
    print("in 'add_task' command.")
    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True, help="reader_ip argument is missing.")
    parser.add_argument("description", required=True, help="reader_mac argument is missing.")
    parser.add_argument("status", required=True, help="app_name argument is missing.")
    data = parser.parse_args()
    if not "all_tasks" in utils.DB.list_collection_names():
        utils.create_collection("all_tasks")
        print ("Collection 'all_tasks' added.")
    try:
        utils.DB['all_tasks'].insert_one(data)
        return "Success", 200
    except Exception as e:
        return f"Failed: {e}", 500

@utils.REG_APP.route("/delete-task", methods=["post"])
def delete_task():
    print("in 'delete_task' command.")
    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True, help="reader_ip argument is missing.")
    parser.add_argument("description", required=False, help="reader_mac argument is missing.")
    parser.add_argument("status", required=False, help="app_name argument is missing.")
    data = parser.parse_args()
    try:
        result = utils.DB['all_tasks'].delete_one({"title": data['title']})
        if result.deleted_count > 0:
            return "Success", 200
        else:
            return "Document not found", 404
    except Exception as e:
        return f"Failed: {e}", 500

@utils.REG_APP.route("/mark-as-completed", methods=["post"])
def mark_as_completed():
    print("in 'mark_as_completed' command.")
    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True, help="reader_ip argument is missing.")
    data = parser.parse_args()
    filter_data = {"title": data['title']}
    update_data = {"status": "completed"}
    try:
        result = utils.DB['all_tasks'].update_one(filter_data, {"$set": update_data})
        if result.modified_count > 0:
            return "Document updated successfully", 200
        else:
            return "Document not found", 404
    except Exception as e:
        return f"Failed: {e}", 500

@utils.REG_APP.route("/show-tasks-list", methods=["get"])
def show_task_list():
    print("in 'show_task_list' command.")
    try:
        tasks = utils.DB['all_tasks'].distinct('title')
        return tasks, 200
    except Exception as e:
        return f"Failed: {e}", 500

@utils.REG_APP.route("/show-completed", methods=["get"])
def show_completed():
    print("in 'show_completed' command.")
    completed = []
    try:
        tasks = utils.DB['all_tasks'].find({"status" : "completed"})
        for task in tasks:
            completed.append(task['title'])
        return completed, 200
    except Exception as e:
        return f"Failed: {e}", 500

@utils.REG_APP.route("/show-pending", methods=["get"])
def show_pending():
    print("in 'show_pending' command.")
    pendings = []
    try:
        tasks = utils.DB['all_tasks'].find({"status" : "pending"})
        for task in tasks:
            pendings.append(task['title'])
        return pendings, 200
    except Exception as e:
        return f"Failed: {e}", 500

def get_local_ip_address():
    '''
    Gets local IP address.
    '''
    main_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    main_socket.connect(("8.8.8.8", 80))
    ip_address = main_socket.getsockname()[0]
    main_socket.close()
    return ip_address

def main():
    '''
    Cloud entry point.
    '''
    utils.REG_APP.run(debug=False, host=get_local_ip_address())

if __name__ == "__main__":
    sys.exit(main())
