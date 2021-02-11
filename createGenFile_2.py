# -----------------------------------------------------------------------
# Lib import
import argparse, sys
import pandas as pd
import os
import csv
import concurrent.futures
import time

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
        self.pedigree = []

        self.loadPedigreeFile()
        self.createGenotypeFile()
        self.populateGenotypeFile()
    
    def loadPedigreeFile(self):
        print("Carrega o arquivo pedigree para o atributo pedigree (Dataframe do pandas)")
        print(f"Arquivo do pedigree: {argv.ped}")

        pedigree_headers = ["Animal", "Sire", "Dam", "Sex"]
        self.pedigree = pd.read_csv(argv.ped, sep=' ', names=pedigree_headers)
        self.pedigree.set_index('Animal', inplace=True)

    def createGenotypeFile(self):
        genotypeHeader = ['ID', 'Chip', 'Genotypes']

        with open(argv.output, "w") as f:
            csv_writer = csv.writer(f, delimiter=' ')

    def populateGenotypeFile(self):
        fileHandlers = App.getFileHandlers()
        # for file in fileHandlers:
        #     genotypes = self.handleGenotypeFile(file)
        #     with open(argv.output, 'a') as f:
        #         csv_w = csv.writer(f, delimiter=" ")
        #         csv_w.writerows(genotypes)

        with concurrent.futures.ProcessPoolExecutor(max_workers=6) as executor:
            for fileHandler, genotypes in zip(fileHandlers, executor.map(self.handleGenotypeFile, fileHandlers)):
                with open("genotypes_"+fileHandler[2:]+".csv", 'w') as f:
                    csv_w = csv.writer(f, delimiter=" ")
                    csv_w.writerows(genotypes)

                # with open(argv.output, a) as f:
                #     print(f"Finalizado arquivo {fileHandler}")
                #     csv_w = csv.writer(csv_file)
                #     csv_w.writerows(result)
        
    def handleGenotypeFile(self, genotype_file):
        genotypes = []

        print(f"Extraindo genotypes de {genotype_file}")
        gen_f, header = self.getAndTrimHeader(open(genotype_file, 'r'))
         
        if header[8] != "Allele1 - AB" or header[9] != "Allele2 - AB": print(f"Arquivo {genotype_file} com headers incorretos: {header}")
        elif argv.debug: print("Headers do arquivo batem!")

        animalName = ""
        animalArr = []
        # i = 0
        for line in gen_f:
            genCols = line.split('\t')
            
            if animalName != genCols[3]:
                if not(animalName == ""): 
                    # i += 1
                    # if i > 1: break
                    
                    if argv.debug: print(f"Mapeando animal {animalName}")
                    start = time.time()
                    genotypes.append( self.mapAnimal(animalArr, header, animalName) )
                    end = time.time()
                    print(f"Animal {animalName} mapeado em {end-start} segundos")
                    time.sleep(0.1)

                    

                animalArr = []                    
                animalName = genCols[3]
            
            animalArr.append(genCols)

        genotypes.append( self.mapAnimal(animalArr, header, animalName) )

        return genotypes
        
    def mapAnimal(self, animalArr, header, animal_name):
        # animalArr:
            # -> Lista, cada posição é um marcador do animal (Linha do arquivo .txt)
        # print(f"AnimalArr: {animalArr[0]}")
        # header:
            # Cabeçalho da "Lista dos animais" ,eg cabeçalho da coluna 0 do animalArr será o header[0]
        # print(f"Header: {header}")
        # print(argv.map)


        # animalArr e header são usados para gerar o DataFrame do pandas, logo em seguida (Gera uma tabelinha)
        # print(header)
        genotype = []
        animalDF = pd.DataFrame(animalArr, columns=header)

        # # Filtra os registros com cromossomo 0, Y, X e MT
        animalDF = animalDF.loc[animalDF['Chr'] != '0'].loc[animalDF['Chr'] != 'MT']
        # .loc[animalDF['Chr'] != 'Y'].loc[animalDF['Chr'] != 'X']  
        animalDF.set_index('SNP Name', inplace=True)

        mapFile = open(argv.map, 'r')
        try: 
            (next(mapFile)) # Pula o cabeçalho do map
        except:
            pass
        
        # Para cada marcador no mapa, faça     map[0]   map[1]      map[2]...
        # Gera String de genótipó do animal : "5        1           2           5           2   1   2   5"
        for line in mapFile:
            
            try:
                marcadorArr = line.split(' ')                
            except:
                print("Erro ao ler marcador")

            # Procura o marcador no animal
            try:
                marcador_animal = animalDF.loc[marcadorArr[0]]
                animal_encontrado = True
            except KeyError:
                animal_encontrado = False

            if not(animal_encontrado):
                # caiu neste if, significa que o marcador não foi encontrado no animal
                genotype.append("0")
                genotype.append("0")
                if argv.debug: print(f"{marcadorArr[0]} - [ N, N ] => 5")
            
            else:
                # Se caiu neste else, o marcador foi encontrado
                # Verifica os alelos

                Allele1 = marcador_animal["Allele1 - Forward"]
                Allele2 = marcador_animal["Allele2 - Forward"]

                if Allele1 in ["A", "T", "C", "G"]: 
                    genotype.append(Allele1) 
                else: 
                    genotype.append("0")

                if Allele2 in ["A", "T", "C", "G"]: 
                    genotype.append(Allele2) 
                else: 
                    genotype.append("0")
                # genotype.append(Allele1)
                # genotype.append(Allele2)

                if argv.debug: print(f"{marcadorArr[0]} - [ {Allele1}, {Allele2} ]")

        # Faz uma pesquisa pelo animal no arquivo de pedigree
        # Se o animal for enocntrado, alimenta os dados, senão põe tudo zerado e femea
        try:
            animal_pedigree = self.pedigree.loc[animal_name]
            # print(f"Animal {animal_name} encontrado no Pedigree!")
            return (["Fam1", animal_name, animal_pedigree["Sire"], animal_pedigree["Dam"], animal_pedigree["Sex"], "0"] + genotype)
        except KeyError:
            print(f"Animal {animal_name} Não encontrado Pedigree!")
            return (["Fam1", animal_name, "0", "0", "F", "0"] + genotype)

        # [Familia, Animal, pai, mae, sexo, phenotype, n genotipos...]
        # return [animal_name, argv.chip, genotype]


    @staticmethod
    def getAndTrimHeader(fp):
        for line in fp:      
            try:
                genCols = line.split('\t')
                if (genCols[0] == 'SNP Name'):
                    return [fp, genCols]
            except:
                print("Houve um erro ao tentar procurar o Header") 

    @staticmethod
    def getFileHandlers():
        fileHandlers = []

        for file in os.listdir(argv.genotype_folder):
            if file.endswith("txt"):                   
                fileHandlers.append(str(argv.genotype_folder)+str(file))

        return fileHandlers
    
   
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', type=bool, help='Enable debug mode', default=0)

    parser.add_argument('--ped', type=str, help='Arquivo do pedigree', default="./pedigree.csv")
    parser.add_argument('--output', type=str, help='Arquivo de saída', default="./genotypes.csv")
    parser.add_argument('--map', type=str, help='Mapa de referência', default="./map.csv")
    parser.add_argument('--chip', type=int, help='Número padrão do chip', default=1)
    parser.add_argument('--genotype-folder', type=str, help='Pasta onde estão localizados os arquivos de genotypes', default="./")

	# parser.add_argument('--loc', type=int, help='Help text', default=0)		
	# parser.add_argument('--betha', type=float, help='Help text', default=0)
	# parser.add_argument('--seriesName', type=str, help='Help text', default="Default")

    return parser.parse_args(argv)

if __name__ == "__main__":
    # First, parse arguments from commandLine
    argv = parse_arguments(sys.argv[1:])

    app = App()
