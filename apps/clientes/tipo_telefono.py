from apps.clientes.cliente_telefono import ClienteTelefonoTipo
from apps.common.result import Result
from apps.common.value_object import ValueObject


class TipoTelefono(ValueObject):

    def __init__(self, value):
        if not value:
            raise  ValueError('El tipo del teléfono es obligatorio')
        if value not in [x.value for x in ClienteTelefonoTipo]:
            raise ValueError('El tipo del teléfono no es válido')

    @classmethod
    def create(cls, tipo):
        try:
            return Result.ok(cls(tipo))
        except Exception as ex:
            return Result.fail({'telefono_tipo':  [str(ex)]})
