''' Тексты для модуля  управления лампами бота '''

navigate: dict = {
    'search': "Найти активные лампы",
    'exit' : 'Выход',
    'list': 'Мой список',
    'return' : 'Возврат',
}

init_lamp: dict = {
    'on': "Вкл",
    'off': "Выкл",
    'state': "Состояние",
    'rename': "Переименовать",
    'scheduler': 'Планировщик',
    'func': 'Доп. функции'
}


init_lamp_exclude: set = set(('scheduler'))
init_lamp_set: set[str] = set(init_lamp) - init_lamp_exclude

kb_func: dict = {
    'sunrise': "рассвет",
    'sunset': "закат",
    'other': "остальные",
    'drop' : "прервать сценарий"

}


kb_scheduler: dict = {
    'task_add': "Новая задача",
    'task_del': "Удалить задачу",
    'task_edit': "Редактировать задачи",
    'schdlr_on': 'Включить планировщик',
    'schdlr_off': 'Выключить планировщик',
    'schdlr_show': 'Показать задачи'

}

answers: dict = {
    'on': "Включено",
    'off': "Выключено",
    'state': ' ! ',
    'rename': 'Устройство переименовано',
    'nothing': "Устройство пропало или не найдено",
    'no_func': "Функционал не задан",
    'scheduler': 'Планировщик установлен',
    'sunrise': "Имитация рассвета",
    'sunset': "Имитация заката",
    'is_working': "Сценарий выполняется, дождитесь окончания",
    'drop' : "Сценарий прерван"


}

messages_text: dict[str:str] = {
    'choose': 'У нас имеются такие лампы, выбери:',
    'kb_1': 'Основные функции управления:',
}