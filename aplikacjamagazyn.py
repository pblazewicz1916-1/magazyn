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
            ("☢️ Burza piaskowa", 1.5, "Ceny rosną! Nikt nie chce wychodzić z bunkra."),
            ("🐀 Inwazja szczurów", 0.5, "Towar nadgryziony, wyprzedaż 50%!"),
            ("🛸 Wizyta obcych", 3.0, "Intergalaktyczna inflacja! Wszystko x3!"),
            ("💧 Znalezisko", 0.8, "Ludzie są szczęśliwsi, ceny lekko w dół.")
        ]

    def pobierz_zapasy(self):
        try:
            response = supabase.table("produkty").select("id, nazwa, liczba, cena").execute()
            return response.data if response.data else []
        except Exception:
            return []

    def dodaj_loot(self, nazwa, liczba, cena):
        data = {"nazwa": nazwa, "liczba": liczba, "cena": cena, "kategoria_id": 1}
        supabase.table("produkty").insert(data).execute()

# --- INTERFEJS STREAMLIT ---
st.set_page_config(page_title="Vault-Tec Terminal", page_icon="☢️")
st.title("☢️ Terminal Zarządzania Schronem")

logic = MagazynApokalipsy()
zapasy = logic.pobierz_zapasy()

# --- PASEK BOCZNY ---
if zapasy:
    with st.sidebar:
        st.header("📊 Statystyki")
        suma_kapsli = sum(item['cena'] * item['liczba'] for item in zapasy)
        st.metric("Całkowita wartość", f"{suma_kapsli:,.2f} 🍾")
        st.write(f"Liczba unikalnych fantów: {len(zapasy)}")

# --- ZAKŁADKI ---
tab1, tab2 = st.tabs(["📦 Magazyn", "🛠️ Zarządzanie"])

with tab1:
    if not zapasy:
        st.warning("🏜️ Twoje półki pokrywa kurz... Magazyn jest pusty!")
        st.info("Przejdź do zakładki 'Zarządzanie', aby dodać swój pierwszy loot.")
    else:
        st.subheader("📋 Aktualne zapasy w bunkrze")
        st.dataframe(zapasy, use_container_width=True, hide_index=True)

with tab2:
    st.write("### ➕ Dodaj nowy loot")
    c1, c2, c3 = st.columns(3)
    nazwa = c1.text_input("Nazwa przedmiotu", placeholder="np. Nuka-Cola")
    ile = c2.number_input("Ilość", min_value=1, step=1)
    cena = c3.number_input("Cena (w kapslach)", min_value=0.01, step=0.5)
    
    if st.button("Składuj w bunkrze", use_container_width=True):
        if nazwa:
            logic.dodaj_loot(nazwa, ile, cena)
            st.toast(f"📦 {nazwa} bezpiecznie schowany!")
            st.rerun()
        else:
            st.error("Przedmiot musi mieć nazwę!")

    if zapasy:
        st.divider()
        st.write("### 🎲 Akcje globalne")
        if st.button("SZABRUJ I HANDLUJ", use_container_width=True):
            zdarzenie, mnoznik, opis = random.choice(logic.zdarzenia)
            st.toast(f"{zdarzenie}: {opis}")
            for p in zapasy:
                nowa_cena = round(p['cena'] * mnoznik, 2)
                supabase.table("produkty").update({"cena": nowa_cena}).eq("id", p['id']).execute()
            st.rerun()

        st.divider()
        st.write("### 🔥 Utylizacja")
        col_id, col_btn = st.columns([2, 1])
        id_del = col_id.number_input("ID do zniszczenia", min_value=0, step=1, key="del_id")
        if col_btn.button("Spal przedmiot", type="primary", use_container_width=True):
            supabase.table("produkty").delete().eq("id", id_del).execute()
            st.success(f"Zutylizowano przedmiot o ID {id_del}")
            st.rerun()
