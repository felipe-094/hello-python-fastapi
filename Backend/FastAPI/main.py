
#Documentacion oficial: https://fastapi.tiangolo.com/es/

# instala FastAPI: pip install *fastapi[all]*

from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

# Recursos estáticos (imágenes, css, js, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Url local: https://127.0.0.1:8000

@app.get("/")
async def root():
    return "Hola FastAPI!"

# Url Local: https://127.0.0.1:8000/url

@app.get("/url")
async def url():
    return { "url":"https://mouredev.com/python" }

# inicia el server: python -m uvicorn main:app --reload
# Detener el server: CTRL+C

# Documentation con Swagger: https://127.0.0.1:8000/docs
# Documentacion con Redocly: https://127.0.0.1:8000/redoc