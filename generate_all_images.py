import json
import heapq
import matplotlib.pyplot as plt
from pathlib import Path
import time

# Setup Folder
DATA_DIR = Path('data')
RESULTS_DIR = Path('results')
RESULTS_DIR.mkdir(exist_ok=True)

# --- FUNGSI DIJKSTRA (Copy-paste agar mandiri) ---
def get_dijkstra_path(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    predecessors = {node: None for node in graph} 
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_node == end: break
        if curr_dist > distances.get(curr_node, float('inf')): continue
            
        for neighbor, weight in graph.get(curr_node, {}).items():
            new_dist = curr_dist + weight
            if neighbor not in distances: distances[neighbor] = float('inf')
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = curr_node
                heapq.heappush(pq, (new_dist, neighbor))
    
    path = []
    curr = end
    if distances.get(end) == float('inf'): return []
    while curr is not None:
        path.append(curr)
        curr = predecessors.get(curr)
    return path[::-1]

# --- GENERATOR GAMBAR MASSAL ---
def generate_all():
    json_files = sorted(list(DATA_DIR.glob('*.json')))
    
    if not json_files:
        print("File data JSON tidak ditemukan!")
        return

    print(f"Mulai membuat gambar untuk {len(json_files)} instance...")
    print("Mohon bersabar, menggambar peta memakan waktu...")
    
    for i, json_path in enumerate(json_files, 1):
        with open(json_path, 'r') as f:
            data = json.load(f)

        nodes_coords = data.get('nodes')
        graph_adj = data.get('graph')
        start_node = str(data['meta']['start_node'])
        end_node = str(data['meta']['end_node'])
        instance_name = json_path.stem # misal: solo_route_G01

        # Hitung Rute
        path_nodes = get_dijkstra_path(graph_adj, start_node, end_node)
        
        # Setup Plot (Tanpa menampilkannya di layar)
        plt.ioff() # Turn off interactive mode
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Gambar Background (Jalanan)
        for u, neighbors in graph_adj.items():
            if u not in nodes_coords: continue
            x1, y1 = nodes_coords[u]['x'], nodes_coords[u]['y']
            for v in neighbors:
                if v in nodes_coords:
                    x2, y2 = nodes_coords[v]['x'], nodes_coords[v]['y']
                    ax.plot([x1, x2], [y1, y2], c='#e0e0e0', linewidth=0.5, zorder=1)

        # Gambar Rute (Merah)
        if path_nodes:
            path_x = [nodes_coords[str(n)]['x'] for n in path_nodes if str(n) in nodes_coords]
            path_y = [nodes_coords[str(n)]['y'] for n in path_nodes if str(n) in nodes_coords]
            
            ax.plot(path_x, path_y, c='red', linewidth=2, label='Rute', zorder=2)
            ax.scatter(path_x[0], path_y[0], c='green', s=100, zorder=3)
            ax.scatter(path_x[-1], path_y[-1], c='blue', s=100, zorder=3)

        ax.set_title(f"{instance_name}", fontsize=12)
        ax.axis('off')
        
        # Simpan
        output_path = RESULTS_DIR / f"img_{instance_name}.png"
        plt.tight_layout()
        plt.savefig(output_path, dpi=100) # dpi 100 biar tidak terlalu besar filenya
        plt.close(fig) # Tutup agar memori tidak penuh
        
        print(f"[{i}/{len(json_files)}] Disimpan: {output_path.name}")

    print("\n[SELESAI] Semua gambar peta tersimpan di folder 'results/'")

if __name__ == "__main__":
    generate_all()