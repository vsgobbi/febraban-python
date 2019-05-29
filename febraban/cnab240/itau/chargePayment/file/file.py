from datetime import datetime
from ....libs.fileUtils import FileUtils
from .header import Header
from .trailer import Trailer


class File(object):

    def __init__(self):
        self.header = Header()
        self.lots = []
        self.trailer = Trailer()

    def add(self, lot):
        lot.setPositionInLot(index=len(self.lots)+1)
        self.lots.append(lot)

    def toString(self, currentDatetime=None):
        self.header.setGeneratedFileDate(currentDatetime or datetime.now())
        self.trailer.setNumberOfLotsAndRegisters(len(self.lots))

        lotsContent = "\r\n".join(lot.toString() for lot in self.lots)
        return "%s\r\n%s\r\n%s\r\n" % (self.header.content, lotsContent, self.trailer.content)

    def setSender(self, user):
        self.header.setSender(user)
        self.header.setSenderBank(user.bank)
        self.trailer.setSenderBank(user.bank)

        for lot in self.lots:
            lot.setSender(user)

    def validate(self):
        self.header.validate()
        for lot in self.lots:
            lot.validate()
        self.trailer.validate()

    def output(self, fileName, path="..", content=None, currentDatetime=None):
        with FileUtils.create(name=fileName, path=path) as fl:
            fl.write(self.toString(currentDatetime or datetime.now()) if not content else content)
