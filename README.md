Планировщик задач:

Простой асинхронный планировщик для создания, изменения и удаления заданий, а также их выполнения в соответствии с определенным расписанием.
Задачи пишутся в БД.
Используется ORM  модель в конкретном варианте создается бд на sqlite.
первоначально планировалась  для создания имитации рассвета диодной лампы, фунции описаны модуле lamps.py

Спасибо openAI за расширение описания:

Описание таблиц:
Определены две таблицы: Duty и Author, используя ORM SQLAlchemy.
Duty содержит информацию о заданиях, таких как автор, время начала, действие, аргументы и другие атрибуты.
Author содержит информацию об авторах заданий.

Методы работы с таблицами:
Определены асинхронные методы, такие как add_author(), add_duty(), update_duty(), check_duty() и get_duty(), для работы с данными в таблицах.
Эти методы выполняют различные операции, такие как добавление, обновление и выборка записей из базы данных.

Функции выполнения заданий:
Определены функции выполнения заданий, такие как show_thread(), sunrise_hue(), lamp_off() и lamp_on().
Эти функции могут выполняться в отдельных потоках или асинхронно в зависимости от их назначения.

