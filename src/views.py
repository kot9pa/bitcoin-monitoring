from datetime import datetime
from json import JSONDecodeError
from aiohttp import web

from models import Price


class Handler:
    # For text in error
    test_price = Price(
        title = "BTCUSDT or ETH,SOL,XMR,DOGE",
        price = 10000.0,
        min_price = 9000.0,
        max_price = 11000.0,
        date = datetime(2024, 9, 16),
        difference = 0.0,
        total_amount = 0.0
    )

    async def get_price(self, request: web.Request):
        price_id = request.match_info.get('price_id')
        price = await Price.get_or_none(id=int(price_id))
        return web.json_response({"price": str(price)})

    async def get_price_all(self, request: web.Request):
        prices = await Price.all()
        return web.json_response({"prices": [str(price) for price in prices]})

    async def add_price(self, request: web.Request):
        try:
            data = await request.json()
            price = Price(
                title = data['title'],
                price = data['price'],
                min_price = data['min_price'],
                max_price = data['max_price'],
                date = datetime.now(),
                difference = data['difference'],
                total_amount = data['total_amount'],
            )
        except (JSONDecodeError, KeyError) as err:
            raise web.HTTPInternalServerError(reason=err, 
                                              text=f"See test price:\n{str(self.test_price)}")
        
        await price.save()
        return web.json_response({"price": str(price)})
    
    async def update_price(self, request: web.Request):
        price_id = request.match_info.get('price_id')
        price = await Price.get_or_none(id=int(price_id))
        if not price:
            raise web.HTTPNotFound()
        try:
            data = await request.json()
            price_new = price.update_from_dict(data)
            await price_new.save()
        except JSONDecodeError as err:
            raise web.HTTPInternalServerError(reason=err, 
                                              text=f"See test price:\n{str(self.test_price)}")
        return web.json_response({"price": str(price)})
    
    async def delete_price(self, request: web.Request):
        price_id = request.match_info.get('price_id')
        price = await Price.get_or_none(id=int(price_id))
        if not price:
            raise web.HTTPNotFound()
        await price.delete()
        return web.HTTPOk()

    async def delete_price_all(self, request: web.Request):
        prices = await Price.all()
        if not prices:
            raise web.HTTPNotFound()
        [await price.delete() for price in prices]
        return web.HTTPOk()
