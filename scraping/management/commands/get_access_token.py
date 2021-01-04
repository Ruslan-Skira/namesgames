import pickle
import re
import urllib

from django.conf import settings
from django.core.management.base import BaseCommand
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    _referer = request.headers.get('Referer', type=str)
    if _referer:
        referer = re.search("(?<=code=)(.*)(?=&state)", _referer).group(1)
        with open(settings.TOKEN_FILE, 'wb') as token:
            pickle.dump(referer, token)

    return Response('Thank you I get Access token')


def run_server_simple():
    run_simple(settings.NAMESGAMES_ADDRESS, 4000, application)


class Command(BaseCommand):
    help = 'Login to linkedin by yourself. It is need for getting access token'

    def handle(self, *args, **options):
        authorization_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&state=foobar" \
                            f"&scope=r_liteprofile&" \
                            f"client_id=78zqy8vv1aerst" \
                            f"&redirect_uri=http%3A%2F%2Fnamesgames.com%2F "

        self.stdout.write(self.style.ERROR('Сlick on me ') + authorization_url)
        run_server_simple()
        self.stdout.write(self.style.SUCCESS(f' Successfully get new access token (^-^)'))

