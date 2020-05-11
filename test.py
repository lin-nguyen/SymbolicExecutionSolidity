
from solidity_parser import parser
from solidity_parser import symbolic
asttree = parser.parse_file("test.sol")
dse = symbolic.SymbolicExecution(asttree)
dse.run()
#print(asttree)