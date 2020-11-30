db = {
    'user': 'root',
    'password': 'root',
    'host': 'python-backend-test.chnlkkw3qbhy.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'miniter'
}

test_db = db

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@" \
         f"{db['host']}:{db['port']}/{db['database']}?charset=utf8"

test_config = {'DB_URL': DB_URL}

JWT_SECRET_KEY = 'secrete'
