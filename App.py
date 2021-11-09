from flask import Flask, render_template
from flask import Flask, request, render_template, jsonify, Response, redirect, url_for, send_file
import os
from random import randrange

app = Flask(__name__)

def generatePrivateKey(publicKey):
    subKey = randrange(99)
    privateKey = []
    for i, values in enumerate(publicKey):
        privateKey.append(publicKey[i] ^ subKey)
    privateKey.append(subKey)
    return privateKey

def generateKeys():
    publicKey = bytearray(os.urandom(1000))
    privateKey = generatePrivateKey(publicKey)
    print(publicKey)
    print(privateKey)

def openFile(img):
    image = img.read()
    img.close()
    image = list(bytearray(image))
    return image

def openFileText(txt):
    text = txt.read()
    txt.close()
    text  = eval(text)
    return text

def openFileKey(txt):
    text = txt.read()
    txt.close()
    text = list(bytearray(text))
    return text

def encriptar(file, key):
    encripted = openFile(file).copy()
    for i, values in enumerate(key):
        encripted.insert(key[i],key[i])
    return encripted

def desencriptar(file, key):
    desencripted = file.copy()
    for i, values in enumerate(key):
        desencripted.pop(key[(len(key)-1)-i])
    return desencripted


@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/encript', methods=['POST'])
def encript():
    uploaded_files = request.files.getlist('file')
    if not uploaded_files:
        return 'No se subio los archicos', 400

    imagen = uploaded_files[0]
    key = openFileKey(uploaded_files[1])
    encriptado = encriptar(imagen,key)

    encF = str(encriptado)
    encName = imagen.filename + ".txt"
    print ('done')
    return Response( encF,mimetype="text/txt", headers={"Content-disposition":"attachment; filename="+encName})

@app.route('/decript', methods=['POST'])
def decript():
    uploaded_files = request.files.getlist('file')
    if not uploaded_files:
        return 'No se subio los archicos', 400
    imagen = openFileText(uploaded_files[0])

    desencName = uploaded_files[0].filename[:-4]
    desencExt = desencName[-3:]
    key = openFileKey(uploaded_files[1])

    lista=desencriptar(imagen, key)
    desencF = bytearray(lista)
    return Response( desencF,mimetype="image/"+desencExt, headers={"Content-disposition":"attachment; filename="+desencName})

@app.route('/publickey')
def publickey():
    encF = 'key'
    encName = 'publickey.txt'
    print ('done')
    return Response( encF,mimetype="text/txt", headers={"Content-disposition":"attachment; filename="+encName})

@app.route('/privatekey')
def privatekey():
    encF = 'key'
    encName = 'privatekey.txt'
    print ('done')
    return Response( encF,mimetype="text/txt", headers={"Content-disposition":"attachment; filename="+encName})

if __name__=='__main__':
    app.run(port = 3000, debug=True) 