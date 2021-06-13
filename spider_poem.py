#coding=utf-8
import requests as rq

header={
	'connection':'keep-alive',
	'user-agent':'mozilla/5.0 (windowS NT 10.0; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/88.0.4324.190 safari/537.36',
}

def get_poem():
	res=rq.get("https://v2.jinrishici.com/one.json?client=browser-sdk/1.2&X-User-Token=ICXSMWftVJsuJ3hV78j5CCpTNg7NkA%2BK",headers=header)
	res.encoding="utf-8"
	return res.json()['data']['content']

# print(get_poem())

