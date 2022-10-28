import os
import xml.etree.ElementTree as Et
from tqdm import tqdm, trange

class Read_xml():
    def __init__(self,directory)-> None:
        self.directory = directory
        
    #Lista arquivos
    def all_files(self):
        return [ os.path.join(self.directory, arq) for arq in os.listdir(self.directory) if arq.lower().endswith(".xml")]
    
    #Realiza leitura e retorno dos dados
    def cfe_data(self, xml):
        root = Et.parse(xml).getroot()
        nsCFe = {"ns" : "http://www.fazenda.sp.gov.br/sat"}

        #DADOS CFe
        data_emissao = self.check_none(root.find("./ns:infCFe/ns:ide/ns:dEmi", nsCFe))
        data_emissao = f"{data_emissao[6:8]}/{data_emissao[4:6]}/{data_emissao[:4]}"
        valor = float(self.check_none(root.find("./ns:infCFe/ns:total/ns:vCFe", nsCFe)))
        dados = [data_emissao, valor]
        return dados

    #Verifica existencia da informação
    def check_none(self, var):
        if var == None:
            return ""
        else:
            return var.text
    
if __name__ == "__main__":
    #Variaveis
    todas_cfes = []
    totais =[]
    valor_total = 0.0
    vdir = input("Cole o diretório dos arquivos: ")
    
    xml = Read_xml(vdir)
    all = xml.all_files() 

    #Apresentação para usuário final
    os.system('cls')
    print("Diretório sendo análisado: ", vdir)
    print("Quantidade de arquivos sendo análisados: ", len(all))

    #Realiza leitura de todos arquivos
    print("\nRealizando leitura dos arquivos XML... Aguarde... ")
    for i in tqdm(all):
        results = xml.cfe_data(i)
        todas_cfes.append(results)
    
    #Adiciona informações do primeiro arquivo lido
    totais.append(todas_cfes[0])

    #Totaliza os valores conforme data
    print("\nTotalizando valores conforme data... Aguarde...")
    for j in tqdm(range(len(todas_cfes))):
        lExiste = False
        for i in range(0, len(totais)):
            if todas_cfes[j][0] == totais[i][0]:
                lExiste = True
        if lExiste:
            for i in range(0, len(totais)):
                if todas_cfes[j][0] == totais[i][0]:
                    totais[i][1] = totais[i][1] + todas_cfes[j][1]
        else:
            totais.append(todas_cfes[j])

    for i in range(0,len(totais)):
        totais[i][1] = round(totais[i][1],2)
        valor_total = valor_total + totais[i][1]

    #Imprime resultados
    print("\n")
    for i in range(0,len(totais)):
        print(totais[i],"\n----------------------")
    print("valor total da pasta: {0:.2f} \n ".format(valor_total))
    
    input ("Tecle Enter para encerrar...")

