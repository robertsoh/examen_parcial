from apps.clientes.cliente import Cliente
from apps.clientes.models import ORMCliente
from apps.clientes.nombre_cliente import NombreCliente


class RepositorioCliente(object):

    def _decode_db(self, db_cliente):
        cliente = Cliente(nombre=NombreCliente(db_cliente.nombre),
                          id=db_cliente.id)
        return cliente

    def create(self, cliente):
        try:
            db_cliente = ORMCliente.objects.create(nombre=cliente.nombre.value)
        except Exception as ex:
            raise ValueError(str(ex))
        return self._decode_db(db_cliente)
