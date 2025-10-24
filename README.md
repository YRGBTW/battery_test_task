# battery_test_task

Тестовое задание 

---

## Стек технологий
- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker + docker-compose
- HTML + JS

---

## Запуск проекта

### 1. Клонирование репозитория

### 2. Настройка окружения

В целях демонстрации работы файл окружения (.env) уже будет загружен в репозиторий.

### 3. Запуск через Docker

```bash
docker-compose up -d --build
```

После запуска документация Swagger доступна по адресу http://localhost:8000/docs
Интерфейс (UI) для взаимодействия с сущностями доступен по адресу http://localhost:8000/static/index.html

---
## Список эндпоинтов

---

### **Batteries**

* `GET /api/v1/batteries` — список всех АКБ
* `GET /api/v1/batteries/device/{device_id}` — список АКБ, привязанных к конкретному устройству
* `POST /api/v1/batteries` — создать новый АКБ
* `PUT /api/v1/batteries/{battery_id}` — обновить данные АКБ по ID
* `DELETE /api/v1/batteries/{battery_id}` — удалить АКБ по ID
* `POST /api/v1/batteries/{battery_id}/assign/{device_id}` — привязать АКБ к устройству

---

### **Devices**

* `GET /api/v1/devices` — список всех устройств
* `GET /api/v1/devices/{device_id}` — получить устройство по ID
* `POST /api/v1/devices` — создать новое устройство
* `PUT /api/v1/devices/{device_id}` — обновить устройство по ID
* `DELETE /api/v1/devices/{device_id}` — удалить устройство по ID

---


