# cryptoapi
Модуль для работы с Crypto API | [Официальное приложение](https://vk.com/app51446412_-221070987)
<br>
<br>
## Установка и импорт
Для установки необходимо прописать в консоль (cmd) следующую команду:
```
pip install apicrypto
```

Для импорта модуля в проект использовать:
```python
from cryptoapi import CryptoAPI
```
## Использование
Перед началом необходимо создать экземпляр класса CryptoAPI, который принимает 2 аргумента:

| Аргумент | Тип | Описание                                    |
| -------- |:---:|:------------------------------------------- |
| user_id  | int | ID Пользователя VK, который получил токен   |
| token    | str | Токен, полученный в самом приложении Crypto |

```python
from cryptoapi import CryptoAPI
crypto = CryptoAPI(user_id=ваш_ID, token="Ваш_Токен")
```

### getUserCoins()
Возвращает баланс указанного пользователя.

| Аргумент | Тип | Описание                                                  |
| -------- |:---:|:--------------------------------------------------------- |
| user_id  | int | ID Пользователя VK, баланс которого необходимо получить   |

`Если не указывать user_id, то подставится ID из созданного экземпляра`

```python
crypto.getUserCoins(user_id=498475943)
>>> 1139888
```

### getTransfers()
Возвращает список всех переводов
```python
crypto.getTransfers()
>>> [{'name': 'Алекса...}]
```

### transfer()
Отправляет перевод.

| Аргумент | Тип | Описание                                 |
| -------- |:---:|:---------------------------------------- |
| toId     | int | ID пользователя, кому отправляем перевод |
| amount   | int | Сумма перевода                           |

```python
crypto.transfer(toId=498475943, amount=100)
>>> {"response": {"recipient_id": 498475943, "amount": 100}}
```

### connectServer()
Настраивает отправку callback уведомлений на Ваш сервер / сайт.

| Аргумент | Тип | Описание                                               |
| -------- |:---:|:------------------------------------------------------ |
| url      | str | Адрес сервера / сайта, куда буду приходить уведомления |

```python
crypto.connectServer(url="https://mysite.mydomain")
>>> {"response": {"url": "https://mysite.mydomain", "user_id": 498475943}}
```

**Обратите внимание, что ссылка обязательно должна начинаться с https:// или http://**

После получения перевода, callback возвращает JSON Объект события следующего вида:
```json
{
  "event": "new_transfer",
  "object": {
    "sender_id": 498475943,
    "amount": 1000,
    "create_date": 1687423373784,
    "secretKey": "18e0f585616e1ece62316072a45f64e4"
  }
}
```

### listen()
Запускает встроенный прослушиватель переводов. При получении нового перевода возвращает JSON.

| Аргумент | Тип | Описание                                                             |
| -------- |:---:|:-------------------------------------------------------------------- |
| interval | int | Задает интервал обновления переводов в секундах (По умолчанию: 1) |

```python
for object in crypto.listen(interval=0.1):
  print(object)
>>> {"name": "Иван Шаповалов", "avatar": "https://sun34-2.userapi.com/impg/0MjzdwFu6WRSYod_65kU0BjdVpNcqWyxXmr76g/ZlbXvz3CTSs.jpg?size=720x720&quality=95&sign=ae29a8d9bacfab080534f3f2cb964963&type=album", "sender_id": 498475943, "recipient_id": 487364833, "create_date": 1687416286823, "amount": 1000}
```

### md5()
Генерирует secretKey для проверки callback переводов на честность (Подробней - https://vk.com/@crypto_play-api?anchor=connectserver)

`Имеется два варианта передачи параметров для генерации secretKey`

`Первый вариант`
| Аргумент    | Тип  | Описание                  |
| ----------- |:----:|:------------------------- |
| create_date | int  | Дата перевода в UNIX      |
| sender_id   | int  | ID Отправителя            |

```python
crypto.md5(create_data=1689398602, sender_id=498475943)
>>> '876104e5cee8669f1b89448282215da5'
```

`Второй вариант`
| Аргумент    | Тип         | Описание                  |
| ----------- |:-----------:|:------------------------- |
| json        | dict / json | JSON полученного перевода |

```python
crypto.md5(json=
{
  'event': 'new_transfer', 
  'object': {
    'sender_id': 1, 
    'amount': 10000, 
    'create_date': 1689408602, 
    'secretKey': '1287a00828e7e44ea83b7d90caf938a1'
  }
})
>>> '1287a00828e7e44ea83b7d90caf938a1'
```
