# Instal dependensi yang diperlukan
pip install osmnx networkx scikit-learn pandas matplotlib seaborn

#Panduan eksekusi
-algoritma heap:
python run.py --instance data/solo_route_G01.json --algo A

-algoritma array
python run.py --instance data/solo_route_G01.json --algo B

-visualisasi
python visualize_route.py --instance data/solo_route_G01.json

-Jalankan run_batch.py untuk menguji ke-15 instance secara -otomatis. Script ini akan:
-Menjalankan Algo A dan B pada setiap file JSON di folder data/.
-Mencatat waktu eksekusi dan memori.
-Mengekspor hasil mentah ke CSV.
-Otomatis membuat plot perbandingan.
python run_batch.py