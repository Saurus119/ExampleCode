import json

from typing import Union
from redis import Redis

from Shared.Cache.i_cache import IRedis

class RedisCache(IRedis):
    """Example class how we can implement own methods if we want to for caching based on INTERFACE.
       Demonstrate knowledge of the Interface/ABC in the python. For MVP classic Redis lib is used.
    """

    def __init__(self):
        self.client = Redis(host="redis", port=6379) 

    def get(self, key: str) -> Union[str, list, dict, int]:
        if data := self.client.get(key):
            data = data.decode("utf-8")

        try:
            return json.loads(data)
        except Exception:
            return data

    def update_or_create(self, key: str, value: Union[str, list, dict, int]) -> None:
        self.client.set(key, value)

    def delete(self, key: str) -> None:
        self.client.delete(key)
