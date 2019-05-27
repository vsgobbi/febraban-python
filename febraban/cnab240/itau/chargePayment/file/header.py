# coding: utf-8

from datetime import datetime
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
        }

    def defaultValues(self):
        structure = [
            # Empty fields or auto-filled by the bank
            emptyStruct(3, 7, numeric),  # CÓDIGO DO LOTE DE SERVIÇO
            emptyStruct(8, 14, alphaNumeric),
            emptyStruct(32, 52, alphaNumeric),
            emptyStruct(57, 58, alphaNumeric),
            emptyStruct(70, 71, alphaNumeric),
            emptyStruct(132, 142, alphaNumeric),
            emptyStruct(157, 166, numeric),
            emptyStruct(166, 171, numeric),  # DENSIDADE DE GRAVAÇÃO DO ARQUIVO - NOTA 2
            emptyStruct(171, 240, alphaNumeric),

            # Fixed fields
            RowStruct(7, 8, 1, numeric, "0"),  # TIPO DE REGISTRO
            RowStruct(14, 17, 3, numeric, "081"),  # VERSÃO DO LAYOUT DE ARQUIVO
            RowStruct(142, 143, 1, numeric, "1"),  # IDENTIFICAÇÃO COMO ARQUIVO DE REMESSA
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def setSender(self, user):
        self.missingFields.discard("Sender")
        structure = [
            RowStruct(17, 18, 1, numeric, "1" if len(user.identifier) == 11 else "2"),
            RowStruct(18, 32, 14, numeric, user.identifier),
            RowStruct(72, 102, 30, alphaNumeric, user.name),
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

    def setGeneratedFileDate(self, date):
        self.missingFields.discard("GeneratedDate")
        structure = [
            RowStruct(143, 151, 8, numeric, date.strftime("%d%m%Y")),  # Dia que o arquivo foi gerado
            RowStruct(151, 157, 6, numeric, date.strftime("%H%M%S")),  # Horario que o arquivo foi gerado
        ]
        self.content = Row.setStructs(structs=structure, content=self.content)

    def validate(self):
        if self.missingFields:
            raise IncompleteHeaderError(len(self.missingFields))
