import os
import random
from supabase import create_client, Client

# --- KONFIGURACJA (Trzymaj to pod kluczem, albo mutanci przejmą bazę!) ---
SUPABASE_URL = "TWOJ_URL"
SUPABASE_KEY = "TWOJ_KLUCZ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class MagazynApokalipsy:
    def __init__(self):
        self.okrzyki_sukcesu = [
            "Znaleziono w ruinach!", "Odbite gangowi motocyklowemu.",
            "Czysty zysk, zero promieniowania.", "Wrzucam do skrzyni, szefie!"
        ]
        self.odpowiedzi_na_blad = [
            "Coś wybuchło. I to nie był dynamit...",
            "Baza danych została zaatakowana przez zmutowane chomiki.",
            "Błąd 404: Twoja godność nie została znaleziona.",
            "Supabase mówi: 'Nie dzisiaj, koleżko'."
        ]

    def dodaj_loot(self, nazwa: str, liczba: int, cena: float, kat_id: int):
        """Dodaje fanty do Twojego schronu."""
        data = {"nazwa": nazwa, "liczba": liczba, "cena": cena, "kategoria_id": kat_id}
        try:
            supabase.table("produkty").insert(data).execute()
            print(f"📦 [{nazwa.upper()}] - {random.choice(self.okrzyki_sukcesu)}")
        except Exception as e:
            print(f"💀 KATASTROFA: {random.choice(self.odpowiedzi_na_blad)} ({e})")

    def zutylizuj(self, produkt_id: int):
        """Usuwa przedmiot (prawdopodobnie został zjedzony przez mutanty)."""
        try:
            res = supabase.table("produkty").delete().eq("id", produkt_id).execute()
            if res.data:
                print(f"🔥 Przedmiot #{produkt_id} został spalony. Popiół rozrzucony na wietrze.")
            else:
                print(f"🕵️ Próbujesz usunąć ducha? ID {produkt_id} nie istnieje w tej rzeczywistości.")
        except Exception as e:
            print(f"☣️ Wyciek radioaktywny przy usuwaniu: {e}")

# --- URUCHAMIANIE PROTOKOŁU ---
if __name__ == "__main__":
    shelter = MagazynApokalipsy()
    
    print("--- ☢️ LOGOWANIE DO TERMINALA VAULT-TEC ☢️ ---")
    
    # Próba dodania czegoś epickiego
    shelter.dodaj_loot("Puszka przeterminowanej fasoli", 100, 2.50, 1)
    
    # Próba usunięcia czegoś, czego pewnie nie ma
    shelter.zutylizuj(999)
