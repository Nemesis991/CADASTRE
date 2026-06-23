import os
import requests
import csv

def run_automation():
    # 1. Папката, където се намира самият Python скрипт (за да намери речника)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Работната папка (папката на чертежа, която LISP-ът подаде чрез BAT файла)
    work_dir = os.getcwd()
    
    # Разпределяне на пътищата
    input_file = os.path.join(work_dir, "selected_ekatte.txt") # Чете кодовете от папката на чертежа
    main_folder = os.path.join(work_dir, "Изходни")            # Записва ZIP файловете при чертежа
    dict_file = os.path.join(script_dir, "ekatte_dict.csv")    # Чете речника от папката на програмата
    
    base_url = "https://kais.cadastre.bg/bg/OpenData/Download"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
    target_files = ["поземлени имоти.zip", "сгради.zip"]

    # 1. Проверка за входни данни от AutoCAD (вече търси при чертежа)
    if not os.path.exists(input_file):
        print(f"ГРЕШКА: Няма намерен файл от AutoCAD ({input_file})")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        ekatte_list = [line.strip() for line in f if line.strip()]

    if not ekatte_list:
        print("Списъкът с ЕКАТТЕ кодове е празен!")
        return

    # 2. Зареждане на речника (Проверява и двата вида UTF кодирания - търси го при програмата)
    ekatte_map = {}
    for encoding_type in ['utf-8-sig', 'utf-8']:
        try:
            with open(dict_file, mode='r', encoding=encoding_type) as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 4:
                        ekatte_map[row[0].strip()] = {"oblast": row[1].strip(), "obshtina": row[2].strip(), "name": row[3].strip()}
            break
        except FileNotFoundError:
            continue

    if not ekatte_map:
        print(f"ГРЕШКА: Локалният речник 'ekatte_dict.csv' липсва в папка:\n{script_dir}")
        return

    print(f"Работна папка (Чертеж): {work_dir}")
    print(f"Папка на програмата: {script_dir}")
    print(f"Започва автоматично изтегляне на {len(ekatte_list)} землища...")

    # 3. Основен цикъл за теглене
    for ekatte in ekatte_list:
        if ekatte not in ekatte_map:
            print(f"[!] ЕКАТТЕ {ekatte} не съществува в речника. Пропуска се.")
            continue
            
        oblast = ekatte_map[ekatte]["oblast"]
        obshtina = ekatte_map[ekatte]["obshtina"]
        name = ekatte_map[ekatte]["name"]
        
        zemlishte_full = f"{name} ({ekatte})"
        location_folder = os.path.join(main_folder, zemlishte_full.replace('/', '_').replace('\\', '_'))
        
        if not os.path.exists(location_folder): 
            os.makedirs(location_folder)

        print(f"\n--- Изтегляне за: {zemlishte_full} ---")

        for file_type in target_files:
            server_path = f"област {oblast}/община {obshtina}/{zemlishte_full}/{file_type}"
            params = {'path': server_path}
            clean_name = f"{ekatte}_{file_type.replace(' ', '_')}"
            
            try:
                resp = requests.get(base_url, params=params, headers=headers, stream=True)
                if resp.status_code == 200:
                    with open(os.path.join(location_folder, clean_name), "wb") as f:
                        for chunk in resp.iter_content(8192): f.write(chunk)
                    print(f"  [V] {file_type} - СВАЛЕН")
                else:
                    print(f"  [X] Не е намерен на сървъра: {file_type}")
            except Exception as e:
                print(f"  [!] Проблем с мрежата: {e}")

if __name__ == "__main__":
    run_automation()
    print("\n" + "="*50)
    print("Процесът завърши!")
    input("Натисни Enter за затваряне на прозореца...")