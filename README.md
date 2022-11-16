# Сервис по анализу городской топологии

Наше веб-ориентированное приложение предназначено для комплексного анализа и планирования инфраструктурного развития городской среды на примере дорожно-транспортной сети. 

Данные, собранные нашим сервисом, в дальнейшем могут быть использованы для автоматизированного распознавания проектировочных недочётов и моделирования результатов принятия тех или иных управленческих решений, касающихся урбанистики.

## Предметная область
- Убранистика
- Проектирование городской среды

## Описание задачи

- Необходимо собрать наиболее полный набор топологических и инфраструктурных данных о выбранных заранее городах.
- Сбор топологической информации должен быть автоматизирован и не зависеть от выбранного города.
- Собранная информация должна быть представлена в переносимом и простом для дальнейшнего использования виде.
- Часть из этой информации (в нашем случае информация о транспортной сети) должна быть перенесена в базу данных, к ней должен быть предоставлен доступ пользовательскому интерфейсу.

## Pipeline

1. Пользователь выбирает интересующий его город.
2. Открывается карта выбранного города.
    - Пользователю предоставляется административное разбиение города, он может выбрать интересующий его с точки зрения анализа район.
    - Если пользователь хочет проанализировать произвольную часть города, он может задать её ограничивающим полигоном.
3. Пользователю предоставляется доступ к графу автомобильных дорог выбранной области и его топологическому разложению.
4. Каждое ребро графа атрибутировано полезными для дальнейшего анализа характеристиками.
5. Производится расчет топологических характеристик графа.
6. При желании пользователь может скачать оба графа в виде таблиц для дальнейшего анализа + изображения каждого графа в векторном формате
    
## Схема базы данных
    
https://dbdiagram.io/d/634d4b47470941019579beb6   

## UI / API
Страницы:
- Страница со списком доступных городов
- Карта города для выделения интересующей области анализа
- Визуализация интерактивных графов с возможностью выкачки в виде таблицы

## Технологии разработки
- Angular
- SQLAlchemy
- FastAPI
- Docker
- PostgreSQL

## Язык программирования
* Typescript
* Python
    
## Разработчики

- Ермолаев Александр
- Тимур Кравцов
- Киселёв Владимир
- Борисова Елена
- Кузнецов Матвей
- Громов Рамиль
- Воробьёв Владислав


  
