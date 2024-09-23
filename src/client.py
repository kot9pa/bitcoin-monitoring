import asyncio
import json
import aiohttp

#TODO Exchange class for cross-converting (ie BTH/ETH)
class Exchange:
    _data_convert = dict()
    _base_url = 'https://pro-api.coinmarketcap.com/'
    _api_url = '/v2/cryptocurrency/quotes/latest'
    _coins_map = {
        'USD': '2781',
        'RUB': '2806',
        'ETH': '1027',
        'XMR': '328',
        'SOL': '5426',
        'DOGE': '74',
    }

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(base_url=self._base_url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CMC_PRO_API_KEY': '86176bf2-03b6-48fa-bcf7-3a17546050c5',
        })
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self._session.closed:
            await self._session.__aexit__(*args, **kwargs)

    async def run(self):
        for coin in self._coins_map:
            data = await self._get_data(coin)
            price = self._get_price(data)
            self._data_convert.update({coin: price})
        print(self._data_convert)
        return self._data_convert
    
    async def _get_data(self, symbol):
        parameters = {
            'id':'1', #BTC
            'convert_id': self._coins_map[symbol]
        }
        async with self._session.get(
            url=self._api_url, 
            params=parameters, 
        ) as resp:
            data = await resp.json()        
        return data["data"]["1"]["quote"][self._coins_map[symbol]]
    
    def _get_price(self, data):
        return float(data["price"])

class Coinmarketcap:
    _data = list()
    _base_url = 'https://sandbox-api.coinmarketcap.com/'
    _api_url = '/v2/cryptocurrency/quotes/latest'
    _coins_map = {
        'BTC': '1',
        'ETH': '1027',
        'XMR': '328',
        'SOL': '5426',
        'DOGE': '74',
    }
 
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(base_url=self._base_url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CMC_PRO_API_KEY': '86176bf2-03b6-48fa-bcf7-3a17546050c5',
        })
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self._session.closed:
            await self._session.__aexit__(*args, **kwargs)
    
    async def run(self):
        self._data.clear()
        for coin in self._coins_map:
            data = await self._get_data(coin)
            percent_change = self._get_percent_change_24h(data)
            price = self._get_price(data)
            self._data.append({'coin': f"{coin}USDT", 
                               'percent_change': percent_change, 
                               'price': price})
        return self._data
    
    async def _get_data(self, symbol):
        parameters = {
            'id': self._coins_map[symbol],
        }
        async with self._session.get(
            url=self._api_url, 
            params=parameters, 
        ) as resp:
            data = await resp.json()        
        return data["data"][self._coins_map[symbol]]["quote"]["USD"]
    
    def _get_percent_change_24h(self, data):
        return float(data["percent_change_24h"])
    
    def _get_price(self, data):
        return float(data["price"])

class Bybit:
    _data = list()
    _base_url = 'https://api.bybit.com/'
    _api_url = '/v5/market/tickers'
    _symbols = ['BTCUSDT','ETHUSDT','SOLUSDT','DOGEUSDT']
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(base_url=self._base_url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self._session.closed:
            await self._session.__aexit__(*args, **kwargs)
    
    async def run(self):
        self._data.clear()
        for symbol in self._symbols:
            data = await self._get_data(symbol)
            percent_change = self._get_percent_change_24h(data)
            price = self._get_price(data)
            self._data.append({'coin': symbol, 
                               'percent_change': percent_change, 
                               'price': price})
        return self._data

    async def _get_data(self, symbol):
        parameters = {
            'category': 'spot',
            'symbol': symbol,
        }        
        async with self._session.get(
            url=self._api_url, 
            params=parameters,
        ) as resp:
            data = await resp.json()        
        return data["result"]["list"][0]
    
    def _get_percent_change_24h(self, data):
        return float(data["price24hPcnt"])
    
    def _get_price(self, data):
        return float(data["lastPrice"])

class Gateio:
    _data = list()
    _base_url = 'https://api.gateio.ws/'
    _api_url = '/api/v4/spot/tickers'
    _symbols = ['BTC_USDT','ETH_USDT','XMR_USDT','SOL_USDT','DOGE_USDT']
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(base_url=self._base_url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self._session.closed:
            await self._session.__aexit__(*args, **kwargs)
    
    async def run(self):
        self._data.clear()
        for symbol in self._symbols:
            data = await self._get_data(symbol)
            percent_change = self._get_percent_change_24h(data)
            price = self._get_price(data)
            self._data.append({'coin': symbol.replace("_",""), 
                    'percent_change': percent_change, 
                    'price': price})
        return self._data

    async def _get_data(self, symbol):
        parameters = {
            'currency_pair': symbol,
        }        
        async with self._session.get(
            url=self._api_url, 
            params=parameters,
        ) as resp:
            data = await resp.json()
        return data[0]
    
    def _get_percent_change_24h(self, data):
        return float(data["change_percentage"])
    
    def _get_price(self, data):
        return float(data["last"])

class Kucoin:
    _data = list()
    _base_url = 'https://api.kucoin.com/'
    _api_url = '/api/v1/market/stats'
    _symbols = ['BTC-USDT','ETH-USDT','XMR-USDT','SOL-USDT','DOGE-USDT']
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(base_url=self._base_url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self._session.closed:
            await self._session.__aexit__(*args, **kwargs)
    
    async def run(self):
        self._data.clear()
        for symbol in self._symbols:
            data = await self._get_data(symbol)            
            percent_change = self._get_percent_change_24h(data)
            price = self._get_price(data)
            self._data.append({'coin': symbol.replace("-",""), 
                    'percent_change': percent_change, 
                    'price': price})
        return self._data

    async def _get_data(self, symbol):
        parameters = {
            'symbol': symbol,
        }
        async with self._session.get(
            url=self._api_url, 
            params=parameters,
        ) as resp:
            data = await resp.json()        
        return data["data"]
    
    def _get_percent_change_24h(self, data):
        return float(data["changeRate"])
    
    def _get_price(self, data):
        return float(data["last"])

class Binance:
    _data = list()
    _base_url = 'https://data-api.binance.vision/'
    _api_url = '/api/v3/ticker/24hr'
    _symbols = ['BTCUSDT','ETHUSDT','SOLUSDT','DOGEUSDT']

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(base_url=self._base_url, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self._session.closed:
            await self._session.__aexit__(*args, **kwargs)

    async def run(self):
        self._data.clear()
        for symbol in self._symbols:
            data = await self._get_data(symbol)
            percent_change = self._get_percent_change_24h(data)
            price = self._get_price(data)
            self._data.append({'coin': symbol, 
                               'percent_change': percent_change, 
                               'price': price})
        return self._data

    async def _get_data(self, symbol):
        parameters = {
            'symbol': symbol,
        }
        async with self._session.get(
            url=self._api_url, 
            params=parameters,
        ) as resp:
            data = await resp.json()        
        return data
    
    def _get_percent_change_24h(self, data):
        return float(data["priceChangePercent"])
    
    def _get_price(self, data):
        return float(data["lastPrice"])
