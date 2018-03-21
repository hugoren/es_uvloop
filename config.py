import os

env = os.getenv('ENV')

if env == 'test':
    HOST = '0.0.0.0'
    PORT = 5454
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'
    REDIS_HOST = "192.168.6.23"
    REDIS_PORT = 6379
    REDIS_DB = 3
    ES_HOST = "192.168.6.23"
    ES_PORT = 9200


elif env == 'prod':
    HOST = '192.168.0.103'
    PORT = 9200
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'

else:
    HOST = '0.0.0.0'
    PORT = 5454
    TOKEN = 'b0350c8c75ddcd99738df4c9346bec48dc9c4914'
    REDIS_HOST = "192.168.6.23"
    REDIS_PORT = 6379
    REDIS_DB = 3
    ES_HOST = "192.168.6.23"
    ES_PORT = 9200

