import traceback
from app.core.security import hash_password
try:
    print(hash_password("password123"))
    print("SUCCESS")
except Exception as e:
    print("ERROR:")
    traceback.print_exc()
