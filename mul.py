from z3 import *
def mul_1(a,b): 
	userBalance=100
	check=	BitVec("check", 32)
	c=add(a,b)+a
	return c
def mul_2(a,b): 
	userBalance=100
	check=	BitVec("check", 32)
	c=a+b
	return c
def mul_3(a,b): 
	userBalance=100
	check=	BitVec("check", 32)
	c=a+b
	return c
def mul_4(a,b): 
	userBalance=100
	check=	BitVec("check", 32)
	c=add(a,b)+a
	return c
def mul_5(a,b): 
	userBalance=100
	check=	BitVec("check", 32)
	for i in range(0,a,1):
		c=2/add(a,2)

	return c
def mul(a,b):
	if a==0 and b==1:mul_1(a,b)
	if not a==0 and a>=b and b==1:mul_2(a,b)
	if not a==0 and a>=b and not b==1:mul_3(a,b)
	if a==0 and not b==1:mul_4(a,b)
	if not a==0 and not a>=b:mul_5(a,b)
