import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
RESULTS_DIR = Path('results')
DATA_FILE = RESULTS_DIR / 'experiment_results.csv'

def generate_scalability_plot():
    print("=== MEMBUAT PLOT SKALABILITAS (X=VISITED NODES) ===")
    
    # 1. Load Data
    if not DATA_FILE.exists():
        print(f"[ERROR] {DATA_FILE} tidak ditemukan. Jalankan run_batch.py dulu.")
        return
        
    df = pd.read_csv(DATA_FILE)
    
    # 2. Pre-processing Data
    # Kita urutkan berdasarkan 'visited' (jumlah node yang diproses)
    # Ini agar grafik garisnya nyambung dari kecil ke besar (misal 58 node -> 2800 node)
    df_sorted = df.sort_values(by='visited')
    
    # 3. Setup Plot
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 7))
    
    # Gambar Garis Waktu
    # Marker 'o' untuk melihat titik data G01-G15
    sns.lineplot(data=df_sorted, x='visited', y='time_ms', hue='algo', 
                 style='algo', markers=True, dashes=False, linewidth=2.5, markersize=8)
    
    # 4. Analisis Titik Divergensi (Kapan mulai beda jauh?)
    # Kita cari titik di mana Array mulai lebih lambat > 10ms dari Heap
    # Pivot dulu biar mudah dibandingkan
    pivot = df_sorted.pivot(index='visited', columns='algo', values='time_ms')
    pivot['diff'] = pivot['Array'] - pivot['Heap']
    
    # Cari titik pertama di mana bedanya signifikan (> 10ms)
    divergence_point = pivot[pivot['diff'] > 10].iloc[0] if not pivot[pivot['diff'] > 10].empty else None
    
    if divergence_point is not None:
        x_div = divergence_point.name # Nilai visited
        y_div = divergence_point['Array'] # Waktu Array
        
        plt.annotate(f'Mulai Meninggalkan Array\n(N={x_div}, Diff > 10ms)', 
                     xy=(x_div, y_div), xytext=(x_div, y_div + 100),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     fontsize=10, fontweight='bold', color='darkred')

    # 5. Kosmetik Grafik
    plt.title('Analisis Skalabilitas: Semakin Banyak Node, Semakin Jauh Bedanya', fontsize=14, fontweight='bold')
    plt.xlabel('Jumlah Node yang Dikunjungi (Workload)', fontsize=12)
    plt.ylabel('Waktu Eksekusi (ms)', fontsize=12)
    plt.legend(title='Algoritma', loc='upper left')
    
    # Tambahkan grid minor agar lebih detail
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    
    # Simpan
    output_path = RESULTS_DIR / 'plot_scalability_sorted.png'
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"[SUKSES] Grafik tersimpan di: {output_path}")

if __name__ == "__main__":
    generate_scalability_plot()