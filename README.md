# Examen parcial

## Configuración de variables de entorno para el sistema:
* `DJANGO_SETTINGS_MODULE=config.settings.dev`
* `ALLOWED_HOSTS` Lista de dominios permitidos para acceder a la aplicación
* `DB_NAME` nombre de la base de datos
* `DB_USER` usuario de la base de datos
* `DB_HOST` servidor de base de datos
* `DB_PORT` puerto de la base de datos
* `SECRET_KEY` Secret Key de Django
* `RABBIT_HOST`
* `RABBIT_VIRTUAL_HOST`
* `RABBIT_USERNAME`
* `RABBIT_PASSWORD`

## Patrones agregados:

- `Unit of Work` en `apps/api_v1/views.py`

```python
from django.db import transaction

@transaction.atomic
def post(self, request, *args, **kwargs):
    pass
```

- `ValueObject` en `apps/clientes/nombre_cliente.py`

```python
from apps.common.value_object import ValueObject

class NombreCliente(ValueObject):

    def __init__(self, value):
        pass
```

- `DTO` en  `apps/api_v1/crear_cliente_proyecto_usuario_dto.py`

```python
from typing import NamedTuple


class CrearClienteDto(NamedTuple):
    nombre_cliente: str
    telefono_tipo: int
    telefono_numero: int

    def serialize(self):
        return self._asdict()
```

- `Migrations` ejem. `apps/clientes/migrations/0001_initial.py`

- Se está usando variables de entorno para la conexión a la BD 

```python
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'ATOMIC_REQUESTS': True,
    }
}

```

- `notificación`

```python
from apps.common.result import Result
from apps.common.value_object import ValueObject


class NombreCliente(ValueObject):

    @classmethod
    def create(cls, nombre):
        try:
            return Result.ok(cls(nombre))
        except Exception as ex:
            return Result.fail({'nombre_cliente':  [str(ex)]})
```

- `repository` ejem `apps/clientes/repositorio_cliente.py`

```python
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
            return self._decode_db(db_cliente)
        except Exception as ex:
            raise ValueError(str(ex))

```


- Enviar a Cola rabbit
```python
import os
import pika


def send_rabit(mensaje):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ.get('RABBIT_HOST'),
            virtual_host=os.environ.get('RABBIT_VIRTUAL_HOST'),
            credentials=pika.PlainCredentials(username=os.environ.get('RABBIT_USERNAME'),
                                              password=os.environ.get('RABBIT_PASSWORD'))))
    channel = connection.channel()

    channel.queue_declare(queue='test')

    channel.basic_publish(exchange='',
                          routing_key='test',
                          body=mensaje)
    connection.close()
```

- Null object pattern

```python

class Null:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return "Null(  )"

    def __nonzero__(self):
        return 0

    def __getattr__(self, name):
        return self

    def __setattr__(self, name, value):
        return self

    def __delattr__(self, name):
        return self
```

- url de prueba `https://examenparcialdcroh.cfapps.io/api/v1/clientes` 
- Method: `POST`
- data de prueba
```python
{
	"nombre_cliente": "Test",
	"telefono_numero": 989898981,
	"telefono_tipo": 1,
}

```

---
QOILABS © 2018
