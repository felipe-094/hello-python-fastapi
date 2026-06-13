from fastapi import APIRouter, Depends, HTTPException, status 
from pydantic import BaseModel 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import jwt, JWTError 
from passlib.context import CryptContext 
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256" 
ACCESS_TOKEN_DURATION = 10
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc56ea230b" 

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login") 

crypt = CryptContext(schemes=["bcrypt"]) 

class User(BaseModel): 
    username: str  
    full_name: str 
    email: str
    disabled: bool 
    
class UserDB(User): 
    password: str


users_db = { 
    "felipeluis": {
       "username": "felipeluis",  
       "full_name": "Luis felipe",
       "email": "felipeluis@example.com",
       "disabled": False,
       "password": "$2b$12$SLSvdpRVfADD2kQqalSM/.7MpW7ksB3RFGUisbNUhxElMg7c9GLWq" 
    },
    "felipeluis2": {
       "username": "felipeluis2",
       "full_name": "Luis felipe 2",
       "email": "felipeluis2@example.com",
       "disabled": True, 
       "password": "$2b$12$MQ8iu4Yk6GQeeKaThW.ZM.UYBtK06ZBHJtegyEdi5B/9Qy4N9AKzi" 
    },
}

def search_user_db(username: str): 
    if username in users_db: 
        return UserDB(**users_db[username]) 
    
def search_user(username: str): 
    if username in users_db: 
        return User(**users_db[username]) 

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Credenciales de autenticacion invalidas", 
        headers={"WWW-Authenticate": "Bearer"})
    
    try:
       username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub") 
       if username is None:
         raise exception
              
    except JWTError:
       raise exception 
     
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):     
    if user.disabled: 
           raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST, 
              detail="Usuario inactivo")
           
    return user


@router.post("/login") 
async def login(form: OAuth2PasswordRequestForm = Depends()): 
   user_db =  users_db.get(form.username) 
   if not user_db: 
          raise HTTPException( 
              status_code=status.HTTP_400_BAD_REQUEST, detail=" El Usuario no es correcto")
          
   user = search_user_db(form.username) 
   
   if not crypt.verify(form.password, user.password): 
          raise HTTPException( 
              status_code=status.HTTP_400_BAD_REQUEST, detail=" La contraseña no es correcta")  
   
   
   access_token = {"sub": user.username, 
                   "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)} 
          
   return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"} 

@router.get("/users/me") 
async def me(user: User = Depends(current_user)): 
    return user
    