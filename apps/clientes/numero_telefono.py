from apps.common.result import Result
from apps.common.value_object import ValueObject


class NumeroTelefono(ValueObject):

    def __init__(self, value):
        if not value:
            raise  ValueError('El número de telefono es obligatorio')
        if len(value) > 9:
            raise ValueError('El número de teléfono no puede tener más de 9 digitos')

    @classmethod
    def create(cls, numero):
        try:
            return Result.ok(cls(numero))
        except Exception as ex:
            return Result.fail({'telefono_numero':  [str(ex)]})
