from ruobr_api import Ruobr, AsyncRuobr
from time import time
import asyncio


# Симуляция множества пользователей
# Не перестарайтесь, а то нарвётесь на защиту от DDoS атак :)
number_of_users = 10
users = [("username", "password") for i in range(number_of_users)]


def syncruobr(username, password):
    r_sync = Ruobr(username, password)
    r_sync.getUser()


async def asyncruobr(username, password):
    r_async = AsyncRuobr(username, password)
    await r_async.getUser()

start = time()
sync_users = [syncruobr(*i) for i in users]
print("Синхронно:", round(time() - start, 2), "секунд")

loop = asyncio.get_event_loop()
start = time()
async_users = [asyncruobr(*i) for i in users]
users = loop.run_until_complete(asyncio.gather(*async_users))
print("Асинхронно:", round(time() - start, 2), "секунд")
