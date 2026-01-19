import streamlit as st
import csv
import os
import io
import pandas as pd

st.set_page_config(page_title="Magazyn", page_icon="📦")
st.title("📦 System magazynowy")

PLIK_CSV = "magazyn.csv"

# ======================
# 💾 FUNKCJE CSV
# ======================
def zapisz_do_csv(magazyn):
    with open(PLIK_CSV, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["produkt", "ilosc"])
        for produkt, ilosc in magazyn.items():
            writer.writerow([produkt, ilosc])

def wczytaj_z_csv():
    magazyn = {}
    if os.path.exists(PLIK_CSV):
        try:
            with open(PLIK_CSV, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    magazyn[row["produkt"]] = int(row["ilosc"])
        except:
            return {}
    return magazyn

# ======================
# 🔄 INICJALIZACJA
# ======================
if "magazyn" not in st.session_state:
    st.session_state.magazyn = wczytaj_z_csv()

# ======================
# ➕ DODAWANIE PRODUKTU
# ======================
st.header("➕ Dodaj produkt")
col1, col2 = st.columns(2)
nazwa = col1.text_input("Nazwa produktu")
ilosc_nowa = col2.number_input("Ilość", min_value=1, step=1)

if st.button("Dodaj / zwiększ stan"):
    if nazwa:
        st.session_state.magazyn[nazwa] = st.session_state.magazyn.get(nazwa, 0) + ilosc_nowa
        zapisz_do_csv(st.session_state.magazyn)
        st.success(f"Dodano {ilosc_nowa} szt. produktu **{nazwa}**")
        st.rerun()
    else:
        st.warning("Podaj nazwę produktu")

st.divider()

# ======================
# 📋 STAN MAGAZYNU (TABELA)
# ======================
st.header("📋 Stan magazynu")

if st.session_state.magazyn:
    # Tworzymy tabelę do edycji
    df = pd.DataFrame(list(st.session_state.magazyn.items()), columns=["produkt", "ilosc"])
    
    # Wyświetlamy interaktywną tabelę
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="edytor")
    
    col_a, col_b = st.columns(2)
    if col_a.button("💾 Zapisz zmiany w tabeli"):
        # Aktualizacja stanu na podstawie edytowanej tabeli
        st.session_state.magazyn = dict(zip(edited_df["produkt"], edited_df["ilosc"]))
        zapisz_do_csv(st.session_state.magazyn)
        st.toast("Zmiany zapisane!")
        st.rerun()

    # Wykres poglądowy
    st.bar_chart(df.set_index("produkt"))
else:
    st.info("Magazyn jest pusty")

st.divider()

# ======================
# 💾 EKSPORT I CZYSZCZENIE
# ======================
st.header("⚙️ Opcje dodatkowe")

# Pobieranie
buffer = io.StringIO()
pd.DataFrame(list(st.session_state.magazyn.items()), columns=["produkt", "ilosc"]).to_csv(buffer, index=False)
st.download_button(label="⬇️ Pobierz CSV", data=buffer.getvalue(), file_name="magazyn.csv", mime="text/csv")

# Czyszczenie
if st.button("🧹 Wyczyść cały magazyn"):
    st.session_state.magazyn = {}
    zapisz_do_csv(st.session_state.magazyn)
    st.rerun()
