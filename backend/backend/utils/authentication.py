from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from person.models import Person


class OpenIdAuthentication(BaseAuthentication):
    def authenticate(self, request):
        openId = request.GET.get("openId")
        if not openId:
            openId = request.POST.get("openId")
        if not openId:
            raise exceptions.AuthenticationFailed("请携带openId参数")

        try:
            user = Person.objects.get(pk=openId)
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)

        return (user, user.openId)
