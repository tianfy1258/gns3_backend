
# 解析config.ini参数
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
host = config.get("gns3", "host")
port = config.get("gns3", "port")

