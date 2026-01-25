import streamlit as st
import random
from supabase import create_client, Client

# --- KONFIGURACJA STREAMLIT ---
st.set_page_config(page_title="Vault-Tec Manager", page_icon="☢️")

# --- POŁĄCZENIE Z BAZĄ ---
# Najlepiej dodać je w panelu Streamlit Cloud w "Secrets"
SUPABASE_URL = st.sidebar.text_input("Supabase URL", type="default")
SUPABASE_KEY = st.sidebar.text_input("Supabase Anon Key", type="password")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.warning("⚠️ Wpisz dane do Supabase w panelu bocznym, aby odblokować terminal!")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- LOGIKA SYSTEMU ---
class MagazynApokalipsy:
    def __init__(self):
        self.zdarzenia = [
            ("☢️ Burza piaskowa", 1.5, "Ceny rosną!"),
            ("🐀 Inwazja szczurów", 0.5, "Wyprzedaż pogryzionych fantów!"),
            ("🛸 Wizyta obcych", 3.0, "Ktoś płaci w galaktycznych kredytach!")
        ]

    def pobierz_zapasy(self):
        return supabase.table("produkty").select("*").execute().data

    def dodaj_loot(self, nazwa, liczba, cena):
        data = {"nazwa": nazwa, "liczba": liczba, "cena": cena, "kategoria_id": 1}
        supabase.table("produkty").insert(data).execute()

# --- INTERFEJS STREAMLIT ---
st.title("☢️ Terminal Zarządzania Schronem")
st.subheader("Witaj w Vault-Tec. Dzisiaj jest piękny dzień na przetrwanie.")

logic = MagazynApokalipsy()

# --- PANEL DODAWANIA ---
with st.expander("➕ Znaleziono nowy loot?"):
    col1, col2, col3 = st.columns(3)
    nazwa = col1.text_input("Co to?")
    ile = col2.number_input("Ile sztuk?", min_value=1, value=1)
    cena = col3.number_input("Cena (kapsle)", min_value=0.1, value=10.0)
    
    if st.button("Dodaj do skrzyni"):
        logic.dodaj_loot(nazwa, ile, cena)
        st.success(f"📦 Wrzucono {nazwa} do schowka!")
        st.balloons() # Mały efekt świętowania

# --- PANEL HANDLU ---
st.divider()
if st.button("🎲 SZABRUJ I HANDLUJ (Zmień ceny)"):
    zdarzenie, mnoznik, opis = random.choice(logic.zdarzenia)
    st.info(f"{zdarzenie}: {opis}")
    
    produkty = logic.pobierz_zapasy()
    for p in produkty:
        nowa_cena = round(p['cena'] * mnoznik, 2)
        supabase.table("produkty").update({"cena": nowa_cena}).eq("id", p['id']).execute()
    st.rerun() # Odśwież stronę, by zobaczyć nowe ceny

# --- WIDOK MAGAZYNU ---
st.header("📋 Twoje Zasoby")
zapasy = logic.pobierz_zapasy()

if zapasy:
    # Wyświetlamy to w ładnej tabeli Streamlit
    st.table(zapasy)
    
    # Usuwanie
    id_do_usuniecia = st.number_input("Wpisz ID do zutylizowania", min_value=1)
    if st.button("🔥 Spal przedmiot"):
        supabase.table("produkty").delete().eq("id", id_do_usuniecia).execute()
        st.warning(f"Zutylizowano przedmiot o ID {id_do_usuniecia}")
        st.rerun()
else:
    st.write("🏜️ Pusto tu... wyślij kogoś na zwiady.")
