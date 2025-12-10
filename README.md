DAA Instance Package (Proyek Shortest Path - Navigasi Solo)

- data/: folder ini berisi instance JSON (15 variasi rute unik di Surakarta).
- run.py: pseudocode untuk mengeksekusi algoritma.
- generate_instances.py: pseudocode generator varian rute per kelompok 1 sampai dengan 15 menggunakan data OpenStreetMap.
- run_batch.py: pseudocode tambahan untuk eksekusi otomatis semua instance, menghitung speedup, dan export hasil ke CSV.

Cara pakai (Single Instance):
python run.py --instance data/solo_route_G01.json --algo A
python run.py --instance data/solo_route_G01.json --algo B

Cara pakai (Batch Experiment):
python run_batch.py

Requirements:
pip install osmnx networkx scikit-learn pandas matplotlib seaborn

Hasil dan Summary
Rata-rata Waktu Heap : 5.0108 ms
Rata-rata Waktu Array: 260.7950 ms
Speedup: Heap 52.05x lebih cepat dari Array

Visualisasi data
result\plot_speedup.png
    -Sumbu X (Instance)     : Kasus rute yang diuji node ke node (G01-G15)
    -Sumbu Y (Speedup)      : Rasio kecepatan uji, misal 50 yang berarti 50x lebih cepat dibanding array
    -Garis Merah            : Performa spesifik per uji
    -Garis Putus-putus      : Rata-rata uji djikstra heap di 15 percobaan dibanding djikstra array