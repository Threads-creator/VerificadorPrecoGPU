# VerificadorPrecoGPU
Script que pega informações de performance e preço e encontra menor valor e custo por frame


## Observações

- Se repetir o codigo de tempos em tempos, ele consegue guardar o menor preço histórico de cada placa de video
- Os dados são limitados a informações do **TomsHardware**, por isso dados da RTX 3060 8GB são ignorados 

### Propriedades da tabela

- **Nome**: modelo da GPU
- **Avg FHD**: média performance em full hd
- **Avg QHD**: média performance em full qhd
- **Preco**: preço atual da GPU
- **Menor Preco**: menor preço ja registrado
- **Data Menor Preco**: data do menor preço ja registrado
- **Loja MP**: loja do menor preço histórico
- **CpF FHD**: custo por fram em full hd
- **CpF QHD**: custo por fram em full qhd
- **Link**: link do preço atual