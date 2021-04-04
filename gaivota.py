import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Interface de navegação#

menu = ["Recomendador", "O Gaivota", "Sistemas de Recomendação", "Contatos"]
choice = st.sidebar.selectbox("Menu", menu)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Navegando à pagina do recomendador de produtos#

if choice == "Recomendador":

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Recepção da área de Recomendação#

    #Conteúdo textual da app
    st.title('Recomendador do Gaivota')
    st.write('Bem vindos ao simulador de compras e recomendações do **_Gaivota_**!')
    
    #Imagem de sistemas de recomendação on site (supermercado) 
    st.image("anexos/recommender_systems.png", width=600, output_format='JPEG')

    #Introdução à seção de compras
    st.subheader("Escolha um ou mais produtos da lista abaixo e arraste o slider para selecionar a quantidade de cada um. Clique em 'Adicionar ao carrinho' e então aparecerá uma tabela com a lista de produtos presentes no carrinho.")

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Tela principal de Recomendação#

    #Importando o dataframe, proveniente do data cleaning, contendo o histórico de compras dos clientes:
    df = pd.read_csv('anexos/df.csv')

    #Lista de produtos para mostrar ao usuário
    product_array = df['product'].unique() #seleciona os produtos únicos da coluna de produtos do dataframe
    show_product_list = product_array.tolist() #transforma em lista o array
    display = (show_product_list) #disponibiliza a lista no display

    options = list(range(len(display))) #options, labels para as opções de escolha, é a lista disponível com desde o primeiro até o último item da lista de produtos
    value = st.selectbox("Lista de produtos", options, format_func=lambda x: display[x]) #atribui à value o produto selecionado pelo widget, com texto Produto, options, função para especificar como mostrar os labels

    #Quantidade do produto:
    qtd = st.slider("Quantidade", 1, 10)

    #Permissão para alterar o cache / salvar a inserção de dados:
    @st.cache(allow_output_mutation=True)


    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Criação do Array do Usuário de Recomendação

    def get_data(): #definimos a função get_data, que retorna uma lista (vazia no momento)
        return []

    #Pivotando o dataframe df (histórico de compras), para usar na captura das colunas a fim de estruturar o dataframe do usuário e posteriormente, para o cálculo da matriz de similaridade:
    pivot_df = pd.pivot_table(df, index=['id'], columns=['product'], aggfunc=[np.sum], values=['amount'], margins=False)

    #Cria a lista de produtos organizadas pela sequência da pivot (importante para manter a ordem no dataframe produzido pelo usuário):
    i=0
    pivot_prod_order_list =[]
    for term in pivot_df.columns:
        pivot_prod_order_list.append(pivot_df.columns[i][2])
        i += 1

    #Cria o dataframe que será usado no cálculo ("cesta escondida"):
    user_df = pd.DataFrame(columns=pivot_prod_order_list)

    #Botão para adicionar produtos aos carrinhos 'show_user_df' e 'user_df':
    if st.button("Adicionar produto ao carrinho"): #botão para appendar ao get_data (lista)
        get_data().append({"Produto": display[value], "Quantidade": qtd}) #appendamos ao get_data (lista) tanto o produto com identificação 'display[value]' como a quantidade 'qtd', formando uma lista de dicionários com a primeira appendada
        user_df.loc[0, display[value]] = qtd #editamos o dataframe do usuário, incluindo a quantidade 'qtd' referente à coluna selecionada em 'display[value]'


    #Botão para limpar o carrinho:
    if st.button("Limpar carrinho"): #botão para limpar o cache (apagará todo o cache do site!)
        from streamlit import caching
        caching.clear_cache()

    #Cria o dataframe que será usado para mostrar as compras (carrinho):

    show_user_df = pd.DataFrame(get_data()) #guardamos o get_data no formato de dataframe, para mostrar ao usuário o que está no carrinho
    if len(show_user_df.columns)>0:
        #st.write(show_user_df.columns[0]) #só mostrando que o termo zero das colunas é 'Produto'
        show_user_df = show_user_df.groupby(show_user_df.columns[0]).sum().T

    st.subheader("Carrinho de compras:")
    st.write(show_user_df)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Cálculo da matriz de similaridade e disposição dos resultados

    ##Seção de geração de sugestões:
    if st.button("Simular compra e sugerir-me produtos"): #botão para gerar as sugestões   

        #Cálculo da matriz de similaridade:
        pivot_array = pivot_df.to_numpy() #agora transformando o pivot em numpy array
        user_array = user_df.merge(show_user_df, how='outer')[pivot_prod_order_list].to_numpy() #mergindo com o show_user_df (merge tipo outer), reorganizando as colunas conforme a pivot do df dos clientes e transformando o dataframe das compras do usuário em numpy array
        from sklearn.metrics.pairwise import nan_euclidean_distances  #importando a biblioteca pra calcular as distâncias euclidianas
        nan = float("NaN") #definindo que os nulos sejam do tipo float
        dist = nan_euclidean_distances(user_array, pivot_array) + 1 #podemos somar 1 a cada distância do array, assim evitamos a divisão por zero
        array_closest_clients = 1/dist # distância entre as linhas de X
        similar_products = pivot_df.iloc[np.nanargmax(array_closest_clients),:] #lista de produtos comprados pela pessoa mais próxima na matriz
        similar_products = similar_products[similar_products.notna()] #só queremos os produtos que sejam não nulos

        st.subheader("Os produtos recomendados pelo Gaivota especialmente para você são:")

        for index, value in similar_products.items(): #informamos os produtos recomendados
            if str(index[2]) not in show_user_df.columns.tolist():    
                st.write('-', str(index[2]))

        #st.subheader("Os produtos em comum com outros clientes foram:")
        #for i in show_user_df.columns.tolist(): #informamos os produtos comprados
            #st.write('-', i)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Navegando à pagina sobre o Gaivota#

elif choice == "O Gaivota":
    st.header("O Gaivota")
    st.write("O Comercial Gaivota é a principal loja varejista da região de Pinheiros a oferecer importados orientais. Também apresenta uma variedade de produtos locais (como guiozas, shoyos e massas) para atender ao público da região.")
    
    st.image("anexos/gaivota.png", width=300, caption="ようこそ!", output_format='JPEG')

    st.text("")
    st.text("")
    st.text("")

    st.image("anexos/produtos_japoneses.jpg", width=300, caption="Seleção de importados.", output_format='JPEG')

    st.text("")
    st.text("")
    st.text("")

    st.image("anexos/takashi_to_frito.jpg", width=300, caption="Produtores locais: Takashi da TO-FRTO, promovendo degustação de tofu frito.", output_format='JPEG')
    
    st.text("")
    st.text("")
    
    st.write("Com as restrições advindas da pandemia, o comércio da região foi fortemente afetado e ocasionou o fechamento de vários empreendimentos em Pinheiros. O faturamento do Gaivota caiu consideravelmente a partir do lockdown de Março porém voltou nos meses seguintes com a reabertura.")

    st.text("")
    st.text("")
    st.text("")

    faturamento = pd.read_csv('anexos/faturamento_diario.csv', sep=';', error_bad_lines=False)#.fillna(value=0) #ler o csv contendo o faturamento diário
    #st.write(faturamento) #dataframe com faturamento diário

    timeseries_faturamento_diario = alt.Chart(faturamento).mark_line().encode(
        x='Data:T',
        y='Faturamento:Q'
    ).properties(
        width=800,
        height=300,
        title='Faturamento diário fantasia de Janeiro/2020 a Julho/2020'
    )
    st.altair_chart(timeseries_faturamento_diario)

    
    #faturamento_grouped = faturamento.groupby('Mês-Num').sum() #dataframe com faturamento mensal
    #st.write(faturamento_grouped) #mostrar o dataframe de faturamento mensal
    
    st.write("Apesar da retomada no faturamento observado são esperados novos lockdowns. A grande variação do faturamento, e principalmente pelo fato dela ser inesperada, é prejudicial à saúde e o planejamento de estoque do comércio, podendo ocorrer sobrestoque de vários produtos considerados supérfluos ou menos conhecidos.")
    st.text("")
    st.text("")
    st.text("")

    boxplot_faturamento_mensal = alt.Chart(faturamento).mark_boxplot().encode(
        x='N-Mês:O',
        y='Faturamento:Q'
    ).properties(
        width=600,
        height=450,
        title='Boxplot do faturamento mensal fantasia de Janeiro/2020 a Julho/2020',
    )
    st.altair_chart(boxplot_faturamento_mensal)

    st.write("A única maneira de sobreviver a essa situação seria através da inovação. Nesse caso, o alcance de um número maior de clientes e divulgação de produtos menos conhecidos pelo público. Aí surge a oportunidade de aplicar um sistema de recomendação de produtos aos clientes da loja, para aumentar a captura em produtos menos conhecidos e beneficiando-se da similaridade de gostos entre os clientes.")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Navegando à pagina sobre o projeto de Sistema de Recomendação#

elif choice == "Sistemas de Recomendação":
    st.header("Sistemas de recomendação")
    st.subheader("Como eles funcionam e como estruturamos o sistema do Gaivota?")
    
    st.subheader("Como era antigamente...")
    st.write("No passado não-distante, o sistema de recomendação usual era a própria vitrine das lojas. Normalmente alí estavam dispostos os maiores best-sellers. Esse modelo priorizava os produtos que mais vendiam por haver uma limitação física com relação ao inventório.")
    
    st.text("")
    st.text("")

    st.image("anexos/vitrine_fisica2.jpg", width=500, caption="Sistema de recomendação 'old school'.", output_format='JPEG')

    st.text("")

    st.subheader("Como é hoje...")    
    st.write("Hoje em dia, em contrapartida, as lojas possuem inventários significativamente maiores, podendo disponibilizar uma quantidade muito maior de produtos. O problema está justamente em como ofertá-los ao consumidor de maneira eficiente.")

    st.text("")
    st.text("") 

    st.image("anexos/vitrine_online_weird.JPG", width=600, caption="Vitrine online do curioso e-commerce Prankalot: https://prankalot.com/.", output_format='JPEG')
    
    st.text("")
    st.text("") 

    st.write("A disponibilidade de coleta, processamento e disposição de dados também possibilita hoje em dia personalizarmos essa experiência de oferta, sendo mais preciso nas sugestões de produtos aos clientes e podendo atender nichos de mercado antes inalcançáveis. No caso do Gaivota, queremos que os clientes explorem outros produtos da loja.")

    st.text("")
    st.text("") 
    
    st.subheader("Modelos")
    st.write("Os sistemas de recomendação mais comuns são baseados em duas técnicas: **_Filtragem Colaborativa_** ou **_Filtragem por Conteúdo_**. O primeiro se baseia na idéia de similaridade de gostos entre pessoas com base nos produtos adquiridos em comum, para sugerir um segundo produto a um deles. O segundo modelo se baseia na similaridade de features/características entre produtos para realizar a recomendação de um segundo produto.")
    
    st.text("")
    st.text("")

    st.image("anexos/recommendation-systems-types.png", width=700, caption="Tipos de filtragem para sistemas de recomendação. Fonte: https://www.themarketingtechnologist.co/building-a-recommendation-engine-for-geeksetting-up-the-prerequisites-13/", output_format='JPEG')

    st.text("")
    st.text("") 

    st.write("Utilizamos o **_Filtragem Colaborativa_** com a **_abordagem de memória_**, já que possuímos o histórico de produtos e quantidades compradas por cada pessoa. Não possuímos nenhuma característica dos produtos no momento (como origem, país, seção da loja, alimento/durável, etc.). Calculamos então a distância entre os usuários pela distância euclidiana e encontramos os usuários mais similares, recomendando produtos desses usuários.")

    st.text("")
    st.text("")

    st.write("Algumas características do dataset que apresentam desafios e oportunidades:")
    st.write("-","Matriz esparsa: muitos produtos, muitos clientes, pouca interação cliente-produtos. Isso gera anomalias no cálculo da distância euclidiana, já que a presença de 1 elemento em quantidade mínima de 1 unidade pode acabar resultando na busca de um cliente que pouco tem a ver com os gostos do primeiro.")
    st.write("-","Possíveis grupos de clientes: existem certos grupos de clientes que podem ser explorados futuramente via Clustering (veganos, orientais, doceiros, etc.), os quais poderiam refinar a recomendação. Isso evitaria sugestões anômalas. Exemplo: uma compra de Panko Bread Crumbs e uma sugestão de Gás Butano.")
    st.write("-","Inconsistência nos labels: produtos com nomes levemente diferentes, devido a origem, peso ou quantidade de unidades, podem acabar sendo sugeridos na compra de produtos praticamente iguais. Exemplo: o cliente comprar um Shoyo Sakura 500ml e os sitema sugerir um Shoyo Ajinomoto 1L.")
    st.write("-","Somente compras realizadas com CPF/CNPJ estão presentes nas base de dados, o que pode deixar a base menos representativa em algumas situações. Exemplo: compras com poucos itens normalmente as pessoas não pedem CPF na nota e há produtos mais associados a compras pequenas, como refrigerantes.")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Navegando à pagina de Contatos#

elif choice == "Contatos":
    st.header("Contatos")
    st.subheader("Comercial Gaivota")
    st.write('-', 'Instagram: https://www.instagram.com/comercialgaivota/?hl=pt')
    st.write('-', 'Facebook: https://www.facebook.com/Comercial-Gaivota-212548015453462/')
    st.write('-', 'Endereço (Google Maps): [Rua Cunha Gago 359, Pinheiros, São Paulo/SP, Brasil](https://www.google.com/maps/place/Gaivota+asian+food/@-23.5655365,-46.6917266,15z/data=!4m2!3m1!1s0x0:0x60e4e73b6f48c387?sa=X&ved=2ahUKEwjP4sT26KrvAhX-DrkGHXKJA1kQ_BIwD3oECBwQBQ)')
    st.subheader('Desenvolvido por:')
    st.write('-', 'Pedro Forastieri de Almeida Prado')
    st.write('-', 'Email: pfaprado@gmail.com')
    st.write('-', 'Github: https://github.com/Forastierii')
    st.write('-', 'LinkedIn: https://www.linkedin.com/in/pedroforastieri/')
    st.write("Agradecimentos a Elcio Hideki Kimura pela disponibilidade dos dados para realizar esse trabalho.")
    
    st.text("")
    st.text("")
    st.text("")

    st.image("anexos/keep_it_local.jpg", width=300, caption="Obrigado!", output_format='JPEG')