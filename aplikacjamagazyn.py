import os
from supabase import create_client, Client

# --- KONFIGURACJA ---
# Dane znajdziesz w panelu Supabase: Project Settings -> API
SUPABASE_URL = "TWOJ_URL_PROJEKTU"
SUPABASE_KEY = "TWOJ_ANON_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def dodaj_produkt(nazwa: str, liczba: int, cena: float, kategoria_id: int):
    """
    Dodaje nowy produkt do bazy danych.
    Wymaga poprawnego kategoria_id istniejącego w tabeli 'kategorie'.
    """
    data = {
        "nazwa": nazwa,
        "liczba": liczba,
        "cena": cena,
        "kategoria_id": kategoria_id
    }
    try:
        response = supabase.table("produkty").insert(data).execute()
        print(f"✅ Produkt '{nazwa}' został dodany.")
        return response
    except Exception as e:
        print(f"❌ Błąd podczas dodawania: {e}")

def usun_produkt(produkt_id: int):
    """
    Usuwa produkt na podstawie jego unikalnego ID.
    """
    try:
        response = supabase.table("produkty").delete().eq("id", produkt_id).execute()
        if response.data:
            print(f"✅ Produkt o ID {produkt_id} został usunięty.")
        else:
            print(f"⚠️ Nie znaleziono produktu o ID {produkt_id}.")
        return response
    except Exception as e:
        print(f"❌ Błąd podczas usuwania: {e}")

# --- PRZYKŁAD UŻYCIA ---
if __name__ == "__main__":
    # 1. Dodawanie produktu (upewnij się, że kategoria o ID 1 istnieje!)
    dodaj_produkt("Wózek Widłowy model A", 5, 15000.50, 1)
    
    # 2. Usuwanie produktu (zmień ID na właściwe)
    # usun_produkt(10)
