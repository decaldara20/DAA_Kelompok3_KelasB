import os
import json
import time
import pandas as pd
from pathlib import Path
# Import algoritma dari run.py yang sudah Anda buat
from run import algo_A_Heap, algo_B_Array, evaluate

# Konfigurasi Folder
DATA_DIR = Path('data')
RESULTS_DIR = Path('results')
RESULTS_DIR.mkdir(exist_ok=True)

def run_experiments():
    print("=== MEMULAI EKSPERIMEN BATCH ===")
    
    # Ambil semua file json di folder data
    instance_files = sorted(list(DATA_DIR.glob('*.json')))
    
    if not instance_files:
        print("Error: Tidak ada file .json di folder data/")
        return

    results = []
    
    print(f"Ditemukan {len(instance_files)} instance. Sedang memproses...")
    print("-" * 60)
    print(f"{'Instance':<20} | {'Nodes':<6} | {'Algo':<4} | {'Time (ms)':<10} | {'Result':<10}")
    print("-" * 60)

    for json_file in instance_files:
        # Load Data
        with open(json_file, 'r') as f:
            inst = json.load(f)
        
        n_nodes = inst['meta']['total_nodes']
        name = json_file.name
        
        # --- Run Algo A (HEAP) ---
        t0 = time.perf_counter()
        res_A = algo_A_Heap(inst)
        t1 = time.perf_counter()
        time_A = (t1 - t0) * 1000.0
        
        results.append({
            'instance': name,
            'n_nodes': n_nodes,
            'algo': 'Heap',
            'time_ms': time_A,
            'result': res_A
        })
        print(f"{name:<20} | {n_nodes:<6} | {'Heap':<4} | {time_A:8.4f} ms | {res_A:<10}")

        # --- Run Algo B (ARRAY) ---
        t0 = time.perf_counter()
        res_B = algo_B_Array(inst)
        t1 = time.perf_counter()
        time_B = (t1 - t0) * 1000.0
        
        results.append({
            'instance': name,
            'n_nodes': n_nodes,
            'algo': 'Array',
            'time_ms': time_B,
            'result': res_B
        })
        print(f"{name:<20} | {n_nodes:<6} | {'Arr':<4} | {time_B:8.4f} ms | {res_B:<10}")

    # Simpan ke CSV
    df = pd.DataFrame(results)
    output_csv = RESULTS_DIR / 'experiment_results.csv'
    df.to_csv(output_csv, index=False)
    
    print("-" * 60)
    print(f"[SUKSES] Hasil disimpan ke: {output_csv}")
    
    # Tampilkan Ringkasan Cepat
    avg_heap = df[df['algo'] == 'Heap']['time_ms'].mean()
    avg_arr = df[df['algo'] == 'Array']['time_ms'].mean()
    print(f"\nRata-rata Waktu Heap : {avg_heap:.4f} ms")
    print(f"Rata-rata Waktu Array: {avg_arr:.4f} ms")
    if avg_heap > 0:
        print(f"Speedup: Heap {avg_arr/avg_heap:.2f}x lebih cepat dari Array")

if __name__ == "__main__":
    run_experiments()