pragma solidity >=0.4.24; 
contract SimpleContract { 
    int etherC;

    int etherA = 100; 
    int etherB = etherA; 
    function sendeth(int amountE, address A, address B) public returns (string memory){
       if(1==1){
           etherA=1;
           
           
       }
       else {
           etherA=2;
            if(etherA==etherB){
                etherA=3;
            }      
            else {
                if (etherA==4){
                    etherA=1;
                }
                else etherA=2;
            }
       }
       
    }
}