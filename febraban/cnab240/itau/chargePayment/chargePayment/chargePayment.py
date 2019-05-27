from ..utils import BarCode
from .header import Header
from .segmentJ import SegmentJ
from .segmentJ52 import SegmentJ52
from .trailer import Trailer


class ChargePayment(object):

    def __init__(self):
        self.header = Header()
        self.segmentJ = SegmentJ()
        self.segmentJ52 = SegmentJ52()
        self.trailer = Trailer()
        self.bankId = None
        self.barCode = None

    def toString(self):
        self.validate()
        return '\r\n'.join((
            self.header.content,
            self.segmentJ.content,
            self.segmentJ52.content,
            self.trailer.content,
        ))

    def setSender(self, user):
        """Sets the sender for the payment. The sender represents a users, its bank and its address."""
        self.header.setSender(user)
        self.header.setSenderBank(user.bank)

        self.segmentJ.setSenderBank(user.bank)
        self.segmentJ52.setSender(user)
        self.segmentJ52.setSenderBank(user.bank)

        self.trailer.setSenderBank(user.bank)

        self.bankId = user.bank.bankId

        self._setPaymentMethod()

    def setIdentifier(self, identifier):
        """Sets the charge identifier that will be returned from the bank. Used for matching results."""
        self.segmentJ.setIdentifier(identifier)

    def setPaymentDate(self, paymentDate):
        """Sets the payment date to be sent to the bank. Defaults to today."""
        self.segmentJ.setPaymentDate(paymentDate)

    def setBarCode(self, barCode):
        barCode = BarCode(barCode)
        self.barCode = barCode
        self.segmentJ.setBarCode(barCode)

        self.trailer.setAmountInCents(barCode.value)

        self._setPaymentMethod()

    def _setPaymentMethod(self):
        """Defines payment method on Header and Trailer object based on NOTE 5."""
        if self.bankId is not None and self.barCode is not None:
            if self.bankId == self.barCode.bankId:
                # Paying charge from same bank
                self.header.setPaymentMethod("30")
                return
            # Paying charge from different bank
            self.header.setPaymentMethod("31")

    def setPaymentKind(self, paymentKind):
        """Sets payment kind based on NOTE 4."""
        self.header.setPaymentKind(paymentKind)

    def setPositionInLot(self, index):
        self.header.setPositionInLot(index)
        self.segmentJ.setPositionInLot(index)
        self.segmentJ52.setPositionInLot(index)
        self.trailer.setPositionInLot(index)

    def validate(self):
        self.header.validate()
        self.segmentJ.validate()
        self.segmentJ52.validate()
        self.trailer.validate()
