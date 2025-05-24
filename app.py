import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets Setup #
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds_json = st.secrets["gcp_service_account"]
creds  = Credentials.from_service_account_info(creds_json).with_scopes(scopes)
client = gspread.authorize(creds)
sheet = client.open("mood_of_the_queue").sheet1

# Streamlit UI #
st.set_page_config(
    page_title="Mood of the Queue",
    page_icon="😊",
    layout="centered",
)
st.title("Mood of the Queue")
st.markdown("### ")
st.markdown("### How are you feeling today?")

# Load Data #
def load_data() -> pd.DataFrame:
    try:
        rows = sheet.get_all_records()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame({
            "Timestamp": pd.to_datetime([], utc=False),
            "Mood": pd.Series(dtype="string"),
            "Note": pd.Series(dtype="string"),
        })

    if not rows:
        return pd.DataFrame({
            "Timestamp": pd.to_datetime([], utc=False),
            "Mood": pd.Series(dtype="string"),
            "Note": pd.Series(dtype="string"),
        })

    df = pd.DataFrame(rows)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"])
    return df


def log_mood(mood: str, note: str = "") -> None:
    """Append a new mood entry"""
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    sheet.append_row([ts, mood, note], value_input_option="USER_ENTERED")

# Sidebar Filters #
st.sidebar.header("Filter entries by date")

df_all = load_data()
if df_all.empty:
    st.sidebar.info("No data to display yet")
    start_date = end_date = date.today()
else:
    min_date = df_all["Timestamp"].dt.date.min()
    max_date = df_all["Timestamp"].dt.date.max()
    start_date = st.sidebar.date_input(
        "Start date", min_value=min_date, value=min_date
    )
    end_date = st.sidebar.date_input(
        "End date", min_value=min_date, max_value=max_date, value=max_date
    )
    if start_date > end_date:
        st.sidebar.error("Start date must be on or before end date")
        st.stop()

# Log a Mood #
with st.form("log_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 3])
    choice = col1.selectbox(
        "Select Mood:",
        ["😊 Happy", "😠 Frustrated", "😕 Confused", "🎉 Excited"],
        index=0,
        label_visibility="visible"
    )
    note = col2.text_input("Note (Optional):")
    if st.form_submit_button("Log Mood"):
        log_mood(choice.split()[0], note)
        st.success("Mood logged! Please refresh to see it reflected below")

st.markdown("##")

# Display Data #
st.subheader("Mood Summary")
mask = (
    (df_all["Timestamp"].dt.date >= start_date) &
    (df_all["Timestamp"].dt.date <= end_date)
)
df = df_all.loc[mask].copy()

if df.empty:
    st.info("No entries in that date range.")
    st.stop()

## Summary Metrics ##
col1, col2, col3 = st.columns(3)
col1.metric("Total Logs", len(df))
common = df["Mood"].mode().iloc[0] if not df["Mood"].empty else "–"
col2.metric("Most Common Mood", common)
days_logged = df["Timestamp"].dt.date.nunique()
col3.metric("Days Logged", days_logged)

st.divider()

## Bar Chart: Mood Counts ##
counts = (
    df["Mood"]
      .value_counts()
      .rename_axis("Mood")
      .reset_index(name="Count")
)
fig_bar = px.bar(
    counts,
    x="Mood",
    y="Count",
    title=f"Mood Counts: {start_date.isoformat()} → {end_date.isoformat()}"
)
fig_bar.update_layout(yaxis_title="Entries", xaxis_title="", template="simple_white")
st.plotly_chart(fig_bar, use_container_width=True)

## Line Chart: Daily Trend ##
daily = (
    df.assign(Date=df["Timestamp"].dt.date)
      .groupby("Date")["Mood"]
      .count()
      .reset_index(name="Count")
)

fig_line = px.line(
    daily,
    x="Date",
    y="Count",
    markers=True,
    title="Daily Entry Trend"
)

fig_line.update_layout(yaxis_title="# logs", xaxis_title="Date", template="simple_white")
st.plotly_chart(fig_line, use_container_width=True)

### Raw Data Expander ###
with st.expander("See raw entries"):
    st.dataframe(df.sort_values("Timestamp", ascending=False), use_container_width=True)