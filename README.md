# job_parser
Приложение собирает основную информацию заданного пользователем количества вакансий по ключевому слову: 
название вакансии, ссылка,  название компании, опыт работы, зарплата, описание. Парсинг ведется по двум ТОП-сайтам рунета: hh.ru
и superjob.ru. После парсинга информация о вакансиях выгружается в два csv-файла - по одному на каждый сервис.

Также после парсинга пользователь может совершить дополнительные действия с выгрузкой: отсортировать по возрастанию или убыванию 
зарплаты, выести заданное количества ТОП-вакансий по зарплате, отобрать вакансии по заданному значению опыта работы, удалить вакансии 
по заданному значению опыта работы.
