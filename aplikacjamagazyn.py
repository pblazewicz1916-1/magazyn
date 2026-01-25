import streamlit as st
import random
from supabase import create_client, Client

# --- INICJALIZACJA SUPABASE (Z SECRETS) ---
try:
    # Streamlit pobiera to z Twojej konfiguracji Secrets
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("💀 Nie znaleziono kluczy w Secrets! Sprawdź ustawienia w Streamlit Cloud.")
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
        try:
            response = supabase.table("produkty").select("id, nazwa, liczba, cena").execute()
            return response.data
        except Exception as e:
            st.error(f"Błąd bazy: {e}")
            return []

    def dodaj_loot(self, nazwa, liczba, cena):
        data = {"nazwa": nazwa, "liczba": liczba, "cena": cena, "kategoria_id": 1}
        supabase.table("produkty").insert(data).execute()

# --- INTERFEJS STREAMLIT ---
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
    else:
        st.write("Brak zasobów.")

# --- ZAKŁADKI ---
tab1, tab2 = st.tabs(["📦 Magazyn", "🛠️ Zarządzanie"])

with tab1:
    st.subheader("📋 Aktualne zapasy")
    if zapasy:
        st.dataframe(zapasy, use_container_width=True)
    else:
        st.info("🏜️ Magazyn jest pusty.")

with tab2:
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
            st.warning("Przedmiot musi mieć nazwę!")

    st.divider()

    st.write("### 🎲 Akcje globalne")
    if st.button("SZABRUJ I HANDLUJ"):
        zdarzenie, mnoznik, opis = random.choice(logic.zdarzenia)
        st.toast(f"{zdarzenie}: {opis}")
        
        for p in zapasy:
            nowa_cena = round(p['cena'] * mnoznik, 2)
            supabase.table("produkty").update({"cena": nowa_cena}).eq("id", p['id']).execute()
        st.rerun()

    st.divider()

    st.write("### 🔥 Utylizacja")
    id_del = st.number_input("Podaj ID do zniszczenia", min_value=0, step=1)
    if st.button("Spal przedmiot", type="primary"):
        supabase.table("produkty").delete().eq("id", id_del).execute()
        st.rerun()
