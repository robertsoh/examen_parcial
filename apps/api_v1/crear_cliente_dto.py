from typing import NamedTuple


class CrearClienteDto(NamedTuple):
    nombre_cliente: str
    telefono_tipo: int
    telefono_numero: int

    def serialize(self):
        return self._asdict()
