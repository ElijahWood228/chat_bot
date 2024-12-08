from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import random

app = FastAPI()

# Хранилище пользователей (временное, как словарь)
users_db = {}

# Модели данных
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Генерация ID пользователя
def generate_user_id():
    return random.randint(1000, 9999)

# Эндпоинт для регистрации
@app.post("/register")
async def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует.")
    
    user_id = generate_user_id()
    users_db[user.email] = {"name": user.name, "password": user.password, "user_id": user_id}
    return {"status": 200, "message": "Регистрация успешна", "user_id": user_id}

# Эндпоинт для входа
@app.post("/login")
async def login(user: UserLogin):
    if user.email not in users_db or users_db[user.email]["password"] != user.password:
        raise HTTPException(status_code=400, detail="Неверный email или пароль.")
    
    return {"status": 200, "message": "Вход успешен", "user_id": users_db[user.email]["user_id"], "name": users_db[user.email]["name"]}
