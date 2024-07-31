import random
def gera_numeros():
    i = 0
    valores = []
    while i <= 2:
        num = random.randint(1,10)
        if num not in valores:
            valores.append(num)
            i+=1
    sorteado = random.randint(0,2)
    resultado = (valores[sorteado] + valores[sorteado - 1])
    random.shuffle(valores)
    valores.append(resultado)
    return valores