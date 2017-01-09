# coding=utf-8
import random

#formula da curva eliptica
#y**2 = x**3 + a*x + b (mod p)
a = 0
b = 7
p = 3
E = [a,b,p]
#parametros publicos da encriptacao
#a curva definida acima
#um ponto P da curva onde P e o gerador
#a ordem n do subgrupo de E
n = 1461501637330902918203686915170869725397159163571
P = (338530205676502674729549372677647997389429898939, 842365456698940303598009444920994870805149798382)
G = (218446380845822009133260914022597958688441204967, 1014310923682614467817833035434561095879856320025)

random.seed()

def somaEliptica(pontoP, pontoQ, p):
	x1, y1 = pontoP
	x2, y2 = pontoQ

	if(pontoP == (float("inf"), float("inf"))):
		return pontoQ

	if(pontoQ == (float("inf"), float("inf"))):
		return pontoP

	if(x1 == x2):
		if(y1 != y2):
			return (float("inf"), float("inf"))

	delta = (y2-y1)/(x2-x1)
	x3 = pow((pow(delta, 2) - x1 - x2), 1, p)
	y3 = pow((delta*(x1 - x3) - y1), 1, p)

	return (x3, y3)

def duplicacaoEliptica(pontoP, p, a):

	if(pontoP == (float("inf"), float("inf"))):
		return pontoP

	x1, y1 = pontoP
	delta = (3*pow(x1,2) + a)/(2*y1)
	x3 = pow((pow(delta, 2) - 2*x1), 1, p)
	y3 = pow((delta*(x1 - x3) - y1), 1, p)

	return (x3, y3)

def intTobinlist(k):
	return [int(x) for x in bin(k)[2:]]

def inverterPonto(pontoP):
	return pontoP[0], -pontoP[1]

def multEscalarEliptica(pontoP, k):
	binK = intTobinlist(k)
	pontoQ = pontoP
	for i in reversed(binK):
		pontoQ = duplicacaoEliptica(pontoQ, p, a)
		if i == 1:
			pontoQ = somaEliptica(pontoQ, pontoP, p)
	return pontoQ

def geraChave(E, P, n):
	d = random.randint(1,n-1)
	Q = multEscalarEliptica(P,d)
	return (Q,d)

def encryption(E, P, n, Q, M):
	k = random.randint(1, n-1)
	C1 = multEscalarEliptica(P, k)
	C2 = somaEliptica(M, multEscalarEliptica(Q, k), E[2])
	return (C1,C2)

def decryption(C1, C2, d, E):
	M = somaEliptica(C1, inverterPonto(multEscalarEliptica(C2,d)), E[2])
	return M

Q, d = geraChave(E, P, n)
print Q, d
C1, C2 = encryption(E, P, n, Q, G)
print C1, C2
M = decryption(C1, C2, d, E)
print M