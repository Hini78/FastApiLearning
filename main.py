from fastapi import FastAPI
from fastapi.responses import FileResponse
from models import *
from models.Feedback import FeedBack
from models.agedUser import AgedUser
import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

dbname = config['database']['dbname']
user = config['database']['user']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']

connection = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)

connection.autocommit = True
cursor = connection.cursor()
#just for test
#cursor.execute("INSERT INTO feedback.user_message(name, message) VALUES ('John Doe', 'testin db')")

app = FastAPI()
user = User(name = "John Doe", id =1)
fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
    3: {"username": "ma_usa", "email": "user@example.com"},
    4: {"username": "ma_secon_usa", "email": "user2@example.com"},
}

class Req(BaseModel):
    num1: str
    num2: str

@app.get("/")
async def root():
    return {"fghvm"}

@app.get("/custom")
async def custom():
    return FileResponse("html_files/index.html")

@app.get("/user")
async def user_response():
    return user

@app.get("/user/{user_id}")
async def read_user(user_id: int):
    return fake_users.get(user_id, {"error": "User not found"})

@app.get("/users_list/{start},{end}")
async def read_user(start: int = 0,end: int = 0):
    return list(fake_users.values())[start:end]

@app.post("/feedback")
async def feedback(fb: FeedBack):
    cursor.execute("INSERT INTO feedback.user_message(name, message) VALUES(%s, %s)", (fb.name, fb.message))
    return {"message": "feedback sent ᗜ˰ᗜ"}

@app.post("/aged_user")
async def aged_user_response(user: AgedUser):
    result = dict(user)
    result["is_adult"] = (user.age >= 18)
    return result

@app.post("/calc")
async def handle_post(req: Req):
    return {str(int(req.num1) + int(req.num2))}