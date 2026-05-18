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

# ─────────────────────────────────────────────
#  ALGORITMO — RULETA
# ─────────────────────────────────────────────

def correrAlgoritmoRuleta(verbose=True):
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

        estadisticas.append((maximo, minimo, promedio, desvStd, genMax, genMin))

        if verbose:
            print(f"\n{'='*75}")
            print(f"  GENERACIÓN {ciclo+1} — RULETA")
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

            idxMejor = funcionObjetivo.index(maximo)
            print(f"Mejor cromosoma:     {''.join(map(str, cromosomas[idxMejor]))}")
            print(f"Valor decimal:       {decimales[idxMejor]}")

        # Ruleta
        ruleta = []
        for i in range(len(funcionObjetivo)):
            for j in range(round(fitness[i]*100)):
                ruleta.append(i)

        # CrossOver
        cromosomasHijos = []
        for i in range(int(len(funcionObjetivo)/2)):
            hijo1 = []
            hijo2 = []
            padre1 = cromosomas[ruleta[random.randint(0, len(ruleta)-1)]]
            padre2 = cromosomas[ruleta[random.randint(0, len(ruleta)-1)]]
            crossover = random.randint(1, 100)
            if crossover <= ProbabilidadCrossover*100:
                corte = random.randint(1, 28)
                for j in range(len(padre1)):
                    if j <= corte:
                        hijo1.append(padre1[j])
                        hijo2.append(padre2[j])
                    else:
                        hijo1.append(padre2[j])
                        hijo2.append(padre1[j])
            else:
                hijo1 = padre1
                hijo2 = padre2

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


# ─────────────────────────────────────────────
#  ALGORITMO — TORNEO
# ─────────────────────────────────────────────

def correrAlgoritmoTorneo(verbose=True):
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

        estadisticas.append((maximo, minimo, promedio, desvStd, genMax, genMin))

        if verbose:
            print(f"\n{'='*75}")
            print(f"  GENERACIÓN {ciclo+1} — TORNEO")
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

            idxMejor = funcionObjetivo.index(maximo)
            print(f"Mejor cromosoma:     {''.join(map(str, cromosomas[idxMejor]))}")
            print(f"Valor decimal:       {decimales[idxMejor]}")

        # Torneo
        cromosomasHijos = []
        for i in range(int(len(funcionObjetivo)/4)):

            # Pareja 1
            padre1 = cromosomas[random.randint(0, len(cromosomas)-1)]
            padre2 = cromosomas[random.randint(0, len(cromosomas)-1)]
            indicePadre1 = cromosomas.index(padre1)
            indicePadre2 = cromosomas.index(padre2)
            fitnessPadre1 = fitness[indicePadre1]
            fitnessPadre2 = fitness[indicePadre2]

            if fitnessPadre1 > fitnessPadre2:
                padreGanador1 = padre1
            else:
                padreGanador1 = padre2

            # Pareja 2
            padre3 = cromosomas[random.randint(0, len(cromosomas)-1)]
            padre4 = cromosomas[random.randint(0, len(cromosomas)-1)]
            indicePadre3 = cromosomas.index(padre3)
            indicePadre4 = cromosomas.index(padre4)
            fitnessPadre3 = fitness[indicePadre3]
            fitnessPadre4 = fitness[indicePadre4]

            if fitnessPadre3 > fitnessPadre4:
                padreGanador2 = padre3
            else:
                padreGanador2 = padre4

            hijo1 = padreGanador1
            hijo2 = padreGanador2

            cromosomasHijos.append(padreGanador2)
            cromosomasHijos.append(padreGanador1)
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


# ─────────────────────────────────────────────
#  ALGORITMO — ELITISMO
# ─────────────────────────────────────────────

def correrAlgoritmoElitismo(verbose=True):
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

        estadisticas.append((maximo, minimo, promedio, desvStd, genMax, genMin))

        if verbose:
            print(f"\n{'='*75}")
            print(f"  GENERACIÓN {ciclo+1} — ELITISMO")
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

            idxMejor = funcionObjetivo.index(maximo)
            print(f"Mejor cromosoma:     {''.join(map(str, cromosomas[idxMejor]))}")
            print(f"Valor decimal:       {decimales[idxMejor]}")

        # Elitismo: guardar los 2 mejores cromosomas directamente
        indicesOrdenados = sorted(range(len(funcionObjetivo)), key=lambda i: funcionObjetivo[i], reverse=True)
        elite = [cromosomas[indicesOrdenados[0]][:], cromosomas[indicesOrdenados[1]][:]]

        # Ruleta
        ruleta = []
        for i in range(len(funcionObjetivo)):
            for j in range(round(fitness[i]*100)):
                ruleta.append(i)

        # CrossOver — genera 8 hijos (los otros 2 los ocupa la elite)
        cromosomasHijos = []
        for i in range(int((len(funcionObjetivo) - 2) / 2)):
            hijo1 = []
            hijo2 = []
            padre1 = cromosomas[ruleta[random.randint(0, len(ruleta)-1)]]
            padre2 = cromosomas[ruleta[random.randint(0, len(ruleta)-1)]]
            crossover = random.randint(1, 100)
            if crossover <= ProbabilidadCrossover*100:
                corte = random.randint(1, 28)
                for j in range(len(padre1)):
                    if j <= corte:
                        hijo1.append(padre1[j])
                        hijo2.append(padre2[j])
                    else:
                        hijo1.append(padre2[j])
                        hijo2.append(padre1[j])
            else:
                hijo1 = padre1[:]
                hijo2 = padre2[:]

            cromosomasHijos.append(hijo1)
            cromosomasHijos.append(hijo2)

        # Mutacion (solo a los hijos, no a la elite)
        for i in range(len(cromosomasHijos)):
            mutacion = random.randint(1, 100)
            if mutacion <= ProbabilidadMutación*100:
                genMutado = random.randint(0, 29)
                if cromosomasHijos[i][genMutado] == 1:
                    cromosomasHijos[i][genMutado] = 0
                else:
                    cromosomasHijos[i][genMutado] = 1

        # Incorporar la elite directamente a la nueva generación
        cromosomasHijos.append(elite[0])
        cromosomasHijos.append(elite[1])

    return estadisticas


# ─────────────────────────────────────────────
#  FUNCIONES COMUNES
# ─────────────────────────────────────────────

def imprimirTablaResumen(todasLasEstadisticas, nCorridas, metodo):
    print(f"\n{'='*150}")
    print(f"  RESUMEN — {nCorridas} CORRIDAS — {metodo}")
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


def ejecutarNCorridas(n, algoritmo, verbose=False):
    todas = []
    inicio = time.time()
    for i in range(n):
        todas.append(algoritmo(verbose=(verbose and i == 0)))
    fin = time.time()
    tiempoTotal = fin - inicio
    tiempoProm  = tiempoTotal / n
    return todas, tiempoTotal, tiempoProm

def graficarEstadisticas(todasLasEstadisticas, nCorridas, metodo):
    #Ejecutar este comando en la terminal de VisualStudio para instalar matplotlib si no lo tienen: pip install matplotlib
    generaciones = list(range(1, CiclosPrograma + 1))

    prom_maximos = []
    prom_minimos = []
    prom_promedios = []

    for gen in range(CiclosPrograma):
        maxs = [corrida[gen][0] for corrida in todasLasEstadisticas]
        mins = [corrida[gen][1] for corrida in todasLasEstadisticas]
        proms = [corrida[gen][2] for corrida in todasLasEstadisticas]

        #Calculo el promedio de los maximos, minimos y promedio del promedio por generacion una vez hechas todas las corridas
        prom_maximos.append(sum(maxs) / nCorridas)
        prom_minimos.append(sum(mins) / nCorridas)
        prom_promedios.append(sum(proms) / nCorridas)

    plt.figure(figsize=(10, 6))
    plt.plot(generaciones, prom_maximos, label='Promedio de valores maximos', color='green', marker='o')
    plt.plot(generaciones, prom_promedios, label='Promedio de la Población', color='blue', linestyle='--')
    plt.plot(generaciones, prom_minimos, label='Promedio de valores minimos', color='red', marker='x')
    plt.title(f'Evolución de la Función Objetivo — {metodo} ({nCorridas} Corridas)')
    plt.xlabel('Generación')
    plt.ylabel('Valor Funcion Objetivo f(x)')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.xticks(range(1, CiclosPrograma + 1))


# ─────────────────────────────────────────────
#  PROGRAMA PRINCIPAL
# ─────────────────────────────────────────────

# ── RULETA ──
print("\n" + "█"*75)
print("  MÉTODO: RULETA")
print("█"*75)

statsR20, tTotalR20, tPromR20 = ejecutarNCorridas(20, correrAlgoritmoRuleta, verbose=True)
imprimirTablaResumen(statsR20, 20, "RULETA")
print(f"  Tiempo total: {tTotalR20:.6f}s  |  Tiempo promedio: {tPromR20:.6f}s")

statsR100, tTotalR100, tPromR100 = ejecutarNCorridas(100, correrAlgoritmoRuleta)
imprimirTablaResumen(statsR100, 100, "RULETA")
print(f"  Tiempo total: {tTotalR100:.6f}s  |  Tiempo promedio: {tPromR100:.6f}s")

statsR200, tTotalR200, tPromR200 = ejecutarNCorridas(200, correrAlgoritmoRuleta)
imprimirTablaResumen(statsR200, 200, "RULETA")
print(f"  Tiempo total: {tTotalR200:.6f}s  |  Tiempo promedio: {tPromR200:.6f}s")

print(f"\n{'='*55}")
print(f"  TABLA DE TIEMPOS — RULETA")
print(f"{'='*55}")
print(f"  {'Corridas':<12} {'Tiempo total':<18} {'Tiempo promedio'}")
print(f"  {'-'*50}")
print(f"  {'20':<12} {tTotalR20:<18.6f} {tPromR20:.6f}s")
print(f"  {'100':<12} {tTotalR100:<18.6f} {tPromR100:.6f}s")
print(f"  {'200':<12} {tTotalR200:<18.6f} {tPromR200:.6f}s")
print(f"{'='*55}")


# ── TORNEO ──
print("\n" + "█"*75)
print("  MÉTODO: TORNEO")
print("█"*75)

statsT20, tTotalT20, tPromT20 = ejecutarNCorridas(20, correrAlgoritmoTorneo, verbose=True)
imprimirTablaResumen(statsT20, 20, "TORNEO")
print(f"  Tiempo total: {tTotalT20:.6f}s  |  Tiempo promedio: {tPromT20:.6f}s")

statsT100, tTotalT100, tPromT100 = ejecutarNCorridas(100, correrAlgoritmoTorneo)
imprimirTablaResumen(statsT100, 100, "TORNEO")
print(f"  Tiempo total: {tTotalT100:.6f}s  |  Tiempo promedio: {tPromT100:.6f}s")

statsT200, tTotalT200, tPromT200 = ejecutarNCorridas(200, correrAlgoritmoTorneo)
imprimirTablaResumen(statsT200, 200, "TORNEO")
print(f"  Tiempo total: {tTotalT200:.6f}s  |  Tiempo promedio: {tPromT200:.6f}s")

print(f"\n{'='*55}")
print(f"  TABLA DE TIEMPOS — TORNEO")
print(f"{'='*55}")
print(f"  {'Corridas':<12} {'Tiempo total':<18} {'Tiempo promedio'}")
print(f"  {'-'*50}")
print(f"  {'20':<12} {tTotalT20:<18.6f} {tPromT20:.6f}s")
print(f"  {'100':<12} {tTotalT100:<18.6f} {tPromT100:.6f}s")
print(f"  {'200':<12} {tTotalT200:<18.6f} {tPromT200:.6f}s")
print(f"{'='*55}")


# ── ELITISMO ──
print("\n" + "█"*75)
print("  MÉTODO: ELITISMO")
print("█"*75)

statsE100, tTotalE100, tPromE100 = ejecutarNCorridas(100, correrAlgoritmoElitismo, verbose=True)
imprimirTablaResumen(statsE100, 100, "ELITISMO")
print(f"  Tiempo total: {tTotalE100:.6f}s  |  Tiempo promedio: {tPromE100:.6f}s")

print(f"\n{'='*55}")
print(f"  TABLA DE TIEMPOS — ELITISMO")
print(f"{'='*55}")
print(f"  {'Corridas':<12} {'Tiempo total':<18} {'Tiempo promedio'}")
print(f"  {'-'*50}")
print(f"  {'100':<12} {tTotalE100:<18.6f} {tPromE100:.6f}s")
print(f"{'='*55}")


# ── GRÁFICAS — todas juntas al final ──
graficarEstadisticas(statsR20,  20,  "Ruleta")
graficarEstadisticas(statsR100, 100, "Ruleta")
graficarEstadisticas(statsR200, 200, "Ruleta")
graficarEstadisticas(statsT20,  20,  "Torneo")
graficarEstadisticas(statsT100, 100, "Torneo")
graficarEstadisticas(statsT200, 200, "Torneo")
graficarEstadisticas(statsE100, 100, "Elitismo")
print("Mostrando gráficos...")
plt.show()
