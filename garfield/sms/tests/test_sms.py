try:  # pragma: no cover
    from http.cookies import SimpleCookie
except ImportError:  # pragma: no cover
    from Cookie import SimpleCookie

from django.test import TestCase
from django.test import Client
from django.test import override_settings

from twilio.request_validator import RequestValidator

from mock import patch


class GarfieldSmsTestClient(Client):
    def sms(self, body, path="/sms/", to="+15558675309", from_="+15556667777",
            extra_params=None):
        params = {"MessageSid": "CAtesting",
                  "AccountSid": "ACxxxxx",
                  "To": to,
                  "From": from_,
                  "Body": body,
                  "Direction": "inbound",
                  "FromCity": "BROOKLYN",
                  "FromState": "NY",
                  "FromCountry": "US",
                  "FromZip": "55555"}

        if extra_params:
            for k, v in extra_params.items():
                params[k] = v

        HTTP_HOST = "example.com"
        validator = RequestValidator("yyyyyyyy")
        absolute_url = "http://{0}{1}".format(HTTP_HOST,
                                              path)
        signature = validator.compute_signature(absolute_url,
                                                params)

        return self.post(path, params,
                         HTTP_X_TWILIO_SIGNATURE=signature,
                         HTTP_HOST=HTTP_HOST)


@override_settings(TWILIO_AUTH_TOKEN="yyyyyyyy",
                   ALLOWED_HOSTS=['example.com'])
class GarfieldSmsTestCase(TestCase):
    def setUp(self):
        self.client = GarfieldSmsTestClient()

    def assert_twiml(self, response):
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "<Response")
