from passlib.context import CryptContext

crypt = CryptContext(schemes=["bcrypt"])

print(crypt.hash("123456"))
print(crypt.hash("654321"))