import redis

rd=redis.Redis(host='127.0.0.1', port=6379, db=0, password='=q82630257204q')


def save_dynamic(dynamic_id):
	rd.lpush("already_dynamic_id", dynamic_id)


def save_official_lucky(official_lucky):
	rd.lpush("official_lucky_uid_dynamic", official_lucky)


def get_dynamic():
	res=rd.lrange("already_dynamic_id", 0, -1)
	return list(map(lambda x:str(x,encoding='utf-8'),res))

# print(get_dynamic())

if __name__ == '__main__':
	print(get_dynamic())