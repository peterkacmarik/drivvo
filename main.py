import flet as ft
# from locales.language_manager import LanguageManager

from views.login_page import LoginView
from views.home_page import HomeView
from views.register_page import RegisterView
from views.forgot_password import ForgotPasswordView


def main(page: ft.Page):
    # LanguageManager()
    # page.window.always_on_top = True
    page.title = "Drivvo"
    page.fonts = {
        "Roboto": "/fonts/Roboto/Roboto-Regular.ttf",
        "OpenSans": "/fonts/Open_Sans/OpenSans-VariableFont_wdth,wght.ttf",
        "ABeeZee": "/fonts/ABeeZee/ABeeZee-Regular.ttf",
        "Roboto_Slap": "/fonts/Roboto_Slab/RobotoSlab-VariableFont_wght.ttf",
    }
    page.theme = ft.Theme(font_family="Roboto")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.adaptive = True
    page.window.width = 400
    page.window.height = 800
    page.update()
        
    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(HomeView(page))
        if page.route == "/login":
            page.views.append(LoginView(page))
        elif page.route == "/register":
            page.views.append(RegisterView(page))
        elif page.route == "/forgot-password":
            page.views.append(ForgotPasswordView(page))

        page.update()

    page.on_route_change = route_change
    page.go("/login")

ft.app(
    target=main, 
    view=ft.AppView.WEB_BROWSER,
    web_renderer=ft.WebRenderer.CANVAS_KIT,
    assets_dir="assets", 
    # port=60235,
    # host="5d9ece8c-4fff-4720-9eaf-5f43a3e26d2d-00-1hj5fujeorajb.kirk.replit.dev"
    # export_asgi_app=True
)




