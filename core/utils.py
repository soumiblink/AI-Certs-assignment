from rest_framework.response import Response
from rest_framework import status


def get_object_or_404_custom(model, **filters):
    """
    Safely fetch a model instance by filters.
    Returns (instance, None) on success or (None, 404 Response) on failure.
    """
    try:
        obj = model.objects.get(**filters)
        return obj, None
    except model.DoesNotExist:
        error_response = Response(
            {"success": False, "message": f"{model.__name__} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
        return None, error_response


def success_response(data, status_code=status.HTTP_200_OK):
    return Response({"success": True, "data": data}, status=status_code)


def error_response(message, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({"success": False, "message": message}, status=status_code)
