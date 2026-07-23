import pandas as pd

print("=== ABO Scanner Data Test ===")

df = pd.read_csv("saham_syariah.csv")

print("Jumlah baris:", len(df))

print("\nKolom:")
print(df.columns.tolist())

print("\n5 data pertama:")
print(df.head())

print("\n=== SELESAI ===")
