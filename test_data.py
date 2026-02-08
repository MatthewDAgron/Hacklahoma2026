"""
MongoDB Atlas Test Data Generator
Generates realistic testing data for posture monitoring application
"""

from pymongo import MongoClient
from pymongo.server_api import ServerApi
import uuid
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv(".env")

# Configuration

# Sample data


def generate_uuid():
    """Generate a unique UUID string"""
    return str(uuid.uuid4())

def get_monday_of_week(date):
    """Get the Monday of the week for a given date"""
    return date - timedelta(days=date.weekday())

def create_week_log_uuid(employee_uuid, monday_date):
    """Create week_log UUID by combining employee UUID and Monday date"""
    date_str = monday_date.strftime("%Y%m%d")
    return f"{employee_uuid}_{date_str}"

def generate_posture_data(week_log_uuid, num_entries=5):
    """Generate realistic posture data entries for a week log"""
    posture_entries = []
    
    for _ in range(num_entries):
        entry = {
            "week_log_uuid": week_log_uuid,
            "avg_neck_angle": round(random.uniform(15.0, 45.0), 2),  # degrees
            "avg_back_angle": round(random.uniform(80.0, 100.0), 2),  # degrees
            "shoulder_offset": round(random.uniform(0.5, 5.0), 2),  # cm
            "time_passed": round(random.uniform(5.1, 3600.0), 2)  # seconds (>5s up to 1 hour)
        }
        posture_entries.append(entry)
    
    return posture_entries

def calculate_bad_posture_hours(posture_data_list):
    """Calculate total hours of bad posture from posture data"""
    # Assume bad posture if neck angle > 30 or back angle < 85 or > 95 or shoulder offset > 3
    total_bad_posture_seconds = 0
    
    for data in posture_data_list:
        is_bad_posture = (
            data["avg_neck_angle"] > 30 or 
            data["avg_back_angle"] < 85 or 
            data["avg_back_angle"] > 95 or 
            data["shoulder_offset"] > 3
        )
        if is_bad_posture:
            total_bad_posture_seconds += data["time_passed"]
    
    return round(total_bad_posture_seconds / 3600, 2)  # Convert to hours

def populate_database(num_managers=3, employees_per_manager=4, weeks_of_data=4):
    """
    Populate MongoDB with test data
    
    Args:
        num_managers: Number of manager accounts to create
        employees_per_manager: Number of employees per manager
        weeks_of_data: Number of weeks of historical data to generate
    """
    password = os.getenv("MONGO_PASSWORD")
    MONGO_URI = "mongodb+srv://mdagron_db_user:"+str(password)+"@cluster0.a63yfb5.mongodb.net/?retryWrites=true&w=majority"

    print(MONGO_URI)
    DATABASE_NAME = "weekly_logs"
    # Connect to MongoDB
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client[DATABASE_NAME]

    COMPANIES = ["TechCorp", "InnovateLabs", "DataSystems", "CloudWorks", "DevHub"]
    FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
    LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    VOICE_MODELS = [
        {"name": "Natural Voice", "key": "voice_natural_v1"},
        {"name": "Professional Voice", "key": "voice_professional_v1"},
        {"name": "Calm Voice", "key": "voice_calm_v1"},
        {"name": "Energetic Voice", "key": "voice_energetic_v1"},
        {"name": "Friendly Voice", "key": "voice_friendly_v1"}
    ]
    
    # Clear existing data (optional - comment out if you want to preserve existing data)
    print("Clearing existing collections...")


    
    db.employees.delete_many({})
    db.managers.delete_many({})
    db.users.delete_many({})
    db.voice_models.delete_many({})
    db.week_log.delete_many({})
    db.posture_data.delete_many({})

    voice_models = db["voice_models"]
    employees = db["employees"]
    managers = db["managers"]
    users = db["users"]
    week_logs = db["week_log"]
    posture_data = db["posture_data"]

    
    # Insert voice models
    print("Inserting voice models...")
    
    voice_models.insert_many(VOICE_MODELS)
    
    all_employees = []
    all_managers = []
    all_users = []
    all_week_logs = []
    all_posture_data = []
    
    # Generate managers
    print(f"Generating {num_managers} managers...")
    for i in range(num_managers):
        manager_uuid = generate_uuid()
        company = random.choice(COMPANIES)
        voice_model_key = random.choice(VOICE_MODELS)["key"]
        
        manager = {
            "uuid": manager_uuid,
            "company": company,
            "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "email": f"manager{i}@{company.lower()}.com"
        }
        
        user = {
            "uuid": manager_uuid,
            "company": company,
            "role": "manager",
            "preferred_voice_model": voice_model_key,
            "created_at": datetime.now()
        }
        
        all_managers.append(manager)
        all_users.append(user)
        
        # Generate employees for this manager
        print(f"  Generating {employees_per_manager} employees for manager {manager['name']}...")
        for j in range(employees_per_manager):
            employee_uuid = generate_uuid()
            
            employee = {
                "uuid": employee_uuid,
                "company": company,
                "manager_uuid": manager_uuid,
                "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                "email": f"employee{i}_{j}@{company.lower()}.com"
            }
            
            user = {
                "uuid": employee_uuid,
                "company": company,
                "role": "employee",
                "preferred_voice_model": random.choice(VOICE_MODELS)["key"],
                "created_at": datetime.now()
            }
            
            all_employees.append(employee)
            all_users.append(user)
            
            # Generate week logs and posture data for this employee
            print(f"    Generating {weeks_of_data} weeks of data for {employee['name']}...")
            for week in range(weeks_of_data):
                # Calculate the Monday of the week (going backwards from today)
                monday = get_monday_of_week(datetime.now() - timedelta(weeks=week))
                week_log_uuid = create_week_log_uuid(employee_uuid, monday)
                
                # Generate posture data for this week
                num_posture_entries = random.randint(10, 30)
                posture_data_list = generate_posture_data(week_log_uuid, num_posture_entries)
                
                # Calculate bad posture hours
                bad_posture_hours = calculate_bad_posture_hours(posture_data_list)
                
                week_log = {
                    "uuid": week_log_uuid,
                    "employee_uuid": employee_uuid,
                    "week_start": monday,
                    "week_end": monday + timedelta(days=6),
                    "total_bad_posture_hours": bad_posture_hours,
                    "created_at": datetime.now()
                }
                
                all_week_logs.append(week_log)
                all_posture_data.extend(posture_data_list)
    
    # Insert all data into MongoDB
    print("\nInserting data into MongoDB...")
    
    if all_managers:
        managers.insert_many(all_managers)
        print(f"✓ Inserted {len(all_managers)} managers")
    
    if all_employees:
        employees.insert_many(all_employees)
        print(f"✓ Inserted {len(all_employees)} employees")
    
    if all_users:
        users.insert_many(all_users)
        print(f"✓ Inserted {len(all_users)} users")
    
    if all_week_logs:
        week_logs.insert_many(all_week_logs)
        print(f"✓ Inserted {len(all_week_logs)} week logs")
    
    if all_posture_data:
        posture_data.insert_many(all_posture_data)
        print(f"✓ Inserted {len(all_posture_data)} posture data entries")
    
    print("\n✅ Database population complete!")
    print(f"\nSummary:")
    print(f"  - {len(all_managers)} managers")
    print(f"  - {len(all_employees)} employees")
    print(f"  - {len(all_users)} total users")
    print(f"  - {len(VOICE_MODELS)} voice models")
    print(f"  - {len(all_week_logs)} week logs")
    print(f"  - {len(all_posture_data)} posture data entries")
    
    client.close()

if __name__ == "__main__":
    # Configure these parameters as needed
    NUM_MANAGERS = 3
    EMPLOYEES_PER_MANAGER = 4
    WEEKS_OF_DATA = 4
    
    print("MongoDB Test Data Generator")
    print("=" * 50)
    print(f"Configuration:")
    print(f"  - Managers: {NUM_MANAGERS}")
    print(f"  - Employees per manager: {EMPLOYEES_PER_MANAGER}")
    print(f"  - Weeks of historical data: {WEEKS_OF_DATA}")
    print(f"  - Total employees: {NUM_MANAGERS * EMPLOYEES_PER_MANAGER}")
    print("=" * 50)
    print()
    
    # Update MONGO_URI and DATABASE_NAME at the top of the file before running!
    populate_database(
        num_managers=NUM_MANAGERS,
        employees_per_manager=EMPLOYEES_PER_MANAGER,
        weeks_of_data=WEEKS_OF_DATA
    )