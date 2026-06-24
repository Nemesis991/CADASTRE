import json
import csv
import os

def generate_ekatte_csv(output_file=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if output_file is None:
        output_file = os.path.join(script_dir, "ekatte_dict.csv")
    
    json_file = os.path.join(script_dir, "ek_atte.json")
    
    print("-" * 50)
    print("1. Зареждане на локалния файл ek_atte.json...")
    print("-" * 50)
    
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        csv_rows = []
        for place in data:
            ekatte = place.get("ekatte")
            if not ekatte:
                continue
                
            # Изчистване на "обл. " и "общ. " от имената
            oblast = place.get("oblast_name", "").replace("обл. ", "").replace("Област ", "").strip()
            obshtina = place.get("obshtina_name", "").replace("общ. ", "").replace("Община ", "").strip()
            
            # Съставяне на пълното име: тип (гр./с./к.) + име
            ptype = place.get("t_v_m", "")
            name = place.get("name", "")
            full_name = f"{ptype} {name}".strip()
            
            csv_rows.append([ekatte, oblast, obshtina, full_name])
                    
        # Сортиране по ЕКАТТЕ код за по-прегледно
        csv_rows.sort(key=lambda x: str(x[0]))
        
        print("2. Записване на CSV файла...")
        
        # Записваме във формат UTF-8-SIG, за да може Excel/CAD да го чете правилно
        with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
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
if __name__ == '__main__':
    generate_ekatte_csv()