import sys
import os
from dotenv import load_dotenv
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon



class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize UI components
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        # Set up window properties
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("static/weather_app_icon.png"))
        self.setGeometry(1100, 500, 800, 800)

        # Layout and styling
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        # Align text and set styles
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Set styles for widgets
        self.setStyleSheet(
            """
            QWidget {
                background-color: #e6f7ee;
            }
            QLabel, QLineEdit, QPushButton {
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#city_label {
                font-size: 50px;
                font-weight: 600;
                color: #4169E1;
            }
            QLineEdit#city_input {
                font-size: 50px;
                padding: 10px;
                border: 2px solid #4169E1;
                border-radius: 10px;
                color: #4169E1;
                font-weight: bold;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                padding: 10px;
                background-color: #4169E1;
                color: white;
                border-radius: 10px;
                border: none;
                height: 60px;
            }
            QPushButton#get_weather_button:hover {
                background-color: #1138ad;
            }
            QLabel#temperature_label {
                font-size: 50px;
                color: #4169E1;
                margin-top: 20px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                margin-top: 20px;
            }
            QLabel#description_label {
                font-size: 60px;
                color: #4169E1;
                bottom: 20px;
                font-weight: 400;
            }
        """
        )

        # Connect button click to get_weather method
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        load_dotenv()
        # Get city name and make API request
        api_key = os.getenv("WEATHER_API_KEY") # Paste your API KEY here
        city = self.city_input.text().strip().title()
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        )

        try:
            # Handle API response
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            # Handle different HTTP errors
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("Not Found\nCity not found")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case __:
                    self.display_error(f"HTTP error occurred\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            # Handle other request exceptions
            self.display_error(f"Requests Error\n{req_error}")

        except Exception as exp:
            self.display_error(f"An unexpected error occurred:\n{exp}")

    def display_error(self, message):
        # Display error message in UI
        self.temperature_label.setStyleSheet("font-size: 35px;" "font-weight: bold;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        # Display weather data in UI
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_c = int(data["main"]["temp"] - 273.15)
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"].capitalize()
        self.temperature_label.setText(f"{temperature_c}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        # Get appropriate emoji for weather condition
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌥️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "🌚"


# Main entry point to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

# Author: Yuuto Akihiro
