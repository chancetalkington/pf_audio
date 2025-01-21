import asyncio

from playwright.async_api import async_playwright, expect

import config
from config import *

from tasks.screen_ai import *
import keyboard


class Pumpfun:
    def __init__(self):
        self.url = 'https://pump.fun/create'
        wallet_path = f'{EXTENSIONS_PATH}\\bhhhlbepdkbapadjdnnojkbgioiodbic'
        version = f'{os.listdir(wallet_path)[-1]}'
        self.wallet_path = f'{wallet_path}\\{version}'

    async def create_token(self):
        print('Creating token')
        async with async_playwright() as p:
            context = await p.chromium.connect_over_cdp(endpoint_url='http://localhost:9222')
            default_context = context.contexts[0]
            flag = False
            for i in default_context.pages:
                if i.url == 'https://pump.fun/create':
                    await i.bring_to_front()
                    page = i
                    flag = True
            if flag is False:
                await context.new_page()
            await page.goto(self.url)

            # Set Token name
            name = page.locator("[id='name']")
            await expect(name).to_be_visible()
            await name.first.clear()
            await name.first.type(config.NAME, delay=150)
            await page.wait_for_timeout(1000)

            # Set token tiker
            name = page.locator("[id='ticker']")
            await expect(name).to_be_visible()
            await name.first.clear()
            await name.first.type(config.TIKER, delay=150)
            await page.wait_for_timeout(1000)

            # Set token description
            name = page.locator("[id='text']")
            await expect(name).to_be_visible()
            await name.first.clear()
            await name.first.type(config.TEXT, delay=150)
            await page.wait_for_timeout(1000)

            # Upload file
            await page.set_input_files('input[type="file"]', FILE)

            # Click Create coin button
            connect = page.get_by_role('button', name="create coin")
            await expect(connect).to_be_visible()
            await connect.click()

            # Fill Amount field
            amount = page.locator("[id='amount']")
            await expect(amount).to_be_visible()
            await name.first.clear()
            await name.click()
            await name.first.type(config.AMOUNT, delay=150)
            await name.press_sequentially(config.AMOUNT)
            await page.wait_for_timeout(1000)

            # Solve Captcha
            # captcha = page.locator("[title='Widget containing a Cloudflare security challenge']")
            # await expect(captcha).to_be_visible()
            solve_captcha(times=50, delay=1000000)

            # Click Create coin button again
            connect = page.get_by_role('button', name="create coin")
            await expect(connect).to_be_enabled(timeout=20000)
            await connect.click()
            await page.wait_for_timeout(1000)

            # Click View button
            connect = page.get_by_role('button', name="View")
            await expect(connect).to_be_visible(timeout=20000)
            await connect.click()
            await page.wait_for_timeout(5000)

            await asyncio.sleep(10)
