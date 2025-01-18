import uvicorn

if __name__ == '__main__':
    uvicorn.run("src.server.main:app", host="0.0.0.0", port=5000, log_level="info", reload=True,
                ssl_keyfile='./https/key.pem', ssl_certfile='./https/cert.pem')
