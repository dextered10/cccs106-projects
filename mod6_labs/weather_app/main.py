# main.py
"""Weather Application using Flet v0.28.3"""

import flet as ft
from weather_service import WeatherService
from config import Config


class WeatherApp:
    """Main Weather Application class."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.weather_service = WeatherService()

        # ===== TEMPERATURE TOGGLE VARIABLES =====
        self.current_unit = "metric"
        self.current_temp = None
        self.current_feels_like = None

        self.setup_page()
        self.build_ui()
    
    def setup_page(self):
        """Configure page settings."""
        self.page.title = Config.APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window.width = Config.APP_WIDTH
        self.page.window.height = Config.APP_HEIGHT
        self.page.window.resizable = False
        
        # Center the window on desktop
        self.page.window.center()
    
    def build_ui(self):
        """Build the user interface."""
        # Title
        self.title = ft.Text(
            "Weather App",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )
        
        # City input field
        self.city_input = ft.TextField(
            label="Enter city name",
            hint_text="e.g., London, Tokyo, New York",
            border_color=ft.Colors.BLUE_400,
            prefix_icon=ft.Icons.LOCATION_CITY,
            autofocus=True,
            on_submit=self.on_search,
        )
        
        # Search button
        self.search_button = ft.ElevatedButton(
            "Get Weather",
            icon=ft.Icons.SEARCH,
            on_click=self.on_search,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
            ),
        )

        # Temperature switch
        self.unit_toggle = ft.Switch(
            label="Show in Fahrenheit",
            value=False,
            on_change=self.toggle_units
        )
        
        # Weather container
        self.weather_container = ft.Container(
            visible=False,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=20,
            animate=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),  # SMOOTH TRANSITION
        )
        
        # Error message
        self.error_message = ft.Text(
            "",
            color=ft.Colors.RED_700,
            visible=False,
        )
        
        # Loading indicator
        self.loading = ft.ProgressRing(visible=False)
        
        # Add all components to page
        self.page.add(
            ft.Column(
                [
                    self.title,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.city_input,
                    self.search_button,
                    self.unit_toggle,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    self.loading,
                    self.error_message,
                    self.weather_container,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )
    
    def on_search(self, e):
        self.page.run_task(self.get_weather)
    
    async def get_weather(self):
        city = self.city_input.value.strip()
        
        if not city:
            self.show_error("Please enter a city name")
            return
        
        # Reset UI
        self.loading.visible = True
        self.error_message.visible = False
        self.weather_container.visible = False
        self.page.update()
        
        try:
            data = await self.weather_service.get_weather(city)
            self.display_weather(data)
            
        except Exception as e:
            self.show_error(str(e))
        
        finally:
            self.loading.visible = False
            self.page.update()
    
    def display_weather(self, data: dict):
        """Display weather information."""
        city_name = data.get("name", "Unknown")
        country = data.get("sys", {}).get("country", "")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "").title()
        icon_code = data.get("weather", [{}])[0].get("icon", "01d")
        wind_speed = data.get("wind", {}).get("speed", 0)

        # Store for unit toggle
        self.current_temp = temp
        self.current_feels_like = feels_like

        # ===== NEW: Weather emojis =====
        weather_emoji = self.get_weather_icon(description)

        # ===== NEW: Animate background color based on condition =====
        self.weather_container.bgcolor = self.get_weather_color(description)

        # Build weather display
        self.weather_container.content = ft.Column(
            [
                ft.Text(
                    f"{city_name}, {country}",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                
                # Icon + emoji
                ft.Row(
                    [
                        ft.Image(
                            src=f"https://openweathermap.org/img/wn/{icon_code}@2x.png",
                            width=100,
                            height=100,
                        ),
                        ft.Text(
                            f"{weather_emoji} {description}",
                            size=20,
                            italic=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                
                ft.Text(
                    f"{temp:.1f}°C",
                    size=48,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                ),
                
                ft.Text(
                    f"Feels like {feels_like:.1f}°C",
                    size=16,
                    color=ft.Colors.GREY_700,
                ),
                
                ft.Divider(),
                
                ft.Row(
                    [
                        self.create_info_card(
                            ft.Icons.WATER_DROP,
                            "Humidity",
                            f"{humidity}%"
                        ),
                        self.create_info_card(
                            ft.Icons.AIR,
                            "Wind Speed",
                            f"{wind_speed} m/s"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        
        self.weather_container.visible = True
        self.error_message.visible = False
        self.page.update()
    
    def create_info_card(self, icon, label, value):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=30, color=ft.Colors.BLUE_700),
                    ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ft.Text(
                        value,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            width=150,
        )
    
    def show_error(self, message: str):
        self.error_message.value = f"❌ {message}"
        self.error_message.visible = True
        self.weather_container.visible = False
        self.page.update()

    
    def get_weather_icon(self, description):
        desc = description.lower()
        if "clear" in desc: return "☀️"
        if "cloud" in desc: return "☁️"
        if "rain" in desc: return "🌧️"
        if "drizzle" in desc: return "🌦️"
        if "thunder" in desc: return "⛈️"
        if "snow" in desc: return "❄️"
        if "mist" in desc or "fog" in desc: return "🌫️"
        return "🌍"

    def get_weather_color(self, description):
        desc = description.lower()
        if "clear" in desc: return "#FFEB3B"  # yellow
        if "cloud" in desc: return "#B0BEC5"  # greyish-blue
        if "rain" in desc: return "#64B5F6"   # blue
        if "drizzle" in desc: return "#81D4FA"
        if "thunder" in desc: return "#9575CD" # purple
        if "snow" in desc: return "#E0E0E0"
        if "mist" in desc or "fog" in desc: return "#CFD8DC"
        return "#FFFFFF"

  
    def toggle_units(self, e):
        if self.current_temp is None:
            return

        if self.unit_toggle.value:
            self.current_unit = "imperial"
            self.current_temp = (self.current_temp * 9/5) + 32
            self.current_feels_like = (self.current_feels_like * 9/5) + 32
        else:
            self.current_unit = "metric"
            self.current_temp = (self.current_temp - 32) * 5/9
            self.current_feels_like = (self.current_feels_like - 32) * 5/9

        self.update_temp_display()

    def update_temp_display(self):
        if not self.weather_container.visible:
            return

        unit = "°F" if self.current_unit == "imperial" else "°C"
        self.weather_container.content.controls[2].value = f"{self.current_temp:.1f}{unit}"
        self.weather_container.content.controls[3].value = (
            f"Feels like {self.current_feels_like:.1f}{unit}"
        )
        self.page.update()


def main(page: ft.Page):
    WeatherApp(page)


if __name__ == "__main__":
    ft.app(target=main)
