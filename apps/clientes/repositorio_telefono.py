from apps.clientes.cliente import Cliente
from apps.clientes.cliente_telefono import ClienteTelefono
from apps.clientes.models import ORMClienteTelefono
from apps.clientes.nombre_cliente import NombreCliente
from apps.clientes.numero_telefono import NumeroTelefono
from apps.clientes.tipo_telefono import TipoTelefono


class RepositorioTelefono(object):

    def _decode_db(self, obj_db):
        cliente_telefono = ClienteTelefono(tipo=TipoTelefono(obj_db.tipo),
                                           numero=NumeroTelefono(obj_db.numero),
                                           cliente=Cliente(nombre=NombreCliente(obj_db.cliente.nombre),
                                                           id=obj_db.cliente.id),
                                           id=obj_db.id)
        return cliente_telefono

    def create(self, obj):
        try:
            obj_db = ORMClienteTelefono.objects.create(tipo=obj.tipo.value,
                                                       numero=obj.numero.value,
                                                       cliente_id=obj.cliente.id)
            return self._decode_db(obj_db)
        except Exception as ex:
            raise ValueError(str(ex))

