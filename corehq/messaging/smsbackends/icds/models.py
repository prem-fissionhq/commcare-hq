from urllib import urlencode
from urllib2 import urlopen

from crispy_forms import layout as crispy
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from corehq.apps.sms.mixin import BackendProcessingException
from corehq.apps.sms.models import SQLSMSBackend
from corehq.apps.sms.forms import BackendForm
from dimagi.utils.django.fields import TrimmedCharField

ERROR_CODES = {
    "-2": "Invalid credentials",
    "-3": "Empty mobile number",
    "-4": "Empty message",
    "-5": "HTTPS disabled",
    "-6": "HTTP disabled",
    "-13": "Internal Error",
    "-201": "Email Delivery Disabled",
    "-401": "Invalid Scheduled Time",
    "-404": "Invalid MsgType",
    "-406": "Invalid Port",
    "-407": "Invalid Expiry minutes",
    "-408": "Invalid Customer Reference Id",
    "-409": "Invalid Bill Reference Id",
    "-410": "Invalid Destination Address",
    "-432": "Invalid Bill Reference Id Length",
    "-433": "Invalid Customer Reference Id Length",
}

RETRY_ERROR_CODES = {"-13"}


class ICDSException(Exception):
    pass


class ICDSBackendForm(BackendForm):
    username = TrimmedCharField(
        label=_('Username'),
    )
    pin = TrimmedCharField(
        label=_('PIN'),
    )
    sender_id = TrimmedCharField(
        label=_('Sender ID'),
    )

    @property
    def gateway_specific_fields(self):
        return crispy.Fieldset(
            _("ICDS Settings"),
            'username',
            'pin',
            'sender_id',
        )


class SQLICDSBackend(SQLSMSBackend):

    class Meta:
        app_label = 'sms'
        proxy = True

    @classmethod
    def get_available_extra_fields(cls):
        return [
            'username',
            'pin',
            'sender_id',
        ]

    @classmethod
    def get_api_id(cls):
        return 'ICDS'

    @classmethod
    def get_generic_name(cls):
        return "ICDS"

    @classmethod
    def get_form_class(cls):
        return ICDSBackendForm

    def get_response_code(self, response):
        api_code_string = "~code=API"
        begin_response = response.find(api_code_string) + len(api_code_string)
        assert begin_response != -1
        end_response = response[begin_response:].find('&')
        assert end_response != -1
        return respone[begin_response:end_response]

    def handle_error(self, response_code):
        exception_message = "Error with ICDS backend. Http respone code: %s, %s" % (
            response_code, ERROR_CODES[response_code]
        )
        if response_code in RETRY_ERROR_CODES:
            raise ICDSException(exception_message)

    def send(self, msg, orig_phone_number=None, *args, **kwargs):
        config = self.config
        phone_number = msg.phone_number
        try:
            text = msg.text.encode("iso-8859-1")
            msg_type = "PM"
        except UnicodeEncodeError:
            text = msg.text.encode("utf-8")
            msg_type = "UC"
        params = {
            "username": config.username,
            "pin": config.pin,
            "mnumber": phone_number,
            "message": text,
            "signature": config.sender_id,
            "msgType": msg_type
        }
        url_params = urlencode(params)
        url = 'https://smsgw.sms.gov.in/failsafe/HttpLink?%s' % url_params
        try:
            response = urlopen("%s?%s" % (url, url_params),
                               timeout=settings.SMS_GATEWAY_TIMEOUT).read()
        except Exception as e:
            msg = "Error sending message from backend: '{}'\n\n{}".format(self.pk, str(e))
            raise BackendProcessingException(msg), None, sys.exc_info()[2]

        response_code = get_response_code(response)
        if response_code != '000':
            self.handle_error(response_code)
