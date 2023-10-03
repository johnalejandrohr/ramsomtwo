import hashlib
import bcrypt

passencript = 'e0177a140c5d7ffe24cc2bbd529cebb8199d1acddb16a4390313f30ecc0d7e39d22c7e5fa58ca0c7b0ab550b730f1ad2f2165fdcb86e7f1ee4ad2fba7ac7a03c'

def get_hash():
    hascomputer = 'hola mundo por tress'
    hascomputer_bytes = hascomputer.encode('utf-8')
    hascomputer = hashlib.sha512(hascomputer_bytes)
    hascomputer = hascomputer.hexdigest()
    print(hascomputer)

def get_hash_bcrypt():
    # Contraseña que quieres hashear
    password = "password"

    # Generar un salt aleatorio y hashear la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Mostrar el hash bcrypt
    print("Hash Bcrypt generado:", hashed_password.decode('utf-8'))

get_hash_bcrypt()
