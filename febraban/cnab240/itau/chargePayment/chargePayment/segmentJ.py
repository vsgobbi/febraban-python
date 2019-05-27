# coding: utf-8
from datetime import date

from ....row import Row, RowStruct, emptyStruct
from ....characterType import numeric, alphaNumeric
from ..errors import IncompleteSegmentJError


class SegmentJ(object):

    def __init__(self):
        self.content = " " * 240
        self.defaultValues()

        self.missingFields = {
            "PositionInLot",
            "SenderBank",
            "BarCode",
            "Identifier",
        }

    def defaultValues(self):
        structure = [
            # Empty fields or auto-filled by the bank
            emptyStruct(167, 182, numeric),
            emptyStruct(203, 215, alphaNumeric),
            emptyStruct(215, 240, alphaNumeric),  # FIELDS FOR RETURN FILE

            # Fixed fields
            RowStruct(7, 8, 1, numeric, "3"),  # TIPO DE REGISTRO
            RowStruct(8, 13, 5, numeric, 1),  # INDEX DO REGISTRO
            RowStruct(13, 14, 1, alphaNumeric, "J"),  # CÓDIGO DE SEGMENTO
            RowStruct(14, 17, 3, numeric, "000"),  # TIPO DE MOVIMENTO

            # Unused fields
            emptyStruct(61, 91, alphaNumeric),
            emptyStruct(91, 99, numeric),
            emptyStruct(114, 129, numeric),
            emptyStruct(129, 144, numeric),

            # Default payment date
            RowStruct(144, 152, 8, numeric, date.today().strftime("%d%m%Y"))
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setSenderBank(self, bank):
        self.missingFields.discard("SenderBank")
        structure = [
            RowStruct(0, 3, 3, numeric, bank.bankId),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setBarCode(self, barCode):
        self.missingFields.discard("BarCode")
        structure = [
            # BarCode itself
            RowStruct(17, 20, 3, numeric, barCode.bankId),
            RowStruct(20, 21, 1, numeric, barCode.currency),
            RowStruct(21, 22, 1, numeric, barCode.dac),
            RowStruct(22, 26, 4, numeric, barCode.dueFactor),
            RowStruct(26, 36, 10, numeric, barCode.value),
            RowStruct(36, 61, 25, numeric, barCode.freeField),

            # Derived from barcode
            RowStruct(99, 114, 15, numeric, barCode.value),  # VALOR NOMINAL DO TÍTULO
            RowStruct(152, 167, 15, numeric, barCode.value),  # VALOR DO PAGAMENTO
            RowStruct(91, 99, 8, numeric, barCode.dueDate.strftime("%d%m%Y")),  # DATA DE VENCIMENTO
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setPaymentDate(self, paymentDate):
        self.missingFields.discard("PaymentDate")
        structure = [
            RowStruct(144, 152, 8, numeric, paymentDate.strftime("%d%m%Y"))
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setIdentifier(self, identifier):
        self.missingFields.discard("Identifier")
        structure = [
            RowStruct(182, 202, 20, alphaNumeric, identifier),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setPositionInLot(self, index):
        self.missingFields.discard("PositionInLot")
        structure = [
            RowStruct(3, 7, 4, numeric, index)
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def validate(self):
        if self.missingFields:
            raise IncompleteSegmentJError(list(self.missingFields))
