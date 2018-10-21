from inspect import getfullargspec


class ArgsSpec(object):

    def __init__(self, method):
        try:
            full_args_spec = getfullargspec(method)
            self._args = full_args_spec[0]
            self._varargs = full_args_spec[1]
            self._keywords = full_args_spec[2]
            self._defaults = full_args_spec[3]
            self._kwonlyargs = full_args_spec[4]
            self._kwonlydefaults = full_args_spec[5]
            self._annotations = full_args_spec[6]
        except Exception as ex:
            raise Exception(str(ex))

    @property
    def args(self):
        return self._args

    @property
    def varargs(self):
        return self._varargs

    @property
    def keywords(self):
        return self._keywords

    @property
    def defaults(self):
        return self._defaults

    @property
    def kwonlyargs(self):
        return self._kwonlyargs

    @property
    def kwonlydefaults(self):
        return self._kwonlydefaults

    @property
    def annotations(self):
        return self._annotations


MIN_NUMBER_ARGS = 1


class ValueObject(object):

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)

        args_spec = ArgsSpec(self.__init__)

        def verifica_argumentos():
            no_argumentos_en_init = len(args_spec.args) <= MIN_NUMBER_ARGS
            if no_argumentos_en_init:
                raise Exception('No se declararon argumentos en __init__')
            if args_spec.varargs:
                raise ValueError('`*args` no están permitidos en __init__')
            if args_spec.keywords:
                raise ValueError('`**kwargs` no están permitidos en __init__')
            if args_spec.kwonlyargs:
                raise ValueError('`kwonlyargs` no están permitidos en __init__')
            if args_spec.kwonlydefaults:
                raise ValueError('`kwonlydefaults` no están permitidos en __init__')
            if args_spec.annotations:
                raise ValueError('`annotations` no están permitidos en __init__')

        def verifica_tipo_dato_mutable():
            tipos_mutable = (list, dict, set)
            for arg in args:
                if type(arg) in tipos_mutable:
                    raise Exception("Parámetros mutables no son permitidos.")

        def asigna_argumentos_instancia():
            defaults = () if not args_spec.defaults else args_spec.defaults
            self.__dict__.update(
                dict(zip(args_spec.args[:0:-1], defaults[::-1]))
            )
            self.__dict__.update(
                dict(list(zip(args_spec.args[1:], args)) + list(kwargs.items()))
            )

        verifica_argumentos()
        verifica_tipo_dato_mutable()
        asigna_argumentos_instancia()

        return self

    def __setattr__(self, name, value):
        raise Exception('No puedes cambiar valores de un value object')

    def __eq__(self, other):
        if other is None:
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __str__(self):
        return repr(self)

    def __repr__(self):
        args_spec = ArgsSpec(self.__init__)
        args_values = ["{}={}".format(arg, getattr(self, arg)) for arg in args_spec.args[1:]]
        return "{}({})".format(self.__class__.__name__, ", ".join(args_values))

    def __hash__(self):
        return self.hash

    @property
    def hash(self):
        return hash(repr(self))
