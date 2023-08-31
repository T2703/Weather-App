import requests
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

API_KEY = "be3aad138a405d894a4f46ebfa0d3755"
API_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

# Gets the data of the weather from the current city typed in.
# Parameters: city (string) The name of the city.
# Returns: Dict a dictonary containing the weather data.
def get_weather_data(city):
    url = API_URL.format(city, API_KEY)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any request errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error occurred while fetching weather data:", e)
        return None

# Converts to fahrenheit. 451
# Parameters: kelvin_temp we are converting this and making it more reasonable.
def convert_to_fahrenheit(kelvin_temp):
    celsius_temp = kelvin_temp - 273.15
    return (celsius_temp * 9/5) + 32

# Display weather information to the user.
# Parameters: weather_data (dict): A dictionary containing weather data fetched from the API.
def display_weather():
    city = city_entry.get()
    weather_data = get_weather_data(city)
    # If the weather data has the data (true)
    if weather_data:
        # Fetch weather icon code from the API response
        weather_icon_code = weather_data["weather"][0]["icon"]
        weather_icon_url = f"http://openweathermap.org/img/w/{weather_icon_code}.png"

        # Download the weather icon image
        icon_response = requests.get(weather_icon_url, stream=True)
        icon_response.raise_for_status()

        # Save the icon image to a temporary file
        icon_filename = "weather_icon.png"
        with open(icon_filename, "wb") as icon_file:
            for chunk in icon_response.iter_content(chunk_size=8192):
                icon_file.write(chunk)

        # Load the icon image using PIL and convert it to a PhotoImage
        weather_icon_image = Image.open(icon_filename)

        # Resize the image to the desired size (e.g., 50x50 pixels)
        desired_size = (120, 120)
        weather_icon_image = weather_icon_image.resize(desired_size)

        # Convert the PIL image to a PhotoImage and assign it to the label
        weather_icon_photo = ImageTk.PhotoImage(weather_icon_image)
        weather_icon_label.config(image=weather_icon_photo)
        weather_icon_label.image = weather_icon_photo

        # Update other labels with weather data
        weather_main = weather_data["weather"][0]["main"]
        temperature_celsius = weather_data["main"]["temp"]
        temperature_fahrenheit = convert_to_fahrenheit(temperature_celsius)
        humidity = weather_data["main"]["humidity"]

        weather_label.config(text=f"Weather: {weather_main}")
        temp_label.config(text=f"Temperature: {temperature_fahrenheit:.2f}°F")
        humidity_label.config(text=f"Humidity: {humidity}%")
        city_search_label.config(text=f"Location: {city}")

        # Delete the temporary icon file
        os.remove(icon_filename)

    # Cannot find the weather data because not enough (false)
    else:
        messagebox.showerror("Error", "Weather data not available.")

def handle_key_event(event):
    if event.keysym == 'Return':
        # Do something when the Enter key is pressed
        display_weather()
        city_entry.delete(0, tk.END)  # Clear the entry field after fetching weather data

# Create the main application window
app = tk.Tk()
app.title("Weather App")
app.geometry("400x500")

# Make the window not resizable
app.resizable(False, False)

# Get the current working directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the full file path for the background image
background_image_path = os.path.join(current_directory, "background.png")

# Construct the full file path for the search image
search_image_path = os.path.join(current_directory, "search.png")

# Check if the image file exists at the given path
if os.path.exists(background_image_path) and os.path.exists(search_image_path):
    background_image = tk.PhotoImage(file=background_image_path)

    # Create a label to display the background image
    background_label = tk.Label(app, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Load the search image using PIL and convert it to a PhotoImage
    search_image = Image.open(search_image_path)

    # Resize the search image to the desired size (e.g., 100x100 pixels)
    desired_size = (20, 20)
    search_image = search_image.resize(desired_size)

    # Convert the PIL image to a PhotoImage with transparency
    search_image_photo = ImageTk.PhotoImage(search_image)

    # Create a label to display the transparent search image
    search_label = tk.Label(app, image=search_image_photo, bg="white")
    search_label.place(x=270, y=31)  # Adjust the position as needed

    # Keep a reference to the PhotoImage to avoid garbage collection
    search_label.image = search_image_photo

else:
    # If the image file is not found, print an error message
    print("Error: background.png or search.png not found in the current directory")

# Create and place the widgets
city_label = tk.Label(app, text="Enter the name of the city:", font = ("Times New Roman", 10), fg = "black")
city_label.pack(pady = 5)
city_entry = tk.Entry(app)
city_entry.pack(pady = 5)

get_weather_button = tk.Button(app, text = "Get Weather", font = ("Times New Roman", 10), fg = "black", command = display_weather)
get_weather_button.pack(pady=10)
# If the user presses the enter key
app.bind('<Return>', handle_key_event) 

# Create and place the widgets
city_search_label = tk.Label(app, text="Waiting for location.", bg = "white", font = ("Times New Roman", 14), fg = "black")
city_search_label.pack(pady=5)

weather_label = tk.Label(app, text="Waiting for data.", bg = "white", font = ("Times New Roman", 14), fg = "black")
weather_label.pack(pady=5)

temp_label = tk.Label(app, text = "Waiting for data.", bg = "white", font = ("Times New Roman", 14), fg = "black")
temp_label.pack(pady=5)

humidity_label = tk.Label(app, text = "Waiting for data.", bg = "white", font = ("Times New Roman", 14), fg = "black")
humidity_label.pack(pady=5)

weather_icon_label = tk.Label(app)
weather_icon_label.pack(pady=5)

app.mainloop()