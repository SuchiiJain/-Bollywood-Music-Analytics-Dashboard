import pandas as pd

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)
    df['Artists'] = df['Artists'].str.split(', ')
    exploded_df = df.explode('Artists')
    return df, exploded_df
