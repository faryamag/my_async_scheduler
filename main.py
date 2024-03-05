import asyncio
from datetime import datetime
from time import time


from random import randint
from time import sleep
import threading

import funcs
import base_operation as bo

func_list = funcs.func_list



async def main():

    await bo.init_base()

    count = 0
    while True: #count < 1:
        start = time()
        print("Curr_time", datetime.now().strftime('%H:%M:%S'))
        count+=1

        curr_time = datetime.now().strftime('%H:%M:%S')
        #curr_time='22:37:00'
        res = await bo.operate_base(bo.get_duty, start_time=curr_time, cells=['start_time', 'duty_id', 'act', 'args','obj', 'is_working'])# , enabled=True, name='Farit!!!', act='print', start_time=datetime.now().strftime('%H:%M:%S'), args="1234 sdcd ewcdsdc")

        if any(res):

            print(threading.get_native_id())
            for duty in res:
                if duty['act'] not in func_list:
                    tm = datetime.now()
                    asyncio.create_task(bo.operate_base(bo.update_duty, duty_id=duty['duty_id'], enabled=False, last_err=f'No such function, {tm}'))

                else:
                    print(duty['act'], duty['obj'], duty['args'])
                    fn = func_list[duty['act']]
                    print(fn, duty['act'], duty['obj'], duty['args'])
                    task = asyncio.to_thread(fn, duty['obj'], duty['args'] )
                    asyncio.create_task(task)
                    print('started', duty['act'])
                    #await asyncio.sleep(0)

        delta = time()-start
        await asyncio.sleep(1-delta)
        print(delta)

asyncio.run(main())