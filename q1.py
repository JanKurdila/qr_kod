import cv2
import os

# Funkcia na načítanie a dekódovanie QR kódu z obrázka
def read_qr_code(image_path):
    img = cv2.imread(image_path)
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(img)
    return data

# Adresár s QR kódmi
directory = 'C:/Users/Ucitel/Desktop/QR_KODY'  # Zmeňte na cestu k vášmu adresáru

# Iterácia cez súbory v adresári
for filename in os.listdir(directory):
    if filename.lower().endswith(('.png', '.jpg')):
        file_path = os.path.join(directory, filename)
        qr_data = read_qr_code(file_path)
        
        if qr_data:
            # Rozdelenie údajov na názov súboru a detaily produktu
            formatted_output = f"{filename}:\n{qr_data.strip()}\n"
            # Tlač formátovaného výstupu
            print(formatted_output)
