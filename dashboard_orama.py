import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title('DASHBOARD DE CONTROLE :technologist:')

verification = None
bar = st.sidebar
escolha = bar.selectbox("Escolha uma opção", ["", "Vendas Totais", "Produtos mais Vendidos"])
if escolha == "":
    bar.write('<span style="color:#E80F0F">Nada selecionado</span>', unsafe_allow_html=True)
if escolha == "Vendas Totais":
    upload_file = bar.file_uploader('Escolha seu arquivo')
    if upload_file is not None:
        df = pd.read_excel(upload_file)
        verification = df.columns[2]
        data_atual = datetime.now()
        dia_anterior = data_atual - timedelta(days=3)
        data_formatada = data_atual.strftime('%d de %B')
        df2 = dia_anterior.strftime('%d')

        if verification == "Valor":
            valores = df["Valor Total"].drop_duplicates()
            df["Valor Total"] = valores
            # Converter a coluna "Data" para o tipo datetime
            df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
            df["Day"] = df["Data"].apply(lambda x: str(x.day))

            with st.sidebar:
                dia = df["Day"].unique().tolist()
                dia_selecionado = st.selectbox("Slecione o Dia", ["todos"] + dia)

                if dia_selecionado:
                    data_formatada = data_atual.strftime('de %B')
                    df_filtered = df[df["Day"] == dia_selecionado]
                    soma_dia = df.groupby(["Day", "Vendedor"])['Valor'].sum().reset_index()
                    df_filtered = pd.merge(df_filtered, soma_dia, on=['Day','Vendedor'], suffixes=('', ' Dia'))
                    total = df_filtered["Valor"].sum()

                    fig = px.bar(df_filtered, x="Vendedor", y="Valor Dia", color="Day", title=f"Total de Vendas Acumulado dia {dia_selecionado} {data_formatada}",
                    template='plotly_dark', barmode="overlay", text="Valor Dia", height=500,)
                    fig.update_layout(bargap=0.1)
                    fig.update_traces(texttemplate="R$%{text},00" ,textposition='outside')
                    fig.add_annotation(
                        x="Da Roça", y=2100,  # Posição do texto
                        text=f"Valor Total: R${total},00", showarrow=False, font=dict(family="Arial",size=12,color="white"))
                    

                if dia_selecionado == "todos":
                    data_formatada = data_atual.strftime('%d de %B')
                    df_filtered = df
                    soma_dia = df_filtered.groupby(["Day", "Vendedor"])['Valor'].sum().reset_index()
                    df_filtered = pd.merge(df_filtered, soma_dia, on=['Day','Vendedor'], suffixes=('', ' Dia'))
                    total = df_filtered["Valor"].sum()
                    
                    fig = px.bar(df_filtered, x="Vendedor", y="Valor Total",
                                 title=f"Total de Vendas Acumulado {df2} a {data_formatada}", text="Valor Total", height=500,
                    template='plotly_dark', barmode="stack")
                    fig.update_layout(bargap=0.1)
                    fig.update_traces(texttemplate="R$%{text},00" ,textposition='outside')
                    fig.add_annotation(
                        x="Sassafraz", y=3500,  # Posição do texto
                        text=f"Valor Total: R${total},00", showarrow=False, font=dict(family="Arial",size=12,color="white"))
                    
            st.plotly_chart(fig, use_container_width=True)
                
            if dia_selecionado == "todos":
                total_vendedor = df['Valor Total'].sum()
                st.write(f'Valor total de vendas para {dia_selecionado} os dias: R${total_vendedor:.2f}')
                st.dataframe(df, use_container_width=True)
            elif dia_selecionado:
                df_filtered = df[df["Day"] == dia_selecionado]
                soma_dia = df.groupby(["Day", "Vendedor"])['Valor'].sum().reset_index()
                df_filtered = pd.merge(df_filtered, soma_dia, on=['Day','Vendedor'], suffixes=('', ' Dia'))
                total_vendedor = df_filtered["Valor"].sum()
                st.write(f'Valor total de vendas para o dia {dia_selecionado}: R${total_vendedor:.2f}')

                st.dataframe(df_filtered, use_container_width=True)
        else:
            bar.write('<span style="color:#E80F0F">Arquivo não esta na opção certa</span>', unsafe_allow_html=True)
elif escolha == "Produtos mais Vendidos":
    upload_file = bar.file_uploader('Escolha seu arquivo')
    if upload_file is not None:
        df = pd.read_excel(upload_file)
        verification = df.columns[2]
        data_atual = datetime.now()
        dia_anterior = data_atual - timedelta(days=3)
        data_formatada = data_atual.strftime('%d de %B')
        df2 = dia_anterior.strftime('%d')

        if verification == "Quantidade":

            # Ajeita a coluna de valores
            df["Valor Total"] = df["Valor Total"].str.replace('R$ ', '')  # Remove o prefixo 'R$ '
            df["Valor Total"] = df["Valor Total"].str.replace('.', '')     # Remove os pontos de milhar
            df["Valor Total"] = df["Valor Total"].str.replace(',', '.')    # Substitui a vírgula por um ponto
            df["Valor Total"] = df["Valor Total"].astype(float)             # Converte para float

            # Converter a coluna "Data" para o tipo datetime
            df["Última Venda"] = pd.to_datetime(df["Última Venda"], dayfirst=True)
            df["Day"] = df["Última Venda"].apply(lambda x: str(x.day))
            col1, col2 = st.columns(2)
            with st.sidebar:
                dia = df["Day"].unique().tolist()
                dia_selecionado = st.selectbox("Slecione o Dia", ["todos"])

                if dia_selecionado:
                    data_formatada = data_atual.strftime('de %B')
                    df_filtered = df[df["Day"] == dia_selecionado]
                    soma_dia = df_filtered.groupby(["Day", "Vendedor"])['Quantidade'].sum().reset_index()
                    df_sorted = pd.merge(df_filtered, soma_dia, on=['Day','Vendedor'], suffixes=('', ' Dia'))

                    fig_prod = px.bar(df_sorted, y="Vendedor", x="Quantidade Dia", text="Quantidade Dia",
                                title=f"Quantidade de produtos dia {dia_selecionado} {data_formatada}", barmode="group", orientation="h")
                    fig_prod.update_layout(bargap=0.1)
                    fig_prod.update_traces(texttemplate="%{text}", textposition='outside')

                    fig_rank = px.pie(df_sorted, values="Quantidade", names="Produto", title=f"Ranking de produtos por PDV dia {dia_selecionado} {data_formatada}",)
                    fig_rank.update_traces(textinfo='percent+label')

                    df_sorted = df_filtered.sort_values(by="Vendedor", ascending=True)
                    fig_pdv = px.bar(df_sorted, y="Quantidade", x="Vendedor", color="Produto", text="Quantidade",
                                title=f"Quantidade de produtos dia {dia_selecionado} {data_formatada}", barmode="group", orientation="v")
                    fig_pdv.update_layout(bargap=0.2)
                    fig_pdv.update_traces(texttemplate="%{text}", textposition='outside')

                if dia_selecionado == "todos":
                    data_formatada = data_atual.strftime('%d de %B')
                    df_filtered = df
                    soma_dia = df_filtered.groupby(["Day", "Vendedor"])['Quantidade'].sum().reset_index()
                    df_sorted = pd.merge(df_filtered, soma_dia, on=['Day','Vendedor'], suffixes=('', ' Dia'))
                    df_sorted = df_filtered.sort_values(by="Total Produtos", ascending=True)

                    fig_prod = px.bar(df_sorted, y="Vendedor", x="Total Produtos", text="Total Produtos",
                                title=f"Quantidade de produtos dia {df2} a {data_formatada}", barmode="overlay", orientation="h", width=600)
                    fig_prod.update_layout(bargap=0.1)
                    fig_prod.update_traces(texttemplate="%{text}", textposition='outside')

                    fig_rank = px.pie(df_sorted, values="Quantidade", names="Produto", title=f"Ranking de produtos {df2} a {data_formatada}",)
                    fig_rank.update_traces(textinfo='percent+label')


                    df_sorted = df_filtered.sort_values(by="Vendedor", ascending=True)
                    fig_pdv = px.bar(df_sorted, y="Quantidade", x="Vendedor", color="Produto", text="Quantidade",
                                title=f"Quantidade de produtos por PDV {df2} a {data_formatada}", barmode="group", orientation="v")
                    fig_pdv.update_layout(bargap=0.2)
                    fig_pdv.update_traces(texttemplate="%{text}", textposition='outside')
                    
                    
            col1.plotly_chart(fig_prod, use_container_width=True)
            col2.plotly_chart(fig_rank, use_container_width=True)
                    
            st.plotly_chart(fig_pdv, use_container_width=True)
            if dia_selecionado == "todos":
                df_filtered = df
                df_sorted = df.sort_values(by="Total Produtos", ascending=False)
                total_vendedor = df_filtered['Valor Total'].sum()
                #st.write(f'Valor total de vendas para {dia_selecionado} os dias: R${total_vendedor:.2f}')
                st.dataframe(df_sorted, use_container_width=True)
            elif dia_selecionado:
                df_filtered = df[df["Day"] == dia_selecionado]
                df_sorted = df.sort_values(by="Day", ascending=True)
                soma_dia = df_filtered.groupby(["Day", "Vendedor"])['Quantidade'].sum().reset_index()
                df_sorted = pd.merge(df_filtered, soma_dia, on=['Day','Vendedor'], suffixes=('', ' Dia'))
                total_vendedor = df_filtered["Valor Total"].sum()
                #st.write(f'Valor total de vendas para o dia {dia_selecionado}: R${total_vendedor:.2f}')

                st.dataframe(df_sorted, use_container_width=True)
        else:
            bar.write('<span style="color:#E80F0F">Arquivo não esta na opção certa</span>', unsafe_allow_html=True)