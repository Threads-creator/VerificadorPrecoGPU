import json
import requests
from bs4 import BeautifulSoup

urlPerf = "https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html"

class Gpu:

    name: str
    fhdPerf: float
    qhdPerf: float
    
    price: float
    lowestPrice = 99999
    dateLowestPrice: str

    def __init__(self, name, fhdPerf, qhdPerf, price = 0.0, lowestPrice = 99999.0, dateLowestPrice = ""):
        self.name = name
        self.fhdPerf = fhdPerf
        self.qhdPerf = qhdPerf
        self.price = price
        self.lowestPrice = lowestPrice
        self.dateLowestPrice = dateLowestPrice


    def __str__(self) -> str:
        return f'{self.name} + - + {self.fhdPerf} + - + {self.qhdPerf} + - + {self.price} + - + {self.lowestPrice} + - + {self.dateLowestPrice} '




def __getAllGpuRows(response):

    soup = BeautifulSoup(response.content, features='html.parser')

    tableBody = soup.find(class_="table__body")

    return tableBody.find_all(class_='table__body__row')

def __getFps(tdRow):

    start = tdRow.find("(")
    end = tdRow.find("fps")

    return float(tdRow[start+1:end])



def getGpuPerfData():

    try:

        response = requests.get(urlPerf)
    
    except:
        print(f'Não possivel acessar o Site com dados das GPUs')
        return


    rows = __getAllGpuRows(response)

    listGpus = [] * len(rows)

    for row in rows:

        name = row.a.text

        tableTd = row.findAll(class_='table_body__data')

        try:

            fhdPerf = __getFps(str(tableTd[1]))
            qhdPerf = __getFps(str(tableTd[3]))
        
        except:

            print(f'Não foi possivel encontrar o FPS da placa {name}')
            continue


        listGpus.append(Gpu(name, fhdPerf, qhdPerf))
    

    return listGpus







urlPrice = "https://placasdevideo.app.br/Precos.json"


gpusFromSite = getGpuPerfData()

def __normalizeGpuName(name):
    name = name.upper()

    idxStart = str(name).find(' ')
    name = name[idxStart + 1 ::].strip()

    subNames = name.split(' ')
    if subNames.__contains__('SUPER'):
        return name
    else:
        name = subNames[0] + " "
        for subName in subNames[1::]:
            name += subName
        return name


# definir gpus buscadas
searchNames = [] * len(gpusFromSite)
for gpu in gpusFromSite:
    
    searchNames.append(__normalizeGpuName(gpu.name))

def getGpusFromApiPrice(qtd):
    try:
        response = requests.get(urlPrice)
    except:
        print(f'Não foi possivel acessar a API de preços')
        return

    try:
        produtos = [] * qtd

        for produto in json.loads(response.content.decode('utf-8')):
            if produto['ModeloSimplificado'] == "RTX 3060" and (produto['Modelo'].__contains__("8GB") or produto['Modelo'].__contains__("8 GB")):
                continue
            produtos.append(produto)
    except:
        print(f'Não foi possivel ler os dados da Request feita a API Preços')

    return produtos

gpusFromJson = getGpusFromApiPrice(len(searchNames))

# pega data da busca
SearchDate = gpusFromJson[0]['Modelo'].split(' ')[2]

gpusFromJson = gpusFromJson[1::]


def __filterGpus(gpus, nameGpus):

    gpusFiltered = []
    for gpu in gpus:
        for gpuName in nameGpus:
            if gpu['ModeloSimplificado'].__contains__(gpuName):
                gpusFiltered.append(gpu)
                break

    return gpusFiltered

gpusFiltered = __filterGpus(gpusFromJson, searchNames)
        

def __findGpuLowerValue(productName, products):
    lowerValue = 9999999.99
    productLowerValue = {}
    
    for product in products:
        if product['ModeloSimplificado'].upper() == productName.upper():
            if lowerValue > product['ValorAV']:
                lowerValue = product['ValorAV']
                productLowerValue = product
    
    return productLowerValue


def __getGpusLowestPriced():
    gpusLowestValue = []

    for gpu in gpusFiltered:
        
        if any(i['ModeloSimplificado'] == gpu['ModeloSimplificado'] for i in gpusLowestValue):
            continue
        else:
            gpuFound = __findGpuLowerValue(gpu['ModeloSimplificado'], gpusFiltered)
            gpusLowestValue.append(gpuFound)

    return gpusLowestValue


gpusLowestValue = __getGpusLowestPriced()

def __sortGpusLists():
    import operator

    gpusLowestValue.sort(key=operator.itemgetter('ModeloSimplificado'))

    gpusFromSite.sort(key=operator.attrgetter('name'))


def getGpusPrice():

    __sortGpusLists()

    return gpusLowestValue


def getGpusAllData():
    
    __sortGpusLists()

    gpusFinalResult = [] * len(gpusLowestValue)

    for aux in gpusLowestValue:
        
        for gpu in gpusFromSite:

            gpuName = gpu.name[gpu.name.find(' ') + 1::].replace(' ', '').upper()
            
            if gpuName.upper() == aux['ModeloSimplificado'].replace(' ', '').upper():

                auxGpu = Gpu(
                    name = gpu.name,
                    fhdPerf = gpu.fhdPerf,
                    qhdPerf = gpu.qhdPerf,
                    price = aux['ValorAV'],
                )
                if aux['ValorAV'] < gpu.lowestPrice:
                    auxGpu.lowestPrice = aux['ValorAV']
                    auxGpu.dateLowestPrice = SearchDate
                
                auxGpu.AvgHD = auxGpu.price / auxGpu.fhdPerf
                auxGpu.AvgQHD = auxGpu.price / auxGpu.qhdPerf
                auxGpu.link = aux['Link']
                gpusFinalResult.append(auxGpu)
                break

    
    return gpusFinalResult


    