# DRF_homework4
## Задание 1
Для сохранения уроков и курсов реализуйте дополнительную проверку на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com.

То есть ссылки на видео можно прикреплять в материалы, а ссылки на сторонние образовательные платформы или личные сайты — нельзя.

## Задание 2
Добавьте модель подписки на обновления курса для пользователя.
> Модель подписки должна содержать следующие поля: 
>  - «пользователь» (FK  на модель пользователя), 
>  - «курс» (FK на модель курса). 
> Можете дополнительно расширить модель при необходимости.

Вам необходимо реализовать эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.

При этом при выборке данных по курсу пользователю необходимо присылать признак подписки текущего пользователя на курс. То есть давать информацию, подписан пользователь на обновления курса или нет.

## Задание 3
Реализуйте пагинацию для вывода всех уроков и курсов.

## Задание 4
Напишите тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.
Сохраните результат проверки покрытия тестами.
_________________
##### Дополнительное задание
Напишите тесты на все имеющиеся эндпоинты в проекте.