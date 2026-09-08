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
# DATABASE INIZIALE CON TUTTE E 45 LE CANALETTE E UTENTI
# =========================================================
def get_initial_data():
    raw_data = {
        "1. Corte Emilia": [("Agosta Angelo", 12), ("Bettoni Maurizio", 6), ("Germiniasi Gabriele", 19), ("Aporti Francesco", 6), ("Bettoni Franco", 5), ("Novellini Eugenio", 2)],
        "2. Pirolo Piena": [("Vighini Angelo", 5), ("Marchini Erminio", 5), ("Morselli Davide", 8), ("Sarzi Sartori Ermete", 5), ("Bettoni Franco", 13), ("Carpen Angiolino", 10), ("Sarzi Alex", 2), ("Novellini Eugenio", 2)],
        "3. Pirolo Ridotta 50 Lt": [],
        "4. Cà Lame": [("Aporti Andrea", 9), ("Morselli Davide", 13), ("Novellini Eugenio", 2), ("Maccagnola Cesare", 10)],
        "5. Madonna Lame -160": [("Bertoli Erminio", 25), ("Morselli Davide", 27), ("SCARICO (A e B)", 8), ("Morselli Paolo", 4), ("Dalai Iacopo", 4), ("Maccagnola Cesare", 40), ("Molinari/Maccagnola", 10), ("Zanafredi/Scario", 0), ("Scarico per pomodori", 18), ("Poli Remo", 8), ("Marchini Gianluigi", 27), ("Fercodini Bruno", 20), ("Teresa Volta", 4), ("SCARICO", 18)],
        "6. Madonna Lame Rid": [("Marchini Gianluigi", 22), ("Gardinazzi Wolmer", 30), ("Pezzali", 20), ("Barbieri Alberto 2", 10), ("SCARICO", 12), ("Marchini Gianluigi", 25), ("Gardinazzi Wolmer", 20), ("SCARICO", 5), ("Fercodini Bruno", 33), ("Fercodini", 10), ("Zanafredi Andrea", 29)],
        "7. Cividale Nord A": [("Germiniasi Gabriele", 5), ("Cracco Sante", 45), ("Molinari Daniele", 28), ("Manfredi Filippo", 15), ("Poli", 2), ("Dalai Iacopo", 4)],
        "8. Belvedere Nord": [("Maccagnola", 5), ("Marchini Gianluigi", 10), ("Germiniasi Gabriele", 10), ("Gandolfi F.lli", 3), ("Vicini Giancarlo", 6), ("Zappaterra Attilio", 10), ("Sanguanini", 3)],
        "9. Belvedere Nord Ridotta": [("Pasin Girolamo", 30), ("Pasetti Angelo", 40), ("F.lli Belletti", 40), ("Zappaterra", 40), ("Gandolfi Mauro", 115), ("Malinverni Davide", 15), ("Sanguanini", 4), ("Taraschi Luigi", 16), ("Belletti F.lli", 150)],
        "10. Cividale Nord Vecchia Rid": [("Maccagnola Bruno", 50), ("Dalai Iacipo", 30)],
        "11. Cividale Nord Vecchia": [("Cracco Sante", 6), ("Dalai Iacopo", 13), ("Marchini Gianluigi", 32), ("Maccagnola Bruno", 30)],
        "12. Cividale Nord Vecchia Pvot": [("Maccagnola Bruno", 50)],
        "13. Cò De Vanni I°": [("Maccagnola Bruno", 50), ("Scarico", 8)],
        "14. Cò De Vanni II°": [("Maiocchi", 15), ("Scarico", 2), ("Bernardi Rosolino", 3), ("Arrighi Ettore", 3), ("Casella", 1), ("Scaglioni Antonio", 2), ("Gardani Massimo", 2), ("Morelli Luigi", 5), ("Maiocchi Italo", 13), ("Tolasi", 2), ("Buttarelli Elia", 10), ("Novellini Nicolò", 18), ("Arrighi Ettore 2", 7), ("Scarico", 17), ("Caleffi Manuele", 50), ("Arrighi Ettore 3", 15), ("SCARICO", 15)],
        "15. Cò De Vanni II° Ridotta": [("Paccini Daniel", 20), ("F.lli Freddi", 15), ("Borroni F.lli", 6), ("Beduschi Guglielmina", 29), ("Arrighi Ettore", 35)],
        "16. I° Gruppo Bocchette": [("Gandolfi Mauro", 80)],
        "17. Spineda": [("Scarico", 2), ("Cirelli Luigi", 10), ("Arrighi Ettore", 5), ("Marchini", 8), ("SCARICO", 5)],
        "18. Spineda Ridotta": [("Pagliari Stefano", 20), ("Maiocchi Italo", 15), ("Arrighi Ettore", 15), ("Belletti F.lli", 20), ("SCARICO", 10), ("Arrighi Ettore", 10), ("Freddi Bruno", 20), ("Ardenghi Luigi", 30), ("Arrighi Ettore", 20), ("Arrighi Ettore", 10), ("Maiocchi Italo", 10), ("Caleffi Silvio", 15), ("Gardani Guido", 15), ("Freddi Bruno", 15), ("SCARICO", 15)],
        "19. Fornace Rid.": [("Gandolfi Mauro", 10)],
        "20. S. Fiore I°": [("Novellini Nicolò", 10)],
        "21. S. Fiore I° Rid": [("Sarzi Maurizio", 20), ("Borroni F.lli", 30), ("Maiocchi", 30), ("Pagliari Stefano", 20), ("Maiocchi Italo 2", 20), ("Borroni F.lli", 35), ("SCARICO", 10), ("Novellini Nicolò", 25), ("Pasini Girolamo", 40), ("Morelli Luigi", 20), ("Marchini Gianluigi", 70), ("SCARICO", 10), ("Maiocchi", 10), ("Freddi Bruno", 10), ("Caleffi Silvio", 20), ("Arrighi Ettore", 10), ("Martelli", 10), ("Marchini Giovanni", 20), ("Torchio Giovanni", 85)],
        "22. S. FIORE II° LT. 160 piena": [("SCARICO", 20), ("Novellini Nicolò", 10)],
        "23. S. Fiore II° Rid": [("Maiocchi", 80), ("Novellini Nicolò", 80), ("Ardenghi Umberto", 80)],
        "24. Cà De Bottoli": [("Paganini Lodovico", 40), ("Paganini Lino", 10), ("Rossi (Eredi)", 10), ("SCARICO", 20), ("Grassi Marcello", 20), ("Monici F.lli", 20)],
        "25. Secondario Pomara SEZ. LT. 50": [("Verdi Giuseppe", 75), ("Paganni Lodovico", 35), ("Pagliari Stefano", 40), ("Zappaterra Az.Agr.", 80), ("Novellini Nicolò", 70)],
        "26. Pomara SEZ. LT. 50": [("Noale Giacinto", 35), ("Bislenghi Cesare", 20), ("Cerati", 10), ("SCARICO", 5)],
        "27. Orti Rid": [("Torchio Mario", 10), ("Maffezzoli Giuliano", 70), ("Dall'Acqua Cesare", 10), ("Verdi Giuseppe", 20), ("Dall'Acqua Gianni", 10), ("Bresciani L.", 30), ("Madella Amadei Elena", 20), ("Adami", 10), ("Pagliari Stefano", 40), ("Borroni F.lli", 20), ("Gobbi Frattini L.", 20), ("SCARICO", 10)],
        "28. S. Pietro Piena": [("SCARICO", 3), ("Sanfelici Giuseppe", 44), ("Pasetti", 8), ("UTENTE", 3), ("Balzanelli Arturo", 6), ("Neri Giovanni", 3)],
        "29. S. Pietro Ridotta": [("Vallari (Eredi)", 15), ("Balzanelli Elena", 15), ("Sanfelici Giuseppe", 50), ("Bislenghi Cesare", 10), ("Ferrari Renato", 10), ("Balzanelli Arturo", 10), ("Gobbi Frattini L.", 10), ("Ferrari Mauro", 15), ("Noale Giacinto", 15), ("Paganini", 15), ("Geremia", 15), ("Verdi Giuseppe", 20), ("Morselli Giacomo", 10), ("Borroni", 60)],
        "30. Ossola": [("Galesi Ettore", 50)],
        "31. Ossola. II°": [("Agosta Ciro", 20), ("Galesi Ettore", 20), ("Geremia Bruno", 25), ("Pasetti F.lli", 15)],
        "32. Agraria Rid": [("Monici Giorgio", 20), ("Paglia Giuseppe", 20), ("Cerati Roberto", 10), ("Grassi Marcello", 10), ("Paglia Gianfranco", 20), ("Sarzi A. Selvino", 10), ("Pedrazzoli Ottorino", 25), ("Bislenghi Cesare", 5), ("Pagliari Stefano", 20), ("Scarico", 30), ("Rossi Edo", 10)],
        "33. Manzoglio": [("Galesi", 30), ("Zardi", 15), ("Scarico", 35), ("Cerati", 40), ("Monici Pierino", 40), ("Galesi Ettore", 80)],
        "34. Fiescale": [("Caldarini Nazzareno", 30), ("Calza Riccardo", 30), ("Lodi Rizzini E.", 30), ("Mattioli", 30), ("Martelli Enzo", 20), ("Noale Giacinto", 40), ("Rondelli Franco", 40), ("SCARICO", 20), ("Scarico", 30), ("Geremia Bruno", 40), ("Rondelli Elio", 50)],
        "35. Tessagli Rid": [("Noale Giacinto", 50), ("Calza Riccardo", 40), ("Galesi", 20), ("Rondelli Franco", 20), ("Lodi Rizzini E.", 50), ("Caldarini", 20), ("Rondelli Elio", 50), ("Tenca Giovanni", 20)],
        "36. Roncole": [("SCARICO", 30), ("Galesi", 30), ("Noale Giacinto", 30), ("Padova Francesco", 20), ("SCARICO", 30), ("Rubini Angelo", 30), ("Maccagnola Bruno", 50), ("Maffezzoli Giuliano", 30), ("Monici Pierino", 20), ("Cerati Mario", 60)],
        "37. Vaja Rid": [("SCARICO", 40), ("Mattioli", 40), ("Rondelli Elio", 40), ("SCARICO", 40), ("Maffezzoli Giuliano", 30), ("Novellini Flavio", 50)],
        "38. Riglio -121": [("Paganini Lino", 25), ("Monici Giorgio", 30), ("Cerati Mario", 50), ("Martelli Luigi", 35), ("Pagliari Stefano", 25), ("Pagliari Stefano", 25), ("Rubini Angelo", 40), ("Asinari Matteo", 20), ("Paglia", 30), ("Galesi", 50), ("Paglia Giuseppe", 50), ("SCARICO", 10), ("Silocchi Mauro", 30)],
        "39. Breda 3° -91": [("Morselli Davide", 12), ("Dalai Iacopo", 3), ("Poli", 22)],
        "40. Breda 4° -92": [("Maccagnola", 8), ("Germiniasi Gabriele", 5), ("SCARICO", 6)],
        "41. Delmoncello I°": [("Aporti Andrea", 20), ("Arrighi Ettore", 20), ("Marchini Agr.", 30), ("Bonassi Mauro 1", 20), ("Cracco Sante", 20), ("Bonassi Mauro 2", 20), ("Fercodini Romano", 10), ("Fercodini Massimo", 20), ("Aporti Andrea", 20), ("Mantovani Giulio", 10), ("Maccagnola Bruno", 20)],
        "42. Delmoncello II°": [("Fercodini Massimo", 3), ("Marchini Gianluigi", 2), ("Morselli Davide", 2), ("Bertoli Erminio", 3)],
        "43. Casamerlino Rid": [("Maccagnola Bruno", 20)],
        "44. Bocchette Sec Casalmerlino": [("Alquati", 8), ("Fercodini Massimo", 4), ("Cozzani", 2)],
        "45. Bocchette sec. casalm.": [("Dalai", 15), ("Fercodini Romano", 15), ("Fazzi", 30), ("Bellini Fabio", 30)]
    }
    
    data_canali = {}
    for canale, utenti in raw_data.items():
        if not utenti: # Gestione canali momentaneamente vuoti
            data_canali[canale] = []
        else:
            data_canali[canale] = [
                {"ordine": i+1, "nome": nome, "ore": ore, "coltura": "Da Definire", "note": ""}
                for i, (nome, ore) in enumerate(utenti)
            ]
    return data_canali

# Inizializzazione Session State
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

stato_canale = st.session_state.stato_canali[canale_selezionato]
utenti_canale = st.session_state.data_canali[canale_selezionato]

with col_sel2:
    st.metric("Utenti Registrati in questa Canaletta", f"{len(utenti_canale)} / 100 max")

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
                        colture_opzioni = ["Mais", "Pomodoro", "Erba Medica", "Soia", "Riso", "Ortaggi", "Da Definire", "Altro", "Scarico"]
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
