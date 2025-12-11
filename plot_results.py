import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Konfigurasi Path
RESULTS_DIR = Path('results')
DATA_FILE = RESULTS_DIR / 'experiment_results.csv'

def generate_plots():
    print("=== MEMULAI PEMBUATAN GRAFIK ===")
    
    # 1. Cek File CSV
    if not DATA_FILE.exists():
        print(f"[ERROR] File {DATA_FILE} tidak ditemukan!")
        print("Solusi: Jalankan 'run_batch.py' terlebih dahulu.")
        return
    
    # 2. Baca Data
    try:
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            print("[ERROR] File CSV kosong.")
            return
        print(f"[INFO] Data berhasil dimuat: {len(df)} baris.")
    except Exception as e:
        print(f"[ERROR] Gagal membaca CSV: {e}")
        return

    # Atur tema grafik agar terlihat ilmiah (putih bersih dengan grid)
    sns.set_theme(style="whitegrid")

    # =========================================================
    # GAMBAR 1: PLOT TIME COMPARISON (plot_time_comparison.png)
    # =========================================================
    try:
        plt.figure(figsize=(12, 6))
        
        # Barplot membandingkan Waktu Heap vs Array
        sns.barplot(data=df, x='instance', y='time_ms', hue='algo', palette='viridis')
        
        # PENTING: Gunakan Skala Logaritmik (Log Scale)
        # Karena Array (200ms) jauh lebih besar dari Heap (5ms). 
        # Tanpa log, bar Heap akan terlihat seperti hilang/nol.
        plt.yscale('log') 
        
        plt.title('Perbandingan Waktu Eksekusi: Heap vs Array (Skala Log)', fontsize=14, fontweight='bold')
        plt.ylabel('Waktu (ms) - Log Scale', fontsize=12)
        plt.xlabel('Instance (Kasus Uji)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title="Algoritma")
        plt.tight_layout()
        
        out_time = RESULTS_DIR / 'plot_time_comparison.png'
        plt.savefig(out_time, dpi=300)
        print(f"[SUKSES] Grafik Waktu disimpan di: {out_time.name}")
        plt.close() # Tutup agar memori hemat
        
    except Exception as e:
        print(f"[ERROR] Gagal membuat plot waktu: {e}")

    # =========================================================
    # GAMBAR 2: PLOT SPEEDUP (plot_speedup.png)
    # =========================================================
    try:
        # Pivot data untuk membandingkan side-by-side
        pivot_df = df.pivot(index='instance', columns='algo', values='time_ms')
        
        # Hitung Speedup = Waktu Array / Waktu Heap
        if 'Array' in pivot_df.columns and 'Heap' in pivot_df.columns:
            pivot_df['speedup'] = pivot_df['Array'] / pivot_df['Heap']
            
            plt.figure(figsize=(12, 6))
            
            # Gambar garis tren speedup
            sns.lineplot(data=pivot_df, x=pivot_df.index, y='speedup', marker='o', color='red', linewidth=3, label='Speedup Factor')
            
            # Tambahkan garis rata-rata (Benchmark)
            avg_speedup = pivot_df['speedup'].mean()
            plt.axhline(avg_speedup, color='blue', linestyle='--', label=f'Rata-rata: {avg_speedup:.1f}x')
            
            plt.title('Speedup Factor (Seberapa cepat Heap dibanding Array?)', fontsize=14, fontweight='bold')
            plt.ylabel('Kali Lipat (x)', fontsize=12)
            plt.xlabel('Instance', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            
            out_speed = RESULTS_DIR / 'plot_speedup.png'
            plt.savefig(out_speed, dpi=300)
            print(f"[SUKSES] Grafik Speedup disimpan di: {out_speed.name}")
            plt.close()
        else:
            print("[WARN] Data tidak lengkap untuk menghitung speedup.")
            
    except Exception as e:
        print(f"[ERROR] Gagal membuat plot speedup: {e}")

    # =========================================================
    # GAMBAR 3: PLOT MEMORY (plot_memory.png) - BONUS
    # =========================================================
    try:
        if 'memory_mb' in df.columns:
            plt.figure(figsize=(12, 6))
            sns.barplot(data=df, x='instance', y='memory_mb', hue='algo', palette='rocket')
            
            plt.title('Perbandingan Penggunaan Memori (Peak RAM)', fontsize=14, fontweight='bold')
            plt.ylabel('Memori (MB)', fontsize=12)
            plt.xlabel('Instance', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.legend(title="Algoritma")
            
            # Zoom-in: Potong bagian bawah grafik agar perbedaan kecil terlihat
            # Hanya jika memori tidak 0
            if df['memory_mb'].max() > 0:
                min_y = df['memory_mb'].min() * 0.95
                plt.ylim(bottom=min_y)
            
            plt.tight_layout()
            out_mem = RESULTS_DIR / 'plot_memory.png'
            plt.savefig(out_mem, dpi=300)
            print(f"[SUKSES] Grafik Memori disimpan di: {out_mem.name}")
            plt.close()
    except Exception as e:
        print(f"[ERROR] Gagal membuat plot memori: {e}")

if __name__ == "__main__":
    generate_plots()