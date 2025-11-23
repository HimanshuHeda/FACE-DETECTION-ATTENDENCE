import os
from supabase import create_client, Client

# Store your credentials in environment variables for security
# In PowerShell, set them before running your script:
# $env:SUPABASE_URL = "https://ymxdeolfkdbnciycfejn.supabase.co"
# $env:SUPABASE_KEY = "your_anon_key_here"

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

data = [{
    "student_id": "24225013",
    "name": "Himanshu Heda",
    "email": "himanshu123@gmail.com",
    "age": 22,
    "major": "Computer Science",
    "department": "MCA"
}]

response = supabase.table("Students").insert(data).execute()
print(response)