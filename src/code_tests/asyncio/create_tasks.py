import asyncio
import time
async def task_func(**kwargs):
    while True:
        for key in kwargs:
            print(f'{time.time()}')

        yield str(time.time())


async def main(loop):
    print('creating task')
    task = loop.create_task(task_func(a=10,c = 'abcd'))
    print('waiting for {!r}'.format(task))
    return_value = await task
    print('task completed {!r}'.format(task))
    print('return value: {!r}'.format(return_value))

event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()
