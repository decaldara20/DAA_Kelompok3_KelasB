import json
import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path('data/solo_route_G01.json') # Sampel representatif

def analyze_dataset():
    print("=== ANALISIS STATISTIK DATASET (Untuk Laporan Bab 2) ===\n")
    
    if not DATA_PATH.exists():
        print("ERROR: File data tidak ditemukan. Jalankan generate_instances.py dulu.")
        return

    with open(DATA_PATH, 'r') as f:
        data = json.load(f)

    # 1. Statistik Dasar (N dan M)
    graph = data['graph']
    n_nodes = len(graph)
    
    # Hitung Edges (m) dan kumpulkan Bobot (Weights)
    edges_weights = []
    m_edges = 0
    
    for u, neighbors in graph.items():
        m_edges += len(neighbors)
        for v, weight in neighbors.items():
            edges_weights.append(weight)
            
    # 2. Sebaran Nilai (Bobot Jalan)
    weights = np.array(edges_weights)
    
    print(f"1. STRUKTUR GRAF (PETA SOLO):")
    print(f"   - Jumlah Node (n) : {n_nodes:,} simpul")
    print(f"   - Jumlah Edge (m) : {m_edges:,} ruas jalan")
    print(f"   - Densitas Graf   : {m_edges / (n_nodes * (n_nodes-1)):.6f} (Sangat Jarang/Sparse)")
    
    print(f"\n2. SEBARAN NILAI BOBOT (Waktu Tempuh/Jarak):")
    print(f"   - Minimum : {weights.min():.2f}")
    print(f"   - Maximum : {weights.max():.2f}")
    print(f"   - Rata-rata (Mean) : {weights.mean():.2f}")
    print(f"   - Median           : {np.median(weights):.2f}")
    print(f"   - Standar Deviasi  : {weights.std():.2f}")

    # 3. Contoh Input (Snippet)
    print(f"\n3. CONTOH FORMAT INPUT (JSON Snippet):")
    snippet = {
        "project": data['project'],
        "meta": data['meta'],
        "graph_sample": {k: graph[k] for k in list(graph.keys())[:2]} # Ambil 2 node saja
    }
    print(json.dumps(snippet, indent=2))

if __name__ == "__main__":
    analyze_dataset()