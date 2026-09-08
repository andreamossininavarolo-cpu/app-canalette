import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Gestione Canalette",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Database di Prova (In-Memory) ---
# In un'app reale, questi dati verrebbero da un database esterno.
# Usiamo st.session_state per rendere i dati modificabili durante la sessione.

def initialize_data():
    """Inizializza i dati solo se non sono già presenti."""
    if 'data_canali' not in st.session_state:
        st.session_state.data_canali = {
            "Corte Emilia": [
                {"ordine": 1, "nome": "Agosta Angelo", "ore": 12, "coltura": "Mais", "note": ""},
                {"ordine": 2, "nome": "Bettoni Maurizio", "ore": 6, "coltura": "Soia", "note": ""},
                {"ordine": 3, "nome": "Germiniasi Gabriele", "ore": 19, "coltura": "Mais", "note": ""},
                {"ordine": 4, "nome": "Aporti Francesco", "ore": 6, "coltura": "Erba Medica", "note": ""},
                {"ordine": 5, "nome": "Bettoni Franco", "ore": 5, "coltura": "Pomodori", "note": ""},
                {"ordine": 6, "nome": "Novellini Eugenio", "ore": 2, "coltura": "Ortaggi", "note": ""}
            ],
            "Pirolo Piena": [
                {"ordine": 1, "nome": "Vighini Angelo", "ore": 5, "coltura": "Mais", "note": ""},
                {"ordine": 2, "nome": "Marchini Erminio", "ore": 5, "coltura": "Soia", "note": ""}
            ]
        }

    if 'stato_app' not in st.session_state:
        st.session_state.stato_app = {
            "canale_selezionato": "Corte Emilia",
            "turno_corrente": 0,
            "ritardo_accumulato": 0,
            "data_partenza_ruota": datetime(2027, 5, 3, 20, 0, 0)
        }

initialize_data()

# --- Titolo Principale ---
st.markdown("<h1 style='text-align: center; color: #1D3557;'>💧 Gestione Integrata Canalette</h1>", unsafe_allow_html=True)

# --- Selettore Canale Globale ---
lista_canali = list(st.session_state.data_canali.keys())
canale_selezionato = st.selectbox(
    "Seleziona la Canaletta su cui operare:",
    lista_canali,
    index=lista_canali.index(st.session_state.stato_app.get("canale_selezionato", "Corte Emilia"))
)
st.session_state.stato_app["canale_selezionato"] = canale_selezionato
utenti_del_canale = st.session_state.data_canali[canale_selezionato]

# --- Definizione Schede (Tabs) ---
tab_gestione, tab_censimento, tab_anagrafica = st.tabs([
    "💧 Gestione Turni (Estivo)",
    "🌾 Censimento Invernale",
    "👥 Gestione Anagrafica"
])


# --- Scheda 1: Gestione Turni (Estivo) ---
with tab_gestione:
    st.header(f"Operatività Canale: {canale_selezionato}")

    # Logica di calcolo turni
    turni_calcolati = []
    orario_corrente = st.session_state.stato_app["data_partenza_ruota"]
    for i, utente in enumerate(utenti_del_canale):
        inizio_turno_base = orario_corrente
        inizio_turno_reale = inizio_turno_base + timedelta(minutes=st.session_state.stato_app.get("ritardo_accumulato", 0)) if i >= st.session_state.stato_app.get("turno_corrente", 0) else inizio_turno_base
        fine_turno = inizio_turno_reale + timedelta(hours=utente["ore"])
        turni_calcolati.append({"ordine": utente["ordine"], "nome": utente["nome"], "inizio": inizio_turno_reale, "fine": fine_turno, "durata": utente["ore"]})
        orario_corrente = inizio_turno_base + timedelta(hours=utente["ore"])

    # UI per il turno corrente e successivo
    idx_attivo = st.session_state.stato_app.get("turno_corrente", 0)
    if idx_attivo < len(turni_calcolati):
        attivo = turni_calcolati[idx_attivo]
        st.markdown(f"""... [omissis - codice interfaccia come prima] ...""") # Codice per visualizzare turno attivo e prossimo
        # ... (il codice per i pulsanti di avanzamento e ritardo va qui)
    else:
        st.success("🎉 Ciclo di irrigazione completato!")

# --- Scheda 2: Censimento Invernale ---
with tab_censimento:
    st.header(f"Censimento Fabbisogno Idrico: {canale_selezionato}")
    st.write("Seleziona un utente per confermare o modificare le ore e la coltura per la prossima stagione.")

    for i, utente in enumerate(utenti_del_canale):
        with st.expander(f"{utente['ordine']}. {utente['nome']} - {utente['ore']} ore ({utente['coltura']})"):
            nuove_ore = st.number_input(f"Ore per {utente['nome']}", min_value=0, max_value=200, value=utente['ore'], key=f"ore_{i}")
            nuova_coltura = st.text_input(f"Coltura per {utente['nome']}", value=utente['coltura'], key=f"coltura_{i}")
            if st.button("Salva Modifiche", key=f"salva_{i}"):
                st.session_state.data_canali[canale_selezionato][i]['ore'] = nuove_ore
                st.session_state.data_canali[canale_selezionato][i]['coltura'] = nuova_coltura
                st.success(f"Dati per {utente['nome']} aggiornati!")
                st.rerun()


# --- Scheda 3: Gestione Anagrafica Utenti ---
with tab_anagrafica:
    st.header(f"Gestione Utenti Canale: {canale_selezionato}")

    # Aggiungere nuovo utente
    with st.expander("➕ Aggiungi Nuovo Utente al Canale"):
        with st.form("form_nuovo_utente", clear_on_submit=True):
            nuovo_nome = st.text_input("Nome e Cognome")
            nuove_ore_anagrafica = st.number_input("Ore di Competenza", min_value=1, max_value=200)
            nuova_coltura_anagrafica = st.text_input("Coltura Iniziale", "Da Definire")
            submitted = st.form_submit_button("Salva Nuovo Utente")
            if submitted:
                nuovo_ordine = len(utenti_del_canale) + 1
                st.session_state.data_canali[canale_selezionato].append({
                    "ordine": nuovo_ordine,
                    "nome": nuovo_nome,
                    "ore": nuove_ore_anagrafica,
                    "coltura": nuova_coltura_anagrafica,
                    "note": ""
                })
                st.success(f"Utente {nuovo_nome} aggiunto a {canale_selezionato}!")
                st.rerun()

    st.write("---")
    st.subheader("Elenco Utenti Esistenti")

    # Modificare e Rimuovere utenti esistenti
    for i, utente in enumerate(utenti_del_canale):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.text(f"{utente['ordine']}. {utente['nome']} ({utente['ore']} ore)")
        with col2:
            if st.button("✏️ Modifica", key=f"edit_{i}"):
                # Questa parte può essere espansa per aprire un popup di modifica
                st.info(f"Funzione di modifica per {utente['nome']} da implementare.")
        with col3:
            if st.button("❌ Rimuovi", key=f"del_{i}"):
                st.session_state.data_canali[canale_selezionato].pop(i)
                # Riordina gli indici
                for j, u in enumerate(st.session_state.data_canali[canale_selezionato]):
                    u['ordine'] = j + 1
                st.success(f"Utente {utente['nome']} rimosso!")
                st.rerun()

