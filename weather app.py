import tkinter as tk
from tkinter import messagebox
import requests

# Function to get weather data
def get_weather(city):
    api_key = "6c279e1740d738218bdcbaa4289f73fb" # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url)
        response.raise_for_status()
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            wind = data["wind"]
            weather = data["weather"][0]
            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]
            weather_description = weather["description"]
            weather_info = (f"Temperature: {temperature}°C\n"
                             f"Pressure: {pressure} hPa\n"
                             f"Humidity: {humidity}%\n"
                             f"Wind Speed: {wind_speed} m/s\n"
                             f"Description: {weather_description}")
        else:
            weather_info = "City Not Found"
        return weather_info
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Function to display weather data
def show_weather(event=None):
    city = city_entry.get()
    if city:
        weather = get_weather(city)
        result_label.config(text=weather)
    else:
        messagebox.showerror("Input Error", "Please enter a city name.")

# Create the main window
root = tk.Tk()
root.title("Weather App")

city_label = tk.Label(root, text="Enter city:")
city_label.pack(pady=10)

city_entry = tk.Entry(root)
city_entry.pack(pady=10)
city_entry.bind("<Return>", show_weather)  # Bind the Enter key to show_weather

get_weather_button = tk.Button(root, text="Get Weather", command=show_weather)
get_weather_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=20)

# Run the application
root.mainloop()