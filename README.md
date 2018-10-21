

## Configuración de variables de entorno para el sistema:
* `DJANGO_SETTINGS_MODULE=config.settings.dev`
* `ALLOWED_HOSTS` Lista de dominios permitidos para acceder a la aplicación
* `DB_NAME` nombre de la base de datos
* `DB_USER` usuario de la base de datos
* `DB_HOST` servidor de base de datos
* `DB_PORT` puerto de la base de datos
* `SECRET_KEY` Secret Key de Django

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


class CrearClienteProyectoUsuarioDto(NamedTuple):
    NombreCliente: str
    NombreProyecto: str
    NombreUsuario: str
    Rol: int = None

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
            return Result.fail({'NombreCliente':  [str(ex)]})
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
        except Exception as ex:
            raise ValueError(str(ex))
        return self._decode_db(db_cliente)
```

- url de prueba `https://examendcroh.cfapps.io/api/v1/clientes` 
- Method: `POST`
- data de prueba
```python
{
	"NombreCliente": "Test",
	"NombreProyecto": "Proyecto 1",
	"NombreUsuario": "test",
	"Presupuesto": 1000
}

```

---
QOILABS © 2018
