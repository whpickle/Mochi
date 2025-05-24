# Mochi Health Takehome

**Mood of the Queue** is a lightweight mood tracking dashboard built with [Streamlit](https://streamlit.io/). Users can quickly log their current mood, add optional notes, and view live mood trends powered by Google Sheets.

## Live Demo

**Launch the app:** [Streamlit Cloud](https://whpickett-mochi-health.streamlit.app)<br>
**View the backend Google Sheet:** [Google Sheet](https://docs.google.com/spreadsheets/d/1BLipzMLRnoP4GxHKRUcEwrxeLyAXWmfL6YF4G5de5x0/edit?usp=sharing)

## Features

- Log a mood using emojis (`😊`, `😠`, `😕`, `🎉`)
- Add optional notes (e.g., “lots of Rx delays today”)
- Filter by custom date range
- Mood visualizations:
  - Summary metrics: total logs, most common mood, days logged
  - Bar chart of mood counts
  - Daily entry trend line chart
- Google Sheet as a backend database
- Expandable view of raw logs

## Tech Stack

- [Streamlit](https://streamlit.io/) for the UI
- [Google Sheets API](https://developers.google.com/sheets/api) for backend data storage
- [Plotly](https://plotly.com/python/) for interactive charts

## Run Locally (Optional)

1. **Clone the repository**
    git clone https://github.com/whpickle/Mochi.git
    cd Mochi

2. **Install dependencies**
    pip install -r requirements.txt

3. **Add your secrets**
Create a `.streamlit/secrets.toml` file with your Google service account credentials

3. **Run the app**
    streamlit run app.py


## Future Considerations

If this were to be used beyond a take-home project, here are some potential next steps and improvements:

- **Authentication:** Add user login to track mood by user or role (e.g., support rep vs. team lead)
- **Weekly summaries:** Auto-generate mood reports or graphs emailed every Friday or end of week
- **Dashboard enhancements:** Tag moods by category (e.g., tech issue, delays, positive feedback)
- **Auto-refresh UX:** Smoother data updates with background refresh
- **Mobile optimization:** Improve layout responsiveness for easier mood logging from phones
- **Admin tools:** Editable mood entries, exports to CSV, chart download options
- **NLP enhancements:** Analyze mood notes to detect positive or negative sentiment, highlight concerning entries, and spot common themes