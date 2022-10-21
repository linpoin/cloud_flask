import pandas as pd

from flask import request
from flask import Blueprint
from .def_user import *

user = Blueprint('user', __name__)


@user.route('/')
def index():
    return 'user.hello'

# 使用者註冊
@user.route('/signup', methods=['POST'])
def user_signup():
    if request.method == 'POST':
        body_json = request.get_json()
        if 'username' in body_json.keys() and 'password' in body_json.keys() and 'phone_number' in body_json.keys():
            name = body_json['username']
            password = body_json['password']
            phone = body_json['phone_number']

            return_me = usercreate(name, password, phone)
            return return_me
        else:
            error = {'code': 400,
                     'message': '請輸入帳號、密碼及手機號碼',
                     }
            return error, 400

# 使用者登入
@user.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        body_json = request.get_json()
        if body_json == None:
            return {'code': 401, 'message': '無附帶body'}
        if 'phone' in body_json.keys() and 'password' in body_json.keys():
            phone = body_json['phone']
            password = body_json['password']
            return_me = user_login_f(phone, password)
            return return_me
        else:
            error = {'code': 400,
                     'message': '請確認電話、密碼',
                     }
            return error, 400

# 使用者詳細資訊
@user.route('/info', methods=['GET'])
def user_info():
    if request.method == 'GET':
        token = request.headers.get('Authorize')
        if token == None:
            return {'code': 401, 'message': '無附帶token'}
        if 'Authorize' in request.headers:
            try:
                user_id = decode_token(token)['user_id']
                return_me = user_info_f(user_id)
                return return_me
            except:
                return {'code': 401, 'message': 'token已過期'}, 401
        else:
            return {'code': 401, 'message': '無附帶token', '123': request.headers}, 401


# "單一"使用者詳細資訊
@user.route('/info/<user_id>', methods=['GET'])
def oneuser_info(user_id):
    if request.method == 'GET':
        try:
            return_me = user_info_f(user_id)
            return return_me
        except:
            return {'code': 401, 'message': '未知錯誤'}, 401

# 使用者資料(指定因子)
@user.route('/<en_name>/data/<factor>', methods=['GET'])
def user_data_factor(en_name, factor):
    if request.method == 'GET':
        token = request.headers.get('Authorize')
        if token == None:
            return {'code': 401, 'message': '無附帶token'}
        if 'Authorize' in request.headers:
            try:
                user_id = jwt.decode(token, 'mindnode',
                                   algorithms=['HS256'])['user_id']
                return_me = user_data_f(user_id, en_name, factor)
                return return_me
            except:
                return {'code': 401, 'message': 'token已過期'}, 401
        else:
            return {'code': 401, 'message': '無附帶token', '123': request.headers}, 401

# 闖關
@user.route('/<en_name>/run_level', methods=['POST'])
def user_runlevel(en_name):
    if request.method == 'POST':
        body_json = request.get_json()
        token = request.headers.get('Authorize')
        if token == None:
            return {'code': 401, 'message': '無附帶token'}
        if 'shop_id' in body_json.keys():
            try:
                decode_jwt = jwt.decode(
                    token, 'mindnode', algorithms=['HS256'])
                phone = decode_jwt['phone']
                shop_id = body_json['shop_id']
                return_me = run_level_f(phone, en_name, shop_id)
                return return_me
            except:
                return {'code': 401, 'message': 'token已過期'}, 401
        else:
            return {'code': 401, 'message': '無附帶shop_id'}, 401

# 抽獎
@user.route('/<en_name>/get_prize', methods=['POST'])
def user_get_prize(en_name):
    if request.method == 'POST':
        token = request.headers.get('Authorize')
        if token == None:
            return {'code': 401, 'message': '無附帶token'}, 401
        else:
            try:
                decode_jwt = jwt.decode(
                    token, 'mindnode', algorithms=['HS256'])
                phone = decode_jwt['phone']

                # 取得user_id
                select_phone_q = f"select * from user.users where phone = '{phone}'"
                have_phone = mysql_engine.execute(select_phone_q).fetchone()
                user_id = have_phone['user_id']
                name = have_phone['name']

                # 取得level_num
                select_level_num_q = f"select {en_name}_num from user.run_level_number where user_id = '{user_id}'"
                level_num = mysql_engine.execute(select_level_num_q).fetchone()
                level_num = int(level_num[f'{en_name}_num'])

                
                # 取得通關數及抽獎方式
                select_lottery_level_num_q = f"select repeat_pass, lottery_method, lottery_level_num from shopping_area.shopping_area_infor where shopping_area_eg_name = '{en_name}'"
                lottery_level_num = mysql_engine.execute(
                    select_lottery_level_num_q).fetchone()
                lottery_method = lottery_level_num['lottery_method']
                repeat_pass = lottery_level_num['repeat_pass']
                lottery_level_num = lottery_level_num['lottery_level_num']
                if lottery_method == 1:
                    if level_num >= int(lottery_level_num):
                        if repeat_pass == 1:
                            level_num = 0
                            level_up_q = f"UPDATE user.run_level_number SET {en_name}_num = '{level_num}'  WHERE user_id = '{user_id}'"
                            mysql_engine.execute(level_up_q)

                        return_me = user_get_prize_f(
                            lottery_method, en_name, user_id, phone)
                        return return_me
                    else:
                        return {'code': 403, 'message': '闖關未達5關'}, 403
                elif lottery_method == 0:
                    return {'code': 400, 'message': '請至核銷專區'}
            except:
                return {'code': 401, 'message': 'token已過期'}, 401

# 使用者獎品列表
@user.route('/prize', methods=['GET'])
def user_prize():
    if request.method == 'GET':
        token = request.headers.get('Authorize')
        if token == None:
            return {'code': 401, 'message': '無附帶token'},401
        if 'Authorize' in request.headers:
            try:
                user_id = jwt.decode(token, 'mindnode',
                                   algorithms=['HS256'])['user_id']
                return_me = user_get_all_prize_f(user_id)
                return return_me
            except:
                return {'code': 401, 'message': 'token已過期'}, 401
        else:
            return {'code': 401, 'message': '無附帶token'}, 401

# 使用者列表
@user.route('/list', methods=['GET'])
def user_list():
    if request.method == 'GET':
            return_me = get_user_list_f()
            return return_me

# 使用者兌換獎品(user提供住址)
@user.route('/prize/redeem', methods=['POST'])
def user_prize_redeem():
    if request.method == 'POST':
        body_json = request.get_json()
        if 'prize_id' in body_json.keys() and 'address' in body_json.keys() and 'en_name' in body_json.keys() and 'Authorize' in request.headers:
            token = request.headers.get('Authorize')
            user_id = decode_token(token)['user_id']

            prize_id = body_json['prize_id']
            address = body_json['address']
            en_name = body_json['en_name']

            return_me = user_prize_redeem_f(en_name, prize_id, user_id, address)
            return return_me
        else:
            error = {'code': 400,
                     'message': '請確認body或Token',
                     }
            return error, 400

# 使用者編輯個人資訊
@user.route('/update/info', methods=['PUT'])
def user_update_info():
    if request.method == 'PUT':
        body_json = request.get_json()
        if 'name' in body_json.keys() and 'phone' in body_json.keys() and 'address' in body_json.keys() and 'Authorize' in request.headers:
            token = request.headers.get('Authorize')
            user_id = decode_token(token)['user_id']

            name = body_json['name']
            phone = body_json['phone']
            address = body_json['address']
        
            return_me = update_user_info_f(user_id, name, phone, address)
            return return_me