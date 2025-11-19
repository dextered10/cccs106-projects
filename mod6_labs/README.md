# Weather Application - Module 6 Lab

## Student Information
- **Name**: Marc Dexter Sael
- **Student ID**: 231004229
- **Course**: CCCS 106
- **Section**: BSCS 3B

## Project Overview
This weather app lets you quickly check the current weather in any city. It shows the temperature, weather condition, humidity, and wind speed in a simple and clean interface. You can also switch between Celsius and Fahrenheit, and the background color changes depending on the weather—like yellow for sunny or blue for rainy. It even uses emojis/icons to match the forecast. Overall, it’s a straightforward and easy-to-use app that makes checking the weather feel more fun and visual.

## Features Implemented

### Base Features
- [✓] City search functionality
- [✓] Current weather display
- [✓] Temperature, humidity, wind speed
- [✓] Weather icons
- [✓] Error handling
- [✓] Modern UI with Material Design

### Enhanced Features
1. [Temperature Unit Toggle]

- This feature lets users switch between Celsius and Fahrenheit when viewing the temperature.

- I chose this feature because people in different regions prefer different temperature units, and it improves usability.

- The challenge was updating the displayed temperature without refetching data from the API. I solved this by storing the current temperature and   “feels like” values in variables and recalculating them when the toggle is switched.

2. [Dynamic Weather Background & Icons]

- This feature changes the background color and shows a matching emoji/icon based on the current weather condition.

- I chose this feature to make the app visually appealing and give users a quick, intuitive sense of the weather.

- The challenge was mapping all weather descriptions to colors and icons and making the transition smooth. I solved it by creating a dictionary of weather conditions to colors/emojis and adding smooth animations for the background change.

## Screenshots
![alt text](<Screenshot 2025-11-18 162355.png>)
![alt text](<Screenshot 2025-11-18 162428.png>)
## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/<username>/cccs106-projects.git
cd cccs106-projects/mod6_labs

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your OpenWeatherMap API key to .env


