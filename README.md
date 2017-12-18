[![Build Status](https://travis-ci.org/balashovartem/weather.svg?branch=master)](https://travis-ci.org/balashovartem/weather)

# weather
Тестовое задание improvado.io
Развернутое приложение - https://protected-harbor-73177.herokuapp.com/
* http://protected-harbor-73177.herokuapp.com/weather_history/ - история измерений погоды по городам с различных источников
* http://protected-harbor-73177.herokuapp.com/last_weather_history/ - последние измерения погоды по городам с различных источников
* http://protected-harbor-73177.herokuapp.com/last_weather_history/?city=tomsk - последние измерения погоды с различных источников отфильтрованные по конкретному городу - **сервис, дай актуальную температуру в таком-то городе.**
* http://protected-harbor-73177.herokuapp.com/update_weather - измерение погоды в указанных городах. **сервис, обнови данные для таких-то городов.** Список городов прислыается в формате json
```
{
  "cities" : ["tomsk", "novosibirsk"]
}
```

