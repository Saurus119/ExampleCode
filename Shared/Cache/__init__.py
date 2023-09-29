from redis import Redis

redis_cache = Redis(host="redis", port=6379) 
# local redis 
# redis_cache = Redis(host="127.0.0.1", port=6379)