import json
import requests
from bs4 import BeautifulSoup

urlPerf = "https://www.tomshardware.com/reviews/gpu-hierarchy,4388.html"

class Gpu:

    codName: str

    name: str
    fhdPerf: float
    qhdPerf: float
    
    price: float
    lowestPrice = 99999
    dateLowestPrice: str
    store: str
    link: str

    def __init__(self, name, fhdPerf = 0.0, qhdPerf = 0.0, price = 0.0, lowestPrice = 99999.0, dateLowestPrice = "", store="", link=""):
        self.name = name
        self.fhdPerf = fhdPerf
        self.qhdPerf = qhdPerf
        self.price = price
        self.lowestPrice = lowestPrice
        self.dateLowestPrice = dateLowestPrice
        self.store = store
        self.link = link


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
    
    name = subNames[0]
    for subName in subNames[1::]:
        name += subName
    return name


# definir gpus buscadas
for gpu in gpusFromSite:
    gpu.codName = __normalizeGpuName(gpu.name)
    

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

gpusFromJson = getGpusFromApiPrice(len(gpusFromSite))

# pega data da busca
SearchDate = gpusFromJson[0]['Modelo'].split(' ')[2]

gpusFromJson = gpusFromJson[1::]


def __filterGpus(gpus, namedGpus):

    gpusFiltered = []
    for gpu in gpus:
        for gpuName in namedGpus:
            if gpu['ModeloSimplificado'].replace(" ", "").__contains__(gpuName.codName):
                gpusFiltered.append(gpu)
                break

    return gpusFiltered

gpusFiltered = __filterGpus(gpusFromJson, gpusFromSite)
        

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


def __convertJsonToGpuClass(gpus):

    convertedGpus = [] * len(gpus)

    for gpu in gpus:
        tempGpu = Gpu(name = gpu["ModeloSimplificado"])
        tempGpu.price=gpu["ValorAV"]
        tempGpu.store = gpu["Loja"]
        tempGpu.link = gpu["Link"]

        convertedGpus.append(tempGpu)

    return convertedGpus


def getGpusPrice():

    __sortGpusLists()

    return __convertJsonToGpuClass(gpusLowestValue)


def getGpusAllData():

    gpusLowestValue = getGpusPrice();
    gpusFinalResult = [] * len(gpusLowestValue)

    for lowValueGpu in gpusLowestValue:
        
        for gpu in gpusFromSite:

            gpuName = gpu.name[gpu.name.find(' ') + 1::].replace(' ', '').upper()
            
            if gpuName.upper() == lowValueGpu.name.replace(' ', '').upper():

                tempGpu = Gpu(
                    name = gpu.name,
                    fhdPerf = gpu.fhdPerf,
                    qhdPerf = gpu.qhdPerf,
                    price = lowValueGpu.price,
                )
                tempGpu.lowestPrice = lowValueGpu.price
                tempGpu.dateLowestPrice = SearchDate
                
                tempGpu.store = lowValueGpu.store
                tempGpu.AvgHD = lowValueGpu.price / tempGpu.fhdPerf
                tempGpu.AvgQHD = lowValueGpu.price / tempGpu.qhdPerf
                tempGpu.link = lowValueGpu.link

                gpusFinalResult.append(tempGpu)
                break


    return gpusFinalResult


    