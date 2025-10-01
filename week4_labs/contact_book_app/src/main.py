import flet as ft
from database import init_db
from app_logic import display_contacts, add_contact

def main(page: ft.Page):
    page.title = "Contact Book"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600
    page.theme_mode = ft.ThemeMode.LIGHT  # default theme
    page.bgcolor = ft.Colors.PINK_50      # light pink for light mode

    # Database connection
    db_conn = init_db()

    # ---------------- Inputs ----------------
    name_input = ft.TextField(label="Name", width=350)
    phone_input = ft.TextField(label="Phone", width=350)
    email_input = ft.TextField(label="Email", width=350)
    inputs = (name_input, phone_input, email_input)

    # ---------------- Search ----------------
    search_input = ft.TextField(
        label="Search Contacts",
        width=350,
        on_change=lambda e: display_contacts(
            page, contacts_list_view, db_conn, search_term=search_input.value
        ),
    )

    # ---------------- Contacts List ----------------
    contacts_list_view = ft.ListView(expand=1, spacing=10, auto_scroll=True)

    # ---------------- Add Contact Button ----------------
    def handle_add_contact(e):
        error_found = False

        # Validate Name
        if not name_input.value.strip():
            name_input.error_text = "Name cannot be empty"
            error_found = True
        else:
            name_input.error_text = None

        # Validate Phone
        if not phone_input.value.strip():
            phone_input.error_text = "Phone cannot be empty"
            error_found = True
        else:
            phone_input.error_text = None

        # Validate Email
        if not email_input.value.strip():
            email_input.error_text = "Email cannot be empty"
            error_found = True
        elif "@" not in email_input.value:
            email_input.error_text = "Email must contain @"
            error_found = True
        else:
            email_input.error_text = None
            
        page.update()

        # If any error, stop
        if error_found:
            return

        # Otherwise, add contact
        add_contact(page, inputs, contacts_list_view, db_conn)

    add_button = ft.ElevatedButton(
        text="Add Contact",
        on_click=handle_add_contact
    )

    # ---------------- Dark Mode Toggle ----------------
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = ft.Colors.PINK_900  # dark pink
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = ft.Colors.PINK_50   # light pink
        page.update()

    theme_switch = ft.Switch(label="Dark Mode", on_change=toggle_theme)

    # ---------------- Page Layout ----------------
    page.add(
        ft.Column(
            [
                ft.Text(
                    "📒 Contact Book",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(),
                ft.Text("Enter Contact Details:", size=20, weight=ft.FontWeight.BOLD),
                name_input,
                phone_input,
                email_input,
                add_button,
                ft.Divider(),
                theme_switch,
                ft.Text("Contacts:", size=20, weight=ft.FontWeight.BOLD),
                search_input,
                contacts_list_view,
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # Load contacts at startup
    display_contacts(page, contacts_list_view, db_conn)

if __name__ == "__main__":
    ft.app(target=main)
