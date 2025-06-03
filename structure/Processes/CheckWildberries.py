from .BaseProcess import BaseProcess

from telegram.ext import ContextTypes
from telegram import Update
import requests
import asyncio
import json


class CheckWildberries(BaseProcess):
    def __init__(self, core):
        self.core = core
        super().__init__(name='CheckWildberries', interval=30, start_delay=1, core=core)

    async def parse_wildberries(self, query, price):
        ids = []
        for page in range(1, 61):
            url = f"https://search.wb.ru/exactmatch/ru/common/v13/search?ab_testid=price_01&curr=rub&dest=-1&lang=ru&query={query}&resultset=catalog&page={page}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = await asyncio.to_thread(requests.get, url, headers=headers)
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
                        return {
                            'name': product['name'],
                            'price': size['price']['total'] / 100,
                            'url': f"https://www.wildberries.ru/catalog/{product['id']}/detail.aspx"
                            }
                ids.append(product['id'])

    async def __call__(self, context: ContextTypes.DEFAULT_TYPE):
        for sub in self.core.all_subs:  
            for query in self.core.all_subs[sub]:
                product = await self.parse_wildberries(query, self.core.all_subs[sub][query])
                if product is None:
                    continue
                await context.bot.send_message(
                            chat_id=sub,
                            text=f"🔥 Найдено соответствие!\n{product['name']}\nЦена: {product['price']}₽\nСсылка: {product['url']}"
                        )
                return