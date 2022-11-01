import redis

import config

redis_client = redis.Redis(
    host=config.RedisConfig.HOST,
    port=config.RedisConfig.PORT,
)  # global instance
