# coding: utf-8

from ....row import Row, RowStruct, emptyStruct
from ....characterType import numeric, alphaNumeric
from ..errors import IncompleteSegmentJ52Error


class SegmentJ52(object):

    def __init__(self):
        self.content = " " * 240
        self.defaultValues()

        self.missingFields = {
            "SenderBank",
            "Sender",
            "PositionInLot",
        }

    def defaultValues(self):
        structure = [
            # Empty fields or auto-filled by the bank
            emptyStruct(187, 240, alphaNumeric),

            # Fixed fields
            RowStruct(7, 8, 1, numeric, "3"),  # TIPO DE REGISTRO
            RowStruct(8, 13, 5, numeric, 1),  # INDEX DO REGISTRO
            RowStruct(13, 14, 1, alphaNumeric, "J"),  # CÓDIGO DE SEGMENTO
            RowStruct(14, 17, 3, numeric, "000"),  # TIPO DE MOVIMENTO
            RowStruct(17, 19, 2, numeric, "52"),  # IDENTIFICAÇÃO DO REGISTRO OPCIONAL

            # Unused fields
            emptyStruct(75, 76, numeric),
            emptyStruct(76, 91, numeric),
            emptyStruct(91, 131, alphaNumeric),
            emptyStruct(131, 132, numeric),
            emptyStruct(132, 147, numeric),
            emptyStruct(147, 187, alphaNumeric),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setSenderBank(self, bank):
        self.missingFields.discard("SenderBank")
        structure = [
            RowStruct(0, 3, 3, numeric, bank.bankId),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setSender(self, user):
        self.missingFields.discard("Sender")
        structure = [
            RowStruct(19, 20, 1, numeric, "1" if len(user.identifier) == 11 else "2"),
            RowStruct(20, 35, 15, numeric, user.identifier),
            RowStruct(35, 75, 40, alphaNumeric, user.name)
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setPositionInLot(self, index):
        self.missingFields.discard("PositionInLot")
        structure = [
            RowStruct(3, 7, 4, numeric, index),
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def validate(self):
        if self.missingFields:
            raise IncompleteSegmentJ52Error(list(self.missingFields))

