from sqlalchemy import create_engine

DB_HOST = "34.73.98.63"      # 你的 MySQL VM 的 external IP
DB_USER = "admin"
DB_PASSWORD = "12345abc"
DB_NAME = "lionswap"         # 如果不是这个请告诉我
DB_PORT = "3306"

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def get_connection():
    return engine.connect()
