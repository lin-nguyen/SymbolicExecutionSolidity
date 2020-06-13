def run(): 
    from solidity_parser import symbolic, parser
    asttree = parser.parse_file("BookStore.sol")
    f = open("renderToPython.py", 'w')
    f.write(open('init.py').read())
    f.close()
    f = open("renderToPython.py", 'a+')
    dse = symbolic.SymbolicExecution(asttree,f )
    listFunc= dse.run()
    f.close()
    import renderToPython
    transaction = renderToPython.BookStore()
    init = ('0xAAAA',
        (renderToPython.ownerToBalance['0xAAAA'], 
        renderToPython.getSumToken(renderToPython.totalToken)), 

            '0xBBBB',
        (renderToPython.ownerToBalance['0xBBBB']+renderToPython.msg.value,
        renderToPython.getSumToken(renderToPython.ownerToOrderList['0xBBBB']) ))
    transaction.implementTransaction('0xBBBB', 'mathematic', 1 )
    final = ('0xAAAA',(renderToPython.ownerToBalance['0xAAAA'], 
            renderToPython.getSumToken(renderToPython.totalToken)), 
            '0xBBBB',(renderToPython.ownerToBalance['0xBBBB'],
            renderToPython.getSumToken(renderToPython.ownerToOrderList['0xBBBB']) ))
    return init, final
result = run()
print(result[0])
print(result[1])