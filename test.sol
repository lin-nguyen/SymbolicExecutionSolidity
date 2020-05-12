pragma solidity >=0.4.24; 
contract SimpleContract { 
    int userBalance = 100; 
    int adminBalance = 100; 
    int userToken = 0; 
    int adminToken = 1; 
    int amountE=15;
    int i ;
    address userAdr = 0xAAAA;
    address adminAdr = 0xBBBB;
    bool check = false ;
    function sendeth() public returns (string memory){
        if (userBalance > amountE){
            userBalance = userBalance - amountE;
            adminBalance = adminBalance + amountE; 
            check = true;
            return "Success"; 
        }
        else{
            if(check==false){
                int i;
                userBalance = userBalance - amountE*i;
            }
            else {

            }
        }
        
    }
}