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
            "ritardo_accumulato": 0, # in minuti
            "data_partenza_ruota": datetime(2027, 5, 3, 20, 0, 0)
        }
    
    if 'censimento' not in st.session_state:
        st.session_state.censimento = {}


initialize_data()

# --- Titolo Principale ---
st.markdown("<h1 style='text-align: center; color: #1D3557;'>💧 Gestione Integrata Canalette</h1>", unsafe_allow_html=True)

# --- Selettore Canale Globale ---
lista_canali = list(st.session_state.data_canali.keys())
canale_selezionato = st.selectbox(
    "Seleziona la Canaletta su cui operare:",
    lista_canali,
    index=lista_canali.index(st.session_state.stato_app.get("canale_selezionato", lista_canali[0]))
)
if st.session_state.stato_app["canale_selezionato"] != canale_selezionato:
    st.session_state.stato_app["canale_selezionato"] = canale_selezionato
    st.session_state.stato_app["turno_corrente"] = 0
    st.session_state.stato_app["ritardo_accumulato"] = 0
    st.rerun()

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
        
        inizio_turno_reale = inizio_turno_base
        if i >= st.session_state.stato_app["turno_corrente"]:
            inizio_turno_reale += timedelta(minutes=st.session_state.stato_app["ritardo_accumulato"])
            
        fine_turno = inizio_turno_reale + timedelta(hours=utente["ore"])
        turni_calcolati.append({"ordine": utente["ordine"], "nome": utente["nome"], "inizio": inizio_turno_reale, "fine": fine_turno, "durata": utente["ore"]})
        orario_corrente = inizio_turno_base + timedelta(hours=utente["ore"])

    # UI per il turno corrente e successivo
    idx_attivo = st.session_state.stato_app["turno_corrente"]
    if idx_attivo < len(turni_calcolati):
        attivo = turni_calcolati[idx_attivo]
        
        st.markdown(f"""
        <div style="background-color: #E6F3FF; padding: 20px; border-radius: 15px; border-left: 8px solid #457B9D; margin-bottom: 20px;">
            <span style="color: #457B9D; font-weight: bold; text-transform: uppercase; font-size: 12px;">🔴 TURNO ATTUALE IN CORSO</span>
            <h2 style="margin: 5px 0; color: #1D3557;">{attivo['nome']}</h2>
            <p style="margin: 0; font-size: 16px; color: #1D3557;">
                Inizio: <b>{attivo['inizio'].strftime('%d/%m/%Y alle %H:%M')}</b><br>
                Fine stimata: <b style="color: #E63946;">{attivo['fine'].strftime('%H:%M')} ({attivo['fine'].strftime('%d/%m')})</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

        if idx_attivo + 1 < len(turni_calcolati):
            prossimo = turni_calcolati[idx_attivo + 1]
            st.markdown(f"""
            <div style="background-color: #F1FAEE; padding: 15px; border-radius: 10px; border-left: 5px solid #2A9D8F; margin-bottom: 20px;">
                <span style="color: #2A9D8F; font-weight: bold; font-size: 11px;">⏭️ IN CODA SUBITO DOPO:</span>
                <h4 style="margin: 2px 0; color: #1D3557;">{prossimo['nome']}</h4>
                <p style="margin: 0; font-size: 13px; color: #1D3557;">Partenza prevista: <b>{prossimo['inizio'].strftime('%H:%M')} del {prossimo['inizio'].strftime('%d/%m')}</b></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Questo è l'ultimo utente della canaletta.")

        st.write("### ⚙️ Azioni Rapide Acquaiolo")
        col1, col2 = st.columns(2)
        if col1.button("✅ Turno Fatto / Avanti", use_container_width=True):
            st.session_state.stato_app["turno_corrente"] += 1
            st.rerun()

        if col2.button("🔄 Ripristina Test", use_container_width=True):
            st.session_state.stato_app["turno_corrente"] = 0
            st.session_state.stato_app["ritardo_accumulato"] = 0
            st.rerun()
        
        st.write("---")
        st.write("⚠️ **C'è un ritardo in questo turno?**")
        col_r1, col_r2, col_r3 = st.columns(3)
        if col_r1.button("+15 Min", use_container_width=True):
            st.session_state.stato_app["ritardo_accumulato"] += 15
            st.rerun()
        if col_r2.button("+30 Min", use_container_width=True):
            st.session_state.stato_app["ritardo_accumulato"] += 30
            st.rerun()
        if col_r3.button("+1 Ora", use_container_width=True):
            st.session_state.stato_app["ritardo_accumulato"] += 60
            st.rerun()

    else:
        st.success("🎉 Ciclo di irrigazione completato!")
        if st.button("🔄 Ricomincia Ciclo (Reset)"):
            st.session_state.stato_app["turno_corrente"] = 0
            st.session_state.stato_app["ritardo_accumulato"] = 0
            st.rerun()

    st.write("---")
    st.write("### 📅 Calendario Completo Canalina (Vista Ufficio)")
    df_turni = pd.DataFrame(turni_calcolati)
    df_turni["Inizio"] = df_turni["inizio"].dt.strftime('%d/%m/%Y %H:%M')
    df_turni["Fine Stimata"] = df_turni["fine"].dt.strftime('%d/%m/%Y %H:%M')
    df_turni["Durata (Ore)"] = df_turni["durata"]
    st.dataframe(df_turni[["ordine", "nome", "Inizio", "Fine Stimata", "Durata (Ore)"]], use_container_width=True)

# --- Scheda 2: Censimento Invernale ---
with tab_censimento:
    st.header(f"Censimento Fabbisogno Idrico: {canale_selezionato}")
    st.write("Seleziona un utente per confermare o modificare le ore e la coltura per la prossima stagione.")

    for i, utente in enumerate(utenti_del_canale):
        with st.expander(f"{utente['ordine']}. {utente['nome']} - Ore Attuali: {utente['ore']}, Coltura: {utente['coltura']}"):
            with st.form(key=f"form_censimento_{i}"):
                nuove_ore_cens = st.number_input("Ore Richieste per la Stagione", min_value=0, max_value=200, value=utente['ore'])
                nuova_coltura_cens = st.text_input("Coltura Prevista", value=utente['coltura'])
                nuove_note_cens = st.text_area("Note dell'Acquaiolo (opzionale)", value=utente.get('note', ''))
                
                censimento_submitted = st.form_submit_button("✅ Salva Censimento per questo Utente")
                if censimento_submitted:
                    st.session_state.data_canali[canale_selezionato][i]['ore'] = nuove_ore_cens
                    st.session_state.data_canali[canale_selezionato][i]['coltura'] = nuova_coltura_cens
                    st.session_state.data_canali[canale_selezionato][i]['note'] = nuove_note_cens
                    st.success(f"Censimento per {utente['nome']} salvato con successo!")
                    st.rerun()

# --- Scheda 3: Gestione Anagrafica Utenti ---
with tab_anagrafica:
    st.header(f"Gestione Utenti Canale: {canale_selezionato}")

    with st.expander("➕ Aggiungi Nuovo Utente al Canale"):
        with st.form("form_nuovo_utente", clear_on_submit=True):
            nuovo_nome = st.text_input("Nome e Cognome")
            nuove_ore_anagrafica = st.number_input("Ore di Competenza", min_value=1, max_value=200, value=10)
            submitted = st.form_submit_button("💾 Salva Nuovo Utente")
            if submitted and nuovo_nome:
                nuovo_ordine = len(utenti_del_canale) + 1
                st.session_state.data_canali[canale_selezionato].append({
                    "ordine": nuovo_ordine, "nome": nuovo_nome, "ore": nuove_ore_anagrafica, "coltura": "Da Definire", "note": ""
                })
                st.success(f"Utente {nuovo_nome} aggiunto a {canale_selezionato}!")
                st.rerun()

    st.write("---")
    st.subheader("Elenco Utenti Esistenti")
    
    for i, utente in enumerate(utenti_del_canale):
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
        with col1:
            st.text(f"{utente['ordine']}. {utente['nome']} ({utente['ore']} ore)")
        with col2:
            if st.button("✏️ Modifica", key=f"edit_{i}", use_container_width=True):
                st.info(f"La modifica dell'utente {utente['nome']} avverrà nella sezione 'Censimento Invernale'.")
        with col3:
            if st.button("❌ Rimuovi", key=f"del_{i}", use_container_width=True):
                st.session_state.data_canali[canale_selezionato].pop(i)
                # Riordina gli indici
                for j, u in enumerate(st.session_state.data_canali[canale_selezionato]):
                    u['ordine'] = j + 1
                st.success(f"Utente {utente['nome']} rimosso!")
                st.rerun()
