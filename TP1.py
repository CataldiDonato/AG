"""
–Probabilidad de Crossover = 0,75
–Probabilidad de Mutación = 0,05
–Población Inicial: 10 individuos
–Ciclos del programa: 20
–Método de Selección: Ruleta
–Método de Crossover: 1 Punto
–Método de Mutación: invertida
"""

import random

ProbabilidadCrossover = 0.75
ProbabilidadMutación = 0.05
PoblaciónInicial= 10 
CiclosPrograma= 20

cromosomas= [[0]*30 for _ in range(PoblaciónInicial)]

coef = (2**30)-1

def f(x):
    return (x/coef)**2

def LlenarCromosomasAlAzar():

    for i in range(len(cromosomas)):
        for j in range(30):
            cromosomas[i][j]=random.randint(0,1)

def MostrarCromosomas():
    for i in range(len(cromosomas)):
        print(cromosomas[i])

# Pasar de binario a decimal
def BinarioDecimal():
    dec=[]
    for i in range(len(cromosomas)):
        decimal = 0
        for j in range(30):
            decimal += cromosomas[i][j] * (2**j)
        dec.append(decimal)
    
    return dec

def FuncionesObjetivo(decimales):
    fo=[]

    for i in range(len(cromosomas)):
        fo.append(f(decimales[i]))
    
    return fo

def MostrarFuncionesObjetivo(fObjetivo):
    for i in range(len(fObjetivo)):
        print(fObjetivo[i])

def SumaFuncionesObjetivos(FO):
    return sum(FO)

def PrintTabla(decimales,fObjetivo,sumafObjetivo):
    
    print(f"{"n°":<5} {"cromosoma":<30} {"decimales":<10} {"fObjetivo":<10} {"Fitness":<10}")
    for i in range(len(cromosomas)):
        cromosoma_str = "".join(map(str, cromosomas[i]))
        print(f"{i:<5} {cromosoma_str:<15} {decimales[i]:<10} {fObjetivo[i]:<10.4f} {fObjetivo[i]/sumafObjetivo:<10.4f}")

    print("-" * 70) # Línea divisoria
    print(f"Suma de f(x):      {sumafObjetivo:.4f}")
    print(f"Promedio de f(x):  {sumafObjetivo/len(cromosomas):.4f}")
    print(f"Maximo:            {max(fObjetivo):.4f}")   

def Prueba():
    decimales=BinarioDecimal()
    fObjetivo=FuncionesObjetivo(decimales)
    sumafObjetivo=SumaFuncionesObjetivos(fObjetivo)
    return decimales,fObjetivo,sumafObjetivo

def ruleta(funcionObjetivo,sumaFuncionObjetivo):
    ruleta=[]
    for i in range(len(funcionObjetivo)):
        for j in range(round(funcionObjetivo[i]/sumaFuncionObjetivo)):
            ruleta.append(i)
    numero = random.randint(1, len(funcionObjetivo))
    return 

LlenarCromosomasAlAzar()
d,f,s=Prueba()
PrintTabla(d,f,s)