# -----------------------------------------------------------------------
# Lib import
import argparse, sys
import pandas as pd
import os

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
        self.createMap()

    def createMap(self):       
        # Pega o mapa em Dataframe
        mapDF = self.getMapDF()

        map_X = mapDF.loc[mapDF['Chr'] == 'X']
        map_X["Pos"] = pd.to_numeric(map_X["Pos"])
        map_X = map_X.sort_values(["Pos", "SNP"])
        
        map_Y = mapDF.loc[mapDF['Chr'] == 'Y']
        map_Y["Pos"] = pd.to_numeric(map_Y["Pos"])
        map_Y = map_Y.sort_values(["Pos", "SNP"])

        # Filtra os SNP's com Chr = 0 e os relacionados ao sexo
        mapDF = mapDF.loc[mapDF['Chr'] != '0'].loc[mapDF['Chr'] != 'Y'].loc[mapDF['Chr'] != 'X'].loc[mapDF['Chr'] != 'MT']

        # Transforma as colunas para numérico, para poder fazer o sort corretamente
        mapDF['Chr'] = pd.to_numeric(mapDF["Chr"])
        mapDF['Pos'] = pd.to_numeric(mapDF["Pos"])


        # Sort by Chromossome, Pos
        mapDF = mapDF.sort_values(["Chr", "Pos", "SNP"])

        todos_df = [mapDF, map_X, map_Y]
        mapDF = pd.concat(todos_df)

        print(f"Exportando o mapa para {argv.output}")
        mapDF.to_csv(argv.output, sep=" ", index=False)

    def getMapDF(self):
        headerFound = False
        curSample = ""
        mapArr = []
        mapHeader = ['SNP','Chr','Pos', 'Chip1']

        file = list(getFilesExtension('txt'))[0]

        print(f"Gerando o mapa a partir do arquivo: {file}")

        fp = open(file, 'r')
        for line_idx, line in enumerate(fp):
            splitted = line.split('\t')

            if headerFound:
                if curSample == "":
                    curSample = splitted[3]
                elif curSample != splitted[3]:
                    break

                mapArr.append([splitted[0], splitted[1], splitted[2], "1"])

            else:
                try:
                    if (splitted[0] == 'SNP Name'):
                        headerFound = True
                except:
                    continue     

        if not(headerFound):
            print("Header não encontrado para arquivo: {}".format(file))
                
        # escrever no arquivo
        return pd.DataFrame(mapArr, columns=mapHeader)

   
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', type=bool, help='Enable debug mode', default=0)
    parser.add_argument('--output', type=str, help='Arquivo de saída', default="./map.csv")

	# parser.add_argument('--loc', type=int, help='Help text', default=0)		
	# parser.add_argument('--betha', type=float, help='Help text', default=0)
	# parser.add_argument('--seriesName', type=str, help='Help text', default="Default")

    return parser.parse_args(argv)

if __name__ == "__main__":
    # First, parse arguments from commandLine
    argv = parse_arguments(sys.argv[1:])

    app = App()
