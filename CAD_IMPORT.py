import os
import requests
import csv

def download_only_with_ekatte(ekatte_list, dict_file="ekatte_dict.csv", main_folder="D:/repo/CADASTRE/Изходни"):
    
    # 1. Зареждане на "Речника" в паметта
    ekatte_map = {}
    try:
        with open(dict_file, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                # Очакваме CSV формат: ЕКАТТЕ, Област, Община, Име
                ekatte_map[row[0].strip()] = {"oblast": row[1].strip(), "obshtina": row[2].strip(), "name": row[3].strip()}
    except FileNotFoundError:
        print(f"ГРЕШКА: Файлът {dict_file} не е намерен! Скриптът се нуждае от него, за да превежда кодовете.")
        return

    base_url = "https://kais.cadastre.bg/bg/OpenData/Download"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
    target_files = ["поземлени имоти.zip", "сгради.zip"]

    # 2. Обхождане само по ЕКАТТЕ
    for ekatte in ekatte_list:
        ekatte = str(ekatte).strip()
        
        # Проверяваме дали го имаме в речника
        if ekatte not in ekatte_map:
            print(f"[!] ЕКАТТЕ {ekatte} не е открито в локалния речник. Пропускаме го.")
            continue
            
        # Извличаме автоматично данните
        oblast = ekatte_map[ekatte]["oblast"]
        obshtina = ekatte_map[ekatte]["obshtina"]
        name = ekatte_map[ekatte]["name"]
        
        # Сглобяваме пълното име както го иска КАИС (напр. "с. Червена могила (80488)")
        zemlishte_full = f"{name} ({ekatte})"
        
        location_folder = os.path.join(main_folder, zemlishte_full.replace('/', '_'))
        if not os.path.exists(location_folder): os.makedirs(location_folder)

        print(f"--- Изтегляне за: {zemlishte_full} (Област {oblast}, Община {obshtina}) ---")

        # 3. Изтегляне
        for file_type in target_files:
            server_path = f"област {oblast}/община {obshtina}/{zemlishte_full}/{file_type}"
            params = {'path': server_path}
            clean_name = f"{ekatte}_{file_type.replace(' ', '_')}"
            
            try:
                resp = requests.get(base_url, params=params, headers=headers, stream=True)
                if resp.status_code == 200:
                    with open(os.path.join(location_folder, clean_name), "wb") as f:
                        for chunk in resp.iter_content(8192): f.write(chunk)
                    print(f"  [V] {clean_name} - ОК")
                else:
                    print(f"  [X] Отказан достъп от КАИС. Провери дали имената съвпадат точно.")
            except Exception as e:
                print(f"  [!] Мрежова грешка: {e}")

# ==========================================
# ВХОД НА ДАННИ - САМО ЕКАТТЕ
# ==========================================
my_ekatte_route = [  
    "80488",
    "69239",
    "61577",
    "24832",
    "22490",
    "81709",
    "38265",
    "36566",
    "83082",
    "55364",
    "52297",
    "48711",
    "46824",
    "39640",
    "24791",
    "21974",
    "18263",
    "15535",
    "04501",
    "02052",
    "02049"
]

download_only_with_ekatte(ekatte_list=my_ekatte_route)