import sqlite3
from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json
import random
import base64

app = Flask(__name__)

def load_key_iv():
    with open('key.json', 'r') as json_file:
        data = json.load(json_file)

    hex_key = data['key']
    hex_iv = data['iv']
    key = bytes.fromhex(hex_key)
    iv=bytes.fromhex(hex_iv)
    return key, iv


key , iv = load_key_iv()

def  encrypt(plaintext):

    cipher = AES.new(key, AES.MODE_CBC,iv)

    padded_password = pad(plaintext.encode('utf-8'), AES.block_size)

    ciphertext = cipher.encrypt(padded_password)
    encrypted_password = base64.b64encode(iv + ciphertext).decode('utf-8')
    return encrypted_password



@app.route('/signup', methods=['POST'])
def signup():
    conn = sqlite3.connect('securite.db')
    username = request.form['username']
    password = request.form['password']
    cur = conn.cursor()
    cur.execute("Select * from users where username = ? ", (username,))
    if cur.fetchone() is None:
        password = encrypt(plaintext=password)
        cur.execute("insert into users (username, password) VALUES (?, ?)",(username,password))
    else:
        conn.commit()
        conn.close()
        return "already exists"
    conn.commit()
    conn.close()
    return "ajouter"

@app.route('/del' , methods=['GET'])
def delall():
    conn = sqlite3.connect('securite.db')
    cur = conn.cursor()
    cur.execute("DROP table users")
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               username TEXT NOT NULL,
               password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    return "suppression effectué"

@app.route('/login', methods=['POST'])
def login():
    conn = sqlite3.connect('securite.db')
    username = request.form['username']
    password = request.form['password']
    cur = conn.cursor()
    cur.execute("Select password from users where username = ? ", (username,))
    row = cur.fetchone()
    conn.commit()
    conn.close()
    if row is None:
        return "not found"
    else:
        if encrypt(password) == row[0]:
            print(row)
            return "connected"
        else:
            print(row[0])
            print(encrypt(password))
            return "not found"

if __name__ == '__main__':
    conn = sqlite3.connect('securite.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               username TEXT NOT NULL,
               password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    print(encrypt('test'))
    app.run(debug=True)
