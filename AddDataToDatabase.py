from supabase import create_client, Client

# Replace with your Supabase project URL and API key
SUPABASE_URL = "url"
SUPABASE_KEY = "key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

data = {
    "321654":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "24225013":
        {
            "name": "Himanshu Heda",
            "major": "Science",
            "starting_year": 2024,
            "total_attendance": 95,
            "standing": "A",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "24225019":
        {
            "name": "Priya Tiwari",
            "major": "Science",
            "starting_year": 2024,
            "total_attendance": 93,
            "standing": "B",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "24225009":
        {
            "name": "Anugraha Swain",
            "major": "Science",
            "starting_year": 2024,
            "total_attendance": 90,
            "standing": "B",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "24225045":
        {
            "name": "Shruti Mishra",
            "major": "Physics",
            "starting_year": 2024,
            "total_attendance": 89,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

# Insert student data into Supabase 'students' table
for key, value in data.items():
    supabase.table("students").upsert({"id": key, **value}).execute()