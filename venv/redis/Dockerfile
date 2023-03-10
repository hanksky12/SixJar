# 使用官方 Redis 映像檔作為基礎映像檔
FROM redis

# 複製自己的 redis.conf 檔案到映像檔中的 /usr/local/etc/redis/ 目錄下
COPY redis.conf /usr/local/etc/redis/redis.conf



# 指定 Redis 啟動時使用的設定檔
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
LABEL image_name="sixjar-redis"
LABEL version="1.0"