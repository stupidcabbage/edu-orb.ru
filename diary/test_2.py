import asyncio

import threading

async def some_callback(args):
    await some_function()


def between_callback(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    Loop.run_until_complete(some_callback(args))
    loop.close()

_thread = threading.Thread(target=between_callback, args=("some text"))
_thread.start()
