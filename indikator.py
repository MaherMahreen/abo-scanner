import pandas as pd

def hitung_bollinger_squeeze(df, periode=20, std_dev=2):
    """
    Menghitung penyempitan Bollinger Bands untuk mendeteksi fase sideways.
    """
    if len(df) < periode:
        return None
        
    # Hitung Moving Average dan Standard Deviation
    df['MA20'] = df['Close'].rolling(window=periode).mean()
    df['STD20'] = df['Close'].rolling(window=periode).std()
    
    # Hitung Garis Atas dan Bawah Bollinger Bands
    df['Upper'] = df['MA20'] + (std_dev * df['STD20'])
    df['Lower'] = df['MA20'] - (std_dev * df['STD20'])
    
    # Bandwidth menentukan seberapa tipis/lebar volatilitas saham
    df['Bandwidth'] = (df['Upper'] - df['Lower']) / df['MA20']
    return df
