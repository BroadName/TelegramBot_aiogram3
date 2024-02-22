# Инструкция по использованию телеграмм бота.
## При первом входе вы увидите приветственное сообщение с описанием базового функционала.
После ввода команды __/start__ код заполняет базу данных PostgreSQL базовым набором слов для их изучения и связывает их с пользователем, так же появляеся три кнопки вместо клавиатуры:
1. **Добавить новое слово** - после нажатия данной кнопки бот ожидает ввода, сначала английский вариант, слово или выражение и потом его перевод. При добавлении существующего слова, бот укажет на это и предложит варианты действий.
2. **Удалить слово** - после этого действия бот ожидает ввода одного слова или выражения на английсом языке, которое вы хотите удалить (удаляется связь пользователя со словом в базе данных)
3. **Let's start** - после этой команды бот выводит случайно рандомное слово (из имеющихся у пользователя) и предлагает случайные слова и одно верное на выбор пользователю при помощи кнопок. Кнопки каждый раз перемешиваются. В случае выбора правильного ответа, бот присылает поздравления и предлагается посредством клавиатурных кнопок продолжить изучение, либо добавить или удалить слово, либо закончить тренировку с ботом. В случае ~~неправильного ответа~~, бот уведомит пользователя об его неправильном выборе и предложит попробовать еще раз (появляются новые клавиатурные кнопки с одним правильным ответом) либо ввести команду **/start** для выбора других действий.
В проекте использовалась база данных *PostgreSQL*, подключение к которой осуществлялось с помощью модуля *asyncpg*.
Схема базы данных следующая:

      ![diagramm_db](https://github.com/BroadName/TelegramBot_aiogram3/assets/145323101/10862be4-3e2c-459b-bdd1-6141751615ad)
