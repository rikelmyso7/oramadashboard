import pandas as pd
import plotly.express as px
import streamlit as st

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

        if verification == "Valor":

            # Ajeita a coluna de valores
            df["Valor"] = df["Valor"].str.replace('R$ ', '').str.replace(',', '.').astype(float)

            df['Total'] = df['Valor'].cumsum()

            # Converter a coluna "Data" para o tipo datetime
            df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
            df["Day"] = df["Data"].apply(lambda x: str(x.day))
            
            with st.sidebar:
                dia = df["Day"].unique().tolist()
                dia_selecionado = st.selectbox("Slecione o Dia", ["todos"] + dia)

                if dia_selecionado:
                    df_filtered = df[df["Day"] == dia_selecionado]

                    fig = px.bar(df_filtered, x="Vendedor", y="Valor", color="Day", title="Total de Vendas Acumulado",
                    template='plotly_dark')

                if dia_selecionado == "todos":
                    df_filtered = df
                    
                    fig = px.bar(df_filtered, x="Vendedor", y="Valor", color="Day", title="Total de Vendas Acumulado",
                    template='plotly_dark', barmode="group")
                
                    
            st.plotly_chart(fig, use_container_width=True)
            if dia_selecionado == "todos":
                total_vendedor = df_filtered['Valor'].sum()
                st.write(f'Valor total de vendas para {dia_selecionado} os dias: R${total_vendedor:.2f}')
            elif dia_selecionado:
                df_filtered = df[df["Day"] == dia_selecionado]
                total_vendedor = df_filtered["Valor"].sum()
                st.write(f'Valor total de vendas para o dia {dia_selecionado}: R${total_vendedor:.2f}')

            st.dataframe(df, use_container_width=True)
        else:
            bar.write('<span style="color:#E80F0F">Arquivo não esta na opção certa</span>', unsafe_allow_html=True)
elif escolha == "Produtos mais Vendidos":
    upload_file = bar.file_uploader('Escolha seu arquivo')
    if upload_file is not None:
        df = pd.read_excel(upload_file)
        verification = df.columns[2]

        if verification == "Quantidade":

            # Ajeita a coluna de valores
            df["Valor Total"] = df["Valor Total"].str.replace('R$ ', '')  # Remove o prefixo 'R$ '
            df["Valor Total"] = df["Valor Total"].str.replace('.', '')     # Remove os pontos de milhar
            df["Valor Total"] = df["Valor Total"].str.replace(',', '.')    # Substitui a vírgula por um ponto
            df["Valor Total"] = df["Valor Total"].astype(float)             # Converte para float

            # Converter a coluna "Data" para o tipo datetime
            df["Última Venda"] = pd.to_datetime(df["Última Venda"], dayfirst=True)
            df["Day"] = df["Última Venda"].apply(lambda x: str(x.day))
            
            with st.sidebar:
                dia = df["Day"].unique().tolist()
                dia_selecionado = st.selectbox("Slecione o Dia", ["todos"] + dia)

                if dia_selecionado:
                    df_filtered = df[df["Day"] == dia_selecionado]

                    fig = px.bar(df_filtered, x="Quantidade", y="Valor Total", color="Produto", 
                                title="Produtos mais Vendidos", barmode="group")
                    fig.update_layout(bargap=0.5,xaxis=dict(autorange="reversed"))

                if dia_selecionado == "todos":
                    df_filtered = df
                    
                    fig = px.bar(df_filtered, x="Quantidade", y="Valor Total", color="Produto", 
                                title="Produtos mais Vendidos", barmode="stack")
                    fig.update_layout(bargap=0.1,xaxis=dict(autorange="reversed"))
                
                    
            st.plotly_chart(fig, use_container_width=True)
            if dia_selecionado == "todos":
                total_vendedor = df_filtered['Valor Total'].sum()
                st.write(f'Valor total de vendas para {dia_selecionado} os dias: R${total_vendedor:.2f}')
            elif dia_selecionado:
                df_filtered = df[df["Day"] == dia_selecionado]
                total_vendedor = df_filtered["Valor Total"].sum()
                st.write(f'Valor total de vendas para o dia {dia_selecionado}: R${total_vendedor:.2f}')

            st.dataframe(df, use_container_width=True)
        else:
            bar.write('<span style="color:#E80F0F">Arquivo não esta na opção certa</span>', unsafe_allow_html=True)