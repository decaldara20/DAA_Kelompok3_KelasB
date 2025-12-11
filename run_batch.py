import os
import json
import time
import pandas as pd
import tracemalloc
from pathlib import Path
# Pastikan run.py ada di folder yang sama dan memiliki fungsi ini
from run import algo_A_Heap, algo_B_Array

# Konfigurasi Folder
DATA_DIR = Path('data')
RESULTS_DIR = Path('results')
RESULTS_DIR.mkdir(exist_ok=True)

def run_experiments():
    print("=== MEMULAI EKSPERIMEN BATCH (DEBUG MODE) ===")
    
    # Cek apakah folder data ada isinya
    instance_files = sorted(list(DATA_DIR.glob('*.json')))
    if not instance_files:
        print(f"[ERROR] Tidak ada file .json di folder {DATA_DIR.absolute()}")
        print("Solusi: Jalankan 'generate_instances.py' terlebih dahulu.")
        return

    results = []
    
    print("-" * 100)
    print(f"{'Instance':<20} | {'Algo':<5} | {'Time (ms)':<10} | {'Mem (MB)':<10} | {'Result':<10}")
    print("-" * 100)

    for json_file in instance_files:
        try:
            with open(json_file, 'r') as f:
                inst = json.load(f)
            
            n_nodes = inst['meta']['total_nodes']
            name = json_file.name
            
            # --- Algo A (HEAP) ---
            tracemalloc.start()
            t0 = time.perf_counter()
            res_A = algo_A_Heap(inst)
            t1 = time.perf_counter()
            _, peak_A = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            time_A = (t1 - t0) * 1000.0
            mem_A = peak_A / (1024 * 1024)
            
            results.append({
                'instance': name, 'n_nodes': n_nodes, 'algo': 'Heap',
                'time_ms': time_A, 'memory_mb': mem_A, 'result': res_A
            })
            print(f"{name:<20} | {'Heap':<5} | {time_A:8.4f} ms | {mem_A:8.4f} MB | {res_A:<10.2f}")

            # --- Algo B (ARRAY) ---
            tracemalloc.start()
            t0 = time.perf_counter()
            res_B = algo_B_Array(inst)
            t1 = time.perf_counter()
            _, peak_B = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            time_B = (t1 - t0) * 1000.0
            mem_B = peak_B / (1024 * 1024)
            
            results.append({
                'instance': name, 'n_nodes': n_nodes, 'algo': 'Array',
                'time_ms': time_B, 'memory_mb': mem_B, 'result': res_B
            })
            print(f"{name:<20} | {'Arr':<5} | {time_B:8.4f} ms | {mem_B:8.4f} MB | {res_B:<10.2f}")
            
        except Exception as e:
            print(f"[ERROR] Gagal memproses {json_file.name}: {e}")

    # --- PENYIMPANAN DATA (CRITICAL) ---
    if not results:
        print("\n[FATAL] Tidak ada hasil yang didapatkan. Cek apakah generate_instances.py sudah dijalankan dengan benar.")
        return

    df = pd.DataFrame(results)
    output_csv = RESULTS_DIR / 'experiment_results.csv'
    
    try:
        df.to_csv(output_csv, index=False)
        print("-" * 100)
        print(f"[SUKSES] Data tersimpan di: {output_csv.absolute()}")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan CSV: {e}")
        return

    # --- RINGKASAN OUTPUT ---
    print("\n=== RINGKASAN EKSPERIMEN ===")
    try:
        avg_heap = df[df['algo'] == 'Heap']['time_ms'].mean()
        avg_arr = df[df['algo'] == 'Array']['time_ms'].mean()
        
        print(f"Rata-rata Waktu Heap : {avg_heap:.4f} ms")
        print(f"Rata-rata Waktu Array: {avg_arr:.4f} ms")
        
        if avg_heap > 0:
            speedup = avg_arr / avg_heap
            print(f"Speedup: Heap {speedup:.2f}x lebih cepat dari Array")
        else:
            print("Speedup: Infinite (Heap instan)")
            
    except Exception as e:
        print(f"[ERROR] Gagal menghitung ringkasan: {e}")

if __name__ == "__main__":
    run_experiments()