#coding=utf-8
import requests as rq
import random,time,dynamic_redis
import json
from time import strftime, localtime
#628290540 #
mids=[382447165]	# 受害用户的ID（获取抽奖动态）
csrf='4e3b91ae62ff1d5aba40e9f955521f4b'
key_list=['抽','奖','送']
header={
	'content-type':'application/x-www-form-urlencoded',
	'cookie':"_uuid=30B8CE79-49BF-F3AD-03DA-178807A753D060817infoc; buvid3=145A68BF-BABD-4BD8-925B-9A546BA1486034772infoc; bfe_id=6f285c892d9d3c1f8f020adad8bed553; fingerprint=2c6eecf15a9f51ad1b944aef5cd44e08; buvid_fp=145A68BF-BABD-4BD8-925B-9A546BA1486034772infoc; buvid_fp_plain=145A68BF-BABD-4BD8-925B-9A546BA1486034772infoc; SESSDATA=784e4c2a%2C1639149385%2C53363%2A61; bili_jct=4e3b91ae62ff1d5aba40e9f955521f4b; DedeUserID=1090970340; DedeUserID__ckMd5=aae500216002dd45; sid=7ehp06q6; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|u)kYuJ~)0J'uYkJlm~lJk",
	'origin':'https://t.bilibili.com',
	'pragma':'no-cache',
	'referer':'https://t.bilibili.com/',
	'user-agent':'mozilla/5.0 (windowS NT 6.1; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/88.0.4324.190 safari/537.36'
}

data_follow={
	'act':'1',
	'fid':'457235238',
	'spmid':'333.169',
	're_src':'0',
	'csrf_token':csrf,
	'csrf':csrf
}


data_repost={
	'uid':'1090970340',
	'dynamic_id':'',
	'content':'我觉得会是我~！',
	'extension':'{"emoji_type":1}',
	'at_uids':'',
	'ctrl':'[]',
	'csrf_token':csrf,
	'csrf':csrf
}

data_comment={
	'oid':'116883742',
	'type':'11',
	'message':'冲一波~',
	'plat':'1',
	'ordering':'heat',
	'jsonp':'jsonp',
	'csrf':csrf
}

data_thumbsUp={
	'uid':'1090970340',
	'dynamic_id':'',
	'up':'1',
	'csrf_token':csrf,
	'csrf':csrf,
}

data_rm_dynamic={
	"dynamic_id": "",
	"csrf_token": csrf,
	"csrf": csrf
}

# 用户信息
u_info="https://api.bilibili.com/x/space/acc/info?mid="

# 受害者用户的抽奖动态url
u_dy_get_url=lambda x:f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={x}&need_top=1&platform=web"

def spider_post(url,data1):
	# asyncio.sleep(3)
	res=rq.post(url,headers=header,data=data1)
	html = res.json()
	return html


def spider_get(url):
	res=rq.get(url,headers=header).json()
	return res


def to_follow(uid):
	data_follow['fid']=uid
	res=spider_post("https://api.bilibili.com/x/relation/modify",data_follow)
	if res['code']==0:
		print("关注成功 ==== ",spider_get(u_info+uid)['data']['name'])
	# print(res)


def to_repost(dynamic_id):
	data_repost['dynamic_id']=dynamic_id
	# data_repost['content']=tuling.get_response(random.choice(['啦啦啦','嘻嘻嘻','嘿嘿嘿']))
	res=spider_post("https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost",data_repost)
	if res['code']==0:
		print("转发成功")


def to_comment(oid):
	# 需要获取动态的oid，才能发送评论
	# get_oid_url="https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id="+dynamic_id
	# oid=spider_get(get_oid_url)['data']['card']['desc']['rid']
	data_comment.update({"oid":oid})
	res=spider_post("https://api.bilibili.com/x/v2/reply/add",data_comment)
	print("评论"+res['data']['success_toast'])


def to_rm_dynamic(dynamic_id):
	# 删除动态
	data_rm_dynamic['dynamic_id']=dynamic_id
	res=spider_post("https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic",data_rm_dynamic)
	print(dynamic_id+"动态=删除成功=" if res['code']==0 else res)

	# 点赞动态
def to_thumbsUp(dynamic_id):
	data_thumbsUp['dynamic_id']=dynamic_id
	res=spider_post("https://api.vc.bilibili.com/dynamic_like/v1/dynamic_like/thumb",data_thumbsUp)
	print(dynamic_id+"动态-点赞成功-" if res['code']==0 else res)


def to_get_all_dynamic(url):
	return spider_get(url)['data']['cards']


def check_dynamic_id():
	# 获取所有已经发送过的存在的动态id
	return dynamic_redis.get_dynamic()


def main_follow_and_post(uid='',dynamic_id='',oid=""):
	time.sleep(5)
	if uid:
		to_follow(uid)
		time.sleep(0.5)
	if dynamic_id and oid:
		dynamic_redis.save_dynamic(dynamic_id)
		to_thumbsUp(dynamic_id)
		time.sleep(3)
		to_comment(oid)
		time.sleep(0.5)
		to_repost(dynamic_id)


def main(mid):
	res=to_get_all_dynamic(u_dy_get_url(mid))
	already_dynamic_id=check_dynamic_id()
	for i in res:
		try:
		# poem=reply.get_sentence()
			per_dynamic=i['desc']['origin']
			card=json.loads(i['card'])
			poem=card['item']['content'].split('//')[0]
			# 动态条件过滤
			if per_dynamic['dynamic_id_str'] in already_dynamic_id: # 匹配已发动态ID
				print(f"\n{per_dynamic['dynamic_id_str']}----已经存在~~~")
				continue
			if "description" not in card['origin']:	
				print(f"\nUP:{card['origin_user']['info']['uname']}---转发内容：{poem}---不是动态")
				continue
			if not any(key in card['origin'] for key in key_list): # 抽奖关键词匹配
				print(f"\n{per_dynamic['dynamic_id_str']}---转发内容：{poem}---不是抽奖动态")
				continue
			# 动态条件过滤
			data_repost['content']=poem
			data_comment['message']=poem
			print("="*30)
			main_follow_and_post(str(per_dynamic['uid']),per_dynamic['dynamic_id_str'],per_dynamic['rid_str'])
			already_dynamic_id.append(per_dynamic['dynamic_id_str'])
			print("="*30)
			
		except Exception as e:
			print("\n出现错误："+str(e))


if __name__ == '__main__':
	print("\n\n"+"*"*30+strftime("%Y-%m-%d %H:%M:%S", localtime())+"*"*30)
	while mids:
		main(mids.pop())
	print("\n"+"*"*30+strftime("%Y-%m-%d %H:%M:%S", localtime())+"*"*30)
