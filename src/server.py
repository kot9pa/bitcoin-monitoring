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
            web.get("/", handler.get_price_all), 
            web.get("/{price_id}", handler.get_price), 
            web.post("/price", handler.add_price),
            web.patch("/{price_id}", handler.update_price),
            web.delete("/", handler.delete_price_all),
            web.delete("/{price_id}", handler.delete_price),
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
