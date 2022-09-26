from sqlalchemy import create_engine
import urllib

#資料庫設定
sql_user = 'root'
sql_ip = 'localhost'
sql_password = urllib.parse.quote_plus('qazWSX!@#52643567')
#sql_password = ''

mysql_engine = create_engine(f"mysql+pymysql://{sql_user}:{sql_password}@{sql_ip}:3306")
shopping_engine = create_engine(f"mysql+pymysql://{sql_user}:{sql_password}@{sql_ip}:3306/shopping_area")