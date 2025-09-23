import flet as ft
from db_connection import connect_db
import mysql.connector

def main(page: ft.Page):
    # Page settings
    page.title = "User Login"
    page.window_width = 400
    page.window_height = 350
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.AMBER_ACCENT

    # Title
    title = ft.Text(
        "User Login",
        size=20,
        weight=ft.FontWeight.BOLD,
        font_family="Arial",
        text_align=ft.TextAlign.CENTER,
        color=ft.Colors.BLACK,
    )

    # Username input
    username = ft.TextField(
        label="User name",
        label_style=ft.TextStyle(color=ft.Colors.BLACK),
        hint_text="Enter your user name",
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
        helper_text="This is your unique identifier",
        helper_style=ft.TextStyle(color=ft.Colors.BLACK),
        width=300,
        autofocus=True,
        icon="person",   # ✅ using string
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
        color=ft.Colors.BLACK,
    )

    # Password input
    password = ft.TextField(
        label="Password",
        label_style=ft.TextStyle(color=ft.Colors.BLACK),
        hint_text="Enter your password",
        hint_style=ft.TextStyle(color=ft.Colors.BLACK54),
        helper_text="This is your secret key",
        helper_style=ft.TextStyle(color=ft.Colors.BLACK),
        width=300,
        password=True,
        can_reveal_password=True,
        icon="lock",   # ✅ using string
        bgcolor=ft.Colors.LIGHT_BLUE_ACCENT,
        color=ft.Colors.BLACK,
    )

    # Dialog helpers
    def close_dialog(e):
        if page.dialog:
            page.dialog.open = False
            page.update()

    def show_dialog(dialog):
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Login logic
    def login_click(e):
        uname = username.value.strip()
        pword = password.value.strip()

        if not uname or not pword:
            invalid_dialog = ft.AlertDialog(
                title=ft.Text("Input Error", color=ft.Colors.BLACK),
                content=ft.Text(
                    "Please enter username and password",
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.BLACK,
                ),
                actions=[ft.TextButton("OK", on_click=close_dialog)],
                icon=ft.Icon(name="info", color=ft.Colors.BLUE),  # ✅ string icon
            )
            show_dialog(invalid_dialog)
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username=%s AND password=%s",
                (uname, pword),
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                success_dialog = ft.AlertDialog(
                    title=ft.Text("Login Successful", color=ft.Colors.BLACK),
                    content=ft.Text(
                        f"Welcome, {uname}!",
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    actions=[ft.TextButton("OK", on_click=close_dialog)],
                    icon=ft.Icon(name="check_circle", color=ft.Colors.GREEN),  # ✅
                )
                show_dialog(success_dialog)
            else:
                failure_dialog = ft.AlertDialog(
                    title=ft.Text("Login Failed", color=ft.Colors.BLACK),
                    content=ft.Text(
                        "Invalid username or password",
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    actions=[ft.TextButton("OK", on_click=close_dialog)],
                    icon=ft.Icon(name="error", color=ft.Colors.RED),  # ✅
                )
                show_dialog(failure_dialog)

        except mysql.connector.Error as err:
            database_error_dialog = ft.AlertDialog(
                title=ft.Text("Database Error", color=ft.Colors.BLACK),
                content=ft.Text(
                    f"An error occurred while connecting to the database:\n{err}",
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.BLACK,
                ),
                actions=[ft.TextButton("OK", on_click=close_dialog)],
                icon=ft.Icon(name="warning", color=ft.Colors.AMBER),  # ✅
            )
            show_dialog(database_error_dialog)

    # Login button
    login_btn = ft.ElevatedButton(
        text="Login",
        on_click=login_click,
        width=100,
        icon="arrow_forward",  # ✅ string icon
    )

    # Layout
    page.add(
        title,
        ft.Container(
            content=ft.Column([username, password], spacing=20),
            alignment=ft.alignment.center,
        ),
        ft.Container(
            content=login_btn,
            alignment=ft.alignment.center_right,
            margin=ft.margin.only(0, 20, 40, 0),
        ),
    )


# Run the app
ft.app(target=main)
