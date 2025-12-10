import osmnx as ox
import networkx as nx
import json
import random
from pathlib import Path

# Setup folder data
BASE_DIR = Path(__file__).resolve().parent / 'data'
BASE_DIR.mkdir(exist_ok=True)

def save_instance(name, data):
    p = BASE_DIR / name
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved: {p}")

def generate_solo_instances():
    print("1. Mendownload Peta Solo (Master)...")
    # Download peta agak luas agar bisa di-crop
    center_point = (-7.5714, 110.8295) # Balai Kota
    G_master = ox.graph_from_point(center_point, dist=2000, network_type='drive')
    G_master = ox.add_edge_speeds(G_master)
    G_master = ox.add_edge_travel_times(G_master)
    
    nodes_list = list(G_master.nodes)
    
    print("2. Membuat 15 Instance Unik...")
    
    # Kita buat 15 variasi (G01 - G15)
    # Variasi bisa berupa: Titik Start/End beda, atau Radius beda.
    
    rnd = random.Random(42) # Seed biar konsisten
    
    for i in range(1, 16):
        # Pilih 2 node acak sebagai Start dan End
        start = rnd.choice(nodes_list)
        end = rnd.choice(nodes_list)
        while start == end:
            end = rnd.choice(nodes_list)
            
        # Konversi Graph ke format Dictionary biar ringan di JSON
        # Kita simpan Adjacency List: {node_id: {neighbor_id: weight, ...}}
        adj_list = {}
        for u, v, data in G_master.edges(data=True):
            if u not in adj_list: adj_list[u] = {}
            if v not in adj_list: adj_list[v] = {}
            
            # Ambil waktu tempuh (travel_time) atau panjang jalan
            weight = data.get('travel_time', data.get('length', 1))
            adj_list[u][v] = weight
            
            # Karena graph jalan bisa satu arah, kita simpan sesuai arahnya (Directed)

        instance_data = {
            "project": "shortest_path_solo",
            "group_id": "Kelompok_Anda",
            "meta": {
                "start_node": start,
                "end_node": end,
                "total_nodes": len(G_master.nodes),
                "total_edges": len(G_master.edges)
            },
            "graph": adj_list # Data peta tersimpan di sini
        }
        
        save_instance(f'solo_route_G{i:02d}.json', instance_data)

if __name__ == "__main__":
    generate_solo_instances()