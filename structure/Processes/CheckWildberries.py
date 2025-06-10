from .BaseProcess import BaseProcess
from settings import PARSER_HEADERS

from telegram.ext import ContextTypes
from telegram import Update
import requests
import asyncio
import json


URL_SEARCH = "https://search.wb.ru/exactmatch/ru/common/v13/search?ab_testid=price_01&curr=rub&dest=-1&lang=ru&query={query}&resultset=catalog&page={page}"
URL_PRODUCT = "https://www.wildberries.ru/catalog/{product}/detail.aspx"

class CheckWildberries(BaseProcess):
    def __init__(self, core):
        self.core = core
        super().__init__(name='CheckWildberries', interval=30, start_delay=1, core=core)

    async def parse_wildberries(self, query, product):
        price, founded = product['price'], product['founded']
        if founded:
            return
        ids = []
        for page in range(1, 61):
            url = URL_SEARCH.format(query=query, page=page)
            response = await asyncio.to_thread(requests.get, url, headers=PARSER_HEADERS)
            payload = json.loads(response.text)
            if 'data' not in payload:
                break
            if 'products' not in payload['data']:
                break
            for product in payload['data']['products']:
                if product['id'] in ids:
                    continue
                if 'sizes' not in product:
                    continue
                for size in product['sizes']:
                    if size['price']['total'] <= price * 100: 
                        ids.append({
                            'name': product['name'],
                            'price': size['price']['total'] / 100,
                            'url': URL_PRODUCT.format(product=product['id'])
                            })
        if len(ids) == 0:
            return
        ids.sort(key=lambda x: x['price'])
        return ids[0]

    async def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        for sub in self.core.get_users():  
            for query in self.core.get_subs(sub).keys():
                product = await self.parse_wildberries(query, self.core.get_query(sub, query))
                if product is None:
                    continue
                self.core.set_founded(sub, query)
                await context.bot.send_message(
                                    chat_id=sub,
                                    text=f"🔥 Найдено соответствие!\n{product['name']}\nЦена: {product['price']}₽\nСсылка: {product['url']}"
                                )