import cv2
import os
import sys

# Funkcia na načítanie a dekódovanie QR kódu z obrázka
def read_qr_code(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    return data

# Funkcia na extrahovanie ceny a názvu tovaru z textu
def extract_product_info(data):
    start_cena_index = data.find("Cena:")
    end_cena_index = data.find("€", start_cena_index)
    start_tovar_index = data.find("Tovar:", end_cena_index)
    if start_cena_index != -1 and end_cena_index != -1 and start_tovar_index != -1:
        cena_str = data[start_cena_index + 5:end_cena_index].strip()
        tovar_str = data[start_tovar_index + 6:].strip()
        try:
            cena = float(cena_str)
            return (cena, tovar_str)
        except ValueError:
            return (None, None)
    return (None, None)

# Absolútna cesta k adresáru s QR kódmi
directory = 'C:/Users/Ucitel/Desktop/QR_KODY'  # Zmeňte na cestu k vášmu adresáru

# Získanie hranice ceny zo vstupu od užívateľa
try:
    hladana_cena = float(input("Prosím, zadajte hranicu ceny: "))
    print()
except ValueError:
    print("Chyba: Zadajte platné číslo pre hranicu ceny.")
    sys.exit(1)

# Premenná na uchovávanie názvov a cien produktov
expensive_products = []

# Iterácia cez súbory v adresári
for filename in os.listdir(directory):
    if filename.endswith('.png') or filename.endswith('.jpg'):
        file_path = os.path.join(directory, filename)
        qr_data = read_qr_code(file_path)
        
        if qr_data:
            cena, tovar = extract_product_info(qr_data)
            if cena is not None and cena > hladana_cena:
                expensive_products.append((filename, cena, tovar))

# Výpis počtu položiek, názvov, názvu tovaru a cien produktov s cenou vyššou ako zadaná hranica
if expensive_products:
    print(f"TOVARY DRAHŠIE AKO {hladana_cena} EUR SÚ:")
    print("=" * 35)
    print(f"Počet položiek: {len(expensive_products)}")
    print()
    for product in expensive_products:
        print(f"qr_kod_bločku: {product[0]}")
        print(f"Cena: {product[1]} EUR")
        print(f"Tovar: {product[2]}")
        print()
else:
    print(f"V adresári nie sú žiadne produkty s cenou vyššou ako {hladana_cena} EUR.")
