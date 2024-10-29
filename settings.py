def initLoadEnv():
    # settings.py

    from dotenv import load_dotenv

    # 一、自动搜索 .env 文件
    load_dotenv(verbose=True)
