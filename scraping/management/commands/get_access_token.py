import pickle
import re

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
    run_simple('namesgames.com', 4000, application)


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



# http://namesgames.com/?code=AQTclHxII-gZendl3WvUlU0Y6AlHppzmU-qQrq3E8Km9ExnKo3VhtWpcL25SKYTUAdGx9cidVJF682k0s-uE9FeLk0f-ndJnPB4NARhl4zvbCGIeTjZDVWfjGxcokTq3Khp-k9eXVrGjZLrOMLcd4jb9Dryc0PvwyLR1vsnpuo6jLnl38fQrVnvgkxHbTA&state=foobar
# https://www.linkedin.com/oauth/v2/authorization?response_type=code&state=foobar&scope=r_emailaddress&client_id=78zqy8vv1aerst&redirect_uri=https%3A%2F%2Fwww.google.com%2F
#
#
# curl -ik -X POST https://www.linkedin.com/oauth/v2/accessToken \
# -d grant_type=authorization_code \
# -d code=AQRiDrqRSFdAIwEEDUG1OQAWlVsZtSBs25byXV8NzYuQybIXgNWOJ82FpCs3Sji4rQ1oAxruaQ33uf0TZ8Zs2ZD2pRkN7KVbiaJiEhpnRxQqqg5psIt97nOeYUKs8MLaTYr-mkmlJDOV1dsBkoGo1pPvAA-5f-UWJ9RFe0D7nIRYQbWFFGdZMI-RizaA5A \
# -d redirect_uri=https%3A%2F%2Fwww.google.com%2F \
# -d client_id=78zqy8vv1aerst \
# -d client_secret=rXsVGPpaUGOkO4SO
# j

# AQXKFbrjEtmEgYtSGqzYCHquX0HMjRB5a_cSKvQdDzrv0y6aPi1DQadej0ZoJQvZ9E_5-QIblP8uK0B9Xk-QJvPaUyxr71YAYAz7RIa5OR9vrHw0RFdpsz6NHjCxzh1DhusBj7bRjFFtm5EwvnXVZ6lwWdYhU_f4NhdlLwIOibUYs9vywdmmg_ZTjs0VzJHaBqyn8UneqTYQeHUYdDgG4T7L39zWtByuOxM7Aks4K8y4HddVz4Q5kWrFQjWh_-zRuv34bkf1y90RRzp87HCLPPGeKLsi7MD2cLL9fDEJIL1vc-JkemJhnwYvfXvUKSyF5h6aICIzffEd8BcfINofNnLKvBXjfA




