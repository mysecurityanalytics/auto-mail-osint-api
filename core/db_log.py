import time
import pymongo
import jwt
import os

db_url = os.environ.get("DATABASE_URL")
client = pymongo.MongoClient(db_url)
db = os.environ.get("DB_NAME")
users_col = client[db]["logs"]

jwt_secret = str(os.environ.get("JWT_SECRET"))


class logging:
    def __init__(self, email):
        self.email = email

    def insert_db(self, token):
        try:
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        except:
            return False
        ts = int(time.time())
        mydict = {
            "user_email": str(data["email"]),
            "checked_email": self.email,
            "timestamp": ts,
        }
        users_col.insert_one(mydict)
        return True
