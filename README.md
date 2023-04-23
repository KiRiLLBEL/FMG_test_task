# FMG_test_task
Solving a test task for an internship in Kaspersky SafeBoard

Как запустить решение:

- Собрать `Docker` образ - `docker build -t fmg:1.0 .`
- Запустить контейнер - `docker run -d --name mycontainer -p 80:80 fmg:1.0`
- Открыть swagger - `http://127.0.0.1:80/docs`