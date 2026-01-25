Skoro klucze masz już bezpiecznie ukryte w Secrets, to kod staje się znacznie czystszy i bezpieczniejszy. Usunąłem pola wyboru z paska bocznego i podpiąłem bezpośrednie pobieranie danych z st.secrets.

Oto poprawiona, w pełni zautomatyzowana wersja Twojego terminala przetrwania:

Python
import streamlit as st
import random
from supabase import create_client, Client

# --- INICJALIZACJA SUPABASE (Z SECRETS) ---
# Streamlit automatycznie szuka ich w .streamlit/secrets.toml lub w panelu Cloud
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("💀 Nie znaleziono kluczy w Secrets! Mutanci musieli je przeciąć.")
    st.stop()

class MagazynApokalipsy:
    def __init__(self):
        self.zdarzenia = [
            ("☢️ Burza piaskowa", 1.5, "Ceny rosną! Nikt nie chce wychodzić z bunkra."),
            ("🐀 Inwazja szczurów", 0.5, "Towar nadgryziony, wyprzedaż 50%!"),
            ("🛸 Wizyta obcych", 3.0, "Intergalaktyczna inflacja! Wszystko x3!"),
            ("💧 Znaleziono źródło czystej wody", 0.8, "Ludzie są szczęśliwsi, ceny lekko w dół.")
        ]

    def pobierz_zapasy(self):
        # Pobieramy ID, nazwę, liczbę i cenę
        response = supabase.table("produkty").select("id, nazwa, liczba, cena").execute()
        return response.data

    def dodaj_loot(self, nazwa, liczba, cena):
        data = {"nazwa": nazwa, "liczba": liczba, "cena": cena, "kategoria_id": 1}
        supabase.table("produkty").insert(data).execute()

# --- INTERFEJS ---
st.set_page_config(page_title="Vault-Tec Terminal", page_icon="☢️")
st.title("☢️ Terminal Zarządzania Schronem")

logic = MagazynApokalipsy()

# --- PASEK BOCZNY (STATYSTYKI) ---
with st.sidebar:
    st.header("📊 Statystyki bunkra")
    zapasy = logic.pobierz_zapasy()
    if zapasy:
        suma_kapsli = sum(item['cena'] * item['liczba'] for item in zapasy)
        st.metric("Całkowita wartość (kapsle)", f"{suma_kapsli:,.2f}")
        st.write(f"Przedmiotów w bazie: {len(zapasy)}")
    else:
        st.write("Brak zasobów.")

# --- ZAKŁADKI ---
tab1, tab2 = st.tabs(["📦 Magazyn", "🛠️ Zarządzanie"])

with tab1:
    st.subheader("📋 Aktualne zapasy")
    if zapasy:
        st.dataframe(zapasy, use_container_width=True)
    else:
        st.info("🏜️ Magazyn jest pusty. Wyślij kogoś na zewnątrz!")

with tab2:
    # Sekcja dodawania
    st.write("### ➕ Dodaj nowy loot")
    c1, c2, c3 = st.columns(3)
    nazwa = c1.text_input("Nazwa przedmiotu")
    ile = c2.number_input("Ilość", min_value=1, step=1)
    cena = c3.number_input("Cena za sztukę", min_value=0.01, step=0.5)
    
    if st.button("Składuj w bunkrze"):
        if nazwa:
            logic.dodaj_loot(nazwa, ile, cena)
            st.success(f"Dodano: {nazwa}")
            st.rerun()
        else:
            st.warning("Przedmiot musi mieć nazwę, szefie!")

    st.divider()

    # Sekcja akcji losowych
    st.write("### 🎲 Akcje globalne")
    if st.button("SZABRUJ I HANDLUJ (Zmień ceny rynkowe)"):
        zdarzenie, mnoznik, opis = random.choice(logic.zdarzenia)
        st.toast(f"{zdarzenie}: {opis}") # Małe powiadomienie w rogu
        
        for p in zapasy:
            nowa_cena = round(p['cena'] * mnoznik, 2)
            supabase.table("produkty").update({"cena": nowa_cena}).eq("id", p['id']).execute()
        st.rerun()

    st.divider()

    # Usuwanie
    st.write("### 🔥 Utylizacja")
    id_del = st.number_input("Podaj ID do zniszczenia", min_value=0, step=1)
    if st.button("Spal przedmiot", type="primary"):
        supabase.table("produkty").delete().eq("id", id_del).execute()
        st.error(f"Przedmiot #{id_del} przestał istnieć.")
        st.rerun()
        
else:
    st.write("🏜️ Pusto tu... wyślij kogoś na zwiady.")
