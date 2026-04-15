import requests
import json
import time
from geopy.geocoders import Nominatim

def fetch_all_kabupatens():
    print("1. Завантажуємо список провінцій Індонезії...")
    prov_url = "https://emsifa.github.io/api-wilayah-indonesia/api/provinces.json"
    provinces = requests.get(prov_url).json()
    
    all_regencies = []
    
    print("2. Збираємо всі округи (Kabupaten) та міста (Kota)...")
    for prov in provinces:
        reg_url = f"https://emsifa.github.io/api-wilayah-indonesia/api/regencies/{prov['id']}.json"
        regencies = requests.get(reg_url).json()
        
        for reg in regencies:
            name_title = reg['name'].title()
            prov_title = prov['name'].title()
            
            all_regencies.append({
                "display_name": name_title,
                "province": prov_title
            })
            
    return all_regencies

def geocode_regencies(regencies):
    geolocator = Nominatim(user_agent="geoguessr_indo_parser")
    final_db = {}
    
    total = len(regencies)
    print(f"\n3. Починаємо пошук координат для {total} локацій.")
    print(f"Це займе близько {total / 60:.1f} хвилин (щоб нас не заблокував OpenStreetMap)...\n")
    
    for i, reg in enumerate(regencies):
        display_name = reg["display_name"]
        province = reg["province"]
        
        query = f"{display_name}, {province}, Indonesia"
        
        clean_name = display_name.replace("Kabupaten ", "").replace("Kota ", "")
        fallback_query = f"{clean_name}, {province}, Indonesia"
        
        try:
            location = geolocator.geocode(query)
            
            if not location:
                location = geolocator.geocode(fallback_query)
                
            if location:
                final_db[display_name] = {
                    "island": province, 
                    "lat": location.latitude,
                    "lon": location.longitude
                }
                print(f"[{i+1}/{total}] ✅ Знайдено: {display_name} -> {province}")
            else:
                print(f"[{i+1}/{total}] ❌ Не знайдено координати: {display_name}")
                
        except Exception as e:
            print(f"[{i+1}/{total}] ⚠️ Помилка з {display_name}: {e}")
            
        time.sleep(1.2)
        
    return final_db

if __name__ == "__main__":
    regencies = fetch_all_kabupatens()
    final_data = geocode_regencies(regencies)
    
    with open("kabupaten.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
        
    print(f"\n🎉 Парсинг завершено! Успішно збережено {len(final_data)} локацій у файл kabupaten.json.")