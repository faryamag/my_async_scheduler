import threading
from yeelight_lamps import lamps

def show_thread(*args):

    thread_id = threading.current_thread()
    print(thread_id.name, threading.get_native_id(), datetime.now())
    sleep(randint(1,30))
    print(thread_id.name, threading.get_native_id(), "awaiked'")


func_list ={
        'print': print,
        'show_thread': show_thread,
        'sunrise_hue': lamps.sunrise_hue,
        'lamp_off': lamps.lamp_off,
        'lamp_on': lamps.lamp_on
    }
