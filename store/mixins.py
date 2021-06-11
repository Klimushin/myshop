from django.core.exceptions import PermissionDenied


class StaffRequiredMixin:
    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied

        # noinspection PyUnresolvedReferences
        return super(StaffRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )
