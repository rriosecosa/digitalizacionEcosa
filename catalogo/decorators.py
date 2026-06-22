from django.core.exceptions import PermissionDenied


def catalogo_required(view_func):

    def wrapper(request, *args, **kwargs):

        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied

        if (
            user.is_superuser
            or
            user.groups.filter(
                name='CATALOGO_ADMIN'
            ).exists()
        ):
            return view_func(
                request,
                *args,
                **kwargs
            )

        raise PermissionDenied

    return wrapper  