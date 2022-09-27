import flask
from flask import jsonify, request
from flask_cors import CORS
import pandas as pd
import time
from datetime import datetime, timedelta
import jwt
import psycopg2
from sqlalchemy import create_engine
import urllib
from flasgger import Swagger
from io import BytesIO
import qrcode
from flask_sqlalchemy import SQLAlchemy
import random
from flask_bcrypt import Bcrypt
from requests_toolbelt.multipart import decoder
import json
from PIL import Image
import numpy as np
from flask import send_file
import base64
import pandas as pd
import string
import os
from MyQR import myqr
import shutil
import cryptocode
from .hash_keys import *


shopping_area_data_path = './shopping_area_data'  # 商圈資料暫存區

# user_token產生
def make_token(user_id, phone):
    print(manage_key())
    key = manage_key()['key']
    now = datetime.utcnow()
    expiretime = timedelta(days=3)
    payload = {
        'user_id': user_id,
        'phone': phone,
        'exp': now + expiretime,
    }
    return jwt.encode(payload, key, algorithm='HS256')

# admin_token產生
def admin_make_token(account, control):
    key = manage_key()['key']
    now = datetime.utcnow()
    expiretime = timedelta(days=3)
    payload = {
        'account': account,
        'control': control,
        'exp': now + expiretime,
    }
    return jwt.encode(payload, key, algorithm='HS256')

# token解析
def decode_token(token):
    key = manage_key()['key']
    return jwt.decode(token, key,
                algorithms=['HS256'])

# 敏感訊息加密(cryptocode)
def hash_data(data):
    key = manage_key()['key']
    str_encoded = cryptocode.encrypt(data, key)
    return str_encoded

# 敏感訊息解密(cryptocode)
def decode_data(data):
    key = manage_key()['key']
    str_decoded = cryptocode.decrypt(data, key)
    return str_decoded

# 密碼加密
def hash_password(password):
    bcrypt = Bcrypt()
    hashed_password = bcrypt.generate_password_hash(password=password).decode()
    return hashed_password

# 將輸出轉換成list
def execute_to_list(ex):
    rows = []
    for _row in ex.cursor._rows:
        row = {}
        for index, column in enumerate(ex._metadata.keys):
            row[column] = _row[index]
        rows.append(row)
    return rows
