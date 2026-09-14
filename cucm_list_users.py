import os
from dotenv import load_dotenv
from ciscoaxl import axl

load_dotenv()

ucm = axl(
    username=os.getenv("CUCM_USER"),
    password=os.getenv("CUCM_PASS"),
    cucm=os.getenv("CUCM_HOST"),
    cucm_version=os.getenv("CUCM_VERSION"),
)

users = ucm.get_users()
for user in users:
    print(f"User ID: {user.userid}, Last Name: {user.lastName}, First Name: {user.firstName}")

phone = ucm.get_phones("SEPAAABBBCCCDDD")
if phone:
    # Assuming phone is a list of objects based on the traceback error
    p = phone[0]
    print(f"Description: {p.description}")
    print(f"CSS: {p.callingSearchSpaceName}")
else:
    print("Phone not found.")