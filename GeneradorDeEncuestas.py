import random
import numpy as np

def generar_datos_censo(archivo_encuestas, archivo_localidades, num_hogares):
    # 1. Definición de la Jerarquía Geográfica (Localidad: Región)
    # Esto simula el contenido de localidades.txt
    mapa_territorial = {
        # V Región
        "Valparaiso": "V_Region",
        "Vina_del_Mar": "V_Region",
        "Quilpue": "V_Region",
        "Villa_Alemana": "V_Region",
        # Región Metropolitana
        "Santiago": "Metropolitana",
        "Maipu": "Metropolitana",
        "Puente_Alto": "Metropolitana",
        "Nunoa": "Metropolitana",
        "Las_Condes": "Metropolitana",
        # VIII Región
        "Concepcion": "VIII_Region",
        "Talcahuano": "VIII_Region",
        "Los_Angeles": "VIII_Region",
        "Chillan": "VIII_Region",
        # I Región
        "Arica": "I_Region",
        "Putre": "I_Region",
        "Camarones": "I_Region",
        # II Región
        "Antofagasta": "II_Region",
        "Calama": "II_Region",
        "Tocopilla": "II_Region",
        # III Región
        "Copiapo": "III_Region",
        "Vallenar": "III_Region",
        "Chanaral": "III_Region",
        # IV Región
        "La_Serena": "IV_Region",
        "Coquimbo": "IV_Region",
        "Ovalle": "IV_Region",
        # VI Región
        "Rancagua": "VI_Region",
        "San_Fernando": "VI_Region",
        "Pichilemu": "VI_Region",
        # VII Región
        "Talca": "VII_Region",
        "Curico": "VII_Region",
        "Linares": "VII_Region",
        # XIV Región
        "Valdivia": "XIV_Region",
        "La_Union": "XIV_Region",
        "Rio_Bueno": "XIV_Region",
    }

    # Guardar el archivo de localidades para los alumnos
    with open(archivo_localidades, 'w', encoding='utf-8') as f_loc:
        for loc, reg in mapa_territorial.items():
            f_loc.write(f"{loc},{reg}\n")

    # 2. Configuración de nombres y parámetros
    nombres_m = ["Juan", "Jose", "Luis", "Carlos", "Andres", "Diego", "Felipe", "Pablo"]
    nombres_f = ["Maria", "Ana", "Claudia", "Paola", "Francisca", "Camila", "Elena"]
    apellidos = ["Perez", "Gonzalez", "Munoz", "Rodriguez", "Soto", "Morales", "Silva", "Diaz"]
    calles = ["Av_Libertad", "Prat", "Condell", "Pajaritos", "Alameda", "O_Higgins"]
    
    localidades_lista = list(mapa_territorial.keys())
    # Pesos por localidad (densidad poblacional simulada)
    pesos_loc = [
        12, 14, 5, 4,              # V Región
        30, 12, 10, 8, 6,          # Metropolitana
        8, 5, 3, 3,                # VIII Región
        3, 1, 1,                   # I Región
        5, 4, 2,                   # II Región
        3, 2, 1,                   # III Región
        5, 5, 2,                   # IV Región
        5, 2, 1,                   # VI Región
        4, 3, 2,                   # VII Región
        3, 2, 1,                   # XIV Región
    ]

    with open(archivo_encuestas, 'w', encoding='utf-8') as f_enc:
        for id_h in range(1, num_hogares + 1):
            # --- GENERAR HOGAR (H) ---
            loc_actual = random.choices(localidades_lista, weights=pesos_loc)[0]
            dir_h = f"{random.choice(calles)}_{random.randint(10, 999)}"
            tipo_v = random.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
            # Bitmask: Luz(1), Agua(2), Internet(4)
            servicios = (1 if random.random() < 0.98 else 0) + \
                        (2 if random.random() < 0.95 else 0) + \
                        (4 if random.random() < 0.70 else 0)
            
            # Formato: H,ID,Direccion,TipoV,Servicios,Localidad
            f_enc.write(f"H,{id_h},{dir_h},{tipo_v},{servicios},{loc_actual}\n")

            # --- GENERAR HABITANTES (P) ---
            n_habitantes = max(1, np.random.poisson(3.2))
            ap_familia = random.choice(apellidos)

            for _ in range(n_habitantes):
                gen = random.choice(['M', 'F', 'N'])
                nom = random.choice(nombres_m if gen == 'M' else nombres_f if gen == 'F' else nombres_m + nombres_f)
                nombre_completo = f"{nom}_{ap_familia}_{random.choice(apellidos)}"
                
                edad = int(max(0, min(95, random.gauss(38, 18))))
                nivel_ed = random.choices(['B', 'M', 'T', 'U', 'P'], weights=[15, 40, 20, 20, 5])[0]
                
                # Ingresos con sesgo por nivel educativo y región
                if edad < 18:
                    sueldo = 0
                else:
                    base = 500000 if nivel_ed in ['B', 'M'] else 900000 if nivel_ed in ['T', 'U'] else 1600000
                    region_actual = mapa_territorial[loc_actual]
                    multiplicador_region = {
                        "Metropolitana": 1.40,
                        "II_Region": 1.30,   # minería
                        "V_Region": 1.10,
                        "IV_Region": 1.05,
                        "VI_Region": 1.00,
                        "VII_Region": 0.95,
                        "XIV_Region": 0.90,
                        "VIII_Region": 0.85,
                        "III_Region": 0.85,
                        "I_Region": 0.80,
                    }.get(region_actual, 1.0)
                    sueldo = int(max(350000, random.gauss(base * multiplicador_region, 300000)))

                f_enc.write(f"P,{nombre_completo},{edad},{gen},{nivel_ed},{sueldo}\n")

    print(f"✅ Archivos generados:\n - {archivo_localidades}\n - {archivo_encuestas} ({num_hogares} hogares)")

# Generar un dataset de prueba grande para el experimento O(n^2)

generar_datos_censo("encuestas_50.txt", "localidades.txt", 50)
generar_datos_censo("encuestas_500.txt", "localidades.txt", 500)

generar_datos_censo("encuestas_5000.txt", "localidades.txt", 5000)

generar_datos_censo("encuestas_50000.txt", "localidades.txt", 50000)

generar_datos_censo("encuestas_500000.txt", "localidades.txt", 500_000)

generar_datos_censo("encuestas_5000000.txt", "localidades.txt", 5_000_000)