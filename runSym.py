from z3 import *
userBalance=100
adminBalance=100
userToken=0
adminToken=1
amountE=15
i=BitVec("i", 32)
userAdr="0xAAAA"
adminAdr="0xBBBB"
check=False
finalState = (userBalance, userAdr, userToken)
(userBalance, userAdr, userToken)
