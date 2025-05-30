# Симулятор Заказов

Имитирует высоконагруженный трафик POST заказов к API Sausage-Store.

## Цель

- Проверить как deployment масштабирует поды в зависимости от нагрузки
- Как реагируют метрики prometheus
- Преверка правильности уведомлений alertmanager

## Конфигурация

- **Настраиваемая baseurl и endpoint**
- **Случайные заказы** (1–5 видов сосисок)
- **Многопоточные пакеты** (`THREADS` параллельных запросов)
- **Метрики пакета** (затраченное время, количество успешных/неудачных запросов, запросов в секунду)
- **Настраиваемая пауза** (`SLEEP_INTERVAL` между пакетами)

## Требования

- Библиотека `requests`

## Установка и запуск:

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests
python3 main.py
```
