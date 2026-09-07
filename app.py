import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configurazione della pagina ottimizzata per smartphone
st.set_page_config(
    page_title="Gestione Canalette - Acquaioli",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 1. DATI REALI CARICATI (Canaletta: Corte Emilia)
UTENTI_CORTE_EMILIA = [
    {"ordine": 1, "nome": "Agosta Angelo", "ore": 12, "presa_dispari": 20, "presa_pari": 8},
    {"ordine": 2, "nome": "Bettoni Maurizio", "ore": 6, "presa_dispari": 8, "presa_pari": 20},
    {"ordine": 3, "nome": "Germiniasi Gabriele", "ore": 19, "presa_dispari": 14, "presa_pari": 2},
    {"ordine": 4, "nome": "Aporti Francesco", "ore": 6, "presa_dispari": 9, "presa_pari": 21},
    {"ordine": 5, "nome": "Bettoni Franco", "ore": 5, "presa_dispari": 15, "presa_pari": 3},
    {"ordine": 6, "nome": "Novellini Eugenio", "ore": 2, "presa_dispari": 20, "presa_pari": 8}
]

# 2. INIZIALIZZAZIONE DELLO STATO DELL'APP
if 'ritardo_accumulato' not in st.session_state:
    st.session_state.ritardo_accumulato = 0  # espresso in minuti
if 'turno_corrente' not in st.session_state:
    st.session_state.turno_corrente = 0

# Titolo App (CORRETTO - Senza vecchi parametri errati)
st.markdown("<h1 style='text-align: center; color: #1D3557;'>💧 Controllo Canalette</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #457B9D;'>Canale: <b>Corte Emilia</b> - Ruota Dispari</p>", unsafe_allow_html=True)
st.write("---")

# Data di partenza concordata
data_partenza_base = datetime(2027, 5, 3, 20, 0, 0) # 03/05/2027 alle 20:00

# 3. CALCOLO DINAMICO DEI TURNI
turni_calcolati = []
orario_corrente = data_partenza_base

for i, utente in enumerate(UTENTI_CORTE_EMILIA):
    inizio_turno_base = orario_corrente
    
    # Applica il ritardo accumulato solo dal turno in cui si è verificato in poi
    inizio_turno_reale = inizio_turno_base
    if i >= st.session_state.turno_corrente:
        inizio_turno_reale += timedelta(minutes=st.session_state.ritardo_accumulato)
        
    fine_turno = inizio_turno_reale + timedelta(hours=utente["ore"])
    
    turni_calcolati.append({
        "ordine": utente["ordine"],
        "nome": utente["nome"],
        "inizio": inizio_turno_reale,
        "fine": fine_turno,
        "durata": utente["ore"]
    })
    
    # Il prossimo turno parte esattamente quando finisce questo
    orario_corrente = inizio_turno_base + timedelta(hours=utente["ore"])

# 4. SCHERMATA CELLULARE ACQUAIOLO
idx_attivo = st.session_state.turno_corrente
if idx_attivo < len(turni_calcolati):
    attivo = turni_calcolati[idx_attivo]
    
    # 🟢 Box Stato Attuale (CORRETTO)
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
    
    # ⏭️ Prossimo Turno in Coda (CORRETTO)
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

    # 🛠️ PULSANTI PER GLI ACQUAIOLI
    st.write("### ⚙️ Azioni Rapide Acquaiolo")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Turno Fatto / Avanti", use_container_width=True):
            if st.session_state.turno_corrente + 1 < len(UTENTI_CORTE_EMILIA):
                st.session_state.turno_corrente += 1
                st.rerun()
            else:
                st.success("Tutti i turni di questa canaletta sono terminati!")
                
    with col2:
        if st.button("🔄 Ripristina Test", use_container_width=True):
            st.session_state.turno_corrente = 0
            st.session_state.ritardo_accumulato = 0
            st.rerun()

    # Gestione Ritardi sul campo
    st.write("---")
    st.write("⚠️ **C'è un ritardo in questo turno?**")
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        if st.button("+15 Min", use_container_width=True):
            st.session_state.ritardo_accumulato += 15
            st.rerun()
    with col_r2:
        if st.button("+30 Min", use_container_width=True):
            st.session_state.ritardo_accumulato += 30
            st.rerun()
    with col_r3:
        if st.button("+1 Ora", use_container_width=True):
            st.session_state.ritardo_accumulato += 60
            st.rerun()

    if st.session_state.ritardo_accumulato > 0:
        st.warning(f"Ritardo applicato alla cascata: **{st.session_state.ritardo_accumulato} minuti**")

else:
    st.success("🎉 Ciclo di irrigazione completato con successo!")
    if st.button("🔄 Ricomincia Ciclo (Reset)"):
        st.session_state.turno_corrente = 0
        st.session_state.ritardo_accumulato = 0
        st.rerun()

# 5. TABELLA DI RIEPILOGO COMPLETA (Vista Ufficio in basso)
st.write("---")
st.write("### 📅 Calendario Completo Canalina (Ufficio)")
df_turni = pd.DataFrame(turni_calcolati)
df_turni["Inizio"] = df_turni["inizio"].dt.strftime('%d/%m/%Y %H:%M')
df_turni["Fine Stimata"] = df_turni["fine"].dt.strftime('%d/%m/%Y %H:%M')
df_turni["Durata (Ore)"] = df_turni["durata"]
st.table(df_turni[["ordine", "nome", "Inizio", "Fine Stimata", "Durata (Ore)"]])
