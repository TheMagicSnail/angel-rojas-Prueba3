import numpy
from typing import Tuple, List
from random import randint

class Lote:
    """Representa un lote que se puede reservar."""
    def __init__(self, nro_lote : int, tamano : int, precio: int, disponibilidad: bool = True):
        self.nro_lote = nro_lote
        self.tamano = tamano
        self.precio = precio
        self.disponibilidad = disponibilidad

    def info(self) -> str:
        """Informacion completa sobre este lote."""
        string = f"Lote nro: {self.nro_lote}\nTamano: {self.tamano} hectareas\nPrecio: {self.precio}\nDisponibilidad: "
        string += "Disponible" if self.disponibilidad else "No disponible"
        return string

    def __str__(self):
        """Representacion visual de un lote."""
        return "[ ]" if self.disponibilidad else "[X]"

class SetDeLotes:
    """Representa el terreno completo que es loteado."""
    def __init__(self, h, w):
        shape = [[None]*w]*h
        self.lotes = numpy.array(shape, dtype=Lote)

    def asignar_lote(self, i : int, j : int, lote: Lote):
        self.lotes[i,j] = lote
    
    def __str__(self):
        """Permite mostrar la disponibilidad de todos los lotes contenidos."""
        string = ""
        for fila in self.lotes:
            for lote in fila:
                string += str(lote)
            string += "\n"
        return string
        

class Cliente:
    """Representa un cliente que compra lotes."""
    def __init__(self, rut : str, nombre : str, telefono : int, email : str):
        self.rut = rut
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def iguales(self, other) -> bool:
        """Permite comparar dos clientes."""
        return self.rut == other.rut and self.nombre == other.nombre and self.telefono == other.telefono and self.email == other.email

    def __str__(self):
        return f"{self.rut}\n{self.nombre}\n{self.telefono}\n{self.email}"

def pedir_respuesta(mensaje : str, valor_min : int, valor_max : int) -> int:
    """Utiliza un mensaje para pedir un numero entre min y max al usuario."""
    valor = None
    while valor == None:
        valor = input(mensaje)
        try:
            valor = int(valor)
            if valor < valor_min or valor > valor_max:
                print(f"Su respuesta debe estar entre {valor_min} y {valor_max}")
                valor = None
        except:
            print(f"\"{valor}\" es invalido. Debe ingresar un numero entero.")
            valor = None
    return valor

def crear_usuario() -> Cliente:
    """No es requerido validar los datos de usuario, por lo que simplemente los pedimos."""
    return Cliente(
        input("Ingrese su RUT: "), 
        input("Ingrese su nombre completo: "), 
        input("Ingrese su telefono: "), 
        input("Ingrese su direccion de correo electronico: ")
    )

def generar_lotes() -> Tuple[int, int, SetDeLotes]:
    # En el enunciado no se especifica cuantos lotes deben haber ni que datos deben contener...
    # Asi que los vamos a generar aleatoriamente.

    # Generacion de terreno
    H = randint(3, 5)
    W = randint(3, 5)
    lotes = SetDeLotes(H, W)

    # Generacion de lotes, lote por lote
    for i in range(H):
        for j in range(W):
            tamano = randint(1, 20) # Hectareas
            costo = randint(1000000, 5000000) * tamano # pesos
            lote = Lote(j + i * H, tamano, costo)
            lotes.asignar_lote(i, j, lote)
    return (H, W, lotes)

def seleccionar_lote(lotes : SetDeLotes, H : int, W : int, clientes : List[Cliente]) -> Lote:
    """Permite seleccionar y reservar un lote."""
    cliente = crear_usuario()
    lote_seleccionado = None
    while lote_seleccionado is None:
        i = pedir_respuesta(str(lotes) + "\nIngrese fila: ", 0, H -1)
        j = pedir_respuesta(str(lotes) + "\nIngrese columna: ", 0, W -1)
        lote_seleccionado = lotes.lotes[i, j]
        # Opcion para escoger otro lote si el actual ya esta seleccionado
        if not lote_seleccionado.disponibilidad:
            mensaje =  "El lote seleccionado no esta disponible. Desea escoger otro lote?\n"
            mensaje += "1- Si\n"
            mensaje += "2- No\n"
            respuesta = pedir_respuesta(mensaje, 1, 2)
            if respuesta == 2:
                return lote_seleccionado
            lote_seleccionado = None
    
    # Actualizacion de disponibilidad de lote.
    lote_seleccionado.disponibilidad = False
    # Agregar cliente solo si no se encuentra en la lista de clientes.
    contenido_en_clientes = False
    for c in clientes:
        if c.iguales(cliente):
            contenido_en_clientes = True
            break
    if not contenido_en_clientes:
        clientes.append(cliente)
    # Mensaje de salida
    print(f"Su lote (nro: {lote_seleccionado.nro_lote}) ha sido reservado.")
    return lote_seleccionado

def main():
    # Inicializacion de datos
    H, W, lotes = generar_lotes()
    clientes : List[Cliente] = []
    seleccionado = None

    # Bucle principal
    while True:
        mensaje =  "Seleccione una de las siguientes opciones:\n"
        mensaje += "1- Ver disponibilidad\n"
        mensaje += "2- Seleccionar un lote\n"
        mensaje += "3- Ver detalles de seleccion\n"
        mensaje += "4- Ver clientes\n"
        mensaje += "5- Salir\n"
        mensaje += "Opcion: "
        opcion = pedir_respuesta(mensaje, 1, 5)
        
        if opcion == 1:
            print("La disponibilidad es la siguiente: ")
            print(lotes)
        elif opcion == 2:
            seleccionado = seleccionar_lote(lotes, H, W, clientes)
        elif opcion == 3:
            if seleccionado is None:
                print("Aun no hay seleccion.")
            else:
                print(seleccionado.info())
        elif opcion == 4:
            print("---------------------------")
            for cliente in clientes:
                print(cliente)
                print("---------------------------")
        elif opcion == 5:
            break
    print("Muchas gracias por utilizar los servicios LoteosDuoc")
    input("Presione ENTER para salir")

# Llamada a funcion principal
main()