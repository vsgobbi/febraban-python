from datetime import date, timedelta


class BarCode(str):
    baseDate = date(year=1997, month=10, day=7)

    def __init__(self, barCodeNumber):
        super(BarCode, self).__init__()
        barCodeNumber = str(barCodeNumber)
        if len(barCodeNumber) != 44:
            raise ValueError("BarCode number must be 44 characters long.")
        self.raw = barCodeNumber

        self.bankId = self.raw[0:3]
        self.currency = self.raw[3:4]
        self.dac = self.raw[4:5]
        self.dueFactor = self.raw[5:9]
        self.value = self.raw[9:19]
        self.freeField = self.raw[19:44]

        dueDays = int(self.dueFactor)
        timeDelta = timedelta(days=dueDays)

        self.dueDate = self.baseDate + timeDelta

    def __str__(self):
        return self.raw


if __name__ == '__main__':
    code = BarCode("34197791600000721441091002168647307144464000")
    print len(code)
    print "My barCode: %r" % code
