import osmnx as ox
import networkx as nx
import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent / 'data'
BASE_DIR.mkdir(exist_ok=True)

def save_instance(name, data):
    p = BASE_DIR / name
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {p}")

def generate_solo_instances():
    print("1. Mendownload Peta Solo (Master)...")
    center_point = (-7.5714, 110.8295) 
    G_master = ox.graph_from_point(center_point, dist=2000, network_type='drive')
    G_master = ox.add_edge_speeds(G_master)
    G_master = ox.add_edge_travel_times(G_master)
    
    nodes_list = list(G_master.nodes)
    
    # --- TAMBAHAN PENTING: SIMPAN KOORDINAT NODE ---
    node_coords = {}
    for node, data in G_master.nodes(data=True):
        node_coords[node] = {'y': data['y'], 'x': data['x']} # Lat, Lon
    
    print("2. Membuat 15 Instance Unik dengan Koordinat...")
    rnd = random.Random(42) 
    
    for i in range(1, 16):
        start = rnd.choice(nodes_list)
        end = rnd.choice(nodes_list)
        while start == end:
            end = rnd.choice(nodes_list)
            
        adj_list = {}
        for u, v, data in G_master.edges(data=True):
            if u not in adj_list: adj_list[u] = {}
            weight = data.get('travel_time', data.get('length', 1))
            adj_list[u][v] = weight

        instance_data = {
            "project": "shortest_path_solo",
            "meta": {
                "start_node": start,
                "end_node": end,
                "total_nodes": len(G_master.nodes),
                "total_edges": len(G_master.edges)
            },
            "nodes": node_coords, # <--- DATA BARU UNTUK VISUALISASI
            "graph": adj_list
        }
        
        save_instance(f'solo_route_G{i:02d}.json', instance_data)

if __name__ == "__main__":
    generate_solo_instances()