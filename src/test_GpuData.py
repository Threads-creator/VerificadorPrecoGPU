import sys
sys.path.append("../")

from models.Gpu import Gpu
from GpuData import getGpuPerfData
from GpuData import getGpusFromApiPrice
from GpuData import getGpusPrice
from GpuData import getGpusAllData

# def main():
#     test_gpuClass()
#     test_getPerfData()
#     test_getGpusFromApiPrice()

def test_gpuClass():
    gpu = Gpu("RTX 3060 12GB", 68.2, 55.4, 34.6, 1800.00)

    assert gpu.name == "RTX 3060 12GB"
    assert gpu.fhdPerf == 68.2
    assert gpu.qhdPerf == 55.4
    assert gpu.fourkPerf == 34.6
    assert gpu.price == 1800.0
    assert gpu.link == ""
    assert gpu.store == ""
    assert gpu.cpfHD == 0.0
    assert gpu.cpfQHD == 0.0

def test_getPerfData():

    result = getGpuPerfData()

    assert type(result) == type([{Gpu}])
    assert result[0].__class__ == Gpu("").__class__

def test_getGpusFromApiPrice():

    objModel = {
        "Modelo": "Última atualização 25/06/2023 - 15:28:32",
        "ValorAV": "0",
        "ValorParc": "0",
        "Loja": "",
        "Link": "/",
        "ModeloSimplificado": ""
    }

    result = getGpusFromApiPrice(100)
    first = result[0]
    second = result[1]

    assert first["ValorAV"] == "0"
    assert first["ValorParc"] == "0"
    assert first["Loja"] == ""
    assert first["Link"] == "/"
    assert first["ModeloSimplificado"] == ""
    
    assert second["Modelo"] != None
    assert second["ValorAV"] != None
    assert second["ValorParc"] != None
    assert second["Loja"] != None
    assert second["Link"] != None
    assert second["ModeloSimplificado"] != None


def test_getGpusPrice():

    result = getGpusPrice()

    assert type(result) == type([Gpu])
    
    for item in result:
        assert item.name != ""
        assert item.fhdPerf == 0.0
        assert item.qhdPerf == 0.0
        assert item.price != 0.0
        assert item.link != ""
        assert item.store != ""
        assert item.cpfHD == 0.0
        assert item.cpfQHD == 0.0
        assert item.price != 0.0
        assert result.count(item) == 1

def test_getGpusAllData():

    result = getGpusAllData()

    assert type(result) == type([Gpu])
    
    for item in result:
        assert item.name != ""
        assert item.fhdPerf != 0.0
        assert item.qhdPerf != 0.0
        assert item.price != 0.0
        assert item.link != ""
        assert item.store != ""
        assert item.cpfHD != 0.0
        assert item.cpfQHD != 0.0
        assert item.price != 0.0
        assert result.count(item) == 1
    


    

# if __name__ == "__main__":
#     main()
