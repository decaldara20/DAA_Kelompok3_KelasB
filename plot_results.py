import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
RESULTS_DIR = Path('results')
DATA_FILE = RESULTS_DIR / 'experiment_results.csv'

def generate_plots():
    # 1. Load Data
    if not DATA_FILE.exists():
        print("File CSV tidak ditemukan! Jalankan run_batch.py dulu.")
        return
    
    df = pd.read_csv(DATA_FILE)
    
    # Set style
    sns.set_theme(style="whitegrid")
    
    # --- PLOT 1: Perbandingan Waktu Eksekusi (Bar Chart) ---
    plt.figure(figsize=(12, 6))
    
    # Kita pakai Log Scale karena bedanya terlalu jauh (5ms vs 260ms)
    # Agar bar Heap tidak terlihat "hilang"
    chart = sns.barplot(data=df, x='instance', y='time_ms', hue='algo', palette='viridis')
    
    plt.yscale('log') # PENTING: Skala Logaritmik
    plt.title('Perbandingan Waktu Eksekusi: Heap vs Array (Skala Log)', fontsize=14, fontweight='bold')
    plt.ylabel('Waktu (ms) - Log Scale', fontsize=12)
    plt.xlabel('Instance (Kasus Uji)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Algoritma')
    
    # Simpan
    output_path = RESULTS_DIR / 'plot_time_comparison.png'
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"[SUKSES] Grafik 1 disimpan di: {output_path}")
    
    # --- PLOT 2: Speedup Factor ---
    # Kita hitung berapa kali lipat Heap lebih cepat per instance
    pivot_df = df.pivot(index='instance', columns='algo', values='time_ms')
    pivot_df['speedup'] = pivot_df['Array'] / pivot_df['Heap']
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=pivot_df, x=pivot_df.index, y='speedup', marker='o', color='red', linewidth=2.5)
    
    plt.title('Speedup Factor (Berapa kali Heap lebih cepat?)', fontsize=14, fontweight='bold')
    plt.ylabel('Kali Lipat (x)', fontsize=12)
    plt.xlabel('Instance', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    
    # Garis rata-rata
    avg_speedup = pivot_df['speedup'].mean()
    plt.axhline(avg_speedup, color='blue', linestyle='--', label=f'Rata-rata: {avg_speedup:.1f}x')
    plt.legend()
    
    # Simpan
    output_path = RESULTS_DIR / 'plot_speedup.png'
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"[SUKSES] Grafik 2 disimpan di: {output_path}")

if __name__ == "__main__":
    generate_plots()