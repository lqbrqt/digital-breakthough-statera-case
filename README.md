# digital-breakthough-statera-case
Решение для распознования номеров на железнодорожнэх вагонах включает в себя 
Api сервис состоящий из нескольких основных этапов:
  YOLOv8 и DETR для разметки номера на фото
  Нейросеть, обученная на SVHN для классификации цифр на фото
  Проверка контрольной суммы
  Формирование ответа в формате JSON
Frontend составляющая с использованием Streamlit для тестирваний вручную

more_info:
назначение ветвей:
train - набор необходимый для обучения YOLOv8 (.parser.ipynb - перобразование разметки датасета к формату необходимому для YOLOv8,train.py - основной файл для запуска обучения(также содержит t.yaml,необходимый при обучении() )
API - api сервис
  uvicorn app_main:app - команда для запуска
  https://disk.yandex.ru/d/f_MiVECowYmryg - ссылка на пердобученные модели
streamlit_front - frontend срвис
  streamlit run main.py - команда для запуска