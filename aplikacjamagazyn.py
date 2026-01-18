import psycopg2
from psycopg2 import sql

class LogisticsManager:
    def __init__(self, db_config):
        """Inicjalizacja połączenia z bazą danych."""
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def dodaj_produkt(self, nazwa, liczba, cena, kategoria_id):
        """Dodaje nowy produkt do bazy danych."""
        try:
            query = """
                INSERT INTO produkty (nazwa, liczba, cena, kategoria_id)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """
            self.cursor.execute(query, (nazwa, liczba, cena, kategoria_id))
            nowe_id = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f"[SUCCESS] Produkt '{nazwa}' dodany z ID: {nowe_id}")
            return nowe_id
        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Nie udało się dodać produktu: {e}")

    def usun_produkt(self, produkt_id):
        """Usuwa produkt na podstawie jego ID."""
        try:
            query = "DELETE FROM produkty WHERE id = %s;"
            self.cursor.execute(query, (produkt_id,))
            if self.cursor.rowcount == 0:
                print(f"[WARNING] Nie znaleziono produktu o ID: {produkt_id}")
            else:
                self.conn.commit()
                print(f"[SUCCESS] Produkt o ID: {produkt_id} został usunięty.")
        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Błąd podczas usuwania: {e}")

    def zamknij_polaczenie(self):
        self.cursor.close()
        self.conn.close()

# --- PRZYKŁAD UŻYCIA ---
config = {
    'dbname': 'twoja_nazwa_bazy',
    'user': 'postgres',
    'password': 'twoje_haslo',
    'host': 'db.xyz.supabase.co',
    'port': '5432'
}

# Logika biznesowa
# manager = LogisticsManager(config)
# manager.dodaj_produkt("Paleta Euro", 150, 89.99, 1) # Zakładając, że kategoria ID=1 istnieje
# manager.usun_produkt(5)
