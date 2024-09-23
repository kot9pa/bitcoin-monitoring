from datetime import datetime
from json import JSONDecodeError
from aiohttp import web

from models import Price


class Handler:
    # For text in error
    test_price = Price(
        title = "BTCUSDT",
        price = 10000.0,
        min_price = 9000.0,
        max_price = 11000.0,
        date = "2024-09-23T18:34:15.185609+00:00",
        difference = 0.0,
        total_amount = 0.0
    )
    
    async def get_prices(self, request: web.Request):
        id = request.query.get('id')
        title = request.query.get('title')
        filters = {}
        try:
            if id:
                filters['id'] = int(id)
            if title:
                filters['title__icontains'] = title
            if filters:
                prices = await Price.filter(**filters)
            else:
                prices = await Price.all()
            return web.json_response({"prices": [str(price) for price in prices]})
        except ValueError as err:
            raise web.HTTPInternalServerError(reason=err)

    async def add_price(self, request: web.Request):
        try:
            data = await request.json()
            price = Price(
                title = data['title'],
                price = data['price'],
                min_price = data['min_price'],
                max_price = data['max_price'],
                date = datetime.fromisoformat(data['date']),
                difference = data['difference'],
                total_amount = data['total_amount'],
            )
        except (JSONDecodeError, KeyError) as err:
            raise web.HTTPInternalServerError(reason=err, 
                                              text=f"See test price:\n{str(self.test_price)}")
        
        await price.save()
        return web.json_response({"price": str(price)})
    
    async def update_price(self, request: web.Request):
        price_id = request.query.get('id')
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
    
    async def delete_prices(self, request: web.Request):
        price_id = request.query.get('id')
        try:
            if price_id:
                price = await Price.get_or_none(id=int(price_id))
                if not price:
                    raise web.HTTPNotFound()
                await price.delete()
            else:
                prices = await Price.all()
                [await price.delete() for price in prices]
            return web.HTTPOk()
        except ValueError as err:
            raise web.HTTPInternalServerError(reason=err)
