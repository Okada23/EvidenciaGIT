import datetime
from tabulate import tabulate

salas_dict = {
    "1": ("Sala A", 150),
    "2": ("Sala B", 200),
    "3": ("Sala C", 250),
    "4": ("Sala D", 300),
    "5": ("Sala E", 50)
}
contador_salas = 6

turnos = {
    "1": "Matutino",
    "2": "Vespertino",
    "3": "Nocturno"
}

reservas_dict = {}
contador_reservas = 1

clientes_dict = {}
contador_clientes = 1

def lista_clientes_ordenados(clientes_dict):
    if not clientes_dict:
        print("\nNo hay clientes registrados aún.")
        return None
    
    while True:
        clientes_ordenados = []

        for clave, (nombre, apellido) in clientes_dict.items():
            clientes_ordenados.append((apellido, nombre, clave))
        clientes_ordenados.sort()

        print("\n**LISTA DE CLIENTES")
        for apellido_cliente, nombre_cliente, clave in clientes_ordenados:
            print(f"{clave} - {apellido_cliente}, {nombre_cliente}")

        respuesta_clave = input("Ingrese la clave del cliente (X para cancelar): ").strip()

        if respuesta_clave.upper() == "X":
            print("\nOperación cancelada.")
            return None

        if respuesta_clave in clientes_dict:
            nombre, apellido = clientes_dict[respuesta_clave]
            print(f"Cliente seleccionado: {apellido}, {nombre}")
            return respuesta_clave, nombre, apellido
        else:
            print("\nNo existe esa clave. Intente de nuevo.")

def seleccionar_fecha_reservacion():
    while True:
        fecha = input("Ingrese la fecha de la reserva (dd/mm/aaaa): ").strip()

        try:
            fecha_reserva = datetime.datetime.strptime(fecha, "%d/%m/%Y").date()
            fecha_minima = datetime.date.today() + datetime.timedelta(days=2)
            if fecha_reserva < fecha_minima:
                print(f"La fecha debe ser al menos dos días posteriores a hoy ({datetime.date.today()}).")
                continue
            return fecha_reserva
        
        except ValueError:
            print("\nFormato de fecha incorrecto. Debería ser dd/mm/aaaa.")

def seleccionar_sala_y_turno(salas_dict, reservas_dict, fecha_reserva, turnos):
    while True:
        print("\n*** TURNOS DISPONIBLES ***")
        for clave_turno, nombre_turno in turnos.items():
            print(f"{clave_turno} - {nombre_turno}")

        respuesta_turno = input("Ingrese la clave del turno: ").strip()

        if respuesta_turno in turnos: 
            turno_seleccionado = turnos[respuesta_turno]
            print(f"Turno seleccionado: {turno_seleccionado}")

            print(f"\n**SALAS DISPONIBLES el {fecha_reserva} en turno {turno_seleccionado}")
            salas_disponibles = []

            for clave_sala, (nombre_sala, cupo) in salas_dict.items():
                if (fecha_reserva, clave_sala, turno_seleccionado) not in reservas_dict:
                    salas_disponibles.append(clave_sala)
                    print(f"{clave_sala} - Sala: {nombre_sala} ({cupo} personas)")

            if not salas_disponibles:
                print("\nNo hay salas disponibles en esa fecha y turno.")
            break
        else:
            print("\nOpción inválida. Intente de nuevo.")

    while True:
        respuesta_sala = input("Ingrese la clave de la sala: ").strip()
        if respuesta_sala in salas_disponibles:
            return respuesta_sala, turno_seleccionado
        else:
            print("\nClave de sala inválida. Intente de nuevo.")

def asignar_nombre_evento():
    while True:
        nombre_evento = input("Ingrese el nombre del evento: ").strip().capitalize()
        while "  " in nombre_evento:
            nombre_evento = nombre_evento.replace("  ", "")
        if nombre_evento == "":
            print("\nEl nombre del evento es obligatorio y no puede dejarse vacío.")
        else:
            return nombre_evento

def registrar_reserva_de_sala(clientes_dict, salas_dict, reservas_dict, contador_reservas, turnos):
    resultado = lista_clientes_ordenados(clientes_dict)
    if not resultado:
        return contador_reservas
    
    respuesta_clave, nombre, apellido = resultado

    fecha_reserva = seleccionar_fecha_reservacion()
    respuesta_sala, turno_seleccionado = seleccionar_sala_y_turno(salas_dict, reservas_dict, fecha_reserva, turnos)
    nombre_evento_final = asignar_nombre_evento()

    folio = f"{contador_reservas:03}"
    contador_reservas += 1

    reservas_dict[(fecha_reserva, respuesta_sala, turno_seleccionado)] = {
        "Folio": folio,
        "Cliente": respuesta_clave,
        "Evento": nombre_evento_final
    }

    print(f"\n**** RESERVA CONFIRMADA ***")
    print(f"Folio: {folio}")
    print(f"Cliente: {respuesta_clave} ({apellido}, {nombre})")
    print(f"Sala: {respuesta_sala} ({salas_dict[respuesta_sala][0]})")
    print(f"Fecha: {fecha_reserva}")
    print(f"Turno: {turno_seleccionado}")
    print(f"Evento: {nombre_evento_final}")

    return contador_reservas

def editar_nombre_de_evento(reservas_dict):
    if not reservas_dict:
        print("\nNo hay reservas registradas.")
        return
    
    while True:
        fecha1_str = input("Ingrese la primera fecha (dd/mm/aaaa): ").strip()
        try:
            fecha1 = datetime.datetime.strptime(fecha1_str, "%d/%m/%Y").date()
            break
        except ValueError:
            print("\nFormato incorrecto. Intente de nuevo.")

    while True:
        fecha2_str = input("Ingrese la segunda fecha (dd/mm/aaaa): ").strip()
        try:
            fecha2 = datetime.datetime.strptime(fecha2_str, "%d/%m/%Y").date()
            if fecha2 <= fecha1:
                print("\nLa segunda fecha debe ser posterior a la primera. Intente de nuevo.")
                continue
            break
        except ValueError:
            print("\nFormato incorrecto. Intente de nuevo.")

    eventos_filtrados = []
    for clave, datos in reservas_dict.items():
        fecha_evento = clave[0]
        if fecha1 <= fecha_evento <= fecha2:
            eventos_filtrados.append([datos["Folio"], datos["Evento"], fecha_evento.strftime("%d/%m/%Y")])

    if not eventos_filtrados:
        print("\nNo hay eventos en el rango de fechas seleccionado.")
        return

    headers = ["Folio", "Nombre del Evento", "Fecha"]
    print(tabulate(eventos_filtrados, headers=headers, tablefmt="grid"))

    while True:
        folio_input = input("Ingrese el folio del evento a modificar (X para cancelar): ").strip()
        if folio_input.upper() == "X":
            print("\nOperación cancelada.")
            return
        
        encontrado = False
        for clave, datos in reservas_dict.items():
            if datos["Folio"] == folio_input:
                encontrado = True
                while True:
                    nuevo_nombre = input("Ingrese el nuevo nombre del evento: ").strip()
                    if nuevo_nombre == "":
                        print("El nombre no puede estar vacío. Intente de nuevo.")
                        continue
                    reservas_dict[clave]["Evento"] = nuevo_nombre
                    print(f"Evento actualizado: {nuevo_nombre}")
                    return
        if not encontrado:
            print("\nFolio no válido. Intente de nuevo.")


def consultar_reservas_por_fecha(reservas_dict, salas_dict):
    if not reservas_dict:
        print("\nNo hay reservas registradas.")
        return
    
    fecha_str = input("Ingrese la fecha a consultar (dd/mm/aaaa): ").strip()
    try:
        fecha_consulta = datetime.datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except ValueError:
        print("\nFormato incorrecto.")
        return

    filas = []
    for clave, datos in reservas_dict.items():
        if clave[0] == fecha_consulta:
            sala_nombre = f"{clave[1]} ({salas_dict[clave[1]][0]})"
            filas.append([datos["Folio"], datos["Evento"], sala_nombre, clave[2], datos["Cliente"]])

    if not filas:
        print("\nNo hay reservas para esa fecha.")
        return
    
    headers = ["Folio", "Evento", "Sala", "Turno", "Cliente"]
    print(tabulate(filas, headers=headers, tablefmt="grid"))


def registrar_cliente(clientes_dict, contador_clientes):
    while True:
        nombre_cliente = input("Ingrese el nombre del cliente: ").strip()
        if nombre_cliente.replace(" ", "").isalpha():
            break
        else:
            print("Nombre inválido: no se aceptan números ni caracteres especiales.")

    while True:
        apellido_cliente = input("Ingrese el apellido del cliente: ").strip()
        if apellido_cliente.replace(" ", "").isalpha():
            break
        else:
            print("Apellido inválido: no se aceptan números ni caracteres especiales.")

    clave_cliente = f"{contador_clientes:03}"
    clientes_dict[clave_cliente] = (nombre_cliente.upper(), apellido_cliente.upper())
    print(f"Cliente registrado con clave: {clave_cliente}")
    contador_clientes += 1
    return contador_clientes, clave_cliente


def registrar_sala(salas_dict, contador_salas):
    while True:
        nombre_sala = input("Ingrese el nombre de la nueva sala: ").strip()

        if nombre_sala.isalpha():
            break
        else:
            print("\nEl nombre de la sala solo puede contener letras.")

    while True:
        try:
            cupo = int(input("Ingrese el cupo de la sala: "))
            if cupo > 0:
                break
            else:
                print("\nEl cupo debe ser un numero entero POSITIVO.")
        except ValueError:
            print("\nEl cupo no admite decimales.")

    clave_salas = f"{contador_salas:02}"
    salas_dict[clave_salas] = (nombre_sala.upper(), cupo)
    contador_salas += 1
    
    print(f"Se registro la sala con la clave: {clave_salas}")
    return contador_salas

def main():
    global contador_reservas, contador_clientes, contador_salas
    while True:
        print("\n*MENU PRINCIPAL")
        print("1. Registrar reserva de una sala")
        print("2. Editar nombre de evento")
        print("3. Consultar reservas existentes")
        print("4. Registrar cliente")
        print("5. Registrar sala")
        print("6. Salir")
        try:
            opcion = int(input("Seleccione una opcion: "))
            if opcion == 1:
                contador_reservas = registrar_reserva_de_sala(clientes_dict, salas_dict, reservas_dict, contador_reservas, turnos)
            elif opcion == 2:
                editar_nombre_de_evento(reservas_dict)
            elif opcion == 3:
                consultar_reservas_por_fecha(reservas_dict, salas_dict)
            elif opcion == 4:
                contador_clientes = registrar_cliente(clientes_dict, contador_clientes)
            elif opcion == 5:
                contador_salas = registrar_sala(salas_dict, contador_salas)
            elif opcion == 6:
                break
            else:
                print("\nDebe ingresar un numero del 1 al 6.")
        except ValueError:
            print("\nSolo se aceptan números enteros del 1 al 6.")

if __name__ == "__main__":
    main()