# coding: utf-8

from ....row import Row, RowStruct, emptyStruct
from ....characterType import numeric, alphaNumeric
from ..errors import IncompleteHeaderError


class Header(object):

    def __init__(self):
        self.content = " " * 240
        self.defaultValues()

        self.missingFields = {
            "Sender",
            "SenderBank",
            "PositionInLot",
            "PaymentKind",
            "PaymentMethod",
        }

    def defaultValues(self):
        structure = [
            # Empty fields or auto-filled by the bank
            emptyStruct(16, 17, alphaNumeric),
            emptyStruct(31, 52, alphaNumeric),
            emptyStruct(57, 58, alphaNumeric),
            emptyStruct(70, 71, alphaNumeric),
            emptyStruct(222, 230, alphaNumeric),
            emptyStruct(230, 240, alphaNumeric),

            # Fixed fields
            RowStruct(7, 8, 1, numeric, "1"),  # TIPO DE REGISTRO
            RowStruct(8, 9, 1, alphaNumeric, "C"),  # TIPO DE OPERAÇÃO
            RowStruct(13, 16, 3, numeric, "030"),  # LAYOUT DO LOTE
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setSender(self, user):
        self.missingFields.discard("Sender")
        numberExtract = ''.join(s for s in user.address.streetLine1 if s.isdigit())
        structure = [
            RowStruct(17, 18, 1, numeric, "1" if len(user.identifier) == 11 else "2"),
            RowStruct(18, 32, 14, numeric, user.identifier),
            RowStruct(72, 102, 30, alphaNumeric, user.name),
            # Address information
            RowStruct(142, 172, 50, alphaNumeric, "%s - %s" % (user.address.streetLine1,
                                                               user.address.district)),
            RowStruct(172, 177, 5, numeric, numberExtract),
            RowStruct(177, 192, 15, alphaNumeric, user.address.streetLine2),
            RowStruct(192, 212, 20, alphaNumeric, user.address.city),
            RowStruct(212, 220, 8, numeric, user.address.zipCode),
            RowStruct(220, 222, 2, alphaNumeric, user.address.stateCode),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setSenderBank(self, bank):
        self.missingFields.discard("SenderBank")
        structure = [
            RowStruct(0, 3, 3, numeric, bank.bankId),
            RowStruct(52, 57, 5, numeric, bank.branchCode),
            RowStruct(58, 70, 12, numeric, bank.accountNumber),
            RowStruct(71, 72, 1, numeric, bank.accountVerifier),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setPositionInLot(self, index):
        self.missingFields.discard("PositionInLot")
        structure = [
            RowStruct(3, 7, 4, numeric, index),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setPaymentKind(self, kind):
        self.missingFields.discard("PaymentKind")
        structure = [
            RowStruct(9, 11, 2, numeric, kind),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setPaymentMethod(self, method):
        self.missingFields.discard("PaymentMethod")
        structure = [
            RowStruct(11, 13, 2, numeric, method),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def validate(self):
        if self.missingFields:
            raise IncompleteHeaderError(list(self.missingFields))
