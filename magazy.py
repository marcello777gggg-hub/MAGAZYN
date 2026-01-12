import streamlit as st

st.set_page_config(page_title="Magazyn", page_icon="📦")
st.title("📦 System magazynowy")

# Inicjalizacja magazynu
if "magazyn" not in st.session_state:
    st.session_state.magazyn = {}

# ======================
# ➕ DODAWANIE PRODUKTU
# ======================
st.header("➕ Dodaj produkt")

col1, col2 = st.columns(2)
nazwa = col1.text_input("Nazwa produktu")
ilosc = col2.number_input("Ilość", min_value=1, step=1)

if st.button("Dodaj / zwiększ stan"):
    if nazwa:
        if nazwa in st.session_state.magazyn:
            st.session_state.magazyn[nazwa] += ilosc
        else:
            st.session_state.magazyn[nazwa] = ilosc
        st.success(f"Dodano {ilosc} szt. produktu **{nazwa}**")
    else:
        st.warning("Podaj nazwę produktu")

st.divider()

# ======================
# 🔍 WYSZUKIWANIE
# ======================
st.header("🔍 Wyszukaj produkt")
szukaj = st.text_input("Wpisz nazwę (lub jej część)").lower()

st.divider()

# ======================
# 📋 STAN MAGAZYNU
# ======================
st.header("📋 Stan magazynu")

if st.session_state.magazyn:
    for produkt, ilosc in list(st.session_state.magazyn.items()):
        if szukaj and szukaj not in produkt.lower():
            continue

        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])

        col1.write(f"**{produkt}**")
        col2.write(f"{ilosc} szt.")

        if col3.button("➖ 1", key=f"minus_{produkt}"):
            if st.session_state.magazyn[produkt] > 1:
                st.session_state.magazyn[produkt] -= 1
            else:
                del st.session_state.magazyn[produkt]
            st.experimental_rerun()

        if col4.button("🗑 Usuń", key=f"usun_{produkt}"):
            del st.session_state.magazyn[produkt]
            st.experimental_rerun()
else:
    st.info("Magazyn jest pusty")

st.divider()

# ======================
# 🧹 WYCZYŚĆ MAGAZYN
# ======================
if st.button("🧹 Wyczyść cały magazyn"):
    st.session_state.magazyn.clear()
    st.success("Magazyn został wyczyszczony")
