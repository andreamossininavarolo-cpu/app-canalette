import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# =========================================================
# CONFIGURAZIONE DELLA PAGINA
# =========================================================
st.set_page_config(
    page_title="Gestione Canalette - Consorzio Navarolo",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DATABASE INIZIALE CON TUTTI I CANALI CARICATI
# =========================================================
def get_initial_data():
    return {
        "Corte Emilia": [
            {"ordine": 1, "nome": "Agosta Angelo", "ore": 12, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Bettoni Maurizio", "ore": 6, "coltura": "Soia", "note": ""},
            {"ordine": 3, "nome": "Germiniasi Gabriele", "ore": 19, "coltura": "Erba Medica", "note": ""},
            {"ordine": 4, "nome": "Aporti Francesco", "ore": 6, "coltura": "Mais", "note": ""},
            {"ordine": 5, "nome": "Bettoni Franco", "ore": 5, "coltura": "Pomodoro", "note": ""},
            {"ordine": 6, "nome": "Novellini Eugenio", "ore": 2, "coltura": "Ortaggi", "note": ""}
        ],
        "Pirolo Piena": [
            {"ordine": 1, "nome": "Vighini Angelo", "ore": 5, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Marchini Erminio", "ore": 5, "coltura": "Soia", "note": ""},
            {"ordine": 3, "nome": "Morselli Davide", "ore": 8, "coltura": "Mais", "note": ""},
            {"ordine": 4, "nome": "Sarzi Sartori Ermete", "ore": 5, "coltura": "Erba Medica", "note": ""},
            {"ordine": 5, "nome": "Bettoni Franco", "ore": 13, "coltura": "Pomodoro", "note": ""},
            {"ordine": 6, "nome": "Carpen Angiolino", "ore": 10, "coltura": "Mais", "note": ""},
            {"ordine": 7, "nome": "Sarzi Alex", "ore": 2, "coltura": "Ortaggi", "note": ""},
            {"ordine": 8, "nome": "Novellini Eugenio", "ore": 2, "coltura": "Mais", "note": ""}
        ],
        "Cà Lame": [
            {"ordine": 1, "nome": "Aporti Andrea", "ore": 9, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Morselli Davide", "ore": 13, "coltura": "Soia", "note": ""},
            {"ordine": 3, "nome": "Novellini Eugenio", "ore": 2, "coltura": "Ortaggi", "note": ""},
            {"ordine": 4, "nome": "Maccagnola Cesare", "ore": 10, "coltura": "Erba Medica", "note": ""}
        ],
        "Madonna Lame -160": [
            {"ordine": 1, "nome": "Bertoli Erminio", "ore": 25, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Morselli Davide", "ore": 27, "coltura": "Soia", "note": ""},
            {"ordine": 3, "nome": "SCARICO (A e B)", "ore": 8, "coltura": "Scarico", "note": ""},
            {"ordine": 4, "nome": "Morselli Paolo", "ore": 4, "coltura": "Mais", "note": ""},
            {"ordine": 5, "nome": "Dalai Iacopo", "ore": 4, "coltura": "Erba Medica", "note": ""},
            {"ordine": 6, "nome": "Maccagnola Cesare", "ore": 40, "coltura": "Mais", "note": ""},
            {"ordine": 7, "nome": "Molinari/Maccagnola", "ore": 10, "coltura": "Pomodoro", "note": ""},
            {"ordine": 8, "nome": "Scarico per pomodori", "ore": 18, "coltura": "Pomodoro", "note": ""},
            {"ordine": 9, "nome": "Poli Remo", "ore": 8, "coltura": "Mais", "note": ""},
            {"ordine": 10, "nome": "Marchini Gianluigi", "ore": 27, "coltura": "Soia", "note": ""},
            {"ordine": 11, "nome": "Fercodini Bruno", "ore": 20, "coltura": "Erba Medica", "note": ""},
            {"ordine": 12, "nome": "Teresa Volta", "ore": 4, "coltura": "Ortaggi", "note": ""},
            {"ordine": 13, "nome": "SCARICO", "ore": 18, "coltura": "Scarico", "note": ""}
        ],
        "Cividale Nord A": [
            {"ordine": 1, "nome": "Germiniasi Gabriele", "ore": 5, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Cracco Sante", "ore": 45, "coltura": "Mais", "note": ""},
            {"ordine": 3, "nome": "Molinari Daniele", "ore": 28, "coltura": "Soia", "note": ""},
            {"ordine": 4, "nome": "Manfredi Filippo", "ore": 15, "coltura": "Erba Medica", "note": ""},
            {"ordine": 5, "nome": "Poli", "ore": 2, "coltura": "Ortaggi", "note": ""},
            {"ordine": 6, "nome": "Dalai Iacopo", "ore": 4, "coltura": "Mais", "note": ""}
        ],
        "Belvedere Nord": [
            {"ordine": 1, "nome": "Maccagnola", "ore": 5, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Marchini Gianluigi", "ore": 10, "
