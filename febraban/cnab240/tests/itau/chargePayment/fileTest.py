from unittest.case import TestCase

from febraban.cnab240.itau.chargePayment.errors import IncompleteHeaderError, IncompleteTrailerError
from febraban.cnab240.itau.chargePayment.file.trailer import Trailer
from febraban.cnab240.itau.chargePayment.file.header import Header
from febraban.cnab240.user import User, UserBank
from datetime import datetime


user = User(
    name="JOHN SMITH",
    identifier="12345678901",
)

bank = UserBank(
    bankId="341",
    branchCode="1234",
    accountNumber="1234567",
    accountVerifier="8"
)


class FileTest(TestCase):

    def testHeaderLength(self):
        string = Header().content
        self.assertEqual(len(string), 240)

    def testTrailerLength(self):
        string = Trailer().content
        self.assertEqual(len(string), 240)

    def testHeaderDefaultValues(self):
        content = Header().content
        self.assertEqual(content[3:7], "0000")
        self.assertEqual(content[7:8], "0")
        self.assertEqual(content[14:17], "081")
        self.assertEqual(content[142:143], "1")

    def testTrailerDefaultValues(self):
        content = Trailer().content
        self.assertEqual(content[3:7], "9999")
        self.assertEqual(content[7:8], "9")

    def testHeaderSets(self):
        header = Header()
        header.setSender(user)
        header.setSenderBank(bank)
        header.setGeneratedFileDate(datetime(2017, 12, 3, 19, 40, 9))
        response = "34100000      081100012345678901                    01234 000001234567 8JOHN SMITH                                                            10312201719400900000000000000                                                                     "
        self.assertEquals(header.content, response)

    def testIncompleteHeader(self):
        header = Header()
        self.assertRaises(IncompleteHeaderError, header.validate)

    def testIncompleteTrailer(self):
        trailer = Trailer()
        self.assertRaises(IncompleteTrailerError, trailer.validate)

    def testTrailerSets(self):
        trailer = Trailer()
        trailer.setSenderBank(bank)
        trailer.setNumberOfLotsAndRegisters(count=3)
        response = "34199999         000003000014                                                                                                                                                                                                                   "
        self.assertEquals(trailer.content, response)
