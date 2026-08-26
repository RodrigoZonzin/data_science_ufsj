import math
import csv
import sys
import matplotlib.pyplot as plt

from numpy.random import uniform        #esa daqui eu uso so para gerar aleatorios, acho mais facil q a random
import numpy as np                      #aqui eu uso so para plotar as cores do grafico de acordo com o colormap, uso np.linspace

class Kmeans: 
    def __init__(self, caminho, K = 2, maxIteracoes = 15): 
        self.caminho = caminho
        self.espaco  = []
        self.dimEspaco = None
        self.K       = K
        self.centroides = None
        self.xmin, self.xmax = None, None
        self.xmin, self.ymax = None, None
        self.maxIteracoes = maxIteracoes 

    def determina_limites(self):
        self.dimEspaco = len(self.espaco[0])
        self.limites = []

        for d in range(self.dimEspaco):
            valores = [p[d] for p in self.espaco]
            self.limites.append((min(valores), max(valores)))

    def print_pontos(self):
        for p in self.espaco:
            print(p)

    """
    def plota_espaco(self, save = False):
        plt.figure(figsize=(8, 6))
        X, Y = zip(*self.espaco)
        plt.scatter(X, Y)

        centroidesX, centroidesY = zip(*self.centroides)
        plt.scatter(centroidesX, centroidesY, marker = '^')

        plt.show()

        if save == True: 
            #plt.savefig()    
            pass
    """
    def plota_espaco(self):
        if self.dimEspaco > 2: 
            print("Plots N-D, N>2 ainda nao habilitado")
            return


        plt.figure(figsize=(8,6))

        #cores = ['red', 'blue', 'green', 'orange', 'purple',
        #         'brown', 'pink', 'gray', 'olive', 'cyan']
        cores = plt.cm.cividis(np.linspace(0.1, 0.9, len(self.grupos)))

        for i, grupo in enumerate(self.grupos):
            if len(grupo) > 0:
                X, Y = zip(*grupo)
                plt.scatter(X, Y, color=cores[i % len(cores)], label=f'Cluster {i}')


        centroidesX, centroidesY = zip(*self.centroides)

        plt.scatter(centroidesX, centroidesY, color='black', marker='^', s = 30, label='Centroides')
        plt.legend()
        plt.savefig('results.png')
        plt.show()

    def ler_arquivo(self):
        with open(self.caminho, 'r') as f: 
            reader = csv.reader(f)

            for i, row in enumerate(reader): 
                if i == 0: continue
    
                #(x1, x2, ... , xn) 
                ponto = tuple(float(xi) for xi in row)
                self.espaco.append(ponto)

        self.determina_limites()

    def dist_euclidiana(self, p1: tuple, p2: tuple):
        #x = (x0, x1, ..., xn) 
        #y = (y0, y1, ..., yn)
        #d(x,y)**2 = sum{xi - yi}**2
        sum = 0
        for i in range(len(p1)): 
            sum += (p1[i] - p2[i])**2 

        return sum**0.5

    def fit(self):
        #[(x1, ..., xn), (y1, ..., yn), ... , (z1, ..., zn)]
        self.centroides = [tuple(uniform(mmin, mmax) for mmin, mmax in self.limites) for _ in range(self.K)]

        for iteracao in range(self.maxIteracoes):
            grupos = [[] for _ in range(self.K)]

            for ponto in self.espaco:

                distancias = [self.dist_euclidiana(ponto, centroide) for centroide in self.centroides]

                indice_centroide = distancias.index(min(distancias))
                grupos[indice_centroide].append(ponto)

            centroides_antigos = self.centroides.copy()

            novos_centroides = []

            for grupo in grupos:
                if len(grupo) == 0:
                    novo_centroide = tuple(uniform(mmin, mmax) for mmin, mmax in self.limites)

                else:
                    medias = []
                    
                    for d in range(self.dimEspaco): 
                        media = sum(p[d] for p in grupo)/len(grupo)
                        medias.append(media)

                    novo_centroide = tuple(medias)

                novos_centroides.append(novo_centroide)

            self.centroides = novos_centroides

            convergiu = True

            for antigo, novo in zip(centroides_antigos, self.centroides):
                if self.dist_euclidiana(antigo, novo) > 1e-6:
                    convergiu = False
                    break

            if convergiu: break

        self.grupos = grupos

    """
    def fit(self):
        self.centroides = [(uniform(self.xmin, self.xmax), uniform(self.ymin, self.ymax)) for _ in range(self.K)]

        for ponto in self.espaco: 
            for centroide in self.centroides:
                print(ponto, centroide, self.dist_euclidiana(ponto, centroide))
    """


if __name__ == "__main__": 
    meuKmeans = Kmeans(caminho=sys.argv[1], K = int(sys.argv[2]))
    meuKmeans.ler_arquivo()
    #meuKmeans.print_pontos()

    meuKmeans.fit()
    meuKmeans.plota_espaco()
    [print(coordCentroides) for coordCentroides in meuKmeans.centroides]
    #print(meuKmeans.espaco[0], meuKmeans.espaco[2])
    #print(meuKmeans.dist_euclidiana(meuKmeans.espaco[0], meuKmeans.espaco[2]))


