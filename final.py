import csv, logging
from tabulate import tabulate
from decimal import Decimal

def main():

    imprimir_separador()
    print("SISTEMA DE GESTIÓN DE FACTURACIÓN")
    imprimir_separador()

    while True:

        print("\nElija una opción: \n\t1. Búsqueda de cliente por nombre\n\t2. Búsqueda total de usuarios por empresa\n\t3. Búsqueda de facturación en viajes por empresa\n\t4. Búsqueda de viajes por documento\n\t5. Salir")

        loguear("Menú")
        opcion = int(input(""))

        if opcion == 5:
            loguear("Salir")
            exit()
        elif opcion == 1:
            loguear("Búsqueda de cliente por nombre")
            buscar_cliente_por_nombre()
        elif opcion == 2:
            loguear("Búsqueda total de usuarios por empresa")
            buscar_usuarios_por_empresa()
        elif opcion == 3:
            loguear("Búsqueda de facturación en viajes por empresa")
            total_dinero_en_viajes_por_empresa()
        elif opcion == 4:
            loguear("Búsqueda de viajes por documento")
            buscar_cantidad_total_viajes_y_monto_por_documento()
        else:
            print("Ingrese una opcion valida. Intente nuevamente.")

#OPCIÓN 1: Permitir la búsqueda de un cliente por su nombre (parcial o total), mostrando todos sus datos.
def buscar_cliente_por_nombre():

    nombre_archivo_clientes = input("\nIngrese el nombre del archivo de clientes: ")

    if validar_csv(nombre_archivo_clientes, ""):

        nombre_cliente = input("\nIngrese el nombre del cliente: ")

        imprimir_separador()
        imprimir_datos_cliente(nombre_archivo_clientes, nombre_cliente, "", "")
        imprimir_separador()

#OPCIÓN 2: Permitir obtener el total de usuarios por empresa, y todos sus datos.
def buscar_usuarios_por_empresa():

    nombre_archivo_clientes = input("\nIngrese el nombre del archivo de clientes: ")

    if validar_csv(nombre_archivo_clientes, ""):

        nombre_empresa = input("\nIngrese el nombre de la empresa: ")

        imprimir_separador()
        total_usuarios_por_empresa(nombre_archivo_clientes, nombre_empresa)
        imprimir_separador()
        imprimir_datos_cliente(nombre_archivo_clientes, "", nombre_empresa, "")
        imprimir_separador()

#Imprimo los datos del cliente segun el parametro pasado (cliente, empresa o documento)
def imprimir_datos_cliente(nombre_archivo_clientes, nombre_cliente, nombre_empresa, documento_cliente):

    try:
        with open(nombre_archivo_clientes, "r", newline="") as file_clientes:

            planilla_clientes = csv.reader(file_clientes)
            next(planilla_clientes)

            for linea in planilla_clientes:
                if nombre_cliente != "" and nombre_cliente in linea[0] or nombre_empresa == linea[5] or documento_cliente == linea[2]:
                    print(linea)
    except IOError:
        print("\nOcurrió un error con el archivo.")

def total_usuarios_por_empresa(nombre_archivo_clientes, nombre_empresa):

    cant_usuarios = 0

    try:
        with open(nombre_archivo_clientes, "r", newline="") as file_clientes:

            planilla_clientes = csv.reader(file_clientes)
            next(planilla_clientes)

            for linea in planilla_clientes:
                if nombre_empresa == linea[5]:
                    cant_usuarios += 1

        print(f"Empresa: {nombre_empresa}\nTotal Usuarios: {cant_usuarios}")
    except IOError:
        print("\nOcurrió un error con el archivo.")

#OPCIÓN 3: Permitir obtener el total de dinero en viajes por nombre de empresa.
def total_dinero_en_viajes_por_empresa():

    nombre_archivo_clientes = input("\nIngrese el nombre del archivo de clientes: ")
    nombre_archivo_viajes = input("\nIngrese el nombre del archivo de viajes: ")

    if validar_csv(nombre_archivo_clientes, nombre_archivo_viajes):

        nombre_empresa = input("\nIngrese el nombre de la empresa: ")
        imprimir_separador()
        imprimir_total_dinero_viajes(nombre_archivo_clientes, nombre_archivo_viajes, nombre_empresa)
        imprimir_separador()

#Imprimo el monto total de dinero en viajes segun el nombre de la empresa
def imprimir_total_dinero_viajes(nombre_archivo_clientes, nombre_archivo_viajes, nombre_empresa):

    monto_total = 0
    lista_clientes = []

    try:
        with open(nombre_archivo_clientes, "r", newline="") as file_clientes:

            planilla_clientes = csv.reader(file_clientes)
            next(planilla_clientes)

            for cliente in planilla_clientes:

                if nombre_empresa == cliente[5]:
                    lista_clientes.append(cliente[2])
            
            with open(nombre_archivo_viajes, "r", newline="") as file_viajes:

                planilla_viajes = csv.reader(file_viajes)
                next(planilla_viajes)

                #Por cada viaje, si el documento coincide con alguno de la lista de documentos, acumulo el monto
                for viaje in planilla_viajes:
                    for cliente in lista_clientes:
                        if cliente == viaje[0]:
                            monto_total = monto_total + Decimal(viaje[2])

        print(f"{nombre_empresa}: ${monto_total}")
    except IOError:
        print("\nOcurrió un error con el archivo.")

#OPCIÓN 4: Permitir obtener cantidad total de viajes realizados y monto total por documento, y mostrar los datos del empleado y los viajes.
def buscar_cantidad_total_viajes_y_monto_por_documento():
    
    nombre_archivo_clientes = input("\nIngrese el nombre del archivo de clientes: ")
    nombre_archivo_viajes = input("\nIngrese el nombre del archivo de viajes: ")

    if validar_csv(nombre_archivo_clientes, nombre_archivo_viajes):

        documento = input("\nIngrese el número de documento: ")

        imprimir_separador()
        print(f"Documento: {documento}")
        imprimir_separador()
        imprimir_datos_cliente(nombre_archivo_clientes, "", "", documento)
        imprimir_separador()
        imprimir_viajes(nombre_archivo_viajes, documento)

#Imprimo el total y monto de viajes segun el documento
def imprimir_viajes(nombre_archivo_viajes, documento):

    cant_viajes = 0
    monto = 0
    lista_viajes = []

    try:
        with open(nombre_archivo_viajes, "r", newline="") as file:

            planilla_viajes = csv.reader(file)
            next(planilla_viajes)

            for viaje in planilla_viajes:
                if viaje[0] == documento:
                    cant_viajes += 1
                    monto += Decimal(viaje[2])
                    lista_viajes.append(viaje)

            print(f"Total viajes: {cant_viajes}, Monto: ${monto}")
            imprimir_separador()
            for viaje in lista_viajes:
                print(viaje)
    except IOError:
        print("\nOcurrió un error con el archivo.")

#Metodo que valida el csv a cargar
def validar_csv(nombre_archivo_clientes, nombre_archivo_viajes):

    es_valido = False

    try:
        if nombre_archivo_clientes != "":
            with open(nombre_archivo_clientes, "r", newline="") as file_clientes:

                planilla_clientes = csv.reader(file_clientes)
                next(planilla_clientes)

                es_valido = validar_csv_clientes(planilla_clientes)

        if nombre_archivo_viajes != "":
            with open(nombre_archivo_viajes, "r", newline="") as file_viajes:

                planilla_viajes = csv.reader(file_viajes)
                next(planilla_viajes)

                es_valido = validar_csv_viajes(planilla_viajes)

        return es_valido
    except IOError:
        print("\nOcurrió un error con el archivo.")

#Metodo particular para validar csv de clientes
def validar_csv_clientes(planilla_clientes):

    es_valido = False

    for cliente in planilla_clientes:
        documento = cliente[2]
        email = cliente[4]

        if validar_documento(documento) and "@" in email and "." in email:
            es_valido = True

    return es_valido

#Metodo particular para validar csv de viajes
def validar_csv_viajes(planilla_viajes):

    es_valido = False

    for viaje in planilla_viajes:

        precio = viaje[2]

        if "." in str(precio):
            decimales = str(precio).split(".")[-1]
            if validar_documento(viaje[0]) and viaje[1] != "" and len(decimales) == 2:
                es_valido = True

    return es_valido
                    

def validar_documento(documento):
    
    if len(documento) == 7 or len(documento) == 8:
        return True
    else:
        print("El documento {documento} contiene {len(documento)} caracteres. Debe contener entre 7 y 8.")
        return False

#Metodo que guarda en log cada accion pasada por parametro
def loguear(accion):
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename='acciones.log',
            filemode='w')
    logging.info(accion)

def imprimir_separador():
    print("-----------------------------------------------------------------------------")

main()
