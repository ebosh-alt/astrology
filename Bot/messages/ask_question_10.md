🧍  Имя: {{person_data.name}}

📅  Дата рождения: {{person_data.birth_data}}

🕐  Время рождения: {{person_data.birth_time}}

🌍  Страна, Город: {{person_data.country}}, {{person_data.city}}

❓  Вопрос: {{person_data.question}}

{% if person_data.question_2 != None %}❓  Дополнительный вопрос: {{person_data.question_2}}
{% else %}Ваш бесплатный ответ будет отправлен вам в сообщении этого бота в аудио формате или будет опубликован в открытом канале @bertotvet согласно вашей очереди.
{% endif %}
