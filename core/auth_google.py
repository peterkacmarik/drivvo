from core.supa_base import get_supabese_client
from supabase import Client

import os
from dotenv import load_dotenv
from typing import Dict, Optional
from datetime import datetime
import flet as ft

load_dotenv()


def handle_google_login(e, page: ft.Page):
    try:
        # Vytvorenie a zobrazenie dialógu
        dialog = create_auth_dialog(page)
        # page.dialog = dialog
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
        
    except Exception as e:
        page.open(
            ft.SnackBar(content=ft.Text(f"Chyba: {str(e)}"))
        )


def create_auth_dialog(page: ft.Page):
    def close_dialog(e):
        dialog.open = False
        page.update()
        
    auth_url: str = get_google_auth_url(page)
    if not auth_url:
        return None

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(value="Google Prihlásenie", size=16),
        content=ft.Container(
            width=600,
            height=600,
            content=ft.WebView(
                javascript_enabled=True,
                url=auth_url,
                expand=True,
                on_page_started=lambda e: print("Page started loading"),
                on_page_ended=lambda e: handle_auth_callback(e, page, dialog) if "callback" in e.data else None,
                on_web_resource_error=lambda e: print("Page error:", e.data),
            )
        ),
        actions=[
            ft.TextButton("Zrušiť", on_click=close_dialog)
        ]
    )
    return dialog


def get_google_auth_url(page: ft.Page) -> str:
    try:
        supabase = get_supabese_client()
        
        # Nastavenie callback URL na špeciálnu cestu
        # callback_url = f"{page.window_url_origin}/callback"
        # callback_url = "https://rtcgmlenucvulsbhitui.supabase.co/auth/v1/callback"  # upravte port podľa vašej aplikácie http://127.0.0.1:51824/login
        
        auth_response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            # "options": {
                # "redirect_to": callback_url,
                # "scopes": "email profile"
            # }
        })
        
        if auth_response and auth_response.url:
            return auth_response.url
        else:
            raise Exception("Nepodarilo sa získať prihlasovaciu URL")
            
    except Exception as e:
        page.open(
            ft.SnackBar(content=ft.Text(f"Chyba: {str(e)}"))
        )
        return None


def handle_auth_callback(e, page: ft.Page, dialog: ft.AlertDialog):
    try:
        # Kontrola či URL obsahuje access_token alebo error
        callback_url = e.data
        
        if "error" in callback_url:
            raise Exception("Prihlásenie zlyhalo")
            
        if "access_token" in callback_url or "session" in callback_url:
            supabase = get_supabese_client()
            session = supabase.auth.get_session()
            
            if session:
                # Uloženie session
                page.client_storage.set("session", session)
                
                # Zatvorenie dialógu
                dialog.open = False
                page.update()
                
                # Presmerovanie na dashboard
                page.go("/")
                
                page.open(
                    ft.SnackBar(content=ft.Text("Úspešné prihlásenie"))
                )
            else:
                raise Exception("Nepodarilo sa získať session")
                
    except Exception as e:
        page.open(
            ft.SnackBar(content=ft.Text(f"Chyba pri prihlásení: {str(e)}"))
        )
        dialog.open = False
        page.update()




















def logout_with_google() -> Dict:
    try:
        supabase: Client = get_supabese_client()
        
        # Odhlásenie používateľa
        response = supabase.auth.sign_out()
        
        return {
            "status": "success",
            "message": "Používateľ bol úspešne odhlásený"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Chyba pri odhlasovaní: {str(e)}"
        }

# Pomocná funkcia na overenie stavu prihlásenia
def get_current_user() -> Optional[Dict]:
    try:
        supabase: Client = get_supabese_client()
        user = supabase.auth.get_user()
        
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "provider": "google"
            }
        return None
        
    except Exception:
        return None
    
