import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def get_artist_stats(df):
    stats = df.groupby('Artists')['Popularity'].agg(['count', 'mean']).reset_index()
    stats.columns = ['Artists', 'Song Count', 'Avg Popularity']
    return stats.sort_values(by=['Avg Popularity', 'Song Count'], ascending=[False, False])

def plot_audio_features_radar(df, artists):
    features = ['danceability', 'energy', 'valence', 'acousticness', 'liveness']
    summary = df[df['Artists'].isin(artists)].groupby('Artists')[features].mean()

    labels = features
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    for artist in summary.index:
        values = summary.loc[artist].tolist()
        values += values[:1]
        ax.plot(angles, values, label=artist)
        ax.fill(angles, values, alpha=0.1)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title('Audio Feature Comparison')
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    return fig

def plot_theme_popularity(df):
    genre_cols = df.columns[20:]
    genre_popularity = {}
    for genre in genre_cols:
        popular_songs = df[df[genre].notnull() & (df['Popularity'] > 0)]
        if not popular_songs.empty:
            genre_popularity[genre] = popular_songs['Popularity'].mean()
    genre_df = pd.Series(genre_popularity).sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=genre_df.index, y=genre_df.values, ax=ax, palette='Greens_d')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_ylabel("Avg Popularity")
    ax.set_title("Average Popularity by Theme/Genre")
    return fig

def plot_artist_feature_heatmap(df):
    top_artists = df['Artists'].value_counts().head(15).index
    features = ['danceability', 'energy', 'valence', 'acousticness', 'liveness']
    subset = df[df['Artists'].isin(top_artists)]
    heatmap_data = subset.groupby('Artists')[features].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt=".2f", ax=ax)
    ax.set_title("Audio Feature Heatmap for Top Artists")
    return fig
