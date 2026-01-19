import streamlit as st
import csv
import os
import io

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
        with open(PLIK_CSV, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                magazyn[row["produkt"]] = int(row["ilosc"])
    return magazyn


def generuj_csv_do_pobrania(magazyn):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["produkt", "ilosc"])

    for produkt, ilosc in magazyn.items():
        writer.writerow([produkt, ilosc])

    return buffer.getvalue()


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
ilosc = col2.number_input("Ilość", min_value=1, step=1)

if st.button("Dodaj / zwiększ stan"):
    if nazwa:
        st.session_state.magazyn[nazwa] = st.session_state.magazyn.get(nazwa, 0) + ilosc
        zapisz_do_csv(st.session_state.magazyn)
        st.success(f"Dodano {ilosc} szt. produktu **{nazwa}**")
    else:
        st.warning("Podaj nazwę produktu")

st.divider()

# ======================
# 📋 STAN MAGAZYNU
# ======================
st.header("📋 Stan magazynu")

if st.session_state.magazyn:
    for produkt, ilosc in list(st.session_state.magazyn.items()):
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])

        col1.write(f"**{produkt}**")
        col2.write(f"{ilosc} szt.")

        if col3.button("➖ 1", key=f"minus_{produkt}"):
            if ilosc > 1:
                st.session_state.magazyn[produkt] -= 1
            else:
                del st.session_state.magazyn[produkt]
            zapisz_do_csv(st.session_state.magazyn)
            st.experimental_rerun()

        if col4.button("🗑 Usuń", key=f"usun_{produkt}"):
            del st.session_state.magazyn[produkt]
            zapisz_do_csv(st.session_state.magazyn)
            st.experimental_rerun()
else:
    st.info("Magazyn jest pusty")

st.divider()

# ======================
# 💾 ZAPIS + POBIERANIE CSV
# ======================
st.header("💾 Eksport danych")

csv_data = generuj_csv_do_pobrania(st.session_state.magazyn)

st.download_button(
    label="⬇️ Pobierz magazyn.csv",
    data=csv_data,
    file_name="magazyn.csv",
    mime="text/csv"
)

# ======================
# 🧹 WYCZYŚĆ MAGAZYN
# ======================
if st.button("🧹 Wyczyść magazyn"):
    st.session_state.magazyn.clear()
    zapisz_do_csv(st.session_state.magazyn)
    st.warning("Magazyn wyczyszczony")
