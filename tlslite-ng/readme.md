# RU

В Ren-Engine нет модуля `_ssl`, потому что:
1. Он не может быть слинкован статически, быть "built-in",
2. Он не может быть динамическим, если питон слинкован статически,
3. Питон слинкован с движком статически, т. к. это даёт +30% к производительности относительно динамической линковки.

Без `_ssl` модуль `urllib.request` не будет работать с протоколом `https`,
а т. к. сейчас около 90% сайтов используют именно его,
то работа с сетью во многом становится просто невозможна.

Для решения этой проблемы используется `tlslite-ng`.  
Включая зависимости:
1. `hmac`,
2. `ecdsa`.
И с удалением некоторого кода для использования:
1. Старого питона,
2. Электронной почты и баз данных,
3. Несуществующих модулей, которые могли бы дать некоторое ускорение.

Пример использования можно посмотреть в файле `main.py`.  
В нём используется класс `HTTPTLSConnection`, который основан на классе
[http.client](https://docs.python.org/3/library/http.client.html)
из стандартной библиотеки.


# EN

There is no `_ssl` module in Ren-Engine because:
1. It cannot be linked statically, be "built-in",
2. It cannot be dynamic if Python is linked statically,
3. Python is linked to the engine statically, because this gives +30% performance compared to dynamic linking.

Without `_ssl` the `urllib.request` module will not work with the `https` protocol,
and since now about 90% of sites use it,
then working with the network in many ways becomes simply impossible.

To solve this problem, `tlslite-ng` is used.  
Including dependencies:
1. `hmac`,
2. `ecdsa`.
And with some code removed for use:
1. Old python,
2. Email and databases,
3. Non-existent modules that could provide some speedup.

An example of use can be found in the `main.py` file.  
It uses the `HTTPTLSConnection` class, which is based on the
[http.client](https://docs.python.org/3/library/http.client.html)
from the standard library.
