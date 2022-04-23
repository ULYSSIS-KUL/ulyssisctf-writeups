from flask import Flask, request, render_template, send_file

from base64 import b64encode, b64decode
from json import dumps, loads
from os import environ
from random import choice
from Crypto import Random
from Crypto.Cipher import AES

app = Flask(__name__, static_url_path='/static')
key = Random.new().read(32)

MOCKING_RESPONSES_INVALID = [
    'Lol, that\'s not even valid input',
    'At least try to give me something valid',
    'Can\'t even produce valid input, can you?',
    'That\'s just meaningless...'
]

MOCKING_RESPONSES_VALID = [
    'Hah, you didn\'t really think I\'d decrypt that for you?',
    'You\'re so naive, thinking this would actually work...',
    'Sure, that looks like your flag alright!',
    'I know what it means, but you don\'t. Hah!'
]


def pad(data):
    length = 16 - (len(data) % 16)
    data += bytes([length])*length
    return data


def is_valid_padding(data):
    padding = data[-data[-1]:]
    return all(b == data[-1] for b in padding)


def bytes_to_b64(b):
    return b64encode(b).decode('utf8')


def encrypt(plaintext):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return bytes_to_b64(iv), bytes_to_b64(cipher.encrypt(pad(bytes(plaintext, 'utf8'))))


def is_valid(iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return is_valid_padding(plaintext)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/code.py', methods=['GET'])
def get_code():
    return send_file(__file__)


@app.route('/flag', methods=['GET'])
def get_encrypted_flag():
    iv, flag = encrypt('FLG{' + environ['FLAG'] + '}')
    return dumps({'iv': iv, 'flag': flag})


@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = loads(request.data)
    iv = b64decode(data['iv'])
    flag = b64decode(data['flag'])
    if len(flag) % 16 != 0 or not is_valid(iv, flag):
        return choice(MOCKING_RESPONSES_INVALID), 400
    return choice(MOCKING_RESPONSES_VALID)


if __name__ == "__main__":
    app.run()
