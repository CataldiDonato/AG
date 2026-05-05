from email.errors import MultipartConversionError 
import random

ProbabilidadCrossover = 0.75
ProbabilidadMutación = 0.05
PoblaciónInicial= 10 
CiclosPrograma= 20

cromosomasHijos= [[0]*30 for _ in range(PoblaciónInicial)]

coef = (2**30)-1

def f(x):   
    return (x/coef)**2

def LlenarCromosomasAlAzar():
    for i in range(len(cromosomasHijos)):
        for j in range(30):
            cromosomasHijos[i][j]=random.randint(0,1)


LlenarCromosomasAlAzar()

for ciclo in range(CiclosPrograma):
    cromosomas=cromosomasHijos
    #Binario a decimal
    decimales=[]
    for i in range(len(cromosomas)):
        decimal = 0
        for j in range(30):
            decimal += cromosomas[i][j] * (2**j)
        decimales.append(decimal)
    
    #Funcion objetivo
    funcionObjetivo=[]      
    for i in range(len(cromosomas)):
        funcionObjetivo.append(f(decimales[i]))
    
    #Suma funcion objetivo
    sumaFuncionObjetivo=sum(funcionObjetivo)
    
    #Pintar tabla
    print(f"{"n°":<5} {"cromosoma":<30} {"decimales":<10} {"fObjetivo":<10} {"Fitness":<10}")
    for i in range(len(cromosomas)):
        cromosoma_str = "".join(map(str, cromosomas[i]))
        print(f"{i:<5} {cromosoma_str:<15} {decimales[i]:<10} {funcionObjetivo[i]:<10.4f} {funcionObjetivo[i]/sumaFuncionObjetivo:<10.4f}")

    print("-" * 70) # Línea divisoria
    print(f"Suma de f(x):      {sumaFuncionObjetivo:.4f}")
    print(f"Promedio de f(x):  {sumaFuncionObjetivo/len(cromosomas):.4f}")
    print(f"Maximo:            {max(funcionObjetivo):.4f}")   

    #Ruleta
    ruleta=[]
    for i in range(len(funcionObjetivo)):
        for j in range(round(funcionObjetivo[i]/sumaFuncionObjetivo*100)):
            ruleta.append(i)

    #CrossOver
    cromosomasHijos=[]
    for i in range(int(len(funcionObjetivo)/2)):
        
        hijo1=[]
        hijo2=[]
        padre1=cromosomas[ruleta[random.randint(0,len(ruleta)-1)]]
        padre2=cromosomas[ruleta[random.randint(0,len(ruleta)-1)]]
        crossover=random.randint(1,100)
        if crossover <= ProbabilidadCrossover*100:  
            corte=random.randint(1,28)
            for j in range(len(padre1)):
                if j<=corte:
                    hijo1.append(padre1[j])
                    hijo2.append(padre2[j])
                else:
                    hijo1.append(padre2[j])
                    hijo2.append(padre1[j])
        else:
            hijo1=padre1
            hijo2=padre2

        cromosomasHijos.append(hijo1)
        cromosomasHijos.append(hijo2)

    #Mutacion

    for i in range(len(cromosomasHijos)):
        mutacion=random.randint(1,100)
        if mutacion <= ProbabilidadMutación*100:
            genMutado=random.randint(0,29)
            if cromosomasHijos[i][genMutado] == 1:
                cromosomasHijos[i][genMutado]=0
            else: cromosomasHijos[i][genMutado]=1
    


            


    

