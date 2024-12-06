import sqlite3
from queue import Queue
from threading import Lock


class ConnectionPool:
    _instance = None
    _lock = Lock()
    _initialized = False

    @classmethod
    # def initialize(cls, db_name='../database.db', pool_size=20):
    def initialize(cls, db_name='./data/database.db', pool_size=20):
        if not cls._initialized:
            with cls._lock:
                if not cls._initialized:
                    cls._instance = cls.__new__(cls)
                    cls._instance.pool = Queue(maxsize=pool_size)
                    for _ in range(pool_size):
                        conn = sqlite3.connect(db_name, check_same_thread=False)
                        cls._instance.pool.put(conn)
                    cls._initialized = True
        return cls._instance

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        if not cls._initialized:
            raise RuntimeError("ConnectionPool not initialized. Call initialize() first.")
        return cls._instance.pool.get()

    @classmethod
    def return_connection(cls, conn):
        if not cls._initialized:
            raise RuntimeError("ConnectionPool not initialized. Call initialize() first.")
        cls._instance.pool.put(conn)

    @classmethod
    def close_pool(cls):
        if cls._initialized:
            while not cls._instance.pool.empty():
                conn = cls._instance.pool.get()
                conn.close()
            cls._initialized = False
            cls._instance = None

    def __init__(self):
        raise RuntimeError("Use ConnectionPool.initialize() to create an instance.")

    @classmethod
    def get_size(cls):
        print(cls._instance.pool.qsize())


# 初始化连接池
connection_pool_one = ConnectionPool.initialize()

