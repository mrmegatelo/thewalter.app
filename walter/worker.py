from uvicorn_worker import UvicornWorker


class WalterWorker(UvicornWorker):
    CONFIG_KWARGS = { "lifespan": "off" }