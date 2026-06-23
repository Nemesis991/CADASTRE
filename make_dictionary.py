import urllib.request
import json
import csv
import os

def generate_ekatte_csv(output_file=None):
    if output_file is None:
        output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ekatte_dict.csv")
    print("-" * 50)
    print("1. Свързване с отворената база данни (GitHub)...")
    print("-" * 50)
    
    url = "https://raw.githubusercontent.com/Kostadin/Places-in-Bulgaria/master/Places-in-Bulgaria.json"
    
    try:
        # Изтегляне на данните
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        print("2. Данните са изтеглени! Започва форматиране...")
            
        csv_rows = []
        # Обхождане на JSON дървото и извличане на нужните 4 параметъра
        for oblast, obshtini in data.items():
            for obshtina, places in obshtini.items():
                for ekatte, details in places.items():
                    name = details.get('name', '')
                    ptype = details.get('type', '')
                    
                    # Сглобяване на името (напр. "гр. Габрово")
                    full_name = f"{ptype} {name}".strip()
                    
                    # Добавяне на реда: ЕКАТТЕ, Област, Община, Име
                    csv_rows.append([ekatte, oblast, obshtina, full_name])
                    
        # Сортиране по ЕКАТТЕ код за по-прегледно
        csv_rows.sort(key=lambda x: x[0])
        
        print("3. Записване на CSV файла...")
        
        # Записваме във формат UTF-8, за да няма йероглифи
        with open(output_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for row in csv_rows:
                writer.writerow(row)
                
        print("-" * 50)
        print(f"[V] УСПЕХ! Речникът е създаден в: {output_file}")
        print(f"[i] Общо въведени населени места: {len(csv_rows)}")
        print("-" * 50)
        
    except Exception as e:
        print(f"[X] Възникна грешка при създаването: {e}")

# Стартиране на процеса
generate_ekatte_csv()