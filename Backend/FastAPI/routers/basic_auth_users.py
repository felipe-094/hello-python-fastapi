from fastapi import APIRouter, Depends, HTTPException, status
# FastAPI → crear la API
# Depends → sistema de dependencias (inyectar funciones automáticamente)
# HTTPException → lanzar errores HTTP
# status → códigos HTTP (401, 400, etc.)


from pydantic import BaseModel 
# Para definir modelos de datos con validación automática

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# OAuth2PasswordBearer → obtiene el token desde el header Authorization
# OAuth2PasswordRequestForm → obtiene username y password desde un formulario tipo login

router = APIRouter()
# Se crea el router principal

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
# Define el sistema de autenticación
# tokenUrl="login" → indica que el endpoint que genera el token es /login
# Este objeto luego se usa para extraer el token automáticamente

class User(BaseModel):
    username: str  # ⚠️ debería ser "username" (error tipográfico)
    full_name: str # Nombre completo
    email: str # Correo electrónico
    disabled: bool # Indica si el usuario está deshabilitado o no (True/False)
    
class UserDB(User):
    password: str
# Hereda de User y añade el password
# Esto representa el usuario TAL COMO está en la base de datos

users_db = { 
    "felipeluis": {
       "username": "felipeluis",  # clave del usuario
       "full_name": "Luis felipe",
       "email": "felipeluis@example.com",
       "disabled": False,
       "password": "123456" # contraseña (en la vida real esto se encripta)
    },
    "felipeluis2": {
       "username": "felipeluis2",
       "full_name": "Luis felipe 2",
       "email": "felipeluis2@example.com",
       "disabled": True, # usuario deshabilitado
       "password": "654321"
    },
}
# Simulación de base de datos (diccionario)

def search_user_db(username: str): # Busca el usuario en la base de datos (users_db) y devuelve un objeto UserDB
    if username in users_db: # verifica si el usuario existe en el diccionario
        return UserDB(**users_db[username])
         # convierte el diccionario en un objeto UserDB usando unpack (**)
# 👉 Esta función: Busca usuario en la “base de datos” Devuelve un objeto con contraseña incluida
    
def search_user(username: str): # Busca el usuario en la base de datos (users_db) y devuelve un objeto User sin contraseña
    if username in users_db: # verifica si el usuario existe en el diccionario
        return User(**users_db[username]) # convierte el diccionario en un objeto User usando unpack (**)
# 👉 Esta función: Busca usuario en la “base de datos” Devuelve un objeto sin contraseña
    
async def current_user(token: str = Depends(oauth2)): # Esta función se ejecuta automáticamente en rutas protegidas para obtener el usuario actual
    user = search_user(token) # usas el token como username para buscar el usuario
    if not user: # si el usuario no existe
           raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED, 
              detail="Credenciales de autenticacion invalidas", 
              headers={"WWW-Authenticate": "Bearer"})
         # 👉 Error 401 → no autorizado 👉 Bloquea el acceso
           
    if user.disabled: # si el usuario está inactivo
           raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST, 
              detail="Usuario inactivo")
        #👉 Si está deshabilitado → error
           
    return user
  # Devuelve el usuario autenticado
  # Este valor se inyecta en otros endpoints


@router.post("/login") # Ruta para iniciar sesión
async def login(form: OAuth2PasswordRequestForm = Depends()): # recibes datos tipo formulario 
# username=felipeluis
# password=123456
   user_db =  users_db.get(form.username) # Busca el usuario directamente en el diccionario
   if not user_db: # Si el usuario no existe, lanza error
          raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST, detail=" El Usuario no es correcto")
          
   user = search_user_db(form.username) # Convierte el usuario a UserDB, que incluye la contraseña
   if not form.password == user.password: # Compara contraseña del formulario con la contraseña del usuario
          raise HTTPException( # error si no coinciden
              status_code=status.HTTP_400_BAD_REQUEST, detail=" La contraseña no es correcta")
          
   return {"access_token": user.username, "token_type": "bearer"}
   # Devuelve el token


@router.get("/users/me") # Ruta protegida, solo accesible con token válido
async def me(user: User = Depends(current_user)): # Esto hace 
    # Esto hace: Ejecuta current_user Si falla → bloquea acceso Si pasa → inyecta el usuario
    return user
    # devuelve los datos del usuario autenticado