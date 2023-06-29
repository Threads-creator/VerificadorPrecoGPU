class Gpu:

    codName: str

    def __init__(self, 
                name: str, 
                fhdPerf = 0.0, 
                qhdPerf = 0.0, 
                price = 0.0, 
                lowestPrice = 99999.0, dateLowestPrice = "", 
                store = "", 
                link = "",
                cpfHD =0.0,
                cpfQHD = 0.0):
        self.name = name
        self.fhdPerf = fhdPerf
        self.qhdPerf = qhdPerf
        self.price = price
        self.lowestPrice = lowestPrice
        self.dateLowestPrice = dateLowestPrice
        self.store = store
        self.link = link
        self.cpfHD = cpfHD
        self.cpfQHD = cpfQHD

        @property
        def name(self):
            return self._name;

        @name.setter
        def name(self, name):
            if not str.isalnum(name):
                raise ValueError("Only alphabeti chairs and numerals is acceptable")
            self._name = name;

        @property
        def fhdPerf(self):
            return self._fhdPerf;

        @fhdPerf.setter
        def fhdPerf(self, fhdPerf):
            self._fhdPerf = fhdPerf;

        @property
        def qhdPerf(self):
            return self._qhdPerf;

        @qhdPerf.setter
        def qhdPerf(self, qhdPerf):
            self._qhdPerf = qhdPerf;

        @property
        def price(self):
            return self._price;

        @price.setter
        def price(self, price):
            self._price = price;

        @property
        def lowestPrice(self):
            return self._lowestPrice;

        @lowestPrice.setter
        def lowestPrice(self, lowestPrice):
            self._lowestPrice = lowestPrice;

        @property
        def dateLowestPrice(self):
            return self._dateLowestPrice;

        @dateLowestPrice.setter
        def dateLowestPrice(self, dateLowestPrice):
            self._dateLowestPrice = dateLowestPrice;

        @property
        def store(self):
            return self._store;

        @store.setter
        def store(self, store):
            self._store = store;

        @property
        def link(self):
            return self._link;

        @link.setter
        def link(self, link):
            self._link = link;
    
        @property
        def cpfHD(self):
            return self._cpfHD
        
        @cpfHD.setter
        def cpfHD(self, cpfHD):
            self._cpfHD = cpfHD;
        
        @property
        def cpfQHD(self):
            return self._cpfQHD
        
        @cpfQHD.setter
        def cpfcpfQHD(self, cpfQHD):
            self._cpfQHD = cpfQHD;


    def __str__(self) -> str:
        return f'{self.name} + - + {self.fhdPerf} + - + {self.qhdPerf} + - + {self.price} + - + {self.lowestPrice} + - + {self.dateLowestPrice} '

