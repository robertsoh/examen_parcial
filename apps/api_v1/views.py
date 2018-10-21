import pika
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api_v1.crear_cliente_dto import CrearClienteDto
from apps.clientes.cliente import Cliente
from apps.clientes.cliente_telefono import ClienteTelefono
from apps.clientes.nombre_cliente import NombreCliente
from apps.clientes.numero_telefono import NumeroTelefono
from apps.clientes.repositorio_cliente import RepositorioCliente
from apps.clientes.repositorio_telefono import RepositorioTelefono
from apps.clientes.tipo_telefono import TipoTelefono
from apps.common.decorators import serialize_exceptions
from apps.common.result import Result


class ClienteCreateAPIView(APIView):

    def __init__(self, *args, **kwargs):
        self._repositorio_cliente = RepositorioCliente()
        self._repositorio_telefono = RepositorioTelefono()
        super().__init__(*args, **kwargs)

    @serialize_exceptions
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        dto = CrearClienteDto(
            nombre_cliente=request.data.get('nombre_cliente'),
            telefono_tipo=request.data.get('telefono_tipo'),
            telefono_numero=request.data.get('telefono_numero')
        )
        nombre_cliente_o_error = NombreCliente.create(dto.nombre_cliente)
        numero_telefono_o_error = NumeroTelefono.create(dto.telefono_numero)
        tipo_telefono_o_error = TipoTelefono.create(dto.telefono_tipo)

        es_invalido, errores = Result.combine([nombre_cliente_o_error,
                                               numero_telefono_o_error,
                                               tipo_telefono_o_error])
        if es_invalido:
            raise ValidationError(errores)
        cliente = Cliente(nombre=nombre_cliente_o_error.value)
        cliente = self._repositorio_cliente.create(cliente)
        telefono = ClienteTelefono(tipo=tipo_telefono_o_error.value,
                                   numero=numero_telefono_o_error.value,
                                   cliente=cliente)
        telefono = self._repositorio_telefono.create(telefono)
        return Response('OK', status=status.HTTP_201_CREATED)

    def send_rabit(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='chimpanzee.rmq.cloudamqp.com',
                virtual_host='ftzmpaoj',
                credentials=pika.PlainCredentials(username='ftzmpaoj', password='pEYJ7Q6W5G36I4o-UWbrSNYctawNNZ6L')))
        channel = connection.channel()

        channel.queue_declare(queue='test')

        channel.basic_publish(exchange='',
                              routing_key='test',
                              body='Hello World!')
        print(" [x] Sent 'Hello World!'")
        connection.close()
