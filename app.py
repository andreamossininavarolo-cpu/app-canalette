import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- Configurazione Pagina e Stile Compatto Mobile ---
st.set_page_config(page_title="Turni Navarolo", layout="centered")

st.markdown("""
<style>
    h1 { font-size: 1.8em !important; margin: 0 !important; padding: 0 !important; }
    [data-testid="column"] {
        width: calc(33.333% - 8px) !important;
        flex: 1 1 calc(33.333% - 8px) !important;
        min-width: calc(33% - 8px) !important;
    }
    [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌊 Turni Irrigui Storti")

GIORNI_IT = {"Monday": "lunedì", "Tuesday": "martedì", "Wednesday": "mercoledì", "Thursday": "giovedì", "Friday": "venerdì", "Saturday": "sabato", "Sunday": "domenica"}
MESI_IT = {"January": "gennaio", "February": "febbraio", "March": "marzo", "April": "aprile", "May": "maggio", "June": "giugno", "July": "luglio", "August": "agosto", "September": "settembre", "October": "ottobre", "November": "novembre", "December": "dicembre"}

def formatta_data_it(dt):
    g_sett = GIORNI_IT.get(dt.strftime('%A'), dt.strftime('%A'))
    g_num = dt.strftime('%d')
    mese = MESI_IT.get(dt.strftime('%B'), dt.strftime('%B'))
    anno = dt.strftime('%y')
    ora = dt.strftime('%H:%M')
    return f"{g_sett} {g_num} <b>{mese}</b> '{anno} alle ore <b>{ora}</b>"

def get_initial_data():
    return pd.DataFrame([
        {"Canale": "Corte Emilia", "Ore": 50.0, "Data_Partenza": "02/05/2026", "Ora_Partenza": "20:00"},
        {"Canale": "Pirolo", "Ore": 50.0, "Data_Partenza": "04/05/2026", "Ora_Partenza": "22:00"},
        {"Canale": "Pirolo Rid.", "Ore": 0.0, "Data_Partenza": "07/05/2026", "Ora_Partenza": "00:00"},
        {"Canale": "Cà Lame", "Ore": 34.0, "Data_Partenza": "07/05/2026", "Ora_Partenza": "00:00"},
        {"Canale": "Madonna Lame", "Ore": 213.0, "Data_Partenza": "08/05/2026", "Ora_Partenza": "10:00"},
        {"Canale": "Madonna Lame ridotta", "Ore": 72.0, "Data_Partenza": "22/04/2026", "Ora_Partenza": "07:00"},
        {"Canale": "Cividale Nord A", "Ore": 99.0, "Data_Partenza": "25/04/2026", "Ora_Partenza": "07:00"},
        {"Canale": "Belvedere Nord", "Ore": 41.0, "Data_Partenza": "29/04/2026", "Ora_Partenza": "10:00"},
        {"Canale": "Belvedere Nord rid", "Ore": 150.0, "Data_Partenza": "01/05/2026", "Ora_Partenza": "03:00"},
        {"Canale": "Cividale Nord vecchia rid.", "Ore": 50.0, "Data_Partenza": "07/05/2026", "Ora_Partenza": "09:00"},
        {"Canale": "Cividale Nord vecchia", "Ore": 81.0, "Data_Partenza": "14/04/2026", "Ora_Partenza": "11:00"},
        {"Canale": "Cividale Nord vecchia Rid Pvot", "Ore": 50.0, "Data_Partenza": "21/04/2026", "Ora_Partenza": "00:00"},
        {"Canale": "Cò de Vanni 1°", "Ore": 58.0, "Data_Partenza": "23/04/2026", "Ora_Partenza": "02:00"},
        {"Canale": "Cò de Vanni 2°", "Ore": 180.0, "Data_Partenza": "25/04/2026", "Ora_Partenza": "12:00"},
        {"Canale": "Cò de Vanni 2° Rid.", "Ore": 35.0, "Data_Partenza": "03/05/2026", "Ora_Partenza": "00:00"},
        {"Canale": "1° Gruppo bocchette", "Ore": 80.0, "Data_Partenza": "04/05/2026", "Ora_Partenza": "11:00"},
        {"Canale": "Spineda", "Ore": 30.0, "Data_Partenza": "07/05/2026", "Ora_Partenza": "19:00"},
        {"Canale": "Spineda Rid.", "Ore": 80.0, "Data_Partenza": "14/04/2026", "Ora_Partenza": "01:00"},
        {"Canale": "Fornace Rid.", "Ore": 10.0, "Data_Partenza": "17/04/2026", "Ora_Partenza": "09:00"},
        {"Canale": "S.Fiore 1°", "Ore": 10.0, "Data_Partenza": "17/04/2026", "Ora_Partenza": "19:00"},
        {"Canale": "S.Fiore 1° Rid.", "Ore": 165.0, "Data_Partenza": "18/04/2026", "Ora_Partenza": "05:00"},
        {"Canale": "S.Fiore 2°.", "Ore": 30.0, "Data_Partenza": "25/04/2026", "Ora_Partenza": "02:00"},
        {"Canale": "S.Fiore 2° Rid.", "Ore": 80.0, "Data_Partenza": "26/04/2026", "Ora_Partenza": "08:00"},
        {"Canale": "Cà de Bottoli rid.", "Ore": 40.0, "Data_Partenza": "29/04/2026", "Ora_Partenza": "16:00"},
        {"Canale": "Sec.Pomara Rid.", "Ore": 150.0, "Data_Partenza": "01/05/2026", "Ora_Partenza": "08:00"},
        {"Canale": "Pomara Rid.", "Ore": 35.0, "Data_Partenza": "07/05/2026", "Ora_Partenza": "14:00"},
        {"Canale": "Orti Rid.", "Ore": 90.0, "Data_Partenza": "14/04/2026", "Ora_Partenza": "01:00"},
        {"Canale": "S.Pietro", "Ore": 67.0, "Data_Partenza": "17/04/2026", "Ora_Partenza": "19:00"},
        {"Canale": "S.Pietro Rid.", "Ore": 90.0, "Data_Partenza": "20/04/2026", "Ora_Partenza": "14:00"},
        {"Canale": "Ossola 1° Rid.", "Ore": 50.0, "Data_Partenza": "24/04/2026", "Ora_Partenza": "08:00"},
        {"Canale": "Ossola 2° Rid.", "Ore": 40.0, "Data_Partenza": "26/04/2026", "Ora_Partenza": "10:00"},
        {"Canale": "Agraria Rid.", "Ore": 60.0, "Data_Partenza": "28/04/2026", "Ora_Partenza": "02:00"},
        {"Canale": "Manzoglio Rid.", "Ore": 80.0, "Data_Partenza": "30/04/2026", "Ora_Partenza": "14:00"},
        {"Canale": "Fiascale Rid.", "Ore": 120.0, "Data_Partenza": "03/05/2026", "Ora_Partenza": "22:00"},
        {"Canale": "Tessagli Rid.", "Ore": 90.0, "Data_Partenza": "13/04/2026", "Ora_Partenza": "22:00"},
        {"Canale": "Roncole Rid.", "Ore": 110.0, "Data_Partenza": "17/04/2026", "Ora_Partenza": "16:00"},
        {"Canale": "Vaja Rid.", "Ore": 80.0, "Data_Partenza": "22/04/2026", "Ora_Partenza": "06:00"},
        {"Canale": "Riglio Rid.", "Ore": 140.0, "Data_Partenza": "25/04/2026", "Ora_Partenza": "14:00"},
        {"Canale": "Breda 3°", "Ore": 37.0, "Data_Partenza": "01/05/2026", "Ora_Partenza": "10:00"},
        {"Canale": "Breda 4°", "Ore": 19.0, "Data_Partenza": "02/05/2026", "Ora_Partenza": "23:00"},
        {"Canale": "Delmoncello 1° ridotta", "Ore": 70.0, "Data_Partenza": "03/05/2026", "Ora_Partenza": "18:00"},
        {"Canale": "Delmoncello 2°", "Ore": 10.0, "Data_Partenza": "06/05/2026", "Ora_Partenza": "16:00"},
        {"Canale": "Casalmerlino ridotta", "Ore": 20.0, "Data_Partenza": "07/05/2026", "Ora_Partenza": "02:00"},
        {"Canale": "Bocchette Secondario Casalmerlino", "Ore": 14.0, "Data_Partenza": "07/05/2026", "Ora_Partenza": "22:00"},
        {"Canale": "Bocchette Secondario Casalmerlino rid", "Ore": 30.0, "Data_Partenza": "13/04/2026", "Ora_Partenza": "12:00"},
        {"Canale": "Bonfanti", "Ore": 300.0, "Data_Partenza": "14/04/2026", "Ora_Partenza": "18:00"},
        {"Canale": "Levata", "Ore": 300.0, "Data_Partenza": "27/04/2026", "Ora_Partenza": "06:00"},
    ])

if 'df_canali' not in st.session_state:
    st.session_state.df_canali = get_initial_data()
if 'data_selezionata' not in st.session_state:
    st.session_state.data_selezionata = datetime.now().date()

with st.expander("⚙️ Impostazioni Stagione", expanded=False):
    d_inizio = st.date_input("Inizio Stagione:", datetime(2026, 4, 1).date(), format="DD/MM/YYYY")
    t_inizio = st.time_input("Ora Inizio:", datetime(2026, 4, 1, 8, 0).time())
    d_fine = st.date_input("Fine Stagione:", datetime(2026, 9, 22).date(), format="DD/MM/YYYY")
    ciclo_giorni = st.number_input("Ogni quanti giorni riparte il ciclo?", min_value=1, value=14)
    if st.button("♻️ Reset Tabella Partenze"):
        st.session_state.df_canali = get_initial_data()
        st.rerun()

end_stagione = datetime.combine(d_fine, datetime.max.time())

with st.expander("📝 Modifica Partenze e Durate", expanded=False):
    edited_df = st.data_editor(
        st.session_state.df_canali,
        num_rows="dynamic", use_container_width=True, hide_index=True,
        column_config={
            "Canale": st.column_config.TextColumn("Canale", required=True),
            "Ore": st.column_config.NumberColumn("Ore", required=True),
            "Data_Partenza": st.column_config.TextColumn("Data Prima Partenza", help="GG/MM/AAAA", required=True),
            "Ora_Partenza": st.column_config.TextColumn("Ora Prima Partenza", help="HH:MM", required=True),
        }
    )
    st.session_state.df_canali = edited_df

@st.cache_data
def calcola_turni_da_partenze(df_canali, fine_stagione, giorni_ciclo):
    turni = []
    df_valid = df_canali.dropna().copy()
    for _, row in df_valid.iterrows():
        try:
            start_dt = datetime.strptime(f"{row['Data_Partenza']} {row['Ora_Partenza']}", "%d/%m/%Y %H:%M")
            durata_ore = float(row['Ore'])
            if durata_ore <= 0: continue
            
            inizio_ciclo_canale = start_dt
            while inizio_ciclo_canale < fine_stagione:
                fine_turno = inizio_ciclo_canale + timedelta(hours=durata_ore)
                turni.append({"Canale": row['Canale'], "Inizio": inizio_ciclo_canale, "Fine": fine_turno})
                inizio_ciclo_canale += timedelta(days=giorni_ciclo)
        except:
            continue
    return pd.DataFrame(turni)

df_risultato = calcola_turni_da_partenze(st.session_state.df_canali, end_stagione, ciclo_giorni)

st.markdown("---")
if not df_risultato.empty:
    st.subheader("📅 Programma del Giorno")

    col_ieri, col_oggi, col_domani = st.columns(3)
    with col_ieri:
        if st.button("⬅️ IERI", use_container_width=True):
            st.session_state.data_selezionata -= timedelta(days=1)
            st.rerun()
    with col_oggi:
        if st.button("📅 OGGI", use_container_width=True):
            st.session_state.data_selezionata = datetime.now().date()
            st.rerun()
    with col_domani:
        if st.button("DOMANI ➡️", use_container_width=True):
            st.session_state.data_selezionata += timedelta(days=1)
            st.rerun()

    giorno_selezionato = st.date_input("Data:", value=st.session_state.data_selezionata, format="DD/MM/YYYY", label_visibility="collapsed")
    if giorno_selezionato != st.session_state.data_selezionata:
        st.session_state.data_selezionata = giorno_selezionato
        st.rerun()

    inizio_giorno = datetime.combine(st.session_state.data_selezionata, datetime.min.time())
    fine_giorno = inizio_giorno + timedelta(days=1)

    turni_del_giorno = df_risultato[
        (df_risultato['Inizio'] < fine_giorno) & (df_risultato['Fine'] > inizio_giorno)
    ].sort_values(by='Inizio')

    if turni_del_giorno.empty:
        st.success(f"✅ Nessun canale in funzione il {st.session_state.data_selezionata.strftime('%d/%m/%Y')}.")
    else:
        for _, turno in turni_del_giorno.iterrows():
            ora_in = formatta_data_it(turno['Inizio'])
            ora_fi = formatta_data_it(turno['Fine'])
            
            p_verde = '<span style="display:inline-block; width:14px; height:14px; background-color:#00FF00; border-radius:50%; border:2px solid #005000; margin-right:8px; vertical-align:middle; box-shadow: 0px 0px 4px #00FF00;"></span>'
            p_rosso = '<span style="display:inline-block; width:14px; height:14px; background-color:#FF0000; border-radius:50%; border:2px solid #500000; margin-right:8px; vertical-align:middle; box-shadow: 0px 0px 4px #FF0000;"></span>'
            
            st.markdown(f"""
            <div style="border-left: 8px solid #1f77b4; background-color: #f0f2f6; padding: 12px; margin-bottom: 8px; border-radius: 5px;">
                <h3 style="margin: 0 0 10px 0; color: #111; font-weight: bold; font-size: 1.25em;">{turno['Canale']}</h3>
                <p style="font-size: 1.1em; margin: 0 0 6px 0; display: flex; align-items: center;">
                    {p_verde} <span><b>Apertura:</b> {ora_in}</span>
                </p>
                <p style="font-size: 1.1em; margin: 0; display: flex; align-items: center;">
                    {p_rosso} <span><b>Chiusura:</b> {ora_fi}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

    with st.expander("📥 Scarica Tabellone Stagionale (CSV)"):
        st.dataframe(df_risultato.style.format({"Inizio": "{:%d/%m/%Y %H:%M}", "Fine": "{:%d/%m/%Y %H:%M}"}), hide_index=True)
        csv = df_risultato.to_csv(index=False, date_format='%d/%m/%Y %H:%M').encode('utf-8')
        st.download_button("Scarica CSV", data=csv, file_name="orari_stagione.csv", mime="text/csv")
else:
    st.warning("Nessun dato da calcolare. Controlla la tabella delle partenze.")
