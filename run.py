import tracemalloc
import json
import argparse
import time
import heapq
from typing import Any

# --- IMPLEMENTASI ALGORITMA A: DIJKSTRA HEAP (O(E log V)) ---
def algo_A_Heap(instance: Any) -> float:
    """Dijkstra menggunakan Priority Queue (Min-Heap)"""
    graph = instance['graph']
    # Pastikan node start/end dibaca sebagai string agar cocok dengan key JSON
    start = str(instance['meta']['start_node']) 
    end = str(instance['meta']['end_node'])
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_node == end:
            return curr_dist
        
        if curr_dist > distances.get(curr_node, float('inf')):
            continue
        
        neighbors = graph.get(curr_node, {})
        for neighbor, weight in neighbors.items():
            new_dist = curr_dist + weight
            
            # Handle node baru jika belum ada di distances
            if neighbor not in distances:
                distances[neighbor] = float('inf')
                
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
                
    return distances.get(end, float('inf'))

# --- IMPLEMENTASI ALGORITMA B: DIJKSTRA ARRAY (O(V^2)) ---
def algo_B_Array(instance: Any) -> float:
    """Dijkstra menggunakan Array/Linear Scan"""
    graph = instance['graph']
    start = str(instance['meta']['start_node'])
    end = str(instance['meta']['end_node'])
    
    nodes = list(graph.keys())
    distances = {node: float('inf') for node in nodes}
    distances[start] = 0
    
    # Unvisited set (simulasi array linear)
    unvisited = {node: float('inf') for node in nodes}
    unvisited[start] = 0
    
    while unvisited:
        # --- LINEAR SCAN (Bottleneck O(V)) ---
        # Mencari node dengan jarak minimum secara manual loop
        current_node = None
        min_val = float('inf')
        
        for node, dist in unvisited.items():
            if dist < min_val:
                min_val = dist
                current_node = node
        
        if current_node is None: # Sisa node infinity (tidak terjangkau)
            break
            
        if current_node == end:
            return distances[end]
            
        # Hapus dari unvisited
        del unvisited[current_node]
        
        # Update neighbors
        neighbors = graph.get(current_node, {})
        for neighbor, weight in neighbors.items():
            if neighbor in unvisited:
                new_dist = distances[current_node] + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    unvisited[neighbor] = new_dist # Update nilai di 'array'
                    
    return distances.get(end, float('inf'))

# --- EVALUATOR ---
def evaluate(instance, result, project):
    # Jika result infinity, berarti gagal menemukan jalur
    if result == float('inf'):
        return 1.0 # Error/Not Found
    return 0.0 # Valid found

# --- MAIN DRIVER ---
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--instance', required=True, help='Path ke file JSON')
    p.add_argument('--algo', choices=['A', 'B'], default='A', help='A=Heap, B=Array')
    args = p.parse_args()
    
    # 1. Load Data
    try:
        with open(args.instance, 'r') as f:
            inst = json.load(f)
    except FileNotFoundError:
        print(f"Error: File {args.instance} tidak ditemukan.")
        return
    
    project = inst.get("project", "unknown")

    # Mulai Tracking Memori
    tracemalloc.start()
    
    # 2. Run Algorithm & Timing
    t0 = time.perf_counter()
    if args.algo == 'A':
        out = algo_A_Heap(inst)
    else:
        out = algo_B_Array(inst)
    t1 = time.perf_counter()
    dt = (t1 - t0) * 1000.0 # milidetik

    # Ambil Snapshot Memori Puncak
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_mb = peak / (1024 * 1024) # Konversi Bytes ke MB (Megabytes)
    
    # 3. Evaluate
    gap = evaluate(inst, out, project)
    
    # 4. Print Result (Wajib format ini untuk laporan/parsing)
    print(f"Project={project} Algo={args.algo} Time_ms={dt:.2f} Peak_Memory_MB={peak_mb:.6f} Result={out:.2f}")

if __name__ == '__main__':
    main()