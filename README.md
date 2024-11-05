# Análise do Mercado de Trabalho nos EUA com Dados do LinkedIn

Este projeto visa explorar as tendências e demandas do mercado de trabalho nos Estados Unidos, com base em dados de vagas publicadas no LinkedIn entre 2023 e 2024. A análise inclui informações sobre salários, tipos de vagas (remotas e presenciais) e projeções de contratações para 2025.

## Ferramentas e Bibliotecas Utilizadas

- **Python**
  - Análise e tratamento de dados, além de visualizações interativas.
  
- **Dash**
  - Criação da interface de visualização dos dados e gráficos interativos.

- **Prophet**
  - Modelo de previsão para identificar tendências de crescimento em áreas específicas.

- **Pandas e NumPy**
  - Manipulação e padronização dos dados.

## Principais Transformações de Dados

1. **Padronização Salariais:**  
   Conversão dos salários para uma base anual, facilitando comparações entre diferentes níveis de senioridade.

2. **Substituição de Valores Nulos:**  
   Valores nulos em salários médios substituídos pela média entre o salário mínimo e máximo, arredondados para o milhar mais próximo.

3. **Padronização Geográfica:**  
   Mapeamento de abreviações de estados e localidades, incluindo regiões internacionais, para um dicionário padronizado.

4. **Criação de Coluna de Controle:**  
   Coluna "calculated_med_salary" criada para validação e consistência dos dados após a padronização.

## Visualizações
Previsão de Vagas em 2025 por Estado nos EUA
 <img src='/project/assets/mapa-grafico.png'>
 
Relação Senioridade X Salário
<img src='/project/assets/senioridade-salario.png'>

Distribuição de Vagas Remotas e Não Remotas
<img src='/project/assets/distribuicao-de-vagas.png'>

Media Salarial: Vagas Remotas Vs Não Remotas
<img src='/project/assets/media-salarial.png'>

## Como Executar o Projeto

1. **Baixe o Dataset**  
   Baixe o dataset necessário a partir deste [link no Kaggle](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) e adicione-o ao diretório de dados do projeto.

2. **Instale as Dependências**  
   Certifique-se de ter o Python 3.8+ instalado. Para instalar as dependências, use o arquivo `requirements.txt` incluído no projeto com o seguinte comando:

   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o Projeto**  
   No terminal, execute o comando:

   ```bash
   python project/linkedin_dashboard/main.py
   ```

4. **Acesse o Dash**  
   Abra um navegador e acesse `http://localhost:8050` para visualizar a interface e interagir com as previsões e dados de mercado.

## Dependências

O arquivo `requirements.txt` inclui as seguintes bibliotecas e versões:

```plaintext
pandas==2.2.2
dash==2.17.1
pydantic-settings==2.4.0
python-dotenv==1.0.1
scikit-learn==1.5.2
matplotlib==3.9.2
ipython==8.27.0
geopandas==1.0.1
numpy==2.1.2
prophet==1.1.6
notebook==7.2.2
```
