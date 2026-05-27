import random
import math
import time
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt

ProbabilidadCrossover = 0.75
ProbabilidadMutación = 0.05
PoblaciónInicial = 10
CiclosPrograma = 20

coef = (2**30)-1

def f(x):   
    return (x/coef)**2

def LlenarCromosomasAlAzar():
    cromosomas = [[0]*30 for _ in range(PoblaciónInicial)]
    for i in range(len(cromosomas)):
        for j in range(30):
            cromosomas[i][j] = random.randint(0,1)
    return cromosomas

# Calcula la desviación estándar del fitness de una generación
# Sirve para ver si la población converge (desv baja) o sigue diversa (desv alta)
def desviacionEstandar(fitness):
    n = len(fitness)
    promedio = sum(fitness) / n
    varianza = sum((fi - promedio)**2 for fi in fitness) / n
    return math.sqrt(varianza)

# Ejecuta una corrida completa del algoritmo genético (20 generaciones)
# Devuelve por cada generación: (maximo, minimo, promedio, desvStd)
def correrAlgoritmo(verbose=True):
    cromosomasHijos = LlenarCromosomasAlAzar()
    estadisticas = []

    for ciclo in range(CiclosPrograma):
        cromosomas = cromosomasHijos

        # Binario a decimal
        decimales = []
        for i in range(len(cromosomas)):
            decimal = 0
            for j in range(30):
                decimal += cromosomas[i][j] * (2**j)
            decimales.append(decimal)

        # Funcion objetivo
        funcionObjetivo = []
        for i in range(len(cromosomas)):
            funcionObjetivo.append(f(decimales[i]))

        sumaFuncionObjetivo = sum(funcionObjetivo)

        # Fitness de cada individuo (qué proporción del total representa)
        fitness = [fo / sumaFuncionObjetivo for fo in funcionObjetivo]

        maximo   = max(funcionObjetivo)
        minimo   = min(funcionObjetivo)
        promedio = sumaFuncionObjetivo / len(funcionObjetivo)
        desvStd  = desviacionEstandar(fitness)
        genMax = cromosomas[funcionObjetivo.index(maximo)]
        genMin = cromosomas[funcionObjetivo.index(minimo)]
        


        

        estadisticas.append((maximo, minimo, promedio, desvStd,genMax,genMin))

        if verbose:
            # Pintar tabla
            print(f"\n{'='*75}")
            print(f"  GENERACIÓN {ciclo+1}")
            print(f"{'='*75}")
            print(f"{'n°':<5} {'cromosoma':<32} {'decimales':<12} {'fObjetivo':<12} {'Fitness':<10}")
            print("-" * 75)
            for i in range(len(cromosomas)):
                cromosoma_str = "".join(map(str, cromosomas[i]))
                print(f"{i:<5} {cromosoma_str:<32} {decimales[i]:<12} {funcionObjetivo[i]:<12.6f} {fitness[i]:<10.6f}")

            print("-" * 75)
            print(f"Suma de f(x):        {sumaFuncionObjetivo:.6f}")
            print(f"Promedio de f(x):    {promedio:.6f}")
            print(f"Maximo:              {maximo:.6f}")
            print(f"Minimo:              {minimo:.6f}")
            print(f"Desv. Std fitness:   {desvStd:.6f}")

            # Muestra el mejor cromosoma de esta generación
            idxMejor = funcionObjetivo.index(maximo)
            print(f"Mejor cromosoma:     {''.join(map(str, cromosomas[idxMejor]))}")
            print(f"Valor decimal:       {decimales[idxMejor]}")  

        #Torneo

        cantJugadores=4
        jugadoresFitness=[]
        jugadores=[]
        cromosomasHijos = []
        
        for i in range(int(len(funcionObjetivo)/2)):
            #Padre 1
            jugadoresFitness=[]
            jugadores=[]
            for cj in range(cantJugadores):
                jugador = cromosomas[random.randint(0, len(cromosomas)-1)]
                indiceJugador = cromosomas.index(jugador)
                fitnessJugador = fitness[indiceJugador]
                jugadores.append([jugador, fitnessJugador])

            maxFitness1 = 0
            maxJugador1 = []
            for jg in range(cantJugadores):
                if maxFitness1 < jugadores[jg][1]:
                    maxFitness1 = jugadores[jg][1]
                    maxJugador1 = jugadores[jg][0]

            #Padre 2
            jugadoresFitness=[]
            jugadores=[]
            for cj in range(cantJugadores):
                jugador = cromosomas[random.randint(0, len(cromosomas)-1)]
                indiceJugador = cromosomas.index(jugador)
                fitnessJugador = fitness[indiceJugador]
                jugadores.append([jugador, fitnessJugador])

            maxFitness2 = 0
            maxJugador2 = []
            for jg in range(cantJugadores):
                if maxFitness2 < jugadores[jg][1]:
                    maxFitness2 = jugadores[jg][1]
                    maxJugador2 = jugadores[jg][0]

             # CrossOver
            hijo1 = []
            hijo2 = []
            
            crossover = random.randint(1, 100)
            if crossover <= ProbabilidadCrossover*100:
                corte = random.randint(1, 28)
                for j in range(len(maxJugador1)):
                    if j <= corte:
                        hijo1.append(maxJugador1[j])
                        hijo2.append(maxJugador2[j])
                    else:
                        hijo1.append(maxJugador2[j])
                        hijo2.append(maxJugador1[j])
            else:
                hijo1 = maxJugador1
                hijo2 = maxJugador2

            cromosomasHijos.append(hijo1)
            cromosomasHijos.append(hijo2)

        # Mutacion
        for i in range(len(cromosomasHijos)):
            mutacion = random.randint(1, 100)
            if mutacion <= ProbabilidadMutación*100:
                genMutado = random.randint(0, 29)
                if cromosomasHijos[i][genMutado] == 1:
                    cromosomasHijos[i][genMutado] = 0
                else:
                    cromosomasHijos[i][genMutado] = 1

    return estadisticas


# Imprime la tabla resumen de máximos, mínimos y promedios por generación
# promediados entre todas las corridas
def imprimirTablaResumen(todasLasEstadisticas, nCorridas):
    print(f"\n{'='*150}")
    print(f"  RESUMEN — {nCorridas} CORRIDAS")
    print(f"{'='*150}")
    print(f"{'Gen':<6} {'cromMax':<35} {'Max':<14} {'crominx':<35} {'Min':<14} {'Promedio':<14} {'Desv.Std':<12}")
    print(f"{'-'*150}")
    for gen in range(CiclosPrograma):
        maximos   = [corrida[gen][0] for corrida in todasLasEstadisticas]
        minimos   = [corrida[gen][1] for corrida in todasLasEstadisticas]
        promedios = [corrida[gen][2] for corrida in todasLasEstadisticas]
        desvs     = [corrida[gen][3] for corrida in todasLasEstadisticas]

        idxMejorCorrida = maximos.index(max(maximos))
        idxPeorCorrida  = minimos.index(min(minimos))
        cromMax = "".join(map(str, todasLasEstadisticas[idxMejorCorrida][gen][4]))
        cromMin = "".join(map(str, todasLasEstadisticas[idxPeorCorrida][gen][5]))
        

        print(f"{gen+1:<6} {cromMax:<35}{sum(maximos)/nCorridas:<14.6f} {cromMin:<35} {sum(minimos)/nCorridas:<14.6f} {sum(promedios)/nCorridas:<14.6f} {sum(desvs)/nCorridas:<12.6f} ")


# Corre el algoritmo N veces y mide el tiempo total y promedio
def ejecutarNCorridas(n, verbose=False):
    todas = []
    inicio = time.time()
    for i in range(n):
        # Solo la primera corrida muestra las tablas detalladas
        todas.append(correrAlgoritmo(verbose=(verbose and i == 0)))
    fin = time.time()
    tiempoTotal = fin - inicio
    tiempoProm  = tiempoTotal / n
    return todas, tiempoTotal, tiempoProm

def graficarEstadisticas(todasLasEstadisticas, nCorridas):
    #Ejecutar este comando en la terminal de VisualStudio para instalar matplotlib si no lo tienen: pip install matplotlib 
    generaciones = list(range(1, CiclosPrograma + 1))
    
    # Extraigo los distintos promedios por generación
    prom_maximos = []
    prom_minimos = []
    prom_promedios = []

    for gen in range(CiclosPrograma):
        # Usamos la misma lógica que en la tabla resumen
        maxs = [corrida[gen][0] for corrida in todasLasEstadisticas]
        mins = [corrida[gen][1] for corrida in todasLasEstadisticas]
        proms = [corrida[gen][2] for corrida in todasLasEstadisticas]
        
        #Calculo el promedio de los maximos, minimos y promedio del promedio por generacion una vez hechas todas las corridas 
        prom_maximos.append(sum(maxs) / nCorridas)
        prom_minimos.append(sum(mins) / nCorridas)
        prom_promedios.append(sum(proms) / nCorridas)

    # Crea la tabla 
    plt.figure(figsize=(10, 6))
    plt.plot(generaciones, prom_maximos, label='Promedio de valores maximos', color='green', marker='o')
    plt.plot(generaciones, prom_promedios, label='Promedio de la Población', color='blue', linestyle='--')
    plt.plot(generaciones, prom_minimos, label='Promedio de valores minimos', color='red', marker='x')
    plt.title(f'Evolución de la Función Objetivo ({nCorridas} Corridas)')
    plt.xlabel('Generación')
    plt.ylabel('Valor Funcion Objetivo f(x)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xticks(range(1, CiclosPrograma + 1))

# ─────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

# Corre 20 veces (la primera con tablas detalladas)
stats20, tTotal20, tProm20 = ejecutarNCorridas(20, verbose=True)
imprimirTablaResumen(stats20, 20)
fitMaxProm20 = sum(corrida[-1][0] for corrida in stats20) / 20
desvProm20 = sum(corrida[-1][3] for corrida in stats20) / 20
print(f"  Fitness Máximo Promedio: {fitMaxProm20:.6f}")
print(f"  Desviación Estándar Promedio: {desvProm20:.6f}")
print(f"  Tiempo total: {tTotal20:.6f}s  |  Tiempo promedio: {tProm20:.6f}s")

# 100 corridas
stats100, tTotal100, tProm100 = ejecutarNCorridas(100)
imprimirTablaResumen(stats100, 100)
fitMaxProm100 = sum(corrida[-1][0] for corrida in stats100) / 100
desvProm100 = sum(corrida[-1][3] for corrida in stats100) / 100
print(f"  Fitness Máximo Promedio: {fitMaxProm100:.6f}")
print(f"  Desviación Estándar Promedio: {desvProm100:.6f}")
print(f"  Tiempo total: {tTotal100:.6f}s  |  Tiempo promedio: {tProm100:.6f}s")

# 200 corridas
stats200, tTotal200, tProm200 = ejecutarNCorridas(200)
imprimirTablaResumen(stats200, 200)
fitMaxProm200 = sum(corrida[-1][0] for corrida in stats200) / 200
desvProm200 = sum(corrida[-1][3] for corrida in stats200) / 200
print(f"  Fitness Máximo Promedio: {fitMaxProm200:.6f}")
print(f"  Desviación Estándar Promedio: {desvProm200:.6f}")
print(f"  Tiempo total: {tTotal200:.6f}s  |  Tiempo promedio: {tProm200:.6f}s")

# Tabla comparativa de tiempos
print(f"\n{'='*55}")
print(f"  TABLA DE TIEMPOS DE EJECUCIÓN")
print(f"{'='*55}")
print(f"  {'Corridas':<12} {'Tiempo total':<18} {'Tiempo promedio'}")
print(f"  {'-'*50}")
print(f"  {'20':<12} {tTotal20:<18.6f} {tProm20:.6f}s")
print(f"  {'100':<12} {tTotal100:<18.6f} {tProm100:.6f}s")
print(f"  {'200':<12} {tTotal200:<18.6f} {tProm200:.6f}s")
print(f"{'='*55}")


# Mostrar gráficas de evolución para cada cantidad de corridas, el plt.show lo dejo para el final y no dentro de graficarEstadisticas() para que se muestren todos los gráficos juntos y no uno por uno
graficarEstadisticas(stats20, 20)
graficarEstadisticas(stats100, 100)
graficarEstadisticas(stats200, 200)
print("Mostrando gráficos...")
plt.show()