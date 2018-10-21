import pika
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api_v1.crear_cliente_proyecto_usuario_dto import CrearClienteProyectoUsuarioDto
from apps.clientes.cliente import Cliente
from apps.clientes.nombre_cliente import NombreCliente
from apps.clientes.repositorio_cliente import RepositorioCliente
from apps.common.decorators import serialize_exceptions
from apps.common.result import Result
from apps.proyectos.nombre_proyecto import NombreProyecto
from apps.proyectos.proyecto import Proyecto
from apps.proyectos.repositorio_proyecto import RepositorioProyecto
from apps.usuarios.nombre_usuario import NombreUsuario
from apps.usuarios.repositorio_usuario import RepositorioUsuario
from apps.usuarios.usuario import Usuario, RolUsuario


class ClienteCreateAPIView(APIView):

    def __init__(self, *args, **kwargs):
        self._repositorio_cliente = RepositorioCliente()
        self._repositorio_proyecto = RepositorioProyecto()
        self._repositorio_usario = RepositorioUsuario()
        super().__init__(*args, **kwargs)

    @serialize_exceptions
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        dto = CrearClienteProyectoUsuarioDto(
            NombreCliente=request.data.get('NombreCliente'),
            NombreProyecto=request.data.get('NombreProyecto'),
            NombreUsuario=request.data.get('NombreUsuario'),
            Presupuesto=request.data.get('Presupuesto')
        )
        nombre_cliente_o_error = NombreCliente.create(dto.NombreCliente)
        nombre_proyecto_o_error = NombreProyecto.create(dto.NombreProyecto)
        nombre_usuario_o_error = NombreUsuario.create(dto.NombreUsuario)
        es_invalido, errores = Result.combine([nombre_cliente_o_error,
                                               nombre_proyecto_o_error,
                                               nombre_usuario_o_error])
        if es_invalido:
            raise ValidationError(errores)
        cliente = Cliente(nombre=nombre_cliente_o_error.value)
        cliente = self._repositorio_cliente.create(cliente)
        proyecto = Proyecto(nombre=nombre_proyecto_o_error.value,
                            cliente=cliente,
                            presupuesto=dto.Presupuesto)
        self._repositorio_proyecto.create(proyecto)
        usuario = Usuario(username=nombre_usuario_o_error.value,
                          cliente=cliente,
                          rol=RolUsuario.Owner)
        self._repositorio_usario.create(usuario)
        self.send_rabit()
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
