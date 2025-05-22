from bot_core import client
from config import bot_token
import db

# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    db.init_db()


    client.run(bot_token)
