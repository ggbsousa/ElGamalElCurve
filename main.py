import random

#Equipe: Anderson Matheus Passos Paiva, Dalai dos Santos Ribeiro, 
#Gabriel Garcez Barros Sousa, Hevelys Sandes Oliveira e Polyana Bezerra da Costa.


#formula da curva eliptica
#y**2 = x**3 + a*x + b (mod p)
a = 0
b = 7
p = 1461501637330902918203686915170869725397159163571
E = [a,b,p]
#parametros publicos da encriptacao
#a curva definida acima
#um ponto P da curva onde P e o gerador
#a ordem n do subgrupo de E
#n = 1461501637330902918203686915170869725397159163571
P = (338530205676502674729549372677647997389429898939, 842365456698940303598009444920994870805149798382)
G = (218446380845822009133260914022597958688441204967, 1014310923682614467817833035434561095879856320025)

random.seed()

def somaEliptica(pontoP, pontoQ, E):
	x1, y1 = pontoP
	x2, y2 = pontoQ

	if(pontoP == (float("inf"), float("inf"))):
		return pontoQ

	if(pontoQ == (float("inf"), float("inf"))):
		return pontoP

	if(x1 == x2):
		if(y1 != y2):
			return (float("inf"), float("inf"))

	delta = ((y2 - y1)*(pow(x2 - x1,  E[2] - 2, E[2])))%E[2]
	#(y2-y1)/(x2-x1)
	
	x3 = pow((pow(delta, 2) - x1 - x2), 1, E[2])
	y3 = pow((delta*(x1 - x3) - y1), 1, E[2])
	
	return (x3, y3)

def duplicacaoEliptica(pontoP, E):

	if(pontoP == (float("inf"), float("inf"))):
		return pontoP

	x1, y1 = pontoP
	delta = ((3*(pow(x1, 2)) + E[0])*(pow(2*y1, E[2] - 2, E[2])))%E[2]
	x3 = pow((pow(delta, 2) - 2*x1), 1, p)
	y3 = pow((delta*(x1 - x3) - y1), 1, p)

	return (x3, y3)

def intTobinlist(k):
	return [int(x) for x in bin(k)[2:]]

def inverterPonto(pontoP):
	return pontoP[0], -pontoP[1]

def multEscalarEliptica(pontoP, k, E):
	binK = intTobinlist(k)
	pontoQ = pontoP
	for i in reversed(binK):
		pontoQ = duplicacaoEliptica(pontoQ, E)
		if i == 1:
			pontoQ = somaEliptica(pontoQ, pontoP, E)
	return pontoQ

def geraChave(E, P):
	d = random.randint(1,E[2])
	Q = multEscalarEliptica(P,d,E)
	return (Q,d)

def encryption(E, P, Q, M):
	k = random.randint(1, E[2])
	C1 = multEscalarEliptica(P, k, E)
	C2 = somaEliptica(M, multEscalarEliptica(Q, k, E), E)
	return (C1,C2)

def decryption(C1, C2, d, E):
	M = somaEliptica(C2, inverterPonto(multEscalarEliptica(C1,d, E)), E)
	return M

print "Ponto original (mensagem): ", G
Q, d = geraChave(E, P)
print "\nPar de chaves \nPública (Q) = ", Q ,"\nPrivada (d) = ", d
C1, C2 = encryption(E, P, Q, G)
print "\nEncriptação: \nC1 = ", C1,"\nC2 = ", C2
M = decryption(C1, C2, d, E)
print "\nDecriptação (mensagem): ", M
if(G == M):
 print "Mensagem decriptada!"
else:
  print "Mensagem não decriptada."
