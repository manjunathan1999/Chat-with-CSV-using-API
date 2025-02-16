from fastapi import Depends, FastAPI, Request, HTTPException, status
from ChatCSV.chatcsvservices import get_chatcsv_query, ingest_csv, import_csv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")


@app.get("/")
def version(reg: Request):
    return "Chat-CSV-API"

# --------------------- For ChatGPT -----------------------#
SECRET_KEY = "Chat-CSV-API"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User database simulation
users_db = {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/register")
async def register(user_data: dict):
    username = user_data["username"]
    password = user_data["password"]
    if username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(password)
    user_dict = {
        "username": username,
        "hashed_password": hashed_password
    }
    users_db[username] = user_dict
    return {"message": "User registered successfully"}
    
@app.post("/login", response_model=Token)
async def login(user_data: dict):
    user = authenticate_user(users_db, user_data["username"], user_data["password"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --------------------- For ChatCSV -----------------------#

@app.post("/execute-sql")
async def generate_csv(req_info: dict, current_user: User = Depends(get_current_user)):
    table = req_info["type"]
    return import_csv(table)


@app.post("/ingest")
async def ingest(req_info: dict, current_user: User = Depends(get_current_user)):
    type = req_info["type"]
    return ingest_csv(type)


@app.post("/query")
async def ask_query(req_info: dict, current_user: User = Depends(get_current_user)):
    query = req_info["question"]
    type = req_info["type"]
    chat_obj = get_chatcsv_query(type)
    return chat_obj.query_chat(query)