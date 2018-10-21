from rest_framework.response import Response


def serialize_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return Response(str(e), status=400)
    return func_wrapper
