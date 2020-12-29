# VK-CLI
VKontakte CLI version

## Команды главной консоли:
**Показать справку:**

`help`

**Добавить новый токен в список:**

`add <token>`

**Список добавленых токенов:**

`list`

**Удалить токен из списка:**

`delete <token id>`

**Авторизоваться с помощью токена:**

`auth <token id>`

**Выйти:**

`exit`

### Пример:
```
Список токенов загружен
(VK-CLI)list
0 7dd020931e...
(VK-CLI)auth 0
Эмиль Иванов (vzlomrtlsoska) - id611955040
Дата рождения: 25.8.1920
      Телефон: +7 *** *** ** 37
       Страна: Россия
       Статус: 
(Эмиль Иванов)>
```
 

 ## Команды профиля:
 
 **Показать справку:**
 
 `help`
 
 **Вывести диалоги:**
 
 `dialogs`
 
 **Выбрать диалог:**
 
 `select <chat id>`

 **Выйти из профиля:**

 `exit`


 ## Команды приватного диалога:
 
 **Прочитать сообщения:**
 
 `read [count]`

 **Выйти из приватного диалога:**
 
 `exit`


 ## Команды чата:

 **Прочитать сообщения:**

 `read [count]`

 **Выйти из чата:**

 `exit`
