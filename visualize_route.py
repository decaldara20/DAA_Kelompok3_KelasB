import json
import heapq
import matplotlib.pyplot as plt
import argparse
from pathlib import Path

# --- FUNGSI DIJKSTRA (Khusus untuk melacak jalur) ---
def get_dijkstra_path(graph, start, end):
    """
    Menjalankan Dijkstra untuk mendapatkan urutan node (path).
    Mengembalikan list node: [start, node_a, node_b, ..., end]
    """
    # Inisialisasi
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    # Dictionary untuk melacak parent node agar bisa backtrack jalur
    predecessors = {node: None for node in graph} 
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_node == end:
            break # Tujuan ditemukan
        
        if curr_dist > distances.get(curr_node, float('inf')):
            continue
            
        # Cek Tetangga
        neighbors = graph.get(curr_node, {})
        for neighbor, weight in neighbors.items():
            new_dist = curr_dist + weight
            
            # Jika belum ada di distances, anggap infinity
            if neighbor not in distances:
                distances[neighbor] = float('inf')
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = curr_node # Simpan jejak
                heapq.heappush(pq, (new_dist, neighbor))
    
    # --- REKONSTRUKSI JALUR (Backtracking) ---
    path = []
    curr = end
    
    # Cek apakah end node terjangkau
    if distances.get(end) == float('inf'):
        return [] # Tidak ada jalur

    while curr is not None:
        path.append(curr)
        curr = predecessors.get(curr)
        
    return path[::-1] # Balik urutan agar dari Start -> End

# --- FUNGSI VISUALISASI ---
def visualize(json_path):
    print(f"--- Memvisualisasikan: {json_path} ---")
    
    # 1. Load Data
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("File tidak ditemukan.")
        return

    nodes_coords = data.get('nodes') # Koordinat {id: {x:..., y:...}}
    graph_adj = data.get('graph')
    
    if not nodes_coords:
        print("ERROR: File JSON ini tidak memiliki data koordinat 'nodes'.")
        print("Solusi: Jalankan ulang 'generate_instances.py' yang baru.")
        return

    start_node = str(data['meta']['start_node'])
    end_node = str(data['meta']['end_node'])
    
    print("1. Menghitung rute terpendek...")
    path_nodes = get_dijkstra_path(graph_adj, start_node, end_node)
    
    if not path_nodes:
        print("PERINGATAN: Tidak ada jalur yang ditemukan antar titik ini.")
        return

    # 2. Setup Plot
    print("2. Menggambar peta (Background)...")
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Gambar semua jalan (Edges) sebagai garis abu-abu tipis
    # Kita iterasi adj_list
    for u, neighbors in graph_adj.items():
        if u not in nodes_coords: continue
        x1, y1 = nodes_coords[u]['x'], nodes_coords[u]['y']
        
        for v in neighbors:
            if v in nodes_coords:
                x2, y2 = nodes_coords[v]['x'], nodes_coords[v]['y']
                # Plot garis tipis (Background Map)
                ax.plot([x1, x2], [y1, y2], c='#d9d9d9', linewidth=0.8, zorder=1)

    print("3. Menggambar rute solusi...")
    # Ambil koordinat untuk jalur merah
    path_x = []
    path_y = []
    for node_id in path_nodes:
        node_id = str(node_id)
        if node_id in nodes_coords:
            path_x.append(nodes_coords[node_id]['x'])
            path_y.append(nodes_coords[node_id]['y'])
    
    # Plot Rute (Garis Merah Tebal)
    ax.plot(path_x, path_y, c='red', linewidth=3, label='Jalur Tercepat', zorder=2)
    
    # Plot Titik Start (Hijau) & End (Biru)
    ax.scatter(path_x[0], path_y[0], c='green', s=150, edgecolors='black', label='Start', zorder=3)
    ax.scatter(path_x[-1], path_y[-1], c='blue', s=150, edgecolors='black', label='End', zorder=3)
    
    # Kosmetik Grafik
    filename = Path(json_path).name
    ax.set_title(f"Visualisasi Rute: {filename}\nNodes: {len(path_nodes)} titik", fontsize=14)
    ax.legend()
    ax.axis('off') # Matikan sumbu X/Y agar terlihat seperti peta bersih
    
    # Simpan
    output_dir = Path('results')
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"visual_{Path(json_path).stem}.png"
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150)
    print(f"[SUKSES] Gambar disimpan di: {output_file}")
    plt.show()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--instance', required=True, help='Path ke file JSON')
    args = p.parse_args()
    
    visualize(args.instance)