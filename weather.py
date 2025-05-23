import datetime
import json
import requests


api = 'aef454789ee3d0bad82fee47b0613904'
directions = ['Северный', 'Северо-восточный',
              'Восточный', 'Юго-восточный',
              'Южный', 'Юго-западный',
              'Западный', 'Северо-западный']
icons = {
    "01d": "☀️", "01n": "🌑",
    "02d": "🌤", "02n": "⛅️",
    "03d": "☁️", "03n": "☁️",
    "04d": "☁️", "04n": "☁️",
    "09d": "🌧", "09n": "🌧",
    "10d": "🌦", "10n": "🌦",
    "11d": "⛈", "11n": "⛈",
    "13d": "❄️", "13n": "❄️",
    "50d": "🌫️", "50n": "🌫️"
}


def get_weather_message(city):
    request = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric&lang=ru')
    data = json.loads(request.text)

    if len(data) == 2 and data['cod'] == 404:
        return "Такого города не существует! Введите другой город."

    try:
        tz = datetime.timezone(datetime.timedelta(seconds=data['timezone']))
        lines = [f"Погода в городе <b>{data['name']}</b> на {str(datetime.datetime.fromtimestamp(data['dt'], tz))}:"]

        if len(data['weather']) <= 1:
            lines.append(f"{icons[data['weather'][0]['icon']]} <b>{data['weather'][0]['main']}</b> "
                         f"<i>({data['weather'][0]['description']})</i>")
        else:
            lines.append("Погода:")
            for weather in data['weather']:
                lines.append(f"\t{icons[weather['icon']]} {weather['main']} <i>({weather['description']})</i>")

        lines.append(f"<b>Температура:</b> {data['main']['temp']} °C <i>(ощущается как "
                     f"{data['main']['feels_like']} °C)</i>")
        lines.append(f"<b>Атмосферное давление:</b> {data['main']['pressure']} hPa")
        lines.append(f"<b>Влажность:</b> {data['main']['humidity']}%")
        lines.append(f"<b>Видимость:</b> {data['visibility']} м")
        lines.append(f"<b>Облачность:</b> {data['clouds']['all']}%")

        wind_dir_index = (round(data['wind']['deg'] * 8 / 360) + 8) % 8
        if 'gust' in data['wind'].keys():
            lines.append(f"<b>Ветер:</b> {directions[wind_dir_index]} {data['wind']['speed']} м/с "
                         f"<i>(с порывами до {data['wind']['gust']} м/с)</i>")
        else:
            lines.append(f"<b>Ветер:</b> {directions[wind_dir_index]} {data['wind']['speed']} м/с")

        if 'rain' in data.keys():
            lines.append(f"<b>Дождевые осадки:</b> {data['rain']['1h']} мм/ч")
        elif 'snow' in data.keys():
            lines.append(f"<b>Снежные осадки:</b> {data['snow']['1h']} мм/ч")
        else:
            lines.append("<b>Без осадков</b>")

        lines.append("\nЧтобы увидеть погоду в другом городе введите его название.")

        return '\n'.join(lines)
    except:
        return "Произошла ошибка! Попробуйте ещё раз."