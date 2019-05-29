# coding: utf-8

from ....row import Row, RowStruct, emptyStruct
from ....characterType import numeric, alphaNumeric
from ..errors import IncompleteLotTrailerError


class Trailer(object):

    def __init__(self):
        self.content = " " * 240
        self.defaultValues()

        self.missingFields = {
            "SenderBank",
            "PositionInLot",
            "PaymentAmount",
        }

    def defaultValues(self):
        structure = [
            # Empty fields or auto-filled by the bank
            emptyStruct(8, 17, alphaNumeric),
            emptyStruct(41, 59, numeric),
            emptyStruct(59, 230, alphaNumeric),
            emptyStruct(230, 240, alphaNumeric),  # FIELD FOR RETURN FILE

            # Fixed fields
            RowStruct(7, 8, 1, numeric, "5"),  # TIPO DE REGISTRO
            RowStruct(17, 23, 6, numeric, "4"),  # QUANTIDADE DE REGISTROS NO LOTE - FIXADO EM 4
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setSenderBank(self, bank):
        self.missingFields.discard("SenderBank")
        structure = [
            RowStruct(0, 3, 3, numeric, bank.bankId),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setAmountInCents(self, value):
        self.missingFields.discard("PaymentAmount")
        structure = [
            RowStruct(23, 41, 18, numeric, value),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setPositionInLot(self, index):
        self.missingFields.discard("PositionInLot")
        structure = [
            RowStruct(3, 7, 4, numeric, index),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setEntryCount(self, count):
        structure = [
            RowStruct(17, 23, 6, numeric, 4 * count),  # Cada lote contém 4 entradas
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def validate(self):
        if self.missingFields:
            raise IncompleteLotTrailerError(list(self.missingFields))
