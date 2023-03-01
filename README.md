# Репозиторий для лабораторных работ по криптографии

## Структура проекта

Проект является веб-приложением, предоставляющим графический интерфейс для демонстрации работы алгоритмов из задач лабораторных работ для курса криптографии

## Установка

```sh
docker compose up -d --build
docker compose exec backend python manage.py makemigations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic
```

Чтобы открыть интерфейс необходимо в браузере перейти по ссылке ```http://localhost:10050```

## Лабораторная работа 1

Первая лабораторная работа состоит из 2ух алгоритмов:

- ADFGX / ADFG(V)X
- Playfair

Реализация алгоритмов описана в классах **ConvertADFGX** и **ConvertPlayfair**, которых хранятся в файле services.py по пути ```./backend/cript/services.py```
