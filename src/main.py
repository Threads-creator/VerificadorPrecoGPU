import pandas as p
from openpyxl import load_workbook
import GpuData
import pandas as p
import os

excelFile = 'Orçamento_PC.xlsx'

colunmNames = ['Nome', 'FHD performance', 'QHD performance', 'Preco', 'Menor Preco', 'Data Menor Preco', 'Avg FHD', 'Avg QHD', 'Link']

fileFounded = True

excelFile = os.getcwd() + '/' + excelFile

try:
    if os.path.isfile(excelFile):
        fileFounded = True
    else: 
        fileFounded = False
except:
    print("Arquivo nao encontrado !! criando um arquivo novo")
    fileFounded = False


if fileFounded:

    dataFrame = p.read_excel(io=excelFile, sheet_name='GPU')

    lastPricesCheckedList = GpuData.getGpusPrice()

    idx = 0
    for row in dataFrame.values.tolist():
        for gpu in lastPricesCheckedList:


            gpuName = row[0][row[0].find(' ') + 1::].replace(' ', '').upper()


            if gpuName.upper() == gpu['ModeloSimplificado'].replace(' ', '').upper():

                
                if gpu['ValorAV'] < row[4]:
                    dataFrame.at[idx, 'Menor Preco'] = gpu['ValorAV']
                    dataFrame.at[idx, 'Data Menor Preco'] = GpuData.SearchDate

        idx += 1

    dataFrame.to_excel(excelFile, index=False, sheet_name='GPU')


else:

    dataGpus = GpuData.getGpusAllData()

    dataFrame = p.DataFrame(data=[x.__dict__.values() for x in dataGpus], columns=colunmNames)


    dataFrame.to_excel(excelFile, index=False, sheet_name='GPU')


print(dataFrame)

# Abrindo outro progrma pelo python 

#substitui as libs system para facilitar o uso
import subprocess

comand = "start excel"

#precisa de shell=true para indicar uma chamada ao promp 
subprocess.run([ "start", "excel", excelFile], shell=True)


print("Terminou de executar o script pyton !")
input("Digite algo para continuar !")