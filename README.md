# VerificadorPrecoGPU
Script que pega informações de performance e preço e encontra menor valor e custo por frame (calculado por = Preço / Quantidade de FPS). Ao final gera uma tabela em **xlsx** com os dados encontrados


## Observações

- Se repetir o codigo de tempos em tempos, ele consegue guardar o menor preço histórico de cada placa de video
- Os dados são limitados a informações do **TomsHardware**, por isso dados da RTX 3060 8GB são ignorados
- Os dados de preços das GPUs dependem de uma API externa, do site **PlacasDeVideoApp**. Ela entra em manutenção esporadicamente. 

### Propriedades da tabela

- **Nome**: modelo da GPU
- **Avg FHD**: média performance em full hd
- **Avg QHD**: média performance em full qhd
- **Preco**: preço atual da GPU
- **Menor Preco**: menor preço ja registrado
- **Data Menor Preco**: data do menor preço ja registrado
- **Loja MP**: loja do menor preço histórico
- **CpF FHD**: custo por frame em full hd
- **CpF QHD**: custo por frame em full qhd
- **Link**: link do preço atual

### Utilização

- Clone ou baixe o repositório
- Crie o ambiente virtual com <code>python -m venv VerificadorPrecoGPU</code>
- Ative o ambiente: <code>.\Scripts\activate</code>
- Baixe as dependências: <code>pip install -r requiriments.txt</code>
- Execute o projeto: <code>python main.py</code>