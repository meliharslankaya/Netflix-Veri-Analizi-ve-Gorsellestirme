import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Stil ve renk paletini ayarlama
sns.set(style="whitegrid")
plt.style.use('seaborn-whitegrid')

# Veri setini okuma
file_path = "netflix_titles.csv"  # CSV dosyanızın yolu
data = pd.read_csv(file_path)

# İlk 5 satırı görüntüleme
print(data.head())

# Pasta Grafik: İçerik türlerine göre yüzdesel dağılım
plt.figure(figsize=(12, 7))
colors = sns.color_palette('pastel')
type_counts = data['type'].value_counts()
type_counts.plot.pie(autopct=lambda p: f'{p:.1f}% ({int(p * len(data) / 100)})', startangle=90, colors=colors, textprops={'fontsize': 12})
plt.title('İçerik Türlerine Göre Dağılım', fontsize=16)
plt.ylabel('')
plt.show()

# 3. Histogram: Yayın tarihine göre içerik sayısı (daha az yıl)
plt.figure(figsize=(12, 7))
data['release_year'] = data['release_year'].astype(int)
recent_data = data[data['release_year'] >= 2000]  # 2000 yılından sonraki verileri al
sns.histplot(recent_data['release_year'], bins=20, kde=False, color='skyblue')
plt.title('Yayın Tarihine Göre İçerik Sayısı (2000 ve Sonrası)', fontsize=16)
plt.xlabel('Yıl', fontsize=14)
plt.ylabel('Sayı', fontsize=14)
plt.xticks(rotation=90, fontsize=12)
plt.yticks(fontsize=12)
plt.show()

# 4. Isı Haritası (Choropleth Map): Ülkelere göre içerik sayısı
# Ülke verilerini ayrıştırma ve sayma
country_data = data['country'].dropna().str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
country_data.name = 'country'
country_data = country_data.value_counts().reset_index()
country_data.columns = ['country', 'count']

# Dünya haritasını yükleme
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world.rename(columns={'name': 'country'})
world_data = world.merge(country_data, how='left', on='country')

# Eşik değerini belirleme
threshold = 50

# Isı haritasını çizme
fig, ax = plt.subplots(1, 1, figsize=(20, 15))
world_data.boundary.plot(ax=ax, linewidth=1)
world_data.plot(column='count', ax=ax, legend=True, cmap='OrRd', missing_kwds={"color": "lightgrey"}, edgecolor='black', linewidth=0.4)

# Eşik değerinin üzerindeki ülke isimlerini ekleme
for x, y, label, count in zip(world_data.geometry.centroid.x, world_data.geometry.centroid.y, world_data['country'], world_data['count']):
    if pd.notna(count) and count > threshold:
        plt.text(x, y, label, fontsize=8, ha='center', color='black')

ax.set_title('Ülkelere Göre İçerik Sayısı', fontsize=20)
ax.set_axis_off()
plt.show()
