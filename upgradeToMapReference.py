# -----------------------------------------------------------------------
# Lib import
import argparse, sys
import pandas as pd
import os
import time
import csv

# -----------------------------------------------------------------------
# Imports Libs

# Argument list from commandline
argv = []


def getFilesExtension(ext):
    return (f for f in os.listdir() if f.endswith('.' + ext))

#Classe de entrada
class App:
    # Inicialização da aplicação
    def __init__(self):
        self.loadReferenceMap()
        self.loadMap()
        self.updateMap()

    def loadReferenceMap(self):
        print("Carrega o arquivo que contem o mapa de referencia (Dataframe do pandas)")
        print(f"Mapa referencia: {argv.ref}")

        reference_headers = ["Chr", "SNP", "Pos1", "Pos2"]
        self.reference = pd.read_csv(argv.ref, sep=' ', names=reference_headers)
        self.reference.set_index('SNP', inplace=True)



    def loadMap(self):
        print("Carrega o arquivo que contem o mapa a ser atualizado (Dataframe do pandas)")
        print(f"Mapa a ser atualizado: {argv.map}")

        map_headers = ["Chr", "SNP", "Pos1", "Pos2"]
        self.map = pd.read_csv(argv.map, sep=' ', names=map_headers)
        self.map.set_index('SNP', inplace=True)

    def updateMap(self):
        updatedMapArr = []
        for Snp, ref_marker in self.reference.iterrows():
            try:
                snp_found = self.map.loc[Snp]
            except KeyError:
                continue

            
            updatedMapArr.append([ref_marker['Chr'], Snp, ref_marker['Pos1'], ref_marker['Pos2']])

        with open(argv.output, "w") as f:
            csv_w = csv.writer(f, delimiter=' ')
            csv_w.writerows(updatedMapArr)

    # def updateMap(self):       
    #     # Pega o mapa em Dataframe
    #     mapDF = self.getMapDF()

    #     map_X = mapDF.loc[mapDF['Chr'] == 'X']
    #     map_X["Pos"] = pd.to_numeric(map_X["Pos"])
    #     map_X = map_X.sort_values(["Pos", "SNP"])
        
    #     map_Y = mapDF.loc[mapDF['Chr'] == 'Y']
    #     map_Y["Pos"] = pd.to_numeric(map_Y["Pos"])
    #     map_Y = map_Y.sort_values(["Pos", "SNP"])

    #     # Filtra os SNP's com Chr = 0 e os relacionados ao sexo
    #     mapDF = mapDF.loc[mapDF['Chr'] != '0'].loc[mapDF['Chr'] != 'Y'].loc[mapDF['Chr'] != 'X'].loc[mapDF['Chr'] != 'MT']

    #     # Transforma as colunas para numérico, para poder fazer o sort corretamente
    #     mapDF['Chr'] = pd.to_numeric(mapDF["Chr"])
    #     mapDF['Pos'] = pd.to_numeric(mapDF["Pos"])


    #     # Sort by Chromossome, Pos
    #     mapDF = mapDF.sort_values(["Chr", "Pos", "SNP"])

    #     todos_df = [mapDF, map_X, map_Y]
    #     mapDF = pd.concat(todos_df)

    #     print(f"Exportando o mapa para {argv.output}")
    #     mapDF.to_csv(argv.output, sep=" ", index=False)
 
   
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', type=bool, help='Enable debug mode', default=0)
    parser.add_argument('--output', type=str, help='Arquivo de saída', default="./upgradedMap.csv")
    parser.add_argument('--ref', type=str, help='Mapa de referencia', default="./ref.csv")
    parser.add_argument('--map', type=str, help='Mapa a ser atualizado', default="./map.csv")

	# parser.add_argument('--loc', type=int, help='Help text', default=0)		
	# parser.add_argument('--betha', type=float, help='Help text', default=0)
	# parser.add_argument('--seriesName', type=str, help='Help text', default="Default")

    return parser.parse_args(argv)

if __name__ == "__main__":
    # First, parse arguments from commandLine
    argv = parse_arguments(sys.argv[1:])

    app = App()
