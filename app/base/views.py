# import sys
# sys.path.append("..")
from ..Module import *

from flask import request
from flask import Blueprint
from .def_base import *
import io

base = Blueprint('base', __name__)


@base.route('/')
def index():
    return 'base.hello'

# 解析圖片
@base.route("/image_parse", methods=["GET", "POST"])
def image_parse():
    if request.method == 'POST':
        img = request.files['file'].read()
        encoded = base64.b64encode(img).decode('utf-8')
        img_type = str(request.files['file'].mimetype)
        encoded = f'data:{img_type};base64,{encoded}'
    return encoded  # 解析圖片

# 讀取csv檔
@base.route("/csv", methods=["GET", "POST"])
def read_csv():
    if request.method == 'POST':
        csv = request.files['file'].read()
        df = pd.read_excel(csv)
        df.columns = ['id', 'shopName', 'shopAddress',
                      'shopPhone', 'lineUrl', 'shopText']
        df = df.astype(str)
        response = str(df.to_dict(orient='records'))
        response = response.replace("'", '"')
    return response
