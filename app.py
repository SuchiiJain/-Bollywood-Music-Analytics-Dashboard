import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.load_data import load_and_prepare_data
from utils.analytics import (
    get_artist_stats,
    plot_audio_features_radar,
    plot_theme_popularity,
    plot_artist_feature_heatmap
)
import os
import json

# Load saved blends if available
blend_path = "data/saved_blends.json"
if "user_blends" not in st.session_state:
    if os.path.exists(blend_path):
        with open(blend_path, "r") as f:
            st.session_state.user_blends = json.load(f)
    else:
        st.session_state.user_blends = {}

if "user_blends" not in st.session_state:
    st.session_state.user_blends = {}

# Spotify-inspired color palette
spotify_green = "#1DB954"
white_text = "#FFFFFF"

st.set_page_config(page_title="Bollywood Music Analytics", layout="wide", page_icon="🎵")

# Header
st.markdown("""
    <div style='display: flex; align-items: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg' width='40' style='margin-right: 10px;'>
        <h1 style='color: #1DB954; margin: 0;'>Bollywood Music Analytics Dashboard</h1>
    </div>
    <p style='color: #ccc;'>Explore energy, mood, and popularity trends across 100+ Bollywood tracks.</p>
""", unsafe_allow_html=True)

# Load data
df, exploded_df = load_and_prepare_data("data/bollywood_combined_music_data.csv")

# Add synthetic release year
np.random.seed(42)
if 'release_year' not in df.columns:
    df['release_year'] = np.random.randint(2000, 2024, size=len(df))
    exploded_df['release_year'] = df['release_year']

# Tabs
tabs = st.tabs([
    "🎧 Artist Popularity",
    "📈 Feature Radar",
    "📊 Mood Over Time",
    "🎼 Theme Highlights",
    "🔍 Song Explorer",
    "🎛️ Build Your Blend"
])

# 🎧 Artist Popularity
with tabs[0]:
    st.header("🎧 Artist Popularity")
    stats = get_artist_stats(exploded_df).reset_index(drop=True)
    st.dataframe(stats, use_container_width=True)

# 📈 Feature Radar
with tabs[1]:
    st.header("📈 Compare Audio Features")
    artists = exploded_df['Artists'].unique().tolist()
    selected = st.multiselect("Choose artists:", artists, default=artists[:2], max_selections=5)
    if selected:
        fig = plot_audio_features_radar(exploded_df, selected)
        st.pyplot(fig)

# 📊 Mood Over Time
with tabs[2]:
    st.header("📊 Mood & Energy Trends by Year")
    feature = st.selectbox("Select a feature to visualize over time:", ['energy', 'valence', 'danceability'])
    line_data = exploded_df.groupby('release_year')[feature].mean().reset_index()
    fig = px.line(line_data, x='release_year', y=feature, markers=True, title=f"Average {feature.title()} Over Time")
    st.plotly_chart(fig, use_container_width=True)

# 🎼 Theme Highlights
with tabs[3]:
    st.header("🎼 Explore Songs by Theme")
    themes = df.columns[20:]
    selected_theme = st.selectbox("Select a theme:", themes)
    filtered = df[df[selected_theme].notnull()].sort_values(by='Popularity', ascending=False).head(10)
    for _, row in filtered.iterrows():
        st.markdown(f"**🎵 {row['song_name']}** — Popularity: {row['Popularity']} | Energy: {row['energy']} | Mood: {row['valence']}")

# 🔍 Song Explorer
with tabs[4]:
    st.header("🔍 Song Explorer")
    with st.expander("ℹ️ Feature Glossary"):
        st.markdown("""
        - **Intensity (Energy)**: Loudness and activity level of a track.
        - **Dance Score**: Rhythmic suitability for dancing.
        - **Mood Score**: Positivity or happiness of the track.
        - **Popularity**: Spotify score from 0–100 based on play data.
        """)

    artist_filter = st.selectbox("Filter by Artist:", ["All"] + sorted(exploded_df['Artists'].unique()))
    pop_range = st.slider("Popularity:", 0, 100, (50, 100))
    energy_range = st.slider("Energy:", 0.0, 1.0, (0.4, 1.0))

    filtered = exploded_df.copy()
    if artist_filter != "All":
        filtered = filtered[filtered['Artists'] == artist_filter]
    filtered = filtered[
        (filtered['Popularity'] >= pop_range[0]) &
        (filtered['Popularity'] <= pop_range[1]) &
        (filtered['energy'] >= energy_range[0]) &
        (filtered['energy'] <= energy_range[1])
    ]

    display_df = filtered.rename(columns={
        'energy': 'Intensity',
        'danceability': 'Dance Score',
        'valence': 'Mood Score'
    })

    st.dataframe(display_df[['Name', 'Artists', 'release_year', 'Popularity', 'Intensity', 'Dance Score', 'Mood Score']], use_container_width=True)

# 🎛️ Build Your Own Blend
with tabs[5]:
    st.header("🎛️ Build Your Own Blend")
    song_list = exploded_df[['Name', 'Artists']].drop_duplicates().sort_values(by='Name')
    selected_songs = st.multiselect("Pick 2 or more songs to blend:", song_list['Name'].unique())

    if len(selected_songs) >= 2:
        blend_df = exploded_df[exploded_df['Name'].isin(selected_songs)]
        blend_features = blend_df[['danceability', 'energy', 'valence', 'acousticness', 'liveness']].mean().to_frame(name='Blend Avg').reset_index()
        fig = px.bar(blend_features, x='index', y='Blend Avg', title="Your Blend's Average Audio Profile", color='Blend Avg')
        st.plotly_chart(fig, use_container_width=True)

        # Save blend logic
        blend_name = st.text_input("Name your blend:")
        if st.button("💾 Save Blend") and blend_name:
            st.session_state.user_blends[blend_name] = {
                "songs": selected_songs,
                "features": blend_df[['danceability', 'energy', 'valence', 'acousticness', 'liveness']].mean().to_dict()
            }
            with open(blend_path, "w") as f:
                json.dump(st.session_state.user_blends, f)
            st.success(f"Blend '{blend_name}' saved!")
    else:
        st.info("Select at least 2 songs to create a blend.")

# --- NEW CODE BLOCK TO ADD TO app.py (after "Build Your Own Blend") ---

# 📊 Compare Blend vs Top Artist
with st.expander("📈 Compare Your Blend to a Top Artist"):
    top_artists = exploded_df['Artists'].value_counts().head(10).index.tolist()
    top_pick = st.selectbox("Pick a top artist to compare:", top_artists)

    if len(selected_songs) >= 2:
        artist_df = exploded_df[exploded_df['Artists'] == top_pick]
        artist_avg = artist_df[['danceability', 'energy', 'valence', 'acousticness', 'liveness']].mean().values.tolist()
        blend_avg = blend_df[['danceability', 'energy', 'valence', 'acousticness', 'liveness']].mean().values.tolist()

        categories = ['Danceability', 'Energy', 'Valence', 'Acousticness', 'Liveness']
        angles = categories + [categories[0]]
        blend_avg += [blend_avg[0]]
        artist_avg += [artist_avg[0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=blend_avg, theta=angles, fill='toself', name='Your Blend'))
        fig.add_trace(go.Scatterpolar(r=artist_avg, theta=angles, fill='toself', name=top_pick))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), showlegend=True, title="Blend vs Artist Audio Profile")
        st.plotly_chart(fig, use_container_width=True)

# 💡 Smart Mood-Based Recommendations
with st.expander("🎯 Mood-Based Recommendations"):
    vibe = st.selectbox("Choose a vibe:", ["High Energy", "Happy", "Danceable", "Chill"])

    if vibe == "High Energy":
        recs = exploded_df[exploded_df['energy'] > 0.85]
    elif vibe == "Happy":
        recs = exploded_df[exploded_df['valence'] > 0.75]
    elif vibe == "Danceable":
        recs = exploded_df[exploded_df['danceability'] > 0.8]
    else:
        recs = exploded_df[(exploded_df['energy'] < 0.4) & (exploded_df['valence'] < 0.5)]

    if recs.empty:
        st.warning("No exact matches found. Showing a few similar songs instead.")
        recs = exploded_df.sample(5)

    st.markdown(f"**Top tracks for: {vibe}**")
    st.dataframe(recs[['Name', 'Artists', 'Popularity', 'energy', 'valence', 'danceability']].sort_values(by='Popularity', ascending=False).head(10))

# Sidebar: View Saved Blends
with st.sidebar.expander("🎼 View Saved Blends"):
    blends = st.session_state.user_blends
    if blends:
        selected_blend = st.selectbox("Choose a blend:", list(blends.keys()))
        st.write("Songs:", blends[selected_blend]["songs"])
        st.bar_chart(pd.Series(blends[selected_blend]["features"]))

        # Load for comparison (sets session variables)
        if st.button("📊 Load Blend for Comparison"):
            selected_songs = blends[selected_blend]["songs"]
            st.rerun()
            
        # Edit blend name
        new_name = st.text_input("✏️ Rename blend:", value=selected_blend)
        if st.button("🔄 Rename") and new_name != selected_blend:
            st.session_state.user_blends[new_name] = st.session_state.user_blends.pop(selected_blend)
            with open(blend_path, "w") as f:
                json.dump(st.session_state.user_blends, f)
            st.success(f"Renamed to '{new_name}'")
            st.rerun()
    

        # Delete blend
        if st.button("🗑️ Delete Blend"):
            del st.session_state.user_blends[selected_blend]
            with open(blend_path, "w") as f:
                json.dump(st.session_state.user_blends, f)
            st.success("Blend deleted.")
            st.rerun()
    else:
        st.info("No blends saved yet.")