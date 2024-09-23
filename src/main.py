import asyncio
from datetime import datetime
from itertools import chain, groupby
import math
import threading
from typing import List


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tortoise import Tortoise, run_async

from client import Binance, Kucoin, Bybit, Gateio, Coinmarketcap, Exchange
from models import Price
from config import config


TOTAL_BTC = 3.0
SCHEDULER_INTERVAL = 5.0
results_to_db = []

async def init():
    # Here we create a PostgresDB connection using config file
    await Tortoise.init(config=config)

async def save_data(price_items: List[Price]):
    # Saving data to DB
    print('Saving data to DB..')
    print(*price_items)
    for price in price_items:
        await price.save()

async def prepare_data(results):
    # Filter by percent change and group by coin
    print('Filter by percent_change and group by coin..')
    results_to_db.clear()
    result_filter = filter(lambda item: 
                            math.isclose(item["percent_change"], 0.03) or \
                            item["percent_change"] > 0.03, 
                            chain(*results)
                            )
    result_groupby = groupby(sorted(result_filter, 
                                    key=lambda x:x['coin']), 
                                    key=lambda x:x['coin'])
    for coin, coin_data in result_groupby:
        data_list = list(coin_data)
        data_price = [data['price'] for data in data_list]
        min_price, max_price = min(data_price), max(data_price)
        price = [Price(
            title = coin, 
            price = data['price'], 
            max_price = max_price, 
            min_price = min_price, 
            date = datetime.now(), 
            difference = (data['price'] - max_price)*TOTAL_BTC, 
            total_amount = data['price']*TOTAL_BTC,
        ) for data in data_list]
        results_to_db.extend(price)
    return results_to_db

async def run_save_data():
    while True:
        # get a unit of work without blocking
        try:
            print("Get item.. QSize:", queue.qsize())
            items = queue.get_nowait()            
            if items:
                items_to_prepare = await asyncio.create_task(prepare_data(items))                
                items_to_save = asyncio.create_task(save_data(items_to_prepare))
                await items_to_save
                if items_to_save.done():
                    print('Saved to DB complete!')
        except asyncio.QueueEmpty:
            print("No item, wait..")
            await asyncio.sleep(10)
            continue

async def fetch_data(*args):
    print('Fetching data..')
    results = await asyncio.gather(*[arg.run() for arg in args])
    #print(results)
    await queue.put(results)

async def run_fetch_data():
    async with (
        Coinmarketcap() as coinmarketcap,
        Binance() as binance,
        Gateio() as gateio,
        Kucoin() as kucoin,
        Bybit() as bybit,
    ):
        print(f'Start requests with interval {SCHEDULER_INTERVAL} seconds..')
        scheduler.add_job(fetch_data, 
                          'interval', 
                          args=(coinmarketcap, binance, gateio, kucoin, bybit),
                          seconds=SCHEDULER_INTERVAL,                          
        )
        scheduler.start()
        while True:
            await asyncio.sleep(1000)

if __name__ == '__main__':
    #TODO Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    #TODO Sendmail
    try:
        # create the shared queue
        queue = asyncio.Queue()
        # define the scheduler
        scheduler = AsyncIOScheduler()
        # init DB
        run_async(init())
        # create and start the thread
        thread = threading.Thread(target=asyncio.run, args=(run_save_data(),))
        thread.start()
        # create new event loop
        asyncio.run(run_fetch_data())
        #thread.join()
    except (KeyboardInterrupt, SystemExit):
        pass
