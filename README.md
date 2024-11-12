**Django online shop "Megano_site"**

Интернет магазин "Megano_site"

Проект разработан с помощью фреймворке Django.
Обращение к данным посредством API(Rest framework), за визуализацию приложения отвечает frontend.

**Запуск приложения**

1.Клонирование репозитория 
`git clone https://gitlab.skillbox.ru/mariia_orlova/python_django_diploma.git`

2.Установить все необходимые зависимости, указанные в файле requirements.txt

3.Перейти в папку с проектом командой cd megano_site

4.Применить миграции
`python3 manage.py makemigrations`

5.Загрузить фикстуры данных Базы Данных
`python3 manage.py loaddata fixtures/db.json`

6.Запустить сервер 
`python3 manage.py runserver`

**Структура сайта**

Главная страница.
Популярные товары, баннеры, ограниченный тираж товаров.
<img width="483" alt="Снимок экрана 2024-11-12 в 13 52 22" src="https://github.com/user-attachments/assets/b72b50b8-38c6-4138-904e-167d6f6031e7">

<img width="483" alt="Снимок экрана 2024-11-12 в 13 52 15" src="https://github.com/user-attachments/assets/01c4174e-5c00-41e0-85b9-d4465a3458fb">


Каталог с фильтром и сортировкой: 

-cам каталог товаров;

<img width="483" alt="Снимок экрана 2024-11-12 в 14 28 26" src="https://github.com/user-attachments/assets/d1d26a3d-8000-4860-9663-a7307d69426d">


-детальная страница товара, с отзывами.

<img width="483" alt="Снимок экрана 2024-11-12 в 14 29 38" src="https://github.com/user-attachments/assets/5b96cdab-2b7f-442f-90f5-b25fb575469c">

Оформление заказа:

-корзина;

<img width="483" alt="Снимок экрана 2024-11-12 в 14 46 11" src="https://github.com/user-attachments/assets/9677108d-0874-4499-89e0-6e2e36b896ec">

-оформление заказа;

<img width="483" alt="Снимок экрана 2024-11-12 в 14 47 22" src="https://github.com/user-attachments/assets/6f1cea1d-895d-430c-98f6-c2bc53a09da6">


-оплата.

<img width="483" alt="Снимок экрана 2024-11-12 в 14 48 24" src="https://github.com/user-attachments/assets/75a93e70-3293-405e-883f-bbfbb306515e">

Личный кабинет:
-профиль;

<img width="483" alt="Снимок экрана 2024-11-12 в 14 51 36" src="https://github.com/user-attachments/assets/4882ecfb-1656-461a-832e-8a7c9819a24d">

-история заказов.

<img width="500" alt="Снимок экрана 2024-11-12 в 14 52 15" src="https://github.com/user-attachments/assets/c3f1af61-e5e2-4df0-add7-59ddf6b237f0">

Административный раздел:

-просмотр и редактирование товаров;
-просмотр и редактирование заказов;
-просмотр и редактирование категорий каталога.


<img width="483" alt="Снимок экрана 2024-11-12 в 14 53 32" src="https://github.com/user-attachments/assets/50baf945-47a1-470e-965f-aeef8134063d">

