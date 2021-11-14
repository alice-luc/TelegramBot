import os
import base64

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
# IP = env.str("ip")  # для айпи адреса хоста

LEGO_CAPTION = 'Топовая модель "Анти-лего". Моментально распознает детальки лего под ногой и превращает \
подошву в недеформируемый панцирь'
TERM_CAPTION = 'Эти красавчики автоматически включают подогрев при температуре ниже 20 и охлаждение \
при температуре выше 35'
LEGO_PIC = 'AgACAgIAAxkBAAMnYY_ICB3koC8bh_r9kAnXygX2P4gAAta1MRts13hIwsi5Uxbo0IsBAAMCAANzAAMiBA'
TERM_PIC = 'AgACAgIAAxkBAAMpYY_IEaylWKJPcFYsqcValML6ktwAAte1MRts13hIemmlIGe_CrABAAMCAANzAAMiBA'


def secure_rand(length=8):
    token = os.urandom(length)
    return base64.b64encode(token)

