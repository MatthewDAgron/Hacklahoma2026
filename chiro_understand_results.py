import os
import json
import pymongo
import sys
from bbl_test_task import badPosture


"""
Database planning:

- Users have a unique ID, work for a company, have a preferred LLM voice model (specific strings from an ENUM)
- Users can be either a manager or employee
- Voice model has a name, a specified key
- Managers own employees identified by their unique ID. Managers and employees must have the same companies. Employees may only have one manager
- Weekly logs are created with a unique identifier, which is based on the week they are intended for and their respective employee's UUID
- Information about the time of day of the detected bad posture, how long it occurred, angle between shoulder and expected position, head and expected position, offset between shoulders
- Statistical inferences go in inferences, which connect to a log

"""



def check_results(user_id, video):
    # TODO


    Mongo_Str = os.getenv("MONGO_STR")
    DB_NAME = "weekly_logs"

    try:
        # connect to DB
        client = pymongo.MongoClient(Mongo_Str)
        db = client[DB_NAME]
        employees = db["employees"]
        managers = db["managers"]
        posture_data = db["posture_data"]
        users = db["users"]
        voice_models = db["voice_models"]
        week_log = db["week_log"]
    except:
        print("failed connection, please try again")
        sys.exit(1)
    

    data = badPosture(video)



    pass