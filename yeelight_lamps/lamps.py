'''Модуль обнаружения  и работы с лампами'''
import yeelight
import threading
from yeelight import Bulb
from dataclasses import dataclass
from math import ceil, floor
from datetime import timedelta
from time import sleep
from lexicon import lamps_text

lamp_script_state : bool = False

@dataclass
class Lamp:
    '''кортеж с минимально необхоимыми параметрами лампы, мб избыточен и брать
    стоит непосредственно объект Bulb'''
    id: str  = None
    name: str = None
    model: str = id
    ip: str = None
    port: int = -1
    power_state: bool = False

def lamps_list() -> dict[str:Lamp]:
    '''ищем доступные лампы  в лок сети и создаем словарь Хостнейм|ID:кортеж
    lamp с необходимыми параметрами '''

    lamps_list = {
        x['capabilities']['name']:Lamp(
        x['capabilities']['id'],
        x['capabilities']['name'],
        x['capabilities']['model'],
        x.get('ip', None),
        x.get('port', -1),
        x['capabilities'].get('power')=='on'
        ) for x in yeelight.discover_bulbs(timeout=3)
    }
    return lamps_list

#Примеры обращений к бульбу
#myLamp = yeelight.Bulb("192.168.11.92", port = 55443)
#myLamp.turn_off()
#myLamp.get_capabilities()
#myLamp.set_capabilities('что-то сет')
#myLamp.set_name("KidsLamp1")

def sunrise_hue(lamp: Bulb = None, args='', duration_m:int = 3, reversed = False, **kwargs) -> None:
    '''Запуск имитации рассвета'''
    if args:
        for kwarg in args.split():
            print(kwarg)
            key, value = kwarg.split("=")
            if key == "duration_m":
                duration_m = int(value)
            elif key == "reversed":
                reversed = True if value=='True' else False
    print(f'duration={duration_m}, reversed={reversed}')

    global lamp_script_state
    lamp_script_state = True

    if not lamp:
        return lamps_text.answers['nothing']

    elif isinstance(lamp, str):
        name=lamps_list()[lamp]
        lamp = Bulb(name.ip)


    duration_time: timedelta = timedelta(minutes=duration_m)

    brightness = 0
    saturation = 100
    hue = 9
    hue_range = 50
    duration = duration_time.seconds
    step = ceil(hue_range/duration)
    step_brightness = 99/hue_range

    lamp.set_hsv(hue, saturation)
    lamp.set_brightness(brightness)
    lamp.turn_on()
    if reversed:
        step, step_brightness = step * -1, step_brightness * -1
        hue, hue_range  = hue_range, hue
        brightness =  99

    for hue in range(hue,hue_range,step):
        if not lamp_script_state:
            lamp.turn_off()
            break

        brightness += step_brightness
        if brightness > 40 :
            saturation -= step_brightness

        lamp.set_hsv(hue, saturation)
        lamp.set_brightness(brightness)
        sleep(duration/hue_range)
        print(hue, brightness)

    lamp_script_state = False


def lamp_off(lamp: Bulb | str = None, args='') -> str:
    global lamp_script_state
    lamp_script_state = False
    if not lamp:
        return lamps_text.answers['nothing']

    elif isinstance(lamp, str):
        name=lamps_list()[lamp]
        lamp = Bulb(name.ip)

    lamp.turn_off()
    return(f'{name.name} {lamps_text.answers["off"]}')

def lamp_on(lamp: Bulb = None, args='') -> str:
    if not lamp:
        return lamps_text.answers['nothing']

    elif isinstance(lamp, str):
        name=lamps_list()[lamp]
        lamp = Bulb(name.ip)
    lamp.turn_on()

    return(f'{name.name} {lamps_text.answers["on"]}')

def lamp_state(lamp: Bulb = None) -> str:
    state: str = lamp.get_capabilities()['power']
    if not state:
        state = 'nothing'
    return f'{lamps_text.answers["state"]}: {lamps_text.answers[state]}'

def lamp_scheduler(lamp: Bulb = None) -> str:
    return lamps_text.answers['sheduler']

def lamp_rename(lamp: Bulb = None) -> str:
    return lamps_text.answers['rename']

def lamp_other(lamp: Bulb = None) -> str:
    return lamps_text.answers['no_func']

def lamp_drop(lamp: Bulb = None) -> str:
    global lamp_script_state
    lamp_script_state = False
    return lamps_text.answers['drop']


def lamp_sunrise(lamp = None):
    global lamp_script_state
    if lamp_script_state:
        return lamps_text.answers['is_working']
    lamp_script_state = True

    func = threading.Thread(target = sunrise_hue, kwargs={'lamp':lamp,})
    func.start()
    return lamps_text.answers['sunrise']

'''
def lamp_sunset(lamp = None,reversed=True):
    global lamp_script_state
    if lamp_script_state:
        return lamps_text.answers['is_working']
    lamp_script_state = True
    func = threading.Thread(target = sunrise_hue, kwargs={'lamp':lamp, 'reversed':True})
    func.start()
    #sunrise_hue(lamp=lamp, reversed=True)
    return lamps_text.answers['sunset']
'''

def lamp_sunset(lamp = None,reversed=True):
    global lamp_script_state
    if lamp_script_state:
        return lamps_text.answers['is_working']
    lamp_script_state = True
    loop = asyncio.get_running_loop()
    #task = sunrise_hue(lamp=lamp, reversed=True)
    #loop.create_task(loop.to_thread(task))
    func = threading.Thread(target = sunrise_hue, kwargs={'lamp':lamp, 'reversed':True})
    func.start()
    #sunrise_hue(lamp=lamp, reversed=True)
    return lamps_text.answers['sunset']

#print(lamps_list())
#lamp = lamps_list()["KidsLamp1"]

#lamp_script_state =True
#sunrise_hue(lamp = Bulb(lamp.ip))
#lamp_script_state = False
#lamp='KidsLamp1'
# lamp_off(lamp)
#lamp_on(lamp)
#sleep(2)
#lamp_off(lamp)