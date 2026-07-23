import pandas as pd

def hitung_bollinger_squeeze(df, periode=20, std_dev=2):
    """
    Calculates Bollinger Bands squeeze to detect consolidation/sideways phases.
    """
    if len(df) < periode:
        return None
        
    df['MA20'] = df['Close'].rolling(window=periode).mean()
    df['STD20'] = df['Close'].rolling(window=periode).std()
    
    df['Upper'] = df['MA20'] + (std_dev * df['STD20'])
    df['Lower'] = df['MA20'] - (std_dev * df['STD20'])
    
    df['Bandwidth'] = (df['Upper'] - df['Lower']) / df['MA20']
    return df
