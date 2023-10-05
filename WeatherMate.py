from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
from PIL import Image, ImageTk
import requests
import json
import pytz

# Initialize tkinter
root = Tk()
root.title("Weather Mate")
root.geometry("900x500+300+200")
root.resizable(False, False)
root.config(background="white")

# Define function to fetch weather data from API
def get_weather_data():
    API_KEY = "9eb0f81c409efd303701273089798c84"
    LOCATION = textfield.get()  # Retrieve user input from the textfield
    geolocator = Nominatim(user_agent="geoapiExercises")
    locate_coordinates = geolocator.geocode(LOCATION)

    tz = TimezoneFinder()
    if locate_coordinates is not None:
        result = tz.timezone_at(lng=locate_coordinates.longitude, lat=locate_coordinates.latitude)
        calculate_tz = pytz.timezone(result)
        local_time = datetime.now(calculate_tz)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
    else:
        messagebox.showerror("Location Error", "Unable to retrieve location information. Please enter a valid location.")
        return

    WEATHER_API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={API_KEY}&units=metric"
    response = requests.get(WEATHER_API_URL)
    if response.status_code == 200:
        data = json.loads(response.text)

        # Extract relevant data from API response
        temperature = int(data['main']['temp'])
        description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        precipitation = data.get('rain', {}).get('1h', 0)

        temp.config(text=str(temperature) + "°C")
        desc.config(text=description + " | FEELS LIKE " + str(temperature) + "°C")

        hum.config(text=humidity)
        press.config(text=pressure)
        windy.config(text=wind)
        prec.config(text=precipitation)
    else:
        messagebox.showerror("Forecast Retrieval Failed", "Failed to retrieve weather forecast. Please try again later.")

    # Schedule the next weather data retrieval after 3 hours
    root.after(3 * 60 * 60 * 1000, get_weather_data)

# Create the search box for the user to enter the location
SearchBar = Image.open("search_bar.png")
resized_image = SearchBar.resize((800, 50), Image.LANCZOS)
SearchBar = ImageTk.PhotoImage(resized_image)
thisSearch = Label(image=SearchBar)
thisSearch.place(x=50, y=50)

textfield = tk.Entry(root, justify="center", width=30, font=("Helvetica", 20, "bold"), border=0)
textfield.place(x=50, y=60)
textfield.focus()

img = Image.open("search_icon.png")
resized_image = img.resize((35, 35), Image.LANCZOS)
SearchIcon = ImageTk.PhotoImage(resized_image)
thisIcon = Button(image=SearchIcon, borderwidth=0, cursor="hand1", command=get_weather_data, background="white")
thisIcon.place(x=770, y=60)

# App logo
Logo = Image.open("logo.png")
resized_image = Logo.resize((100, 100), Image.LANCZOS)
Logo = ImageTk.PhotoImage(resized_image)
thisLogo = Label(image=Logo)
thisLogo.place(x=10, y=50)

# Frame for displaying weather data
FrameImg= Image.open("frame.png")
resized_image = FrameImg.resize((1500, 600), Image.LANCZOS)
FrameImg = ImageTk.PhotoImage(resized_image)
thisFrame = Label(image=FrameImg)
thisFrame.place(x=0, y=170)

# Display the time
clock = Label(root, font=("Helvetica", 20), fg="black", background="white")
clock.place(x=30, y=20)

# Labels to display weather data
name = Label(root, text="TODAY'S FORECAST", font=("Arial", 20, "bold"), fg="black", background="white")
name.place(x=250, y=130)

temp = Label(root, font=("Arial", 80, "bold"), fg="black", background="white")
temp.place(x=450, y=210)
desc = Label(root, font=("Arial", 20, "bold"), fg="black", background="white")
desc.place(x=450, y=340)

hum_label = Label(root, text="HUMIDITY", font=("Arial", 20, "bold"), fg="white", background="#38b6ff")
hum_label.place(x=120, y=200)
press_label = Label(root, text="PRESSURE", font=("Arial", 20, "bold"), fg="white", background="#38b6ff")
press_label.place(x=120, y=280)
wind_label = Label(root, text="WIND", font=("Arial", 20, "bold"), fg="white", background="#38b6ff")
wind_label.place(x=120, y=360)
prec_label = Label(root, text="PRECIPITATION", font=("Arial", 20, "bold"), fg="white", background="#38b6ff")
prec_label.place(x=120, y=440)

hum = Label(root, font=("Arial", 15, "bold"), fg="white", background="#38b6ff")
hum.place(x=360, y=210)
press = Label(root, font=("Arial", 15, "bold"), fg="white", background="#38b6ff")
press.place(x=360, y=290)
windy = Label(root, font=("Arial", 15, "bold"), fg="white", background="#38b6ff")
windy.place(x=360, y=370)
prec = Label(root, font=("Arial", 15, "bold"), fg="white", background="#38b6ff")
prec.place(x=360, y=450)

# Call the get_weather_data function initially
get_weather_data()

# Start the tkinter main event loop
root.mainloop()
