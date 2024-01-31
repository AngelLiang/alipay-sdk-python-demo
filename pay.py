from dotenv import load_dotenv
import sys
import os
import logging
import traceback
from uuid import uuid4

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.FileItem import FileItem
from alipay.aop.api.domain.AlipayTradeAppPayModel import AlipayTradeAppPayModel
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.domain.GoodsDetail import GoodsDetail
from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
from alipay.aop.api.domain.SettleInfo import SettleInfo
from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayOfflineMaterialImageUploadRequest import AlipayOfflineMaterialImageUploadRequest
from alipay.aop.api.request.AlipayTradeAppPayRequest import AlipayTradeAppPayRequest
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayOfflineMaterialImageUploadResponse import AlipayOfflineMaterialImageUploadResponse
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')

sys.path.append(os.getcwd())

load_dotenv()

ALIPAY_SERVER_URL = os.getenv('ALIPAY_SERVER_URL')
ALIPAY_APPID = os.getenv('ALIPAY_APPID')
ALIPAY_APP_PRIVATE_KEY = os.getenv('ALIPAY_APP_PRIVATE_KEY')
ALIPAY_PUBLIC_KEY = os.getenv('ALIPAY_PUBLIC_KEY')
BUYER_UID = os.getenv('BUYER_UID')

alipay_client_config = AlipayClientConfig()
alipay_client_config.server_url = ALIPAY_SERVER_URL
alipay_client_config.app_id = ALIPAY_APPID
alipay_client_config.app_private_key = ALIPAY_APP_PRIVATE_KEY
alipay_client_config.alipay_public_key = ALIPAY_PUBLIC_KEY


"""
得到客户端对象。
注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
logger参数用于打印日志，不传则不打印，建议传递。
"""
client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)


def test_pay():
    """
    pytest pay.py -s

    系统接口示例：alipay.trade.pay
    """
    out_trade_no = uuid4().hex
    subject = "大乐透"
    total_amount = 9.00

    # 对照接口文档，构造请求对象
    model = AlipayTradePayModel()

    # 必填。买家用户支付宝的UID
    model.auth_code = BUYER_UID
    # 必填。商户网站唯一订单号。
    model.out_trade_no = out_trade_no
    # 必填。订单标题。
    model.subject = subject
    # 必填。订单总金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000]，金额不能为0
    model.total_amount = total_amount

    request = AlipayTradePayRequest(biz_model=model)
    # 如果有auth_token、app_auth_token等其他公共参数，放在udf_params中
    # udf_params = dict()
    # from alipay.aop.api.constant.ParamConstants import *
    # udf_params[P_APP_AUTH_TOKEN] = "xxxxxxx"
    # request.udf_params = udf_params
    # 执行请求，执行过程中如果发生异常，会抛出，请打印异常栈
    response_content = None
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc())

    if not response_content:
        print("failed execute")
    else:
        response = AlipayTradePayResponse()
        # 解析响应结果
        response.parse_response_content(response_content)
        # 10003表示等待用户支付的状态
        # 输出示例：
        # {"code":"10003","msg":" order success pay inprocess","buyer_logon_id":"djg***@sandbox.com","buyer_pay_amount":"0.00","buyer_user_id":"2088722029208721","buyer_user_type":"PRIVATE","invoice_amount":"0.00","out_trade_no":"286963ee406143e09fa0331ba3f860aa","point_amount":"0.00","receipt_amount":"0.00","total_amount":"9.00","trade_no":"2024013122001408720502004161"}
        print(response.body)
        if response.is_success():
            # 如果业务成功，则通过respnse属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        else:
            # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
