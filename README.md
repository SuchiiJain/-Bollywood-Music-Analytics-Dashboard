# 🎶 Bollywood Music Analytics Dashboard

An advanced interactive music analytics dashboard built using **Python** and **Streamlit**, focused on exploring **artist-wise popularity** and **audio features** of Bollywood songs on Spotify.

This project combines two Spotify datasets to provide deep insights into how Bollywood songs perform, what makes them popular, and how audio traits differ across artists and genres.

Link to Dashboard: https://suchiijain-bollywood-music-analytics-dashboard-app-eehocg.streamlit.app/

---

## 📌 Features

- 🎧 **Artist Popularity Explorer**  
  View average, max, and min popularity of every artist and song.

- 📊 **Audio Feature Radar**  
  Compare artists across danceability, energy, valence, and more.

- 🎼 **Theme/Genre-Based Popularity**  
  Discover what themes (e.g. Romantic Ballad, Sufi, Retro) drive high popularity.

- 🔥 **Feature Heatmap for Top Artists**  
  Analyze how top artists score across audio features.

- 🔍 **Filterable Song Explorer**  
  Easily search and explore songs based on artists and features.

---

## 🧠 Business Problem

**How does artist-wise song popularity vary based on audio characteristics and genre themes in Bollywood music?**

This dashboard helps:
- Record labels identify trends and high-performing artist traits
- Fans and analysts explore what makes a song successful
- Developers and data scientists showcase analytics skillsets

---

## 🗃️ Dataset Description

This project merges two datasets:
1. **Popular Hindi Songs** – Top 950 Spotify tracks with popularity scores and artists
2. **Spotify Audio Features** – 1445 Bollywood songs with:
   - Audio traits: `danceability`, `energy`, `valence`, `acousticness`, etc.
   - Genre/theme tags: `Sufi`, `Romantic Ballad`, `Wedding`, etc.
   - Metadata: `artist_name`, `spotify_link`, `duration`, `mode`, etc.

---

## ▶️ How to Run

Make sure you have Python 3.7+ installed.

# 1. Clone the repository
git clone https://github.com/suchijain/bollywood-analytics-dashboard.git
cd bollywood-analytics-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
