🧍  Имя: {{person_data.name}}

📅  Дата рождения: {{person_data.birth_data}}

🕐  Время рождения: {{person_data.birth_time}}

🌍  Страна, Город: {{person_data.country}}, {{person_data.city}}

❓  Вопрос: {{person_data.question}}

{% if person_data.question_2 != None %}❓  Дополнительный вопрос: {{person_data.question_2}}
{% else %}Если всё верно, нажмите на кнопку ниже. Вы получите свой ответ в течение 5-20 секунд. 
{% endif %}
{%if date_response != None %}Ответ на 10 вопросов будут готовы: {{date_response}}
{% endif %}
