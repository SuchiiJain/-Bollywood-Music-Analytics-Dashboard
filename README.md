# Bollywood Music Analytics Dashboard 🎶

A Spotify-style Streamlit dashboard to explore and analyze Bollywood music using Spotify audio features. Built to help users discover trends in artist popularity, song mood, energy levels, and genre patterns.

## 🔍 Features
- 🎧 Artist popularity explorer
- 📈 Audio feature radar (energy, mood, danceability)
- 🎼 Theme/genre trend analysis (Romantic, Sufi, Retro, etc.)
- 🔥 Heatmap comparing top artists on key audio metrics
- 🔎 Filterable song explorer by artist, popularity, and energy

## 🛠️ Tech Stack
- **Frontend/UI:** Streamlit
- **Backend/Data:** Python, Pandas
- **Visualizations:** Matplotlib, Seaborn

## 📁 Project Structure
```
project/
├── app.py                      # Main Streamlit app
├── data/
│   └── bollywood_combined_music_data.csv
├── utils/
│   ├── load_data.py           # Data loading and preprocessing
│   └── analytics.py           # Chart and stats logic
```

## 🚀 Run Locally
1. Clone the repo
```bash
git clone [your-repo-link]
cd project
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Launch the app
```bash
streamlit run app.py
```

## 📊 Data Source
Spotify audio features + manually tagged Bollywood genre/theme labels

## 🌐 Live Demo
https://suchiijain-bollywood-music-analytics-dashboard-app-eehocg.streamlit.app/

Made with ❤️ by Suchi — feel free to connect or give feedback!

## 📄 License
MIT License

## ▶️ How to Run

Make sure you have Python 3.7+ installed.

# 1. Clone the repository
git clone https://github.com/suchijain/bollywood-analytics-dashboard.git
cd bollywood-analytics-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
