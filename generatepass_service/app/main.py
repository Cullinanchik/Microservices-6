from fastapi import FastAPI, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Annotated
import uvicorn
import os
from database import database as database
from model.model import Password
from typing import List
import string
import random
from keycloak import KeycloakOpenID
from prometheus_fastapi_instrumentator import Instrumentator

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

Instrumentator().instrument(app).expose(app)

words_list = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry", "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yam", "zucchini"]

# Данные для подключения к Keycloak
KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

user_token = ""
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)

@app.post("/get_token")
async def get_token(username: str = Form(...), password: str = Form(...)):
    try:
        # Получение токена
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        global user_token
        user_token = token
        return token
    except Exception as e:
        print(e)  # Логирование для диагностики
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def check_user_roles():
    global user_token
    token = user_token
    try:
        token_info = keycloak_openid.introspect(token["access_token"])
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        user_token = ''
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

def generate_password(length=12, use_special=True, use_numbers=True, use_uppercase=True):
    """
    Генерирует случайный пароль заданной длины.
    
    Args:
        length (int): Длина генерируемого пароля.
        use_special (bool): Включать ли специальные символы.
        use_numbers (bool): Включать ли цифры.
        use_uppercase (bool): Включать ли заглавные буквы.

    Returns:
        str: Сгенерированный пароль.
    """
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    return ''.join(random.choice(characters) for _ in range(length))

def generate_passphrase(num_words=4):
    """
    Генерирует пароль-фразу, состоящую из заданного числа случайных слов.
    
    Args:
        num_words (int): Количество слов в фразе.
        
    Returns:
        str: Сгенерированная фраза.
    """
    return ''.join(random.choice(words_list) for _ in range(num_words))

@app.get("/generate-password")
async def password(length: int = 12, use_special: bool = False, use_numbers: bool = True, use_uppercase: bool = True, db: Session = Depends(get_db)):
    if (check_user_roles()):
        if length < 6 or length > 128:
            raise HTTPException(status_code=400, detail="Length should be between 6 and 128 characters")
        generated_password = generate_password(length, use_special, use_numbers, use_uppercase)
        db_password = database.Password(password=generated_password, password_type="password")
        db.add(db_password)
        db.commit()
        return {"password": generated_password}
    else:
        return "Wrong JWT Token"

@app.get("/generate-passphrase")
async def passphrase(num_words: int = 4, db: Session = Depends(get_db)):
    if (check_user_roles()):
        if num_words < 1 or num_words > 10:
            raise HTTPException(status_code=400, detail="Number of words should be between 1 and 10")
        generated_passphrase = generate_passphrase(num_words)
        db_passphrase = database.Password(password=generated_passphrase, password_type="passphrase")
        db.add(db_passphrase)
        db.commit()
        return {"passphrase": generated_passphrase}
    else:
        return "Wrong JWT Token"

@app.get("/get_passwords")
async def get_passwords(db: db_dependency):
    if (check_user_roles()):
        result = db.query(database.Password).offset(0).limit(100).all()
        return result
    else: 
        return "Wrong JWT Token"

@app.get("/health", status_code=status.HTTP_200_OK)
async def generatepass_health():
    if (check_user_roles()):
        return {'message': 'service is active'}
    else:
        return "Wrong JWT Token"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
