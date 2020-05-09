tabela = soup.find_all('table')[8]

# Removendo os valores com percentual
for span_tag in tabela.findAll('span', {'class': 'varperc'}):
    span_tag.replace_with('')

# O objeto que vem pra cá é um beautifulsoup. Preciso converter pra TXT pra ser traa
ano = pd.read_html(str(tabela))

# O read_html retorna uma tabela. Ao fazer o concat ela vira um df
df = pd.concat(ano)

# Tirando linhas e colunas sem dados
df = df.drop(['Unnamed: 1'], axis=1)
df = df.drop(0, axis=0)

# Mudando a orientação da tabela
df.set_index('Unnamed: 0', inplace=True)
df = df.transpose()

# Resetando o Index
df = df.reset_index(drop=False)

# Trocando Header
df = df.rename(columns={'index': 'Ano'})

# Ordenando por ano
df.sort_values(by=['Ano'], inplace=True)

# Resentando o index
df = df.reset_index(drop=True)

# Tirando colunas desnecessárias
df = df.drop(['Common Shares Outstanding',
              'Depreciation and Amortization'], axis=1)

# Transformando tudo pra string (pra tirar dados desnecessários como pontos e porcentagens)
df = df.applymap(str)
df = df.applymap(lambda x: x.replace("%", "").replace(".", ""))
df = df.applymap(int)


# Joga fora linhas que não tem valores
df.dropna()
print(ticker_company)
df
