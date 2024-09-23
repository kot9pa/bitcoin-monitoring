import logging
from aiohttp import web
from tortoise.contrib.aiohttp import register_tortoise

from views import Handler
from config import WEB_PORT, config

logging.basicConfig(level=logging.DEBUG)


def start_server():
    app = web.Application()    
    handler = Handler()
    app.add_routes(
        [
            web.get("/get", handler.get_prices),
            web.post("/add", handler.add_price),
            web.patch("/update", handler.update_price),
            web.delete("/delete", handler.delete_prices),
        ]
    )
    register_tortoise(
        app, 
        config=config, 
        generate_schemas=True
    )
    #TODO Clear DB on shutdown
    #app.on_shutdown.append(on_shutdown)
    web.run_app(app, port=int(WEB_PORT))

# CLI run
if __name__ == "__main__":
    start_server()
