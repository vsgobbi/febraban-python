# coding: utf-8

from datetime import datetime
from ....row import Row, RowStruct, emptyStruct
from ....characterType import numeric, alphaNumeric
from ..errors import IncompleteTrailerError


class Trailer(object):

    defaultStructure = (
        # Empty fields or auto-filled by the bank
        emptyStruct(8, 17, alphaNumeric),
        emptyStruct(29, 240, alphaNumeric),

        # Fixed fields
        RowStruct(3, 7, 4, alphaNumeric, "9999"),  # CÓDIGO DE LOTE DE SERVIÇO
        RowStruct(7, 8, 1, numeric, "9"),  # TIPO DE REGISTRO
    )

    def __init__(self):
        self.senderBank = None
        self.totalLotCount = 0
        self.content = " " * 240
        self.defaultValues()

        self.missingFields = {
            "SenderBank",
        }

    def defaultValues(self):
        structure = [
            # Empty fields or auto-filled by the bank
            emptyStruct(8, 17, alphaNumeric),
            emptyStruct(29, 240, alphaNumeric),

            # Fixed fields
            RowStruct(3, 7, 4, alphaNumeric, "9999"),  # CÓDIGO DE LOTE DE SERVIÇO
            RowStruct(7, 8, 1, numeric, "9"),  # TIPO DE REGISTRO
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setSenderBank(self, bank):
        self.missingFields.discard("SenderBank")
        structure = [
            RowStruct(0, 3, 3, numeric, bank.bankId),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setNumberOfLotsAndRegisters(self, count):
        self.missingFields.discard("NumberOfLotsAndRegisters")
        structure = [
            RowStruct(17, 23, 6, numeric, count),
            RowStruct(23, 29, 6, numeric, 2 + 4 * count),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def validate(self):
        if self.missingFields:
            raise IncompleteTrailerError(list(self.missingFields))
