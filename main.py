import folium
from folium.plugins import HeatMap
import pandas as pd

# Veri setini yükle
url = "https://storage.googleapis.com/dft-statistics/road-traffic/downloads/rawcount/region_id/dft_rawcount_region_id_3.csv"
data = pd.read_csv(url, dtype={'start_junction_road_name': str, 'end_junction_road_name': str})

# Yıl sütununu oluştur
data['year'] = pd.to_datetime(data['count_date']).dt.year

# Edinburgh merkezi ve incelenecek yıllar
edinburgh_center = [55.9533, -3.1883]
filtered_years = [2018, 2020, 2022]

# Haritaları kaydetmek için boş bir liste (README için bağlantı oluştururken kullanılacak)
github_links = []

for year in filtered_years:
    # Veriyi yıla göre filtrele
    year_data = data[data['year'] == year]
    heat_data = year_data[['latitude', 'longitude', 'pedal_cycles']].dropna().values.tolist()

    # Haritayı oluştur
    main_map = folium.Map(location=edinburgh_center, zoom_start=12)
    HeatMap(heat_data, radius=25, blur=15, min_opacity=0.5).add_to(main_map)

    # HTML dosyasını kaydet
    map_file = f"bicycle_heatmap_{year}.html"
    main_map.save(map_file)  # Harita HTML dosyası olarak kaydedilir
    print(f"Harita kaydedildi: {map_file}")

    # GitHub Raw bağlantısı için bir şablon (kendi repo bilgilerinizi ekleyin)
    raw_url = f"https://raw.githubusercontent.com/<kullanıcı-adı>/<repo-adı>/main/{map_file}"
    preview_url = f"https://htmlpreview.github.io/?{raw_url}"
    github_links.append((year, preview_url))

# GitHub bağlantılarını README dosyasına yazdırma
print("\nAşağıdaki bağlantıları README dosyasına ekleyebilirsiniz:\n")
for year, link in github_links:
    print(f"- [{year} Heatmap]({link})")
