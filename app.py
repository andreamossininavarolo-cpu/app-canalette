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
            {"ordine": 2, "nome": "Marchini Gianluigi", "ore": 10, "coltura": "Soia", "note": ""},
            {"ordine": 3, "nome": "Germiniasi Gabriele", "ore": 10, "coltura": "Mais", "note": ""},
            {"ordine": 4, "nome": "Gandolfi F.lli", "ore": 3, "coltura": "Erba Medica", "note": ""},
            {"ordine": 5, "nome": "Vicini Giancarlo", "ore": 6, "coltura": "Mais", "note": ""},
            {"ordine": 6, "nome": "Zappaterra Attilio", "ore": 10, "coltura": "Pomodoro", "note": ""},
            {"ordine": 7, "nome": "Sanguanini", "ore": 3, "coltura": "Ortaggi", "note": ""}
        ],
        "Cò De Vanni I°": [
            {"ordine": 1, "nome": "Maccagnola Bruno", "ore": 50, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Scarico", "ore": 8, "coltura": "Scarico", "note": ""}
        ],
        "Cò De Vanni II°": [
            {"ordine": 1, "nome": "Maiocchi", "ore": 15, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Scarico", "ore": 2, "coltura": "Scarico", "note": ""},
            {"ordine": 3, "nome": "Bernardi Rosolino", "ore": 3, "coltura": "Soia", "note": ""},
            {"ordine": 4, "nome": "Arrighi Ettore", "ore": 3, "coltura": "Mais", "note": ""},
            {"ordine": 5, "nome": "Casella", "ore": 1, "coltura": "Ortaggi", "note": ""},
            {"ordine": 6, "nome": "Scaglioni Antonio", "ore": 2, "coltura": "Erba Medica", "note": ""},
            {"ordine": 7, "nome": "Gardani Massimo", "ore": 2, "coltura": "Mais", "note": ""},
            {"ordine": 8, "nome": "Morelli Luigi", "ore": 5, "coltura": "Pomodoro", "note": ""},
            {"ordine": 9, "nome": "Maiocchi Italo", "ore": 13, "coltura": "Soia", "note": ""},
            {"ordine": 10, "nome": "Tolasi", "ore": 2, "coltura": "Mais", "note": ""},
            {"ordine": 11, "nome": "Buttarelli Elia", "ore": 10, "coltura": "Erba Medica", "note": ""},
            {"ordine": 12, "nome": "Novellini Nicolò", "ore": 18, "coltura": "Mais", "note": ""},
            {"ordine": 13, "nome": "Arrighi Ettore 2", "ore": 7, "coltura": "Soia", "note": ""},
            {"ordine": 14, "nome": "Scarico", "ore": 17, "coltura": "Scarico", "note": ""},
            {"ordine": 15, "nome": "Caleffi Manuele", "ore": 50, "coltura": "Mais", "note": ""},
            {"ordine": 16, "nome": "Arrighi Ettore 3", "ore": 15, "coltura": "Pomodoro", "note": ""},
            {"ordine": 17, "nome": "SCARICO", "ore": 15, "coltura": "Scarico", "note": ""}
        ],
        "Spineda": [
            {"ordine": 1, "nome": "Scarico", "ore": 2, "coltura": "Scarico", "note": ""},
            {"ordine": 2, "nome": "Cirelli Luigi", "ore": 10, "coltura": "Mais", "note": ""},
            {"ordine": 3, "nome": "Arrighi Ettore", "ore": 5, "coltura": "Soia", "note": ""},
            {"ordine": 4, "nome": "Marchini", "ore": 8, "coltura": "Erba Medica", "note": ""},
            {"ordine": 5, "nome": "SCARICO", "ore": 5, "coltura": "Scarico", "note": ""}
        ],
        "S. Pietro Piena": [
            {"ordine": 1, "nome": "SCARICO", "ore": 3, "coltura": "Scarico", "note": ""},
            {"ordine": 2, "nome": "Sanfelici Giuseppe", "ore": 44, "coltura": "Mais", "note": ""},
            {"ordine": 3, "nome": "Pasetti", "ore": 8, "coltura": "Soia", "note": ""},
            {"ordine": 4, "nome": "UTENTE", "ore": 3, "coltura": "Mais", "note": ""},
            {"ordine": 5, "nome": "Balzanelli Arturo", "ore": 6, "coltura": "Erba Medica", "note": ""},
            {"ordine": 6, "nome": "Neri Giovanni", "ore": 3, "coltura": "Ortaggi", "note": ""}
        ],
        "Fiescale": [
            {"ordine": 1, "nome": "Caldarini Nazzareno", "ore": 30, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Calza Riccardo", "ore": 30, "coltura": "Soia", "note": ""},
            {"ordine": 3, "nome": "Lodi Rizzini E.", "ore": 30, "coltura": "Erba Medica", "note": ""},
            {"ordine": 4, "nome": "Mattioli", "ore": 30, "coltura": "Mais", "note": ""},
            {"ordine": 5, "nome": "Martelli Enzo", "ore": 20, "coltura": "Pomodoro", "note": ""},
            {"ordine": 6, "nome": "Noale Giacinto", "ore": 40, "coltura": "Mais", "note": ""},
            {"ordine": 7, "nome": "Rondelli Franco", "ore": 40, "coltura": "Soia", "note": ""},
            {"ordine": 8, "nome": "SCARICO", "ore": 20, "coltura": "Scarico", "note": ""},
            {"ordine": 9, "nome": "Scarico", "ore": 30, "coltura": "Scarico", "note": ""},
            {"ordine": 10, "nome": "Geremia Bruno", "ore": 40, "coltura": "Mais", "note": ""},
            {"ordine": 11, "nome": "Rondelli Elio", "ore": 50, "coltura": "Mais", "note": ""}
        ],
        "Bocchette Sec Casalmerlino": [
            {"ordine": 1, "nome": "Alquati", "ore": 8, "coltura": "Mais", "note": ""},
            {"ordine": 2, "nome": "Fercodini Massimo", "ore": 4, "coltura": "Soia", "note": ""},
            {"ordine": 3, "nome": "Cozzani", "ore": 2, "coltura": "Ortaggi", "note": ""}
        ]
    }

if 'data_canali' not in st.session_state:
    st.session_state.data_canali = get_initial_data()

if 'stato_canali' not in st.session_state:
    st.session_state.stato_canali = {
        canale: {"turno_corrente": 0, "ritardo_minuti": 0, "data_partenza": datetime(2027, 5, 3, 20, 0, 0)}
        for canale in st.session_state.data_canali.keys()
    }

# =========================================================
# HEADER E SELETTORE CANALE
# =========================================================
st.markdown("<h1 style='text-align: center; color: #1D3557;'>💧 Gestione Integrata Canalette</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #457B9D;'>Consorzio di Bonifica Navarolo - Agro Cremonese Mantovano</p>", unsafe_allow_html=True)

lista_canali = list(st.session_state.data_canali.keys())

col_sel1, col_sel2 = st.columns([3, 1])
with col_sel1:
    canale_selezionato = st.selectbox("Seleziona la Canaletta su cui operare:", lista_canali)

if canale_selezionato not in st.session_state.stato_canali:
    st.session_state.stato_canali[canale_selezionato] = {
        "turno_corrente": 0,
        "ritardo_minuti": 0,
        "data_partenza": datetime(2027, 5, 3, 20, 0, 0)
    }

stato_canale = st.session_state.stato_canali[canale_selezionato]
utenti_canale = st.session_state.data_canali[canale_selezionato]

with col_sel2:
    st.metric("Utenti Registrati", f"{len(utenti_canale)} / 100 max")

st.write("---")

# =========================================================
# SCHEDE OPERATIVE (TABS)
# =========================================================
tab_turni, tab_censimento, tab_anagrafica = st.tabs([
    "💧 Gestione Turni (Estivo)",
    "🌾 Censimento Invernale",
    "👥 Gestione Anagrafica"
])

# ---------------------------------------------------------
# TAB 1: GESTIONE TURNI (ESTIVO)
# ---------------------------------------------------------
with tab_turni:
    st.subheader(f"Operatività: {canale_selezionato}")

    # Calcolo sequenziale a cascata
    turni_calcolati = []
    orario_progressivo = stato_canale["data_partenza"]

    for i, u in enumerate(utenti_canale):
        inizio_nominale = orario_progressivo
        inizio_effettivo = inizio_nominale

        # Applica ritardo solo dal turno attivo in avanti
        if i >= stato_canale["turno_corrente"]:
            inizio_effettivo += timedelta(minutes=stato_canale["ritardo_minuti"])

        fine_effettiva = inizio_effettivo + timedelta(hours=u["ore"])

        turni_calcolati.append({
            "ordine": u["ordine"],
            "nome": u["nome"],
            "inizio": inizio_effettivo,
            "fine": fine_effettiva,
            "durata": u["ore"]
        })

        orario_progressivo = inizio_nominale + timedelta(hours=u["ore"])

    # Visualizzazione Turno Attivo
    idx = stato_canale["turno_corrente"]

    if len(turni_calcolati) > 0 and idx < len(turni_calcolati):
        t_attivo = turni_calcolati[idx]

        st.markdown(f"""
        <div style="background-color: #E6F3FF; padding: 18px; border-radius: 12px; border-left: 8px solid #1D3557; margin-bottom: 15px;">
            <span style="color: #457B9D; font-weight: bold; font-size: 12px; text-transform: uppercase;">🔴 TURNO ATTUALE IN CORSO</span>
            <h2 style="margin: 4px 0; color: #1D3557;">{t_attivo['nome']}</h2>
            <p style="margin: 0; font-size: 15px; color: #1D3557;">
                Inizio presa: <b>{t_attivo['inizio'].strftime('%d/%m/%Y alle %H:%M')}</b> &nbsp;|&nbsp; 
                Fine stimata: <b style="color: #E63946;">{t_attivo['fine'].strftime('%d/%m/%Y alle %H:%M')}</b> ({t_attivo['durata']} ore)
            </p>
        </div>
        """, unsafe_allow_html=True)

        if idx + 1 < len(turni_calcolati):
            t_succ = turni_calcolati[idx + 1]
            st.markdown(f"""
            <div style="background-color: #F1FAEE; padding: 12px; border-radius: 10px; border-left: 5px solid #2A9D8F; margin-bottom: 20px;">
                <span style="color: #2A9D8F; font-weight: bold; font-size: 11px;">⏭️ PROSSIMO IN CODA:</span>
                <h4 style="margin: 2px 0; color: #1D3557;">{t_succ['nome']} ({t_succ['durata']} ore)</h4>
                <p style="margin: 0; font-size: 13px; color: #1D3557;">Inizio previsto: <b>{t_succ['inizio'].strftime('%d/%m/%Y ore %H:%M')}</b></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Questo è l'ultimo consorziato della sequenza.")

        # Pulsanti Azione Acquaiolo
        st.write("#### ⚙️ Azioni Rapide Acquaiolo")
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("✅ Turno Concluso / Passa al Successivo", use_container_width=True):
                if stato_canale["turno_corrente"] + 1 < len(utenti_canale):
                    stato_canale["turno_corrente"] += 1
                    st.rerun()
                else:
                    st.success("Tutti i turni della canaletta sono completati!")

        with btn_c2:
            if st.button("🔄 Ripristina Primo Turno", use_container_width=True):
                stato_canale["turno_corrente"] = 0
                stato_canale["ritardo_minuti"] = 0
                st.rerun()

        # Gestione Ritardi
        st.write("---")
        st.write("⚠️ **Segnalazione Ritardo sul Campo** (ricalcola all'istante i turni successivi):")
        r_c1, r_c2, r_c3, r_c4 = st.columns(4)
        with r_c1:
            if st.button("+15 Minuti", use_container_width=True):
                stato_canale["ritardo_minuti"] += 15
                st.rerun()
        with r_c2:
            if st.button("+30 Minuti", use_container_width=True):
                stato_canale["ritardo_minuti"] += 30
                st.rerun()
        with r_c3:
            if st.button("+1 Ora", use_container_width=True):
                stato_canale["ritardo_minuti"] += 60
                st.rerun()
        with r_c4:
            if st.button("Azzera Ritardi", use_container_width=True):
                stato_canale["ritardo_minuti"] = 0
                st.rerun()

        if stato_canale["ritardo_minuti"] > 0:
            st.warning(f"⚠️ Ritardo cumulativo attivo su questo canale: **{stato_canale['ritardo_minuti']} minuti**.")
    else:
        st.info("Nessun utente inserito in questa canaletta. Aggiungine uno nella scheda 'Gestione Anagrafica'.")

    # Tabella completa di riepilogo
    if len(turni_calcolati) > 0:
        st.write("---")
        st.write("### 📅 Tabella Orari Completa (Vista Ufficio)")
        df_t = pd.DataFrame(turni_calcolati)
        df_t["Inizio Previsto"] = df_t["inizio"].dt.strftime('%d/%m/%Y %H:%M')
        df_t["Fine Prevista"] = df_t["fine"].dt.strftime('%d/%m/%Y %H:%M')
        df_t["Ore"] = df_t["durata"]
        st.dataframe(df_t[["ordine", "nome", "Inizio Previsto", "Fine Prevista", "Ore"]], use_container_width=True)

# ---------------------------------------------------------
# TAB 2: CENSIMENTO INVERNALE (COLTURE & ORE)
# ---------------------------------------------------------
with tab_censimento:
    st.subheader(f"🌾 Censimento Fabbisogno Invernale: {canale_selezionato}")
    st.write("Compila le ore richieste e la coltura durante le visite invernali ai consorziati.")

    if len(utenti_canale) == 0:
        st.info("Nessun utente da censire in questo canale.")
    else:
        for idx_u, u in enumerate(utenti_canale):
            with st.expander(f"{u['ordine']}. {u['nome']} - Attuali: {u['ore']} ore ({u['coltura']})"):
                with st.form(f"form_censimento_{canale_selezionato}_{idx_u}"):
                    c_col1, c_col2 = st.columns(2)
                    with c_col1:
                        nuove_ore = st.number_input(
                            f"Ore Richieste per la Nuova Stagione:",
                            min_value=0, max_value=200, value=int(u["ore"])
                        )
                    with c_col2:
                        colture_opzioni = ["Mais", "Pomodoro", "Erba Medica", "Soia", "Riso", "Ortaggi", "Altro", "Scarico"]
                        idx_c = colture_opzioni.index(u["coltura"]) if u["coltura"] in colture_opzioni else 0
                        nuova_coltura = st.selectbox("Coltura Prevista:", colture_opzioni, index=idx_c)

                    nuove_note = st.text_area("Note / Modifiche Terreno (opzionale):", value=u.get("note", ""))

                    if st.form_submit_button("💾 Salva Dati Censimento", use_container_width=True):
                        st.session_state.data_canali[canale_selezionato][idx_u]["ore"] = nuove_ore
                        st.session_state.data_canali[canale_selezionato][idx_u]["coltura"] = nuova_coltura
                        st.session_state.data_canali[canale_selezionato][idx_u]["note"] = nuove_note
                        st.success(f"Dati aggiornati per {u['nome']}!")
                        st.rerun()

        st.write("---")
        st.write("### 📊 Riepilogo Censimento Invernale")
        df_cens = pd.DataFrame(utenti_canale)
        st.dataframe(df_cens[["ordine", "nome", "ore", "coltura", "note"]], use_container_width=True)

# ---------------------------------------------------------
# TAB 3: GESTIONE ANAGRAFICA (AGGIUNGI, MODIFICA, RIMUOVI)
# ---------------------------------------------------------
with tab_anagrafica:
    st.subheader(f"👥 Gestione Consorziati: {canale_selezionato}")

    # Modulo Aggiunta Nuovo Utente
    with st.expander("➕ Inserisci Nuovo Utente (Massimo 100 per Canale)"):
        if len(utenti_canale) >= 100:
            st.error("Hai raggiunto il limite massimo di 100 utenti per questo canale.")
        else:
            with st.form("form_nuovo_nominativo", clear_on_submit=True):
                in_nome = st.text_input("Cognome e Nome / Ditta:")
                in_ore = st.number_input("Ore di Competenza:", min_value=1, max_value=200, value=10)
                in_coltura = st.selectbox("Coltura Iniziale:", ["Mais", "Pomodoro", "Erba Medica", "Soia", "Ortaggi", "Altro", "Scarico"])
                in_note = st.text_input("Note (es. Mappale, Frazione):", "")

                if st.form_submit_button("💾 Salva e Aggiungi in Coda", use_container_width=True):
                    if in_nome.strip():
                        nuovo_ordine = len(utenti_canale) + 1
                        st.session_state.data_canali[canale_selezionato].append({
                            "ordine": nuovo_ordine,
                            "nome": in_nome.strip(),
                            "ore": in_ore,
                            "coltura": in_coltura,
                            "note": in_note.strip()
                        })
                        st.success(f"Utente '{in_nome.strip()}' inserito con successo con ordine #{nuovo_ordine}!")
                        st.rerun()
                    else:
                        st.warning("Inserisci il nome del consorziato.")

    st.write("---")
    st.write(f"#### Elenco Nominativi Esistenti ({len(utenti_canale)} su 100 max)")

    for idx_u, u in enumerate(utenti_canale):
        col_info, col_mod, col_del = st.columns([0.6, 0.25, 0.15])
        with col_info:
            st.write(f"**#{u['ordine']} - {u['nome']}** | {u['ore']}h | {u['coltura']}")
        with col_mod:
            # Modifica rapida ore
            nuove_ore_veloci = st.number_input(
                f"Mod. Ore", min_value=1, max_value=200, value=int(u["ore"]),
                key=f"qore_{canale_selezionato}_{idx_u}", label_visibility="collapsed"
            )
            if nuove_ore_veloci != u["ore"]:
                st.session_state.data_canali[canale_selezionato][idx_u]["ore"] = nuove_ore_veloci
                st.rerun()
        with col_del:
            if st.button("🗑️", key=f"del_{canale_selezionato}_{idx_u}", help="Elimina utente"):
                st.session_state.data_canali[canale_selezionato].pop(idx_u)
                # Riordina la sequenza progressiva
                for j, user in enumerate(st.session_state.data_canali[canale_selezionato]):
                    user["ordine"] = j + 1
                if stato_canale["turno_corrente"] >= len(st.session_state.data_canali[canale_selezionato]):
                    stato_canale["turno_corrente"] = max(0, len(st.session_state.data_canali[canale_selezionato]) - 1)
                st.rerun()
