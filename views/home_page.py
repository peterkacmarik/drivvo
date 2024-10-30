import flet as ft
from locales.language_manager import LanguageManager
from locales.translations import get_translation
from components.logo import page_logo
from components.buttons import logout_button

class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/")
        self.page = page
        self.bgcolor = ft.colors.WHITE
        self.scroll = ft.ScrollMode.AUTO
        self.fullscreen_dialog = True
        
        self.current_language = LanguageManager.get_current_language()
        self.translation = get_translation(self.current_language)
        self.init_components()
        
        # Snack bar
        self.snack_bar = ft.SnackBar(
            content=ft.Text(""),
            show_close_icon=True
        )
        self.page.overlay.append(self.snack_bar)
        
        
    def init_components(self):
        # Tvorba prepínača jazyka a prihlasovacieho formulára
        self.language_switch_button = self.language_switch()
        self.page_logo = page_logo()
        self.logout_button = logout_button(self.translation, self.page)
        
        # Pridanie komponentov do hlavnej časti stránky
        self.controls = [
            ft.Container(
                alignment=ft.alignment.center,
                padding=ft.padding.only(20, 30, 20, 0),
                content=ft.Column(
                    controls=[
                        self.language_switch_button,
                        self.page_logo,
                        self.logout_button,
                    ]
                )
            )
        ]
    
    # def validate_fields(self, e=None):
    #     # Získame hodnoty z polí
    #     email = self.login_fields.content.controls[0].value
    
    #     # Aktivujeme tlačidlo len ak sú obe polia vyplnené
    #     if email:
    #         self.login_button.content.disabled = False
    #     else:
    #         self.login_button.content.disabled = True
            
    #     # Aktualizujeme UI
    #     self.login_button.update()
    
    
    def language_switch(self):
        return ft.Container(
            # padding=ft.padding.only(left=20),
            alignment=ft.Alignment(x=-1.0, y=0.0),
            content=ft.Dropdown(
                options=[
                    ft.dropdown.Option(
                        key="en", 
                        # text="English",
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Image(
                                        src="/icons/us.svg",
                                        width=24,
                                        height=24,
                                        fit=ft.ImageFit.CONTAIN,
                                        repeat=ft.ImageRepeat.NO_REPEAT,
                                    ),
                                    ft.Text("English"),
                                ]
                            )
                        ),
                    ),
                    ft.dropdown.Option(
                        key="sk", 
                        # text="Slovenčina"
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Image(
                                        src="/icons/sk.svg",
                                        width=24,
                                        height=24,
                                        fit=ft.ImageFit.CONTAIN,
                                        repeat=ft.ImageRepeat.NO_REPEAT,
                                    ),
                                    ft.Text("Slovenčina"),
                                ]
                            )
                        ),
                    ),
                    ft.dropdown.Option(
                        key="cs", 
                        # text="Čeština"
                        content=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Image(
                                        src="/icons/cz.svg",
                                        width=24,
                                        height=24,
                                        fit=ft.ImageFit.CONTAIN,
                                        repeat=ft.ImageRepeat.NO_REPEAT,
                                    ),
                                    ft.Text("Čeština"),
                                ]
                            )
                        ),
                    ),
                ],
                width=150,
                # padding=ft.padding.only(left=0),
                border=ft.InputBorder.NONE,
                value=self.current_language,
                border_radius=10,
                on_change=self.change_language
            )
        )
        
        
    def change_language(self, e):
        # Update the global language through the manager
        LanguageManager.set_language(e.control.value)
        # The update_language method will be called automatically through the subscription
    

    def did_mount(self):
        LanguageManager.subscribe(self.update_language)
        
        
    def will_unmount(self):
        LanguageManager.unsubscribe(self.update_language)
        
        
    def update_language(self):
        self.current_language = LanguageManager.get_current_language()
        self.translation = get_translation(self.current_language)
        self.update_ui()
        
        
    def update_ui(self):
        # Update all UI components with new translation
        self.controls.clear()
        self.init_components()
        self.page.update()
        
    
    def handle_forgot_password(self):
        self.page.go("/forgot-password")