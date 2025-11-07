# TPI - Gestión de Países en CSV 
import csv
import re # Expresiones regulares
from pathlib import Path

# Utilidades generales

def normalizar_nombre(texto): # Normaliza nombres (título, sin espacios extras).
    return " ".join(texto.strip().split()).title()

def limpiar_separadores(texto): # Elimina puntos y comas como separadores de miles.
    return str(texto).replace(".", "").replace(",", "")

def es_entero_no_negativo(texto): # Valida entero >= 0 
    if texto is None:
        return False
    t = limpiar_separadores(str(texto)).strip() # Quitar espacios y separadores
    return t.isdigit() # Solo dígitos

def convertir_entero_no_negativo(texto):# Convierte a entero >= 0, devolviendo (ok, valor).
    if not es_entero_no_negativo(texto): 
        return (False, 0)  
    t = int(limpiar_separadores(str(texto).strip())) # Convertir a entero
    return (True, t) 

# Patrón para validar nombres (letras con acentos/ñ, espacios, guiones y apóstrofes internos).
PATRON_NOMBRE = r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ '\-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*" 

def nombre_valido(texto):# Valido que el nombre sea legible, sin símbolos raros, y con longitud razonable.
    if texto is None:
        return False
    t = " ".join(str(texto).strip().split()) # Normalizar espacios
    if len(t) < 2 or len(t) > 60: 
        return False
    return re.fullmatch(PATRON_NOMBRE, t) is not None 

# Entrada/Salida CSV

def cargar_csv(ruta):  # Carga el CSV, valida y devuelve una lista de diccionarios (países).
    paises = []
    if not ruta.exists():
        return paises

    with ruta.open("r", encoding="utf-8", newline="") as f: # Abre el archivo CSV para lectura
        lector = csv.DictReader(f) # Crea un lector CSV que interpreta cada fila
        for _num_linea, fila in enumerate(lector, start=2): # comienza en 2 (después del encabezado)
            nombre = (fila.get("nombre", "") or "").strip() # Extrae y limpia campos
            poblacion_txt = (fila.get("poblacion", "") or "").strip()
            superficie_txt = (fila.get("superficie", "") or "").strip()
            continente = (fila.get("continente", "") or "").strip()

            # Validación de vacíos
            if not (nombre and poblacion_txt and superficie_txt and continente):
                continue

            # Valido formato de nombre y continente
            if not nombre_valido(nombre) or not nombre_valido(continente):
                continue

            ok_pob, poblacion = convertir_entero_no_negativo(poblacion_txt)
            ok_sup, superficie = convertir_entero_no_negativo(superficie_txt)

            if not ok_pob or not ok_sup:
                continue
            if superficie == 0:  # superficie debe ser > 0
                continue

            paises.append({
                "nombre": normalizar_nombre(nombre),
                "poblacion": poblacion,
                "superficie": superficie,
                "continente": normalizar_nombre(continente),
            })
    return paises

def guardar_csv(ruta, paises):  # Guarda la lista de países en el CSV.
    campos = ["nombre", "poblacion", "superficie", "continente"]  # Encabezados
    ruta.parent.mkdir(parents=True, exist_ok=True)  # Asegura carpeta
    with ruta.open("w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for p in paises:
            # Asegurar tipos enteros al escribir
            ok_pob, pob = convertir_entero_no_negativo(p.get("poblacion", "0"))
            ok_sup, sup = convertir_entero_no_negativo(p.get("superficie", "0"))
            if not ok_pob or not ok_sup or sup == 0:
                continue
            escritor.writerow({
                "nombre": p.get("nombre", ""),
                "poblacion": pob,
                "superficie": sup,
                "continente": p.get("continente", ""),
            })

# Núcleo de operaciones

def buscar_por_nombre(paises, patron):
    patron = patron.lower().strip()
    resultado = []
    for p in paises:
        if patron in p["nombre"].lower():
            resultado.append(p)
    return resultado

def existe_nombre(paises, nombre):
    objetivo = nombre.lower().strip()
    for p in paises:
        if p["nombre"].lower() == objetivo:
            return True
    return False

def agregar_pais(paises, nombre, poblacion, superficie, continente):
    nombre_n = normalizar_nombre(nombre)
    continente_n = normalizar_nombre(continente)

    if not (nombre_n and continente_n):
        return "Error: nombre y continente no pueden estar vacíos."
    if not nombre_valido(nombre_n):
        return "Error: el nombre del país contiene caracteres no permitidos."
    if not nombre_valido(continente_n):
        return "Error: el nombre del continente contiene caracteres no permitidos."
    if poblacion < 0 or superficie <= 0:
        return "Error: población debe ser ≥ 0 y superficie > 0."
    if existe_nombre(paises, nombre_n):
        return "Error: ya existe un país con ese nombre."

    paises.append({
        "nombre": nombre_n,
        "poblacion": int(poblacion),
        "superficie": int(superficie),
        "continente": continente_n,
    })
    return None

def actualizar_pais(paises, nombre, nueva_poblacion, nueva_superficie):
    objetivo = nombre.lower().strip()
    for p in paises:
        if p["nombre"].lower() == objetivo:
            if nueva_poblacion is not None:
                if nueva_poblacion < 0:
                    return "Error: la población debe ser ≥ 0."
                p["poblacion"] = int(nueva_poblacion)
            if nueva_superficie is not None:
                if nueva_superficie <= 0:
                    return "Error: la superficie debe ser > 0."
                p["superficie"] = int(nueva_superficie)
            return None
    return "Error: país no encontrado."

# Filtros y ordenamientos

def filtrar_por_continente(paises, continente):
    c = continente.lower().strip()
    resultado = []
    for p in paises:
        if p["continente"].lower() == c:
            resultado.append(p)
    return resultado

def filtrar_por_rango_poblacion(paises, minimo, maximo):
    resultado = []
    for p in paises:
        ok_min = (minimo is None) or (p["poblacion"] >= minimo)
        ok_max = (maximo is None) or (p["poblacion"] <= maximo)
        if ok_min and ok_max:
            resultado.append(p)
    return resultado

def filtrar_por_rango_superficie(paises, minimo, maximo):
    resultado = []
    for p in paises:
        ok_min = (minimo is None) or (p["superficie"] >= minimo)
        ok_max = (maximo is None) or (p["superficie"] <= maximo)
        if ok_min and ok_max:
            resultado.append(p)
    return resultado

# Claves de orden
def clave_nombre(p):
    return p["nombre"]

def clave_poblacion(p):
    return p["poblacion"]

def clave_superficie(p):
    return p["superficie"]

def ordenar_paises(paises, por, descendente=False):
    # Elijo la función criterio según el campo pedido.
    clave_str = por.lower().strip()
    if clave_str == "poblacion":
        criterio_orden = clave_poblacion
    elif clave_str == "superficie":
        criterio_orden = clave_superficie
    else:
        criterio_orden = clave_nombre  # por defecto
    return sorted(paises, key=criterio_orden, reverse=descendente)

# Estadísticas

def mayor_menor_poblacion(paises):
    if not paises:
        return ({}, {})
    mayor = paises[0]
    menor = paises[0]
    for p in paises[1:]:
        if p["poblacion"] > mayor["poblacion"]:
            mayor = p
        if p["poblacion"] < menor["poblacion"]:
            menor = p
    return mayor, menor

def promedio_poblacion(paises):
    if not paises:
        return 0.0
    total = 0
    for p in paises:
        total += p["poblacion"]
    return total / len(paises)

def promedio_superficie(paises):
    if not paises:
        return 0.0
    total = 0
    for p in paises:
        total += p["superficie"]
    return total / len(paises)

def cantidad_por_continente(paises):
    conteo = {}
    for p in paises:
        c = p["continente"]
        if c in conteo:
            conteo[c] += 1
        else:
            conteo[c] = 1
    return conteo

# Interfaz de consola

def pedir_entero_opcional(mensaje):
    texto = input(mensaje).strip()
    if texto == "":
        return None
    ok, valor = convertir_entero_no_negativo(texto)
    if not ok:
        print("Valor inválido. Deja vacío para omitir o ingresa un entero ≥ 0.")
        return None
    return valor

def imprimir_lista(paises):
    if not paises:
        print("(Sin resultados)")
        return
    for p in paises:
        pob = str(p["poblacion"])
        sup = str(p["superficie"])
        print(f"- {p['nombre']} | Población: {pob} | Superficie: {sup} km² | {p['continente']}")

def menu():
    # Ruta al CSV (relativa al script)
    csv_ruta = Path(__file__).resolve().parent / "datos" / "paises.csv"

    paises = cargar_csv(csv_ruta)
    print("\nSistema de Gestión de Países — CSV:", csv_ruta)

    while True:
        print("""
======== MENÚ ========
1) Agregar país
2) Actualizar población/superficie
3) Buscar país por nombre (parcial o exacto)
4) Filtrar países
5) Ordenar países
6) Mostrar estadísticas
0) Salir
======================
""")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre: ").strip()
            poblacion_txt = input("Población (entero ≥ 0): ").strip()
            superficie_txt = input("Superficie km² (entero > 0): ").strip()
            continente = input("Continente: ").strip()

            if not (nombre and poblacion_txt and superficie_txt and continente):
                print("Error: no se permiten campos vacíos.")
                continue

            if not nombre_valido(nombre) or not nombre_valido(continente):
                print("Error: nombre de país/continente con caracteres no permitidos.")
                continue

            ok_pob, pob = convertir_entero_no_negativo(poblacion_txt)
            ok_sup, sup = convertir_entero_no_negativo(superficie_txt)
            if not ok_pob or not ok_sup or sup == 0:
                print("Error: población/superficie inválidas (enteros; puntos y comas aceptados).")
                continue

            error = agregar_pais(paises, nombre, pob, sup, continente)
            if error:
                print("→", error)
            else:
                guardar_csv(csv_ruta, paises)
                print("País agregado correctamente.")

        elif opcion == "2":
            nombre = input("Nombre del país a actualizar: ").strip()
            nueva_poblacion = pedir_entero_opcional("Nueva población (Enter para no cambiar): ")
            nueva_superficie = pedir_entero_opcional("Nueva superficie (Enter para no cambiar): ")

            error = actualizar_pais(paises, nombre, nueva_poblacion, nueva_superficie)
            if error: 
                print("", error) 
            else:
                guardar_csv(csv_ruta, paises)
                print("Datos actualizados.")

        elif opcion == "3":
            patron = input("Nombre o parte del nombre: ").strip()
            resultados = buscar_por_nombre(paises, patron)
            imprimir_lista(resultados)

        elif opcion == "4":
            print("a) Por continente | b) Rango población | c) Rango superficie")
            sub = input("Elegí a/b/c: ").strip().lower()
            if sub == "a":
                c = input("Continente: ").strip()
                imprimir_lista(filtrar_por_continente(paises, c))
            elif sub == "b":
                minimo = pedir_entero_opcional("Población mínima: ")
                maximo = pedir_entero_opcional("Población máxima: ")
                if minimo is not None and maximo is not None and minimo > maximo:
                    print("Rango inválido (mínimo mayor que máximo)")
                else:
                    imprimir_lista(filtrar_por_rango_poblacion(paises, minimo, maximo))
            elif sub == "c":
                minimo = pedir_entero_opcional("Superficie mínima: ")
                maximo = pedir_entero_opcional("Superficie máxima: ")
                if minimo is not None and maximo is not None and minimo > maximo:
                    print("Rango inválido (mínimo mayor que máximo)")
                else:
                    imprimir_lista(filtrar_por_rango_superficie(paises, minimo, maximo))
            else:
                print("Opción inválida.")

        elif opcion == "5":
            print("Ordenar por: a) nombre  b) población  c) superficie")
            sub = input("Elegí a/b/c: ").strip().lower()
            if sub == "b":
                clave = "poblacion"
            elif sub == "c":
                clave = "superficie"
            else:
                clave = "nombre"
            descendente = input("Descendente? (s/n): ").strip().lower() == "s"
            ordenados = ordenar_paises(paises, clave, descendente=descendente)
            imprimir_lista(ordenados)

        elif opcion == "6":
            mayor, menor = mayor_menor_poblacion(paises)
            if not mayor:
                print("No hay datos.")
                continue
            print(f"Mayor población: {mayor['nombre']} ({mayor['poblacion']:,})")
            print(f"Menor población: {menor['nombre']} ({menor['poblacion']:,})")
            print(f"Promedio de población: {promedio_poblacion(paises):,.2f}")
            print(f"Promedio de superficie: {promedio_superficie(paises):,.2f} km²")
            conteo = cantidad_por_continente(paises)
            print("Países por continente:")
            for cont in conteo:
                print(f"  - {cont}: {conteo[cont]}")

        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
