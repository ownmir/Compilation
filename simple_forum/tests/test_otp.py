from django_otp.tests import TestCase as OTPTestCase
from django_otp.plugins.otp_totp.tests import TOTPDeviceMixin


class OtpTestCase(TOTPDeviceMixin, OTPTestCase):
    def setUp(self):
        super().setUp()
        # print("alice", self.alice, "tokens[3]", self.tokens[3], self.device.verify_token(self.tokens[3]))
        # self.test_default_key()
        # self.test_single()

    # def test_default_key(self):
    #     device = self.alice.totpdevice_set.create()
    #
    #     # Make sure we can decode the key.
    #     print(device.bin_key)

    def test_single(self):
        result = self.device.verify_token(self.tokens[3])

        self.assertEqual(result, True)
