#coding = utf-8
import requests
import random

KEY = random.choice(['40d56dcf5e1d4edc8a891eb824a11437','ec3cff2c300048a2b11ed63c0180b3cd','8edce3ce905a4c1dbb965e6b35c3834d','294d52df9b184448a933b535475d2dbd'])

def get_response(msg):
  apiUrl = 'http://www.tuling123.com/openapi/api'
  data = {
    'key'  : KEY,
    'info'  : msg,
    'userid' : 'pth-robot',
  }
  try:
    r = requests.post(apiUrl, data=data).json()
    return '嘿嘿嘿~' if "请求次数" in r.get('text') else r.get('text')
  except:
    return "嘻嘻嘻~"

