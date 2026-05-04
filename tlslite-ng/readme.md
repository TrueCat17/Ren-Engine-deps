# RU

В Ren-Engine нет модуля `_ssl`, потому что есть проблемы с его сборкой,
запуском получившейся сборки и общим весом, добавляемым к движку.

Без `_ssl` модуль `urllib.request` не будет работать с протоколом `https`,
а т. к. сейчас около 90% сайтов используют именно его,
то работа с сетью во многом становится просто невозможна.

Для решения этой проблемы используются `tlslite-ng` и её библиотека-зависимость `ecdsa`.

В коде `tlslite-ng` удалена поддержка некоторых вещей:
1. Старые версий питона;
2. Электронная почта и базы данных;
3. Несуществующие модулей, которые могли бы дать некоторое ускорение.

Пример использования можно посмотреть в файле `main.py`.  
В нём используется класс `HTTPTLSConnection`, который основан на классе
[http.client](https://docs.python.org/3/library/http.client.html)
из стандартной библиотеки.


# EN

Ren-Engine doesn't have a `_ssl` module because there are problems with building it,
running the resulting build, and the overall weight added to the engine.

Without `_ssl`, the `urllib.request` module will not work with the `https` protocol,
and since now about 90% of sites use it,
working with the network in many ways becomes simply impossible.

To solve this problem, `tlslite-ng` and its dependency library `ecdsa` are used.

The `tlslite-ng` code has removed support for some things:
1. Old versions of Python;
2. Email and databases;
3. Non-existent modules that could provide some speedup.

An example of use can be found in the `main.py` file.  
It uses the `HTTPTLSConnection` class, which is based on the
[http.client](https://docs.python.org/3/library/http.client.html)
class from the standard library.
