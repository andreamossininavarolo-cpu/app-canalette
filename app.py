import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configurazione della pagina ottimizzata per smartphone
st.set_page_config(
    page_title="Gestione Canalette - Consorzio Navarolo",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# 1. INIZIALIZZAZIONE DATI E STATO
# ---------------------------------------------------------
UTENTI_CORTE_EMILIA = [
    {"ordine": 1, "nome": "Agosta Angelo", "ore": 12, "coltura": "Mais"},
    {"ordine": 2, "nome": "Bettoni Maurizio", "ore": 6, "coltura": "Mais"},
    {"ordine": 3, "nome": "Germiniasi Gabriele", "ore": 19, "coltura": "Erba Medica"},
    {"ordine": 4, "nome": "Aporti Francesco", "ore": 6, "coltura": "Mais"},
    {"ordine": 5, "nome": "Bettoni Franco", "ore": 5, "coltura": "Pomodoro"},
    {"ordine": 6, "nome": "Novellini Eugenio", "ore": 2, "coltura": "Soia"}
]

# Salvataggio dello stato della sessione (ritardi, turni, censimento)
if 'ritardo_accumulato' not in st.session_state:
    st.session_state.ritardo_accumulato = 0
if 'turno_corrente' not in st.session_state:
    st.session_state.turno_corrente = 0
if 'censimento' not in st.session_state:
    st.session_state.censimento = {
        u["nome"]: {"coltura": u["coltura"], "ore": u["ore"], "note": "", "stato": "⚪ Da Visitare"}
        for u in UTENTI_CORTE_EMILIA
    }

# ---------------------------------------------------------
# 2. INTESTAZIONE E SELETTORE MODALITÀ (SCHEDE / TABS)
# ---------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: #1D3557;'>💧 Controllo Canalette</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #457B9D;'>Canale: <b>Corte Emilia</b> - Consorzio Navarolo</p>", unsafe_allow_html=True)

# Creazione delle due schede operative
tab_estivo, tab_invernale = st.tabs(["💧 Gestione Turni (Estivo)", "🌾 Censimento Invernale"])

# =========================================================
# TAB 1: GESTIONE TURNI (OPERATIVITÀ ESTIVA)
# =========================================================
with tab_estivo:
    data_partenza_base = datetime(2027, 5, 3, 20, 0, 0)  # Partenza: 03/05/2027 ore 20:00 (Ruota Dispari)
    
    turni_calcolati = []
    orario_corrente = data_partenza_base

    for i, utente in enumerate(UTENTI_CORTE_EMILIA):
        # Utilizza le ore aggiornate dal censimento invernale se presenti
        ore_competenza = st.session_state.censimento[utente["nome"]]["ore"]
        
        inizio_turno_base = orario_corrente
        inizio_turno_reale = inizio_turno_base
        
        if i >= st.session_state.turno_corrente:
            inizio_turno_reale += timedelta(minutes=st.session_state.ritardo_accumulato)
            
        fine_turno = inizio_turno_reale + timedelta(hours=ore_competenza)
        
        turni_calcolati.append({
            "ordine": utente["ordine"],
            "nome": utente["nome"],
            "inizio": inizio_turno_reale,
            "fine": fine_turno,
            "durata": ore_competenza
        })
        
        orario_corrente = inizio_turno_base + timedelta(hours=ore_competenza)

    idx_attivo = st.session_state.turno_corrente
    if idx_attivo < len(turni_calcolati):
        attivo = turni_calcolati[idx_attivo]
        
        # Box Turno Attuale
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
        
        # Prossimo turno in coda
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

    st.write("---")
    st.write("### 📅 Calendario Completo Canalina (Ufficio)")
    df_turni = pd.DataFrame(turni_calcolati)
    df_turni["Inizio"] = df_turni["inizio"].dt.strftime('%d/%m/%Y %H:%M')
    df_turni["Fine Stimata"] = df_turni["fine"].dt.strftime('%d/%m/%Y %H:%M')
    df_turni["Durata (Ore)"] = df_turni["durata"]
    st.table(df_turni[["ordine", "nome", "Inizio", "Fine Stimata", "Durata (Ore)"]])


# =========================================================
# TAB 2: CENSIMENTO INVERNALE (VISITE UTENTI)
# =========================================================
with tab_invernale:
    st.write("### 🌾 Censimento Invernale Colture & Fabbisogno")
    st.write("Compila le informazioni raccolte durante le visite invernali ai consorziati.")
    
    # Selezione Utente da intervistare
    utente_sel = st.selectbox("Seleziona Consorziato da Intervistare:", list(st.session_state.censimento.keys()))
    dati_attuali = st.session_state.censimento[utente_sel]

    st.info(f"**Stato Visita:** {dati_attuali['stato']} | **Ore Anno Precedente:** {dati_attuali['ore']}h")

    with st.form("form_censimento"):
        st.write(f"#### Rilevazione per: **{utente_sel}**")

        # Selezione Coltura
        colture_disponibili = ["Mais", "Pomodoro", "Erba Medica", "Soia", "Riso", "Ortaggi / Altro"]
        idx_coltura = colture_disponibili.index(dati_attuali["coltura"]) if dati_attuali["coltura"] in colture_disponibili else 0
        nuova_coltura = st.selectbox("Coltura Prevista per la Prossima Stagione:", colture_disponibili, index=idx_coltura)

        # Inserimento Nuove Ore
        nuove_ore = st.number_input("Ore di Competenza Richieste:", min_value=0, max_value=200, value=int(dati_attuali["ore"]))
        
        # Note dell'acquaiolo
        note = st.text_area("Note dell'Utente o dell'Acquaiolo (opzionale):", value=dati_attuali["note"], placeholder="Es. Cambio parcella, cessione terreno...")

        btn_salva = st.form_submit_button("💾 Salva e Conferma Censimento", use_container_width=True)

    if btn_salva:
        st.session_state.censimento[utente_sel] = {
            "coltura": nuova_coltura,
            "ore": nuove_ore,
            "note": note,
            "stato": "🟢 Completato"
        }
        st.success(f"Censimento per {utente_sel} salvato con successo!")
        st.rerun()

    st.write("---")
    st.write("### 📊 Riepilogo Censimento Canaletta (Vista Ufficio)")
    df_cens = pd.DataFrame.from_dict(st.session_state.censimento, orient='index')
    st.dataframe(df_cens, use_container_width=True)
