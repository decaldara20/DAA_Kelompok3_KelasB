import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
RESULTS_DIR = Path('results')
DATA_FILE = RESULTS_DIR / 'experiment_results.csv'

def generate_advanced_plots():
    print("=== MEMBUAT VISUALISASI LANJUTAN (BOXPLOT & SCATTER) ===")
    
    if not DATA_FILE.exists():
        print(f"[ERROR] {DATA_FILE} tidak ditemukan. Jalankan run_batch.py dulu.")
        return
        
    df = pd.read_csv(DATA_FILE)
    sns.set_theme(style="whitegrid")

    # =========================================================
    # 1. BOXPLOT (Distribusi Waktu Eksekusi)
    # =========================================================
    plt.figure(figsize=(10, 6))
    
    # Boxplot untuk melihat sebaran data (Min, Max, Median, Outlier)
    sns.boxplot(data=df, x='algo', y='time_ms', palette='viridis', showfliers=True)
    
    # Gunakan Log Scale karena perbedaan Array vs Heap terlalu ekstrem
    plt.yscale('log')
    
    plt.title('Distribusi Waktu Eksekusi (Log Scale)', fontsize=14, fontweight='bold')
    plt.ylabel('Waktu (ms) - Logaritmik', fontsize=12)
    plt.xlabel('Algoritma', fontsize=12)
    
    # Simpan
    out_box = RESULTS_DIR / 'plot_boxplot_distribution.png'
    plt.tight_layout()
    plt.savefig(out_box, dpi=300)
    print(f"[SUKSES] Boxplot disimpan di: {out_box.name}")

    # =========================================================
    # 2. SCATTER PLOT (Korelasi: Visited Nodes vs Time)
    # =========================================================
    plt.figure(figsize=(12, 7))
    
    # Scatter plot: Titik-titik data
    sns.scatterplot(data=df, x='visited', y='time_ms', hue='algo', style='algo', s=100, palette='deep')
    
    # Tambahkan garis regresi (tren) tipis untuk memperjelas arah
    # (Opsional: Matikan ci=None jika ingin melihat area confidence)
    sns.regplot(data=df[df['algo']=='Array'], x='visited', y='time_ms', scatter=False, color='orange', label='Tren Array (Linear/Quad)', ci=None)
    sns.regplot(data=df[df['algo']=='Heap'], x='visited', y='time_ms', scatter=False, color='blue', label='Tren Heap (Log/Flat)', ci=None)

    plt.title('Scatter Plot: Hubungan Beban Kerja (Visited) vs Waktu', fontsize=14, fontweight='bold')
    plt.xlabel('Jumlah Node yang Dikunjungi (Visited)', fontsize=12)
    plt.ylabel('Waktu Eksekusi (ms)', fontsize=12)
    plt.legend()
    
    # Simpan
    out_scatter = RESULTS_DIR / 'plot_scatterplot_correlation.png'
    plt.tight_layout()
    plt.savefig(out_scatter, dpi=300)
    print(f"[SUKSES] Scatterplot disimpan di: {out_scatter.name}")

if __name__ == "__main__":
    generate_advanced_plots()