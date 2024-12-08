import tkinter as tk
import requests
import datetime
from PIL import Image, ImageTk
import io
import urllib.request

class WeatherClock(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.languages = {
            'ru': {
                'weekdays': {
                    0: 'Понедельник', 1: 'Вторник', 2: 'Среда',
                    3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'
                },
                'months': {
                    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
                    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
                    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
                },
                'weather': {
                    0: "Ясно", 1: "Преимущественно ясно",
                    2: "Переменная облачность", 3: "Пасмурно",
                    45: "Туман", 48: "Изморозь",
                    51: "Легкая морось", 53: "Умеренная морось",
                    55: "Сильная морось", 56: "Легкий ледяной дождь",
                    57: "Сильный ледяной дождь", 61: "Небольшой дождь",
                    63: "Умеренный дождь", 65: "Сильный дождь",
                    66: "Легкий ледяной дождь", 67: "Сильный ледяной дождь",
                    71: "Небольшой снег", 73: "Умеренный снег",
                    75: "Сильный снег", 77: "Снежные зёрна",
                    80: "Небольшой ливень", 81: "Умеренный ливень",
                    82: "Сильный ливень", 85: "Небольшой снегопад",
                    86: "Сильный снегопад", 95: "Гроза",
                    96: "Гроза с небольшим градом", 99: "Гроза с сильным градом"
                },
                'ui': {
                    'city': 'Город:',
                    'humidity': 'Влажность:',
                    'wind_speed': 'Скорость ветра:',
                    'error': 'Ошибка',
                    'city_not_found': 'Город не найден',
                    'weather_error': 'Не удалось получить погоду',
                    'connection_error': 'Проверьте подключение к интернету',
                    'ms': 'м/с'
                }
            },
            'en': {
                'weekdays': {
                    0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                    3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'
                },
                'months': {
                    1: 'January', 2: 'February', 3: 'March', 4: 'April',
                    5: 'May', 6: 'June', 7: 'July', 8: 'August',
                    9: 'September', 10: 'October', 11: 'November', 12: 'December'
                },
                'weather': {
                    0: "Clear", 1: "Mostly Clear",
                    2: "Partly Cloudy", 3: "Overcast",
                    45: "Foggy", 48: "Frost",
                    51: "Light Drizzle", 53: "Moderate Drizzle",
                    55: "Heavy Drizzle", 56: "Light Freezing Rain",
                    57: "Heavy Freezing Rain", 61: "Light Rain",
                    63: "Moderate Rain", 65: "Heavy Rain",
                    66: "Light Freezing Rain", 67: "Heavy Freezing Rain",
                    71: "Light Snow", 73: "Moderate Snow",
                    75: "Heavy Snow", 77: "Snow Grains",
                    80: "Light Showers", 81: "Moderate Showers",
                    82: "Heavy Showers", 85: "Light Snow Showers",
                    86: "Heavy Snow Showers", 95: "Thunderstorm",
                    96: "Thunderstorm with Light Hail", 99: "Thunderstorm with Heavy Hail"
                },
                'ui': {
                    'city': 'City:',
                    'humidity': 'Humidity:',
                    'wind_speed': 'Wind Speed:',
                    'error': 'Error',
                    'city_not_found': 'City not found',
                    'weather_error': 'Failed to get weather',
                    'connection_error': 'Check internet connection',
                    'ms': 'm/s'
                }
            }
        }
        
        self.current_lang = 'ru'
        
        self.weather_icons = {
            0: "01d", 1: "01d", 2: "02d", 3: "04d",
            45: "50d", 48: "50d", 51: "09d", 53: "09d",
            55: "09d", 56: "13d", 57: "13d", 61: "10d",
            63: "10d", 65: "10d", 66: "13d", 67: "13d",
            71: "13d", 73: "13d", 75: "13d", 77: "13d",
            80: "09d", 81: "09d", 82: "09d", 85: "13d",
            86: "13d", 95: "11d", 96: "11d", 99: "11d"
        }
        
        self.title("Weather Clock")
        self.resizable(True, True)
        self.configure(bg='#000000')
        
        self.current_city = "Moscow"
        self.current_coords = {"lat": 55.7558, "lon": 37.6173}
        self.weather_icon = None
        
        self.create_widgets()
        self.bind('<Configure>', self.on_resize)
        self.update_time()
        self.update_weather()
    
    def change_language(self):
        self.current_lang = 'en' if self.current_lang == 'ru' else 'ru'
        self.lang_btn.config(text='RU' if self.current_lang == 'en' else 'EN')
        self.city_label.config(text=self.languages[self.current_lang]['ui']['city'])
        self.update_time()
        self.update_weather()
    
    def create_widgets(self):
        main_container = tk.Frame(self, bg='#000000')
        main_container.pack(fill="both", expand=True)
        
        # Кнопка переключения языка
        self.lang_btn = tk.Button(
            main_container,
            text='EN',
            command=self.change_language,
            font=('Arial', 12, 'bold'),
            bg='#1a237e',
            fg='white',
            relief=tk.FLAT,
            activebackground='#000051',
            activeforeground='white',
            width=3
        )
        self.lang_btn.pack(side="top", anchor="ne", padx=10, pady=5)
        
        time_date_frame = tk.Frame(main_container, bg='#000000')
        time_date_frame.pack(fill="x", pady=(20, 10))
        
        self.time_label = tk.Label(
            time_date_frame,
            font=('Arial', 100, 'bold'),
            bg='#000000',
            fg='white'
        )
        self.time_label.pack()
        
        self.date_label = tk.Label(
            time_date_frame,
            font=('Arial', 32),
            bg='#000000',
            fg='white'
        )
        self.date_label.pack(pady=(0, 10))
        
        weather_container = tk.Frame(main_container, bg='#000000')
        weather_container.pack(fill="both", expand=True)
        
        weather_main = tk.Frame(weather_container, bg='#000000')
        weather_main.pack(side="left", padx=30)
        
        self.weather_icon_label = tk.Label(
            weather_main,
            bg='#000000'
        )
        self.weather_icon_label.pack()
        
        self.temp_label = tk.Label(
            weather_main,
            font=('Arial', 72, 'bold'),
            bg='#000000',
            fg='white'
        )
        self.temp_label.pack()
        
        self.weather_desc_label = tk.Label(
            weather_main,
            font=('Arial', 36),
            bg='#000000',
            fg='white'
        )
        self.weather_desc_label.pack(pady=5)
        
        info_frame = tk.Frame(weather_container, bg='#000000')
        info_frame.pack(side="right", padx=30)
        
        self.humidity_label = tk.Label(
            info_frame,
            font=('Arial', 28),
            bg='#000000',
            fg='white'
        )
        self.humidity_label.pack(pady=5)
        
        self.wind_label = tk.Label(
            info_frame,
            font=('Arial', 28),
            bg='#000000',
            fg='white'
        )
        self.wind_label.pack(pady=5)
        
        city_frame = tk.Frame(main_container, bg='#000000')
        city_frame.pack(side="bottom", pady=20)
        
        self.city_label = tk.Label(
            city_frame,
            text=self.languages[self.current_lang]['ui']['city'],
            font=('Arial', 16, 'bold'),
            bg='#000000',
            fg='white'
        )
        self.city_label.pack(side="left", padx=5)
        
        self.city_entry = tk.Entry(
            city_frame,
            font=('Arial', 16),
            width=15,
            bg='#1a1a1a',
            fg='white',
            insertbackground='white'
        )
        self.city_entry.insert(0, self.current_city)
        self.city_entry.pack(side="left", padx=5)
        
        self.change_city_btn = tk.Button(
            city_frame,
            text="✓",
            command=self.change_city,
            font=('Arial', 16),
            bg='#1a237e',
            fg='white',
            relief=tk.FLAT,
            activebackground='#000051',
            activeforeground='white',
            width=2
        )
        self.change_city_btn.pack(side="left", padx=5)
    
    def update_time(self):
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        
        weekday = self.languages[self.current_lang]['weekdays'][now.weekday()]
        day = now.day
        month = self.languages[self.current_lang]['months'][now.month]
        year = now.year
        
        if self.current_lang == 'en':
            date_str = f"{weekday}, {month} {day}, {year}"
        else:
            date_str = f"{weekday}, {day} {month} {year}"
        
        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)
        
        self.after(1000, self.update_time)
    
    def update_weather(self):
        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.current_coords['lat']}&longitude={self.current_coords['lon']}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m&temperature_unit=celsius"
            response = requests.get(url)
            
            if response.status_code != 200:
                self.temp_label.config(text=self.languages[self.current_lang]['ui']['error'])
                self.weather_desc_label.config(text=self.languages[self.current_lang]['ui']['weather_error'])
                return
            
            data = response.json()
            current = data['current_weather']
            current_hour = datetime.datetime.now().hour
            
            temp = round(current['temperature'])
            weather_code = current['weathercode']
            wind_speed = round(current['windspeed'])
            humidity = data['hourly']['relativehumidity_2m'][current_hour]
            
            weather_desc = self.languages[self.current_lang]['weather'].get(weather_code, "Unknown")
            
            icon_code = self.weather_icons.get(weather_code, "01d")
            icon = self.get_weather_icon(icon_code)
            if icon:
                self.weather_icon = icon
                self.weather_icon_label.config(image=self.weather_icon)
            
            self.temp_label.config(text=f"{temp}°C")
            self.weather_desc_label.config(text=weather_desc)
            self.humidity_label.config(text=f"{self.languages[self.current_lang]['ui']['humidity']} {humidity}%")
            self.wind_label.config(text=f"{self.languages[self.current_lang]['ui']['wind_speed']} {wind_speed} {self.languages[self.current_lang]['ui']['ms']}")
            
        except requests.exceptions.RequestException:
            self.temp_label.config(text=self.languages[self.current_lang]['ui']['error'])
            self.weather_desc_label.config(text=self.languages[self.current_lang]['ui']['connection_error'])
        except Exception as e:
            self.temp_label.config(text=self.languages[self.current_lang]['ui']['error'])
            self.weather_desc_label.config(text=str(e))
        
        self.after(1800000, self.update_weather)
    
    def get_city_coordinates(self, city_name):
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
            headers = {'User-Agent': 'WeatherClock/1.0'}
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data:
                return {
                    "lat": float(data[0]["lat"]),
                    "lon": float(data[0]["lon"])
                }
            return None
        except:
            return None
    
    def change_city(self):
        new_city = self.city_entry.get().strip()
        if new_city:
            coords = self.get_city_coordinates(new_city)
            if coords:
                self.current_coords = coords
                self.update_weather()
            else:
                self.temp_label.config(text=self.languages[self.current_lang]['ui']['error'])
                self.weather_desc_label.config(text=self.languages[self.current_lang]['ui']['city_not_found'])
    
    def on_resize(self, event):
        width = self.winfo_width()
        height = self.winfo_height()
        
        time_size = min(width // 10, height // 6)
        date_size = min(width // 25, height // 15)
        temp_size = min(width // 12, height // 8)
        desc_size = min(width // 22, height // 15)
        info_size = min(width // 30, height // 20)
        input_size = min(width // 50, height // 35)
        
        self.time_label.config(font=('Arial', time_size, 'bold'))
        self.date_label.config(font=('Arial', date_size))
        self.temp_label.config(font=('Arial', temp_size, 'bold'))
        self.weather_desc_label.config(font=('Arial', desc_size))
        self.humidity_label.config(font=('Arial', info_size))
        self.wind_label.config(font=('Arial', info_size))
        self.city_label.config(font=('Arial', input_size, 'bold'))
        self.city_entry.config(font=('Arial', input_size))
        self.change_city_btn.config(font=('Arial', input_size))
        
        icon_size = min(width // 10, height // 7)
        if hasattr(self, 'current_icon_code'):
            icon = self.get_weather_icon(self.current_icon_code, icon_size)
            if icon:
                self.weather_icon = icon
                self.weather_icon_label.config(image=self.weather_icon)
    
    def get_weather_icon(self, icon_code, size=80):
        try:
            url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            image = Image.open(io.BytesIO(raw_data))
            image = image.resize((size, size), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except:
            return None

if __name__ == "__main__":
    app = WeatherClock()
    app.mainloop() 
