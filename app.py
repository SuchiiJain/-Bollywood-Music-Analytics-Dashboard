import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.load_data import load_and_prepare_data
from utils.analytics import (
    get_artist_stats,
    plot_audio_features_radar,
    plot_theme_popularity,
    plot_artist_feature_heatmap
)

# Spotify-inspired color palette
spotify_green = "#1DB954"
white_text = "#FFFFFF"

st.set_page_config(page_title="Bollywood Music Analytics", layout="wide", page_icon="🎵")

# Page header with logo
st.markdown("""
    <div style='display: flex; align-items: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg' width='40' style='margin-right: 10px;'>
        <h1 style='color: #1DB954; margin: 0;'>Bollywood Music Analytics Dashboard</h1>
    </div>
    <p style='color: #ccc;'>Explore insights into Bollywood songs using Spotify data — popularity trends, artist comparisons, and audio features.</p>
""", unsafe_allow_html=True)

# Load data
df, exploded_df = load_and_prepare_data("data/bollywood_combined_music_data.csv")

# Tab layout
tabs = st.tabs([
    "🎧 Artist Popularity",
    "📈 Audio Features",
    "🎼 Theme Trends",
    "🔥 Heatmap",
    "🔍 Song Explorer"
])

# 🎧 Artist Popularity
with tabs[0]:
    st.header("🎧 Artist Popularity")
    artist_stats = get_artist_stats(exploded_df).reset_index(drop=True)
    st.dataframe(artist_stats, use_container_width=True)

# 📈 Audio Feature Radar
with tabs[1]:
    st.header("📈 Compare Artists by Audio Features")
    artist_options = exploded_df['Artists'].unique().tolist()
    selected = st.multiselect("Select artists:", artist_options, default=artist_options[:3], max_selections=5)
    if selected:
        fig = plot_audio_features_radar(exploded_df, selected)
        st.pyplot(fig)

# 🎼 Theme Trends
with tabs[2]:
    st.header("🎼 Theme and Genre Popularity")
    st.markdown("Themes are assigned based on song mood, lyrics, and vibe (e.g. Sufi, Romantic, Retro).")
    fig = plot_theme_popularity(df)
    st.pyplot(fig)

# 🔥 Heatmap
with tabs[3]:
    st.header("🔥 Artist Feature Heatmap")
    fig = plot_artist_feature_heatmap(exploded_df)
    st.pyplot(fig)

# 🔍 Song Explorer
with tabs[4]:
    st.header("🔍 Song Explorer")

    with st.expander("ℹ️ What do these features mean?"):
        st.markdown("""
        - **Intensity (Energy)**: How powerful and active the song sounds. High = loud, fast, strong beats.
        - **Dance Score (Danceability)**: How suitable the track is for dancing. High = steady rhythm and beat.
        - **Mood Score (Valence)**: The positivity or happiness of a track. High = cheerful; Low = sad or serious.
        - **Popularity**: Spotify's internal score (0–100) based on plays and recency.
        """)

    artist_filter = st.selectbox("Filter by Artist:", ["All"] + sorted(exploded_df['Artists'].unique()))
    popularity = st.slider("Popularity Range:", 0, 100, (50, 100))
    energy = st.slider("Intensity Range:", 0.0, 1.0, (0.4, 1.0))

    filtered = exploded_df.copy()
    if artist_filter != "All":
        filtered = filtered[filtered['Artists'] == artist_filter]
    filtered = filtered[
        (filtered['Popularity'] >= popularity[0]) &
        (filtered['Popularity'] <= popularity[1]) &
        (filtered['energy'] >= energy[0]) &
        (filtered['energy'] <= energy[1])
    ]

    renamed = filtered.rename(columns={
        'energy': 'Intensity',
        'danceability': 'Dance Score',
        'valence': 'Mood Score'
    })

    st.dataframe(
        renamed[['Name', 'Artists', 'Popularity', 'Intensity', 'Dance Score', 'Mood Score']],
        use_container_width=True
    )
