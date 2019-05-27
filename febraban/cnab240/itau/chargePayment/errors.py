from ....errors import BaseError


class ChargePaymentBaseError(BaseError):
    pass


############ HEADER ############
class HeaderError(ChargePaymentBaseError):
    pass


class IncompleteHeaderError(HeaderError):
    def __str__(self):
        return "Header in ChargePayment file missing: {missingInformation}".format(
            missingInformation=self.args,
        )


############ LOT-HEADER ############
class LotHeaderError(ChargePaymentBaseError):
    pass


class IncompleteLotHeaderError(LotHeaderError):
    def __str__(self):
        return "LotHeader in ChargePayment file missing: {missingInformation}".format(
            missingInformation=self.args,
        )


############ SEGMENT J ############
class SegmentJError(ChargePaymentBaseError):
    pass


class IncompleteSegmentJError(SegmentJError):
    def __str__(self):
        return "SegmentJ in ChargePayment file missing: {missingInformation}".format(
            missingInformation=self.args,
        )


############ SEGMENT J-52 ############
class SegmentJ52Error(ChargePaymentBaseError):
    pass


class IncompleteSegmentJ52Error(SegmentJ52Error):
    def __str__(self):
        return "SegmentJ52 in ChargePayment file missing: {missingInformation}".format(
            missingInformation=self.args,
        )


############ LOT-TRAILER ############
class LotTrailerError(ChargePaymentBaseError):
    pass


class IncompleteLotTrailerError(LotTrailerError):
    def __str__(self):
        return "LotTrailer in ChargePayment file missing: {missingInformation}".format(
            missingInformation=self.args,
        )


############ TRAILER ############
class TrailerError(ChargePaymentBaseError):
    pass


class IncompleteTrailerError(TrailerError):
    def __str__(self):
        return "Trailer in ChargePayment file missing: {missingInformation}".format(
            missingInformation=self.args,
        )
