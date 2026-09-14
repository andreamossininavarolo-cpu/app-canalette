import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# =========================================================
# CONFIGURAZIONE DELLA PAGINA E STILE
# =========================================================
st.set_page_config(
    page_title="Gestione Canalette - Consorzio Navarolo",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    h1 {
        font-size: 1.8em !important;
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
    }
    [data-testid="column"] {
        width: calc(33.333% - 6px) !important;
        flex: 1 1 calc(33.333% - 6px) !important;
        min-width: calc(33% - 6px) !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNZIONI PER DATE IN ITALIANO
# =========================================================
GIORNI_IT = {"Monday": "lunedì", "Tuesday": "martedì", "Wednesday": "mercoledì", "Thursday": "giovedì", "Friday": "venerdì", "Saturday": "sabato", "Sunday": "domenica"}
MESI_IT = {"January": "gennaio", "February": "febbraio", "March": "marzo", "April": "aprile", "May": "maggio", "June": "giugno", "July": "luglio", "August": "agosto", "September": "settembre", "October": "ottobre", "November": "novembre", "December": "dicembre"}

def formatta_data_it(dt):
    g_sett = GIORNI_IT.get(dt.strftime('%A'), dt.strftime('%A'))
    g_num = dt.strftime('%d')
    mese = MESI_IT.get(dt.strftime('%B'), dt.strftime('%B'))
    anno = dt.strftime('%y')
    ora = dt.strftime('%H:%M')
    return f"{g_sett} {g_num} <b>{mese}</b> '{anno} alle ore <b>{ora}</b>"

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
        if not utenti: 
            data_canali[canale] = []
        else:
            data_canali[canale] = [{"ordine": i+1, "nome": nome, "ore": ore, "coltura": "Da Definire", "note": ""} for i, (nome, ore) in enumerate(utenti)]
    return data_canali

# Inizializzazione Session State
if 'data_canali' not in st.session_state or len(st.session_state.data_canali) < 40:
    st.session_state.data_canali = get_initial_data()

if 'stato_canali' not in st.session_state or len(st.session_state.stato_canali) < 40:
    st.session_state.stato_canali = {
        canale: {"turno_corrente": 0, "ritardo_minuti": 0, "data_partenza": datetime(2027, 5, 3, 20, 0, 0)}
        for canale in st.session_state.data_canali.keys()
    }

if 'data_selezionata' not in st.session_state:
    st.session_state.data_selezionata = datetime.now().date()

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
        if i >= stato_canale["turno_corrente"]:
            inizio_effettivo += timedelta(minutes=stato_canale["ritardo_minuti"])
        fine_effettiva = inizio_effettivo + timedelta(hours=u["ore"])
        turni_calcolati.append({
            "ordine": u["ordine"], "nome": u["nome"], "inizio": inizio_effettivo,
            "fine": fine_effettiva, "durata": u["ore"]
        })
        orario_progressivo = inizio_nominale + timedelta(hours=u["ore"])

    # Pulsanti di Navigazione Rapida
    col_ieri, col_oggi, col_domani = st.columns(3)
    with col_ieri:
        if st.button("⬅️ IERI", use_container_width=True):
            st.session_state.data_selezionata -= timedelt
