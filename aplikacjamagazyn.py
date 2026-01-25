import streamlit as st
import random
from supabase import create_client, Client

# --- INICJALIZACJA SUPABASE ---
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("💀 Błąd połączenia z bazą danych. Sprawdź Secrets!")
    st.stop()

class MagazynApokalipsy:
    def __init__(self):
        self.zdarzenia = [
            ("☢️ Burza piaskowa", 1.5, "Ceny rosną!"),
            ("🐀 Inwazja szczurów", 0.5, "Wyprzedaż!"),
            ("🛸 Wizyta obcych", 3.0, "Inflacja galaktyczna!"),
            ("💧 Znalezisko", 0.8, "Ceny w dół.")
        ]
        # Lista startowa - 10 niezbędnych produktów
        self.produkty_startowe = [
            {"nazwa": "Nuka-Cola", "liczba": 24, "cena": 15.0, "kategoria_id": 1},
            {"nazwa": "AntyRad", "liczba": 5, "cena": 120.0, "kategoria_id": 1},
            {"nazwa": "Puszka fasoli", "liczba": 50, "cena": 5.5, "kategoria_id": 1},
            {"nazwa": "Amunicja 10mm", "liczba": 100, "cena": 2.0, "kategoria_id": 1},
            {"nazwa": "Zardzewiały nóż", "liczba": 3, "cena": 45.0, "kategoria_id": 1},
            {"nazwa": "Licznik Geigera", "liczba": 1, "cena": 350.0, "kategoria_id": 1},
            {"nazwa": "Czysta woda", "liczba": 12, "cena": 25.0, "kategoria_id": 1},
            {"nazwa": "Stymulant", "liczba": 8, "cena": 80.0, "kategoria_id": 1},
            {"nazwa": "Maska przeciwgazowa", "liczba": 2, "cena": 150.0, "kategoria_id": 1},
            {"nazwa": "Bateria termojądrowa", "liczba": 1, "cena": 999.0, "kategoria_id": 1}
        ]

    def pobierz_zapasy(self):
        try:
            response = supabase.table("produkty").select("id, nazwa, liczba, cena").execute()
            data = response.data if response.data else []
            
            # Jeśli magazyn jest pusty, automatycznie go zatowaruj!
            if not data:
                st.info("📦 Magazyn był pusty. Generuję 10 podstawowych produktów...")
                supabase.table("produkty").insert(self.produkty_startowe).execute()
                # Pobierz ponownie, żeby mieć ID z bazy
                response = supabase.table("produkty").select("id, nazwa, liczba, cena").execute
