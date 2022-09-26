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


shopping_area_data_path = './shopping_area_data'  # 商圈資料暫存區

# user_token產生
def make_token(data):
    keys = 'mindnode'
    now = datetime.utcnow()
    expiretime = timedelta(days=3)
    payload = {
        'phone': data,
        'exp': now + expiretime,
    }
    return jwt.encode(payload, keys, algorithm='HS256')

# admin_token產生
def admin_make_token(account, control):
    keys = 'mindnode'
    now = datetime.utcnow()
    expiretime = timedelta(days=3)
    payload = {
        'account': account,
        'control': control,
        'exp': now + expiretime,
    }
    return jwt.encode(payload, keys, algorithm='HS256')

# token解析
def decode_token(token):
    return jwt.decode(token, 'mindnode',
                algorithms=['HS256'])

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
