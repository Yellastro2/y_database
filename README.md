# y_database

Общий модуль доступа к SQLite/MySQL для Telegram-ботов.

## Обновление от 2026-07-22

Настройка SQLite переведена на безопасную позднюю инициализацию. Импорт
`DbHelper` или `db_repo` больше не создаёт соединение и не фиксирует имя базы.
Имя фиксируется только при первом реальном SQL-запросе.

Раньше при неудачном порядке импортов мог незаметно использоваться файл
`yDatabase.db` или `some.db`. Теперь база без явной настройки не создаётся:
первый запрос завершится `RuntimeError` с сообщением о необходимости вызвать
`y_database.configure(...)`.

После первого SQL-запроса изменить имя базы нельзя. Повторная настройка с тем
же именем допустима, а попытка переключиться на другой файл завершится
`RuntimeError`. Это защищает работающий бот от записи в две разные базы из-за
порядка импортов.

## Подключение в боте

В основном запускаемом модуле настройте базу до инициализации таблиц, запуска
ядра и выполнения любых запросов:

```python
from y_database import configure

configure("my_bot.db")

from y_database import db_initer
from y_bot_core import module_init
```

Импортировать `db_repo` до `configure()` безопасно, если при импорте приложение
не выполняет SQL-запросы:

```python
from y_database import db_repo
from y_database import configure

configure("my_bot.db")
```

Для старого кода сохранён совместимый вызов:

```python
from y_database import db_confings

db_confings.set_default_name("my_bot.db")
```

Он работает так же, как `configure()`. Новому коду рекомендуется использовать
публичный импорт `from y_database import configure`.

## Явная отдельная база

Если одному процессу нужна дополнительная SQLite-база, передайте имя прямо в
helper. Такая база не использует и не блокирует глобальную конфигурацию:

```python
from y_database import DbHelper, db_repo

archive_db = DbHelper(db_name="archive.db")
users = db_repo.get_all(yUser, f_db=archive_db)
```

Параметр `db_name` поддерживается для SQLite. Настройки подключения MySQL
по-прежнему берутся из конфигурации MySQL-модуля.

## Требования к совместимому коду

- Каждый бот должен явно вызвать `configure("имя.db")` до первого запроса.
- Не выполнять запросы к БД на уровне импорта модуля.
- Не использовать `DbHelper()` как default argument функции. Использовать
  `f_db=None` и создавать helper внутри функции.
- Не рассчитывать на автоматическое создание `yDatabase.db` или `some.db`.
- При обновлении общего модуля обновлять `y_database` и `y_bot_core` вместе.

Правильный шаблон функции с необязательным helper:

```python
def load_data(f_db=None):
  if f_db is None:
    f_db = DbHelper()
  return f_db.fetch_all("SELECT * FROM data")
```

