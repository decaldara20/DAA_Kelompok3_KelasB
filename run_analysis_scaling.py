import json
import time
import heapq
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path

# Setup
DATA_PATH = Path('data/solo_route_G01.json') # Kita pakai G01 sebagai sampel master
RESULTS_DIR = Path('results')
RESULTS_DIR.mkdir(exist_ok=True)

# --- MODIFIKASI ALGORITMA (Dengan Visited Counter) ---

def algo_A_Heap_Count(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited_count = 0  # Counter
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_dist > distances.get(curr_node, float('inf')):
            continue
        
        visited_count += 1  # Hitung saat node di-pop dari PQ (resmi dikunjungi)
        
        if curr_node == end:
            return curr_dist, visited_count
        
        for neighbor, weight in graph.get(curr_node, {}).items():
            new_dist = curr_dist + weight
            if neighbor not in distances: distances[neighbor] = float('inf')
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
                
    return distances.get(end, float('inf')), visited_count

def algo_B_Array_Count(graph, start, end):
    nodes = list(graph.keys())
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0
    unvisited = {node: float('inf') for node in nodes}
    unvisited[start] = 0
    visited_count = 0 # Counter
    
    while unvisited:
        # Linear Scan
        current_node = None
        min_val = float('inf')
        for node, dist in unvisited.items():
            if dist < min_val:
                min_val = dist
                current_node = node
        
        if current_node is None: break
        
        visited_count += 1 # Hitung saat node dipilih dari set unvisited
        
        if current_node == end:
            return distances[end], visited_count
            
        del unvisited[current_node]
        
        for neighbor, weight in graph.get(current_node, {}).items():
            if neighbor in unvisited:
                new_dist = distances[current_node] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    unvisited[neighbor] = new_dist
                    
    return distances.get(end, float('inf')), visited_count

# --- FUNGSI SUB-GRAPH GENERATOR ---
def get_subgraph(full_graph, n_limit):
    """Mengambil n node pertama dari graf untuk simulasi peta kecil"""
    nodes = list(full_graph.keys())[:n_limit]
    subgraph = {k: full_graph[k] for k in nodes}
    
    # Bersihkan edge yang mengarah ke node di luar limit
    clean_subgraph = {}
    for u, neighbors in subgraph.items():
        clean_neighbors = {v: w for v, w in neighbors.items() if v in subgraph}
        clean_subgraph[u] = clean_neighbors
        
    return clean_subgraph, nodes[0], nodes[-1] # Ambil start/end dari subset

# --- MAIN EXPERIMENT ---
def run_scaling_test():
    print("=== MEMULAI ANALISIS SKALABILITAS (SCALING TEST) ===")
    
    # Load Master Data
    if not DATA_PATH.exists():
        print("ERROR: Jalankan generate_instances.py dulu!")
        return
        
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    full_graph = data['graph']
    total_nodes = len(full_graph)
    
    # Skenario Ukuran N
    node_steps = [50, 100, 200, 400, 800, 1500, 2500, 3796]
    results = []
    
    print(f"Menguji performa pada ukuran graf: {node_steps}")
    print("-" * 80)
    print(f"{'N Nodes':<10} | {'Algo':<6} | {'Time (ms)':<10} | {'Visited':<10}")
    print("-" * 80)
    
    for n in node_steps:
        # Buat Sub-graf
        subgraph, start, end = get_subgraph(full_graph, n)
        
        # 1. Test HEAP
        t0 = time.perf_counter()
        _, vis_A = algo_A_Heap_Count(subgraph, start, end)
        t_A = (time.perf_counter() - t0) * 1000
        
        results.append({'N': n, 'Algo': 'Heap', 'Time': t_A, 'Visited': vis_A})
        print(f"{n:<10} | {'Heap':<6} | {t_A:8.4f} ms | {vis_A:<10}")
        
        # 2. Test ARRAY
        t0 = time.perf_counter()
        _, vis_B = algo_B_Array_Count(subgraph, start, end)
        t_B = (time.perf_counter() - t0) * 1000
        
        results.append({'N': n, 'Algo': 'Array', 'Time': t_B, 'Visited': vis_B})
        print(f"{n:<10} | {'Arr':<6} | {t_B:8.4f} ms | {vis_B:<10}")

    # --- PLOTTING ---
    df = pd.DataFrame(results)
    sns.set_theme(style="whitegrid")
    
    # Plot 1: Time vs N (Menjawab: "Kapan mulai beda?")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='N', y='Time', hue='Algo', style='Algo', markers=True, linewidth=2.5)
    plt.title('Analisis Skalabilitas: Kapan Array Mulai Tertinggal?', fontsize=14, fontweight='bold')
    plt.ylabel('Waktu Eksekusi (ms)', fontsize=12)
    plt.xlabel('Jumlah Node dalam Graf (N)', fontsize=12)
    
    # Anotasi titik divergence (misal di N=400 atau 800)
    # Kita cari titik di mana Array 2x lebih lambat dari Heap
    for n in node_steps:
        t_heap = df[(df['N']==n) & (df['Algo']=='Heap')]['Time'].values[0]
        t_arr = df[(df['N']==n) & (df['Algo']=='Array')]['Time'].values[0]
        if t_arr > 2 * t_heap and t_arr > 1.0: # Threshold 1ms biar ga noise
            plt.annotate(f'Mulai Divergen (N={n})', 
                         xy=(n, t_arr), xytext=(n, t_arr + 50),
                         arrowprops=dict(facecolor='black', shrink=0.05))
            break
            
    plt.savefig(RESULTS_DIR / 'plot_scaling_analysis.png', dpi=300)
    print(f"\n[SUKSES] Grafik Scaling disimpan di results/plot_scaling_analysis.png")
    
    # Plot 2: Visited Nodes (Menjawab pertanyaan user tentang jumlah node)
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x='N', y='Visited', hue='Algo', palette='muted')
    plt.title('Validasi: Jumlah Node yang Dikunjungi (Selalu Sama)', fontsize=14)
    plt.ylabel('Count', fontsize=12)
    plt.xlabel('Jumlah Node (N)', fontsize=12)
    plt.savefig(RESULTS_DIR / 'plot_visited_check.png', dpi=300)
    print(f"[SUKSES] Grafik Visited Count disimpan di results/plot_visited_check.png")

if __name__ == "__main__":
    run_scaling_test()