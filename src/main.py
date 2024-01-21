import pandas as p
import openpyxl
import GpuData
import models.Gpu
import os
import json


colunmNames = ['Nome', 'Avg FHD', 'Avg QHD', 'Preco', 'Menor Preco', 'Data Menor Preco', 'Loja MP', 'CpF FHD', 'CpF QHD', 'Link']

def main():

    configFile = 'config.json'
    excelFile = 'Orçamento_PC.xlsx'

    fileFounded = True
    configParams = {
        'showConsole': 'true',
        'openExcel':  'true'
    }

    excelFile = os.getcwd() + '/' + excelFile
    configFile = os.getcwd() + '/' + configFile

    try:
        if os.path.isfile(excelFile):
            fileFounded = True
        else: 
            fileFounded = False
        
        if not os.path.isfile(configFile):
            newConfigFile = open(configFile, 'a')
            newConfigFile.write(json.dumps(configParams))
            newConfigFile.close()

        with open(configFile, 'r') as f:
            configParams = json.load(f)
            
    except:
        print("Arquivo nao encontrado !! criando um arquivo novo")
        fileFounded = False


    if fileFounded:

        dataFrame = p.read_excel(io=excelFile, sheet_name='GPU')

        lastPricesCheckedList = GpuData.getGpusPrice()

        

        if dataFrame["Nome"].values.size < len(lastPricesCheckedList):

            dataFrame = updateAllGpuDataInDataFrame(dataFrame)

        else:

            dataFrame = updateOnlyPriceInDataFrame(dataFrame, lastPricesCheckedList)

        dataFrame.to_excel(excelFile, index=False, sheet_name='GPU')

        
    else:

        dataFrame = createFirstDataFrame()
        
        dataFrame.to_excel(excelFile, index=False, sheet_name='GPU')


    print(dataFrame)
    print(configParams)

    # Abrindo outro progrma pelo python 

    #substitui as libs system para facilitar o uso
    import subprocess

    comand = "start excel"

    if configParams['openExcel'].__eq__('true'):
    #precisa de shell=true para indicar uma chamada ao promp 
        subprocess.run(["start", "excel", excelFile], shell=True)

    if configParams['showConsole'].__eq__('true'):
        print("Terminou de executar o script pyton !")
        input("Digite algo para continuar !")

def make_hyperlink(value):
    return '=HYPERLINK("%s", "%s")' % (value, value)

def createFirstDataFrame():
    dataGpus = GpuData.getGpusAllData()

    dataFrame = p.DataFrame();

    idx = 0
    for gpu in dataGpus:
        dataFrame.at[idx, colunmNames[0]] = gpu.name
        dataFrame.at[idx, colunmNames[1]] = gpu.fhdPerf
        dataFrame.at[idx, colunmNames[2]] = gpu.qhdPerf
        dataFrame.at[idx, colunmNames[3]] = gpu.price
        dataFrame.at[idx, colunmNames[4]] = gpu.lowestPrice
        dataFrame.at[idx, colunmNames[5]] = gpu.dateLowestPrice
        dataFrame.at[idx, colunmNames[6]] = gpu.store
        dataFrame.at[idx, colunmNames[7]] = gpu.cpfHD
        dataFrame.at[idx, colunmNames[8]] = gpu.cpfQHD
        dataFrame.at[idx, colunmNames[9]] = make_hyperlink(gpu.link)

        idx += 1

    return dataFrame

def updateOnlyPriceInDataFrame(dataFrame, lastPricesChecked):
    
    idx = 0
    for row in dataFrame.values.tolist():
        for gpu in lastPricesChecked:

            gpuName = row[0][row[0].find(' ') + 1::].replace(' ', '').upper()
            
            if gpuName.upper() == gpu.name.replace(' ', '').upper():
              
                if gpu.price < row[4]:
                    dataFrame.at[idx, 'Menor Preco'] = gpu.price
                    dataFrame.at[idx, 'Data Menor Preco'] = GpuData.SearchDate
                    dataFrame.at[idx, 'Loja MP'] = gpu.store
                
                dataFrame.at[idx, 'Preco'] = gpu.price
                dataFrame.at[idx, 'Link'] = make_hyperlink(gpu.link)
                dataFrame.at[idx, 'CpF FHD']  = gpu.price / dataFrame.at[idx, 'Avg FHD']
                dataFrame.at[idx, 'CpF QHD']  = gpu.price / dataFrame.at[idx, 'Avg QHD']

        idx += 1
    
    return dataFrame
    
def updateAllGpuDataInDataFrame(dataFrame):
    
    dataGpus = GpuData.getGpusAllData()

    newDataFrame = p.DataFrame();

    idx = 0
    for gpu in dataGpus:

        if gpu.name in dataFrame["Nome"].values:

            i = dataFrame.index[dataFrame['Nome'] == gpu.name].tolist()[0]
            

            if gpu.lowestPrice > dataFrame.at[i, colunmNames[4]]:
                gpu.lowestPrice = dataFrame.at[i, colunmNames[4]] 
                gpu.dateLowestPrice = dataFrame.at[i, colunmNames[5]]
                gpu.store = dataFrame.at[i, colunmNames[6]]

        newDataFrame.at[idx, colunmNames[0]] = gpu.name
        newDataFrame.at[idx, colunmNames[1]] = gpu.fhdPerf
        newDataFrame.at[idx, colunmNames[2]] = gpu.qhdPerf
        newDataFrame.at[idx, colunmNames[3]] = gpu.price
        newDataFrame.at[idx, colunmNames[4]] = gpu.lowestPrice
        newDataFrame.at[idx, colunmNames[5]] = gpu.dateLowestPrice
        newDataFrame.at[idx, colunmNames[6]] = gpu.store
        newDataFrame.at[idx, colunmNames[7]] = gpu.cpfHD
        newDataFrame.at[idx, colunmNames[8]] = gpu.cpfQHD
        newDataFrame.at[idx, colunmNames[9]] = make_hyperlink(gpu.link)
        idx += 1
    
    newDataFrame.sort_values(by=['Nome'])
    return newDataFrame

    

if __name__ == "__main__":
    main()