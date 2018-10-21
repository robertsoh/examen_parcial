

class ResultCommonLogic(object):

    def __init__(self, is_failure, error):
        if is_failure:
            if not error:
                raise ValueError('No se ha incluido el error para el caso de falla')
        else:
            if error:
                raise ValueError('Se ha incluido error para el caso exitoso ')
        self._is_failure = is_failure
        self._error = error

    @property
    def is_success(self):
        return not self._is_failure

    @property
    def is_failure(self):
        return self._is_failure

    @property
    def error(self):
        if self.is_success:
            raise ValueError('No hay error para el caso exitoso')
        return self._error


class Result(object):

    def __init__(self, is_failure, value=None, error=None):
        self._logic = ResultCommonLogic(is_failure, error)
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def is_success(self):
        return self._logic.is_success

    @property
    def is_failure(self):
        return self._logic.is_failure

    @property
    def error(self):
        return self._logic.error

    @classmethod
    def ok(cls, value=None):
        return cls(False, value, None)

    @classmethod
    def fail(cls, error):
        return cls(True, None, error)

    @classmethod
    def combine(cls, results):
        is_failure = any([result.is_failure for result in results])
        errors = []
        for result in results:
            if result.is_failure:
                errors.append(result.error)
        return is_failure, errors
