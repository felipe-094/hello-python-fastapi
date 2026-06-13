# Stop-Service MongoDB # ESTE COMANDO APAGA MONGODB EN LOCAL
# Get-Service MongoDB # CON ESTE SE VERIFICA QUE SI SE APAGO

# Start-Service MongoDB # ESTE COMANDO INICIA MONGODB EN LOCAL
# Get-Service MongoDB # CON ESTE SE VERIFICA QUE SI SE INICIO


from pymongo import MongoClient

# base de datos local
# db_client = MongoClient().local

# base de datos remota
db_client = MongoClient(
    "mongodb+srv://lfbalanta74_db_user:test@cluster0.krygsek.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

db = db_client["test"]