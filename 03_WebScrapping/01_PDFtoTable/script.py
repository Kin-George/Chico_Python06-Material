import pdfplumber
import pandas as pd
import re

# --- CONFIGURACIÓN ---
pdf_path = r"01_PDFtoTable\Data\cp-PMEnfoqueDiferencial-2024.pdf"
with pdfplumber.open(pdf_path) as pdf:
    page = pdf.pages[12]  # página 13
    text = page.extract_text()

# Extraer solo la sección de la Tabla 12
inicio = text.find("Condición Población Jefe de hogar")
fin = text.find("Fuente:")

tabla_texto = text[inicio:fin]

# Patrón: condición + número + número
pattern = r'(.+?)\s+(\d+,\d+)\s+(\d+,\d+)'

matches = re.findall(pattern, tabla_texto)

rows = []

for condicion, poblacion, jefe in matches:
    rows.append([
        condicion.strip(),
        float(poblacion.replace(",", ".")),
        float(jefe.replace(",", "."))
    ])

df = pd.DataFrame(rows, columns=["Condición", "Población", "Jefe_de_hogar"])

df.to_excel("tabla_12_migracion.xlsx", index=False)

print(df)