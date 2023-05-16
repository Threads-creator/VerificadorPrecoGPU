import pandas as p
import openpyxl
import GpuData
import os

excelFile = 'Orçamento_PC.xlsx'

colunmNames = ['Nome', 'Avg FHD', 'Avg QHD', 'Preco', 'Menor Preco', 'Data Menor Preco', 'Loja MP', 'CpF FHD', 'CpF QHD', 'Link']

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
            


            if gpuName.upper() == gpu.name.replace(' ', '').upper():
              
                if gpu.price < row[4]:
                    dataFrame.at[idx, 'Menor Preco'] = gpu.price
                    dataFrame.at[idx, 'Data Menor Preco'] = GpuData.SearchDate
                    dataFrame.at[idx, 'Loja MP'] = gpu.store
                
                dataFrame.at[idx, 'Preco'] = gpu.price
                dataFrame.at[idx, 'Link'] = gpu.link
                dataFrame.at[idx, 'CpF FHD']  = gpu.price / dataFrame.at[idx, 'Avg FHD']
                dataFrame.at[idx, 'CpF QHD']  = gpu.price / dataFrame.at[idx, 'Avg QHD']

        idx += 1

    dataFrame.to_excel(excelFile, index=False, sheet_name='GPU')


else:

    dataGpus = GpuData.getGpusAllData()

    dataFrame = p.DataFrame();

    idx = 0;
    for gpu in dataGpus:
        dataFrame.at[idx, colunmNames[0]] = gpu.name
        dataFrame.at[idx, colunmNames[1]] = gpu.fhdPerf
        dataFrame.at[idx, colunmNames[2]] = gpu.qhdPerf
        dataFrame.at[idx, colunmNames[3]] = gpu.price
        dataFrame.at[idx, colunmNames[4]] = gpu.lowestPrice
        dataFrame.at[idx, colunmNames[5]] = gpu.dateLowestPrice
        dataFrame.at[idx, colunmNames[6]] = gpu.store
        dataFrame.at[idx, colunmNames[7]] = gpu.AvgHD
        dataFrame.at[idx, colunmNames[8]] = gpu.AvgQHD
        dataFrame.at[idx, colunmNames[9]] = gpu.link

        idx += 1

    dataFrame.to_excel(excelFile, index=False, sheet_name='GPU')


print(dataFrame)

# Abrindo outro progrma pelo python 

#substitui as libs system para facilitar o uso
import subprocess

comand = "start excel"

#precisa de shell=true para indicar uma chamada ao promp 
subprocess.run(["start", "excel", excelFile], shell=True)


print("Terminou de executar o script pyton !")
input("Digite algo para continuar !")