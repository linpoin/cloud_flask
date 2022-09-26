from flask import request
from flask import Blueprint
from .def_admin import *

admin = Blueprint('admin', __name__)


@admin.route('/')
def index():
    return 'admin.hello'

# 管理者登入
@admin.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        body_json = request.get_json()
        if body_json == None:
            return {'code': 401, 'message': '無附帶body'}
        if 'account' in body_json.keys() and 'password' in body_json.keys():
            account = body_json['account']
            password = body_json['password']
            return_me = admin_login_f(account, password)
            return return_me
        else:
            error = {'code': 401,
                     'message': '請確認帳號、密碼',
                     }
            return error, 401

# 當前管理者資訊
@admin.route('/current_info', methods=['GET'])
def admin_current_info():
    if request.method == 'GET':
        token = request.headers.get('Authorize')
        if token == None:
            return {'code': 401, 'message': '無附帶token'}, 401
        else:
            try:
                token_data = decode_token(token)
                account = token_data['account']
                control = token_data['control']
                select_admin_token_q = f"select token from shopping_area.admin_member where account = '{account}'"
                sql_admin_token = mysql_engine.execute(select_admin_token_q).fetchone()['token']
                print(sql_admin_token)
                if sql_admin_token == token:
                    return_me = current_admin_info_f(account, control)
                    return return_me
                else:
                    return {'code': 401, 'message': 'token已失效'}, 401
            except:
                return {'code': 401, 'message': 'token已過期'}, 401

# admin登出
@admin.route('/signout', methods=['GET'])
def admin_signout():
    if request.method == 'GET':
        token = request.headers.get('Authorize')
        if token == None:
            return {'code': 401, 'message': '無附帶token'}
        else:
            try:
                token_data = decode_token(token)
                account = token_data['account']
                select_admin_token_q = f"select token from shopping_area.admin_member where account = '{account}'"
                sql_admin_token = mysql_engine.execute(select_admin_token_q).fetchone()['token']
                if sql_admin_token == token:
                    signout_admin_q = f"UPDATE shopping_area.admin_member SET token = '{None}'  WHERE account = '{account}'"
                    mysql_engine.execute(signout_admin_q)
                    return {'code': 200, 'message': f'{account}已登出'}, 200
                else:
                    return {'code': 401, 'message': 'token已失效'}, 401
            except:
                return {'code': 401, 'message': 'token已過期'}, 401

# 管理者掃描兌獎
@admin.route('/<en_name>/redeem', methods=['POST'])
def admin_redeem(en_name):
    if request.method == 'POST':
        body_json = request.get_json()
        if body_json == None:
            return {'code': 401, 'message': '無附帶body'}
        if 'user_id' in body_json.keys():
            user_id = body_json['user_id']

            # 取得user_name
            select_user_id_q = f"select * from user.users where user_id = '{user_id}'"
            have_user_id = mysql_engine.execute(select_user_id_q).fetchone()
            name = have_user_id['name']

            # 取得level_num
            select_level_num_q = f"select {en_name}_num from user.run_level_number where user_id = '{user_id}'"
            level_num = mysql_engine.execute(select_level_num_q).fetchone()
            if level_num == None:
                return {'code': 402, 'message': '無此user_id'}, 402
            level_num = int(level_num[f'{en_name}_num'])

            # 取得通關數及抽獎方式
            select_lottery_level_num_q = f"select repeat_pass,lottery_method,lottery_level_num from shopping_area.shopping_area_infor where shopping_area_eg_name = '{en_name}'"
            lottery_level_num = mysql_engine.execute(
                select_lottery_level_num_q).fetchone()
            repeat_pass = lottery_level_num['repeat_pass']
            lottery_level_num = lottery_level_num['lottery_level_num']

            if level_num >= int(lottery_level_num):
                return_me = user_redeem_f(
                    en_name, name, user_id, repeat_pass, level_num)
                return return_me
            else:
                return {'code': 202, 'message': f'闖關未達{lottery_level_num}關'}, 202
        else:
            return {'code': 400, 'message': '請輸入user_id'}, 400

# 管理者已兌換列表
@admin.route('/<en_name>/redeem_list', methods=['GET'])
def admin_redeem_list(en_name):
    if request.method == 'GET':
        return_me = user_redeem_list_f(en_name)
        return return_me

# 刪除商圈
@admin.route('/delete/shop_area/<en_name>', methods=['DELETE'])
def admin_delete_shoparea(en_name):
    if request.method == 'DELETE':
        return_me = remove_shoparea_f(en_name)
        return return_me

# 刪除商店
@admin.route('/delete/shop/<en_name>/<shop_id>', methods=['DELETE'])
def admin_delete_shop(en_name, shop_id):
    if request.method == 'DELETE':
        return_me = remove_shop_f(en_name, shop_id)
        return return_me
