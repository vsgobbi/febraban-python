from unittest.case import TestCase
from datetime import date
from febraban.cnab240.itau.chargePayment.chargePayment.header import Header
from febraban.cnab240.itau.chargePayment.chargePayment.segmentJ import SegmentJ
from febraban.cnab240.itau.chargePayment.chargePayment.segmentJ52 import SegmentJ52
from febraban.cnab240.itau.chargePayment.chargePayment.trailer import Trailer
from febraban.cnab240.itau.chargePayment.utils import BarCode
from febraban.cnab240.user import User, UserBank, UserAddress


user = User(
    name="JOHN SMITH",
    identifier="12345678901",
    address=UserAddress(
        streetLine1="AV PAULISTA 1000",
        city="SAO PAULO",
        stateCode="SP",
        zipCode="01310000"
    )
)

bank = UserBank(
    bankId="341",
    branchCode="1234",
    accountNumber="1234567",
    accountVerifier="8"
)

barCode = BarCode("34197791600000721441091002168647307144464000")


class PaymentTest(TestCase):

    def testHeaderLength(self):
        string = Header().content
        self.assertEqual(240, len(string))

    def testSegmentJLength(self):
        string = SegmentJ().content
        self.assertEqual(240, len(string))

    def testSegmentJ52Length(self):
        string = SegmentJ52().content
        self.assertEqual(240, len(string))

    def testTrailerLength(self):
        string = Trailer().content
        self.assertEqual(240, len(string))

    def testHeaderDefaultValues(self):
        content = Header().content
        self.assertEqual("1", content[7:8])
        self.assertEqual("C", content[8:9])
        self.assertEqual("030", content[13:16])

    def testSegmentJDefaultValues(self):
        content = SegmentJ().content
        self.assertEqual("3", content[7:8])
        self.assertEqual("00001", content[8:13])
        self.assertEqual("J", content[13:14])
        self.assertEqual("000", content[14:17])

    def testSegmentJ52DefaultValues(self):
        content = SegmentJ52().content
        self.assertEqual("3", content[7:8])
        self.assertEqual("00002", content[8:13])
        self.assertEqual("J", content[13:14])
        self.assertEqual("000", content[14:17])
        self.assertEqual("52", content[17:19])

    def testTrailerDefaultValues(self):
        content = Trailer().content
        self.assertEqual("5", content[7:8])

    def testHeaderSets(self):
        header = Header()
        header.setSender(user)
        header.setSenderBank(bank)
        header.setPositionInLot(2)
        header.setPaymentKind("88")
        header.setPaymentMethod("99")
        header.validate()
        response = "34100021C8899030 100012345678901                    01234 000001234567 8JOHN SMITH                                                            AV PAULISTA 1000 -            01000               SAO PAULO           01310000SP                  "
        self.assertEqual(response, header.content)

    def testSegmentJSets(self):
        segment = SegmentJ()
        segment.setBarCode(barCode)
        segment.setSenderBank(bank)
        segment.setPaymentDate(date(2017, 11, 30))
        segment.setIdentifier("DEV-1234567890987654321")
        segment.setPositionInLot(3)
        segment.validate()
        response = "3410003300001J00034197791600000721441091002168647307144464000                              1006201900000000007214400000000000000000000000000000030112017000000000072144000000000000000DEV-1234567890987654                                      "
        self.assertEqual(response, segment.content)

    def testSegmentJ52Sets(self):
        segment = SegmentJ52()
        segment.setSender(user)
        segment.setSenderBank(bank)
        segment.setPositionInLot(4)
        segment.validate()
        response = "3410004300002J000521000012345678901JOHN SMITH                              0000000000000000                                        0000000000000000                                                                                             "
        self.assertEqual(response, segment.content)

    def testTrailerSets(self):
        trailer = Trailer()
        trailer.setAmountInCents(44400)
        trailer.setEntryCount(1)
        trailer.setSenderBank(bank)
        trailer.setPositionInLot(5)
        trailer.validate()
        response = "34100055         000004000000000000044400000000000000000000                                                                                                                                                                                     "
        self.assertEqual(response, trailer.content)
