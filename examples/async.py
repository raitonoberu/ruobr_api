import asyncio
from ruobr_api import AsyncRuobr

ruobr = AsyncRuobr("username", "password")

async def main():
    mail = await ruobr.get_mail()
    letters = await asyncio.gather(
        *[ruobr.get_message(m["id"]) for m in mail if m["type_id"] != 2]
    )
    print(letters)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())