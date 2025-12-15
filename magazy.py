import streamlit as st

st.title("📦 Prosty magazyn")

# Inicjalizacja listy w pamięci sesji
if "magazyn" not in st.session_state:
    st.session_state.magazyn = []

# Dodawanie towaru
st.header("Dodaj towar")
nowy_towar = st.text_input("Nazwa towaru")

if st.button("Dodaj"):
    if nowy_towar:
        st.session_state.magazyn.append(nowy_towar)
        st.success(f"Dodano towar: {nowy_towar}")
    else:
        st.warning("Wpisz nazwę towaru")

# Wyświetlanie magazynu
st.header("Stan magazynu")

if st.session_state.magazyn:
    for i, towar in enumerate(st.session_state.magazyn):
        col1, col2 = st.columns([3, 1])
        col1.write(f"{i + 1}. {towar}")
        if col2.button("Usuń", key=i):
            st.session_state.magazyn.pop(i)
            st.experimental_rerun()
else:
    st.info("Magazyn jest pusty")
