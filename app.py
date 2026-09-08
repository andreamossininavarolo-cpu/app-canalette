import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Gestione Canalette",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Database di Prova (In-Memory) ---
# In un'app reale, questi dati verrebbero da un database esterno.
# Usiamo st.session_state per rendere i dati modificabili durante la sessione.

if 'dati_canale' not in st.session_state:
    st.session_state.dati_canale = {
        "Corte Emilia": [
            {"ordine": 1, "nome": "Agosta Angelo", "ore": 12, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Bettoni Maurizio", "ore": 6, "coltura": "Soia", "note": ""},
            {"ordine": 3, "nome": "Germiniasi Gabriele", "ore": 19, "coltura": "Mais", "note": ""},
            {"ordine": 4, "nome": "Aporti Francesco", "ore": 6, "coltura": "Erba Medica", "note": ""},
            {"ordine": 5, "nome": "Bettoni Franco", "ore": 5, "coltura": "Pomodori", "note": ""},
            {"ordine": 6, "nome": "Novellini Eugenio", "ore": 2, "coltura": "Ortaggi", "note": ""}
        ]
        # Qui potremmo aggiungere gli altri 44 canali
    }

if 'stato_app' not in st.session_state:
    st.session_state.stato_app = {
        "canale_selezionato": "Corte Emilia",
        "turno_corrente": 0,
        "ritardo_accumulato": 0, # in minuti
        "data_partenza_ruota": datetime(2027, 5, 3, 20, 0, 0) # Esempio: Ruota Dispari
    }

# --- Inter
