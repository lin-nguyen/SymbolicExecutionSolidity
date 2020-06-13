import collections
class lst(list): 
    def push(self, something): 
        super().append(something)

class order:
    def __init__ (self, token, time, quantity, price):
        self.token = token 
        self.time = time 
        self.quantity = quantity
        self.price = price
def getBalance(): 
    #return 1 câu request API để get Balance
    return 0;
now = None
totalToken = {'mathematic': 3, 'physics':12 , 'computer': 5}
users = ['0xBBBB', 'OxCCCC', 'OxDDDD']
ownerToOrderList = collections.defaultdict(lambda : 0)
ownerToOrderList['0xBBBB']= lst([order('mathematic', 0, 2, 0.1)])


ownerToBalance= collections.defaultdict(lambda : 0)
ownerToBalance['0xAAAA'] = 100 # balance admin
ownerToBalance['0xBBBB'] = 20
ownerToBalance['0xcAd4954fA4cb431bAD9a84c3ae8e279fe069A6De']=30
class Msg: 
    def __init__ (self, sender, customer, value ): 
        self.customer = customer
        self.sender = sender
        self.value = value 
        ownerToBalance[customer] -= value
msg = Msg('0xAAAA', '0xBBBB', 0.3) # địa chỉ người gửi vào và số tiền thanh toán giao dịch
ownerToBalance['0x0000'] =  getBalance()+ msg.value
admin = '0xAAAA'
this  ='0x0000' # balance của hợp đồng

def getSumToken(totalToken): 
    sum=0
    if type(totalToken) is not lst: 
        for x in totalToken.keys(): 
            sum+= totalToken[x]
    else: 
        for x in totalToken:
            sum+= x.quantity
    return sum
def sendtoken(_token, _quantity): # only for admin
    totalToken[_token]-=_quantity
class Address: 
    
    def __init__ (self, adr): 
        self.adr = adr 
        self.balance = ownerToBalance[self.adr]
    def transfer(self, amount ): # chuyển số tiền về adress này     
        ownerToBalance[self.adr]+= amount
        ownerToBalance['0x0000']-=amount
class base: 
    def address(self,adr): 
        return Address(adr)
    def require(self,something, str="None"): 
        pass
