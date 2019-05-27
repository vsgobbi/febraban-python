# coding: utf-8

from febraban.cnab240.itau.chargePayment import File, ChargePayment
from febraban.cnab240.user import User, UserAddress, UserBank


sender = User(
    name="STARK BANK SA",
    identifier="20018183000180",
    bank=UserBank(
        bankId="341",
        branchCode="7307",
        accountNumber="14444",
        accountVerifier="9"
    ),
    address=UserAddress(
        streetLine1="AV PAULISTA 10000",
        city="SAO PAULO",
        stateCode="SP",
        zipCode="01310000"
    )
)

barCodes = {
    "testError": "34196792100000005451090057233457307144464000",
    "test1": "34195789900000001001090000217527307144464000",
    "test2": "34191789900000001001090000217607307144464000",
    "test3": "34192789900000001001090000217787307144464000",
}

for name, barCode in barCodes.iteritems():
    fileObj = File()
    fileObj.setSender(sender)

    chargePayment = ChargePayment()
    chargePayment.setSender(sender)
    chargePayment.setBarCode(barCode)
    chargePayment.setIdentifier("DEV-1234567890-" + name)
    chargePayment.setPaymentKind("98")
    fileObj.add(chargePayment)

    fileObj.output(fileName=name + '.REM')
