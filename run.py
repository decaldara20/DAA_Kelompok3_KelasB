import tracemalloc
import json
import argparse
import time
import heapq
import math  # [BARU] Import math untuk logaritma
from typing import Any
import sys

# --- FUNGSI ANALISIS TEORITIS (Fitur Presentasi) ---
def analyze_complexity(graph, algo_type):
    """
    Menghitung estimasi operasi teoritis untuk 'pamer' ke dosen.
    Ini membuktikan kita paham bedanya V^2 dan E log V.
    """
    V = len(graph)
    # Menghitung total Edges (E)
    E = sum(len(neighbors) for neighbors in graph.values())
    
    print(f"\n--- [STATISTIK GRAF & ANALISIS] ---")
    print(f"  Nodes (V) : {V}")
    print(f"  Edges (E) : {E}")
    
    if algo_type == 'A':
        print(f"  Algoritma : A (Dijkstra Min-Heap)")
        print(f"  Kompleksitas : O(E log V)")
        
        # Estimasi beban kerja Heap
        # log2(V) adalah biaya rata-rata push/pop heap
        if V > 0:
            est_ops = E * math.log2(V)
            print(f"  Est. Operasi : {E} * log2({V}) ≈ {int(est_ops):,} instruksi dasar")
        else:
            print("  Est. Operasi : 0")
            
    else:
        print(f"  Algoritma : B (Dijkstra Array/Linear)")
        print(f"  Kompleksitas : O(V^2)")
        
        # Estimasi beban kerja Array
        est_ops = V * V
        print(f"  Est. Operasi : {V}^2 = {int(est_ops):,} instruksi dasar")
        
    print(f"-----------------------------------\n")

# --- IMPLEMENTASI ALGORITMA A: DIJKSTRA HEAP (O(E log V)) ---
def algo_A_Heap(instance: Any):
    """Dijkstra menggunakan Priority Queue (Min-Heap)"""
    graph = instance['graph']
    start = str(instance['meta']['start_node']) 
    end = str(instance['meta']['end_node'])
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    visited_count = 0
    
    # Loop berjalan selama PQ tidak kosong
    while pq:
        # [STEP 1] Extract Min: O(log V) - Sangat Cepat
        curr_dist, curr_node = heapq.heappop(pq)
        
        # Lazy Deletion Check
        if curr_dist > distances.get(curr_node, float('inf')):
            continue

        visited_count += 1
        
        if curr_node == end:
            return curr_dist, visited_count
        
        neighbors = graph.get(curr_node, {})
        # Loop Tetangga: Total berjalan E kali sepanjang algoritma
        for neighbor, weight in neighbors.items():
            new_dist = curr_dist + weight
            
            if neighbor not in distances:
                distances[neighbor] = float('inf')
                
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                # [STEP 2] Insert Heap: O(log V)
                heapq.heappush(pq, (new_dist, neighbor))
                
    return distances.get(end, float('inf')), visited_count

# --- IMPLEMENTASI ALGORITMA B: DIJKSTRA ARRAY (O(V^2)) ---
def algo_B_Array(instance: Any):
    """Dijkstra menggunakan Array/Linear Scan"""
    graph = instance['graph']
    start = str(instance['meta']['start_node'])
    end = str(instance['meta']['end_node'])
    
    nodes = list(graph.keys())
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0
    
    unvisited = {node: float('inf') for node in nodes}
    unvisited[start] = 0
    
    visited_count = 0
    
    # Loop Utama: Berjalan V kali
    while unvisited:
        # [STEP 1] Linear Scan: O(V) - INI BIANG KEROK KELAMBATAN
        # Kita harus cek satu-satu semua node di 'unvisited'
        current_node = None
        min_val = float('inf')
        
        for node, dist in unvisited.items():
            if dist < min_val:
                min_val = dist
                current_node = node
        
        if current_node is None: 
            break
        
        visited_count += 1
            
        if current_node == end:
            return distances[end], visited_count
            
        del unvisited[current_node]
        
        # Relaksasi Tetangga
        neighbors = graph.get(current_node, {})
        for neighbor, weight in neighbors.items():
            if neighbor in unvisited:
                new_dist = distances[current_node] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    unvisited[neighbor] = new_dist 
                    
    return distances.get(end, float('inf')), visited_count

# --- EVALUATOR ---
def evaluate(instance, result, project):
    if result == float('inf'):
        return 1.0 
    return 0.0

# --- MAIN DRIVER ---
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--instance', required=True, help='Path ke file JSON')
    p.add_argument('--algo', choices=['A', 'B'], default='A', help='A=Heap, B=Array')
    args = p.parse_args()
    
    try:
        with open(args.instance, 'r') as f:
            inst = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {args.instance} tidak ditemukan.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File {args.instance} bukan JSON yang valid.")
        sys.exit(1)
    
    project = inst.get("project", "unknown")

    # [BARU] Panggil Analisis Kompleksitas sebelum eksekusi
    # Ini akan mencetak estimasi beban kerja ke layar
    analyze_complexity(inst['graph'], args.algo)

    tracemalloc.start()
    
    t0 = time.perf_counter()
    
    if args.algo == 'A':
        out, visited = algo_A_Heap(inst)
    else:
        out, visited = algo_B_Array(inst)
        
    t1 = time.perf_counter()
    dt = (t1 - t0) * 1000.0 

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_mb = peak / (1024 * 1024)
    
    gap = evaluate(inst, out, project)
    
    print(f"Project={project} Algo={args.algo} Time_ms={dt:.2f} Peak_Memory_MB={peak_mb:.6f} Visited={visited} Result={out:.2f}")

if __name__ == '__main__':
    main()