import openpyxl
from pathlib import Path
from pyproj import Transformer


raiz = Path(__file__).resolve().parent.parent

encontrados = list(raiz.rglob("Paso1_Datos_Organizados_Facatativa.xlsx"))
if not encontrados:
    raise SystemExit(f"No encontré Paso1_Datos_Organizados_Facatativa.xlsx dentro de {raiz}")
entrada = encontrados[0]
salida = entrada.with_name("Paso2_Coordenadas_Facatativa.xlsx")
print("Leyendo:", entrada)

# WGS84 -> MAGNA-SIRGAS / Colombia Bogotá zone (Gauss-Krüger origen Bogotá)
t = Transformer.from_crs("EPSG:4326", "EPSG:3116", always_xy=True)
wb = openpyxl.load_workbook(entrada)

for ws in wb.worksheets:
    if not ws.title.startswith("Ciclo"):
        continue
    ws["P5"], ws["Q5"] = "Este (m)", "Norte (m)"
    fila = 6
    while ws[f"D{fila}"].value is not None:
        este, norte = t.transform(-ws[f"E{fila}"].value, ws[f"D{fila}"].value)
        ws[f"P{fila}"], ws[f"Q{fila}"] = round(este, 3), round(norte, 3)
        fila += 1

wb.save(salida)
print("Listo:", salida)