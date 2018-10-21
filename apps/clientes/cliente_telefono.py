from enum import Enum


class ClienteTelefonoTipo(Enum):
    fijo = 1
    movil = 2


class ClienteTelefono(object):

    def __init__(self, tipo, numero, cliente, id=None):
        self.tipo = tipo
        self.numero = numero
        self.id = id
        self.cliente = cliente
