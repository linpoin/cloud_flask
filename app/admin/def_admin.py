from ..Module import *
from ..db_setting import *

# 管理員登入
def admin_login_f(account, password):
    bcrypt = Bcrypt()
    select_account_q = f"select * from shopping_area.admin_member where account = '{account}'"
    have_account = mysql_engine.execute(select_account_q).fetchone()
    if have_account != None:
        sql_account = have_account['account']
        sql_password = have_account['password']
        sql_control = have_account['control']

        if bcrypt.check_password_hash(sql_password, str(password)):
            token = admin_make_token(sql_account, sql_control)
            save_token_q = f"UPDATE shopping_area.admin_member SET token = '{token}'  WHERE account = '{sql_account}'"
            mysql_engine.execute(save_token_q)
            return {'code': 200, 'account': sql_account, 'token': token, 'control': sql_control, 'message': '登入成功'}, 200
        else:
            return {'code': 401, 'message': '密碼錯誤'}, 401
    else:
        return {'code': 401, 'message': '無此管理者帳號'}, 401

# 當前管理者資訊
def current_admin_info_f(account, control):
    return {'code': 200, 'account': account, 'control': control}, 200

# 使用者兌獎
def user_redeem_f(en_name, name, user_id, repeat_pass, level_num):
    select_lottery_user_q = f"select user_id from shoparea_{en_name}.lottery_user where user_id = '{user_id}'"
    select_lottery_user = mysql_engine.execute(
        select_lottery_user_q).fetchone()
    if select_lottery_user == None or repeat_pass == 1:
        if repeat_pass == 1:
            level_num = 0
            level_up_q = f"UPDATE user.run_level_number SET {en_name}_num = '{0}'  WHERE user_id = '{user_id}'"
            mysql_engine.execute(level_up_q)

        while(True):
            # 產生英數10位隨機數
            lottery_id = ''.join(random.choice(
                string.ascii_letters + string.digits) for _ in range(8))

            select_lottery_id_q = f"select lottery_id from shoparea_{en_name}.lottery_user where lottery_id = '{lottery_id}'"
            select_lottery_id = mysql_engine.execute(
                select_lottery_id_q).fetchone()
            if select_lottery_id == None:
                update_lottery = f"INSERT INTO shoparea_{en_name}.lottery_user (user_name, user_id, lottery_id) VALUES ('{name}','{user_id}','{lottery_id}')"
                mysql_engine.execute(update_lottery)
                return {'code': 200, 'name': name, 'user_id': user_id, 'level_num': level_num}, 200
    else:
        return {'code': 403, 'message': '此用戶已兌換過抽獎資格'}, 403

# 已兌換列表
def user_redeem_list_f(en_name):
    select_lottery_q = f"select lottery_id,user_name,user_id from shoparea_{en_name}.lottery_user"
    select_lottery_list = mysql_engine.execute(select_lottery_q)
    return jsonify(execute_to_list(select_lottery_list))
    
# 刪除商圈
def remove_shoparea_f(en_name):
    try:
        mysql_engine.execute(
            f"drop database shoparea_{en_name}"
        )
        mysql_engine.execute(
            f"DELETE FROM shopping_area.admin_member WHERE account = '{en_name}'"
        )
        mysql_engine.execute(
            f"DELETE FROM shopping_area.shopping_area_infor WHERE shopping_area_eg_name = '{en_name}'"
        )
        mysql_engine.execute(
            f"ALTER TABLE user.run_level_number DROP COLUMN {en_name}_num"
        )
        return {'code':200, 'message':f'完成，已刪除{en_name}商圈'},200
    except:
        return {'code':400, 'message':f'錯誤，未完成刪除{en_name}商圈'},400

# 刪除商圈
def remove_shop_f(en_name, shop_id):
    try:
        mysql_engine.execute(
            f"DELETE FROM shoparea_{en_name}.shop WHERE shop_id = '{shop_id}'"
        )
        return {'code':200, 'message':f'完成，已刪除商店'},200
    except:
        return {'code':400, 'message':f'錯誤，未完成刪除商店'},400