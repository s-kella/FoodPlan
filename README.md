# Сервис FoodPlan
Проект содержит телеграмм-бота, который отправляет информацию о рецептах,
приготовления блюд согласно запросам пользователя и параметрам выбранной им подписки.
Пользователь идентифицируется по имени, фамилии и номеру телефона.
Затем пользователю предлагается либо оформить новую подписку, 
либо выбрать параметры уже имеющейся подписки. При оформлении новой подписки
пользователю предлагаются на выбор классическое, низкоуглеродное, вегетерианское и 
кетогенное меню. Затем предлагается выбрать количество приёмов пищи, количество персон
и аллергии, которые могут быть у пользователя. Далее выбирается срок подписки.
Для завершения процесса оформления подписку необходимо оплатить. 
После этого в разделе "мои подписки" пользователю будут доступны все офорленные 
подписки. После выбора подписки бот пришлёт информацию о рецепте согласно заданным парамерам.
### Как установить
Необходимо создать телеграм-бота с помощью отца ботов @BotFather, 
написав ему и выбрав имена для бота.
В качестве базы данных для бота используются google-таблицы.
Подробная [инструкция](https://habr.com/ru/post/483302/) для получения ключа и сервисного акканунта.
После получения ключа необходимо создать гугл таблицу foodPlan, нажав
"Настройки доступа", вести сервисный аккаунт и предоставить доступ на 
редактирование.
Затем необходимо получить токен, необходимый для оплаты, согласно [инструкции](https://core.telegram.org/bots/payments#getting-a-token)
В проекте используются переменные окружения, необходимо создать файл .env
для их хранение. Пример заполненного файла:
```
BOT_TOKEN = 1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234
GOOGLE_SHEETS_KEY = 'foodplan-123456-78910gfdhhhfhsh.json'
PAYMENTS_PROVIDER_TOKEN='12345678912376543:TEST:123456'
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).