import os
import json
import pymongo
import sys
import dotenv

dotenv.load_dotenv(".env")

def getEmployeesOfManager(managerUUID):
    # COMPLETE: Returns list of employees
    try:
        
        Mongo_Str = os.getenv("MONGO_STR")
        DB_NAME = "weekly_logs"

        # connect to DB
        client = pymongo.MongoClient(Mongo_Str)
        db = client[DB_NAME]
        employees = db["employees"]
    except:
        print("failed connection, please try again")
        sys.exit(1)


    # 


    employeesOfManager = list()
    with employees.find({"manager_uuid": managerUUID}) as cursor:
        for employee in cursor:
            employeesOfManager.append(employee)

    return employeesOfManager

def getWLofEmployee(employeeUUID):
    try:
        
        Mongo_Str = os.getenv("MONGO_STR")
        DB_NAME = "weekly_logs"

        # connect to DB
        client = pymongo.MongoClient(Mongo_Str)
        db = client[DB_NAME]
        week_log = db["week_log"]
    except:
        print("failed connection, please try again")
        sys.exit(1)

    WLofEmployee = list()
    with week_log.find({"employee_uuid": employeeUUID}) as cursor:
        for log in cursor:
            WLofEmployee.append(log)

    return WLofEmployee

def getModelOfUser(userID):
    try:
        
        Mongo_Str = os.getenv("MONGO_STR")
        DB_NAME = "weekly_logs"

        # connect to DB
        client = pymongo.MongoClient(Mongo_Str)
        db = client[DB_NAME]
        users = db["users"]
        voice_models = db["voice_models"]
    except:
        print("failed connection, please try again")
        sys.exit(1)
    
    user = users.find_one({"uuid": userID})
    vkey = user["preferred_voice_model"]
    vmodel = voice_models.find_one()

    return vmodel

    
print(getModelOfUser("b4d4f365-6e4d-4baf-918c-2cf3ebe00212"))




