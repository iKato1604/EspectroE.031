#Importando librerías
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

#st.title("Espectro Sismo Máximo según E.031")
st.title(":black[Espectro Sismo Máximo según E.031]")
"" #Salto de línea

c1, c2 = st.columns([5,2.5]) #para colocar a la derecha dividimos en 2 columnas con esas dimensiones
with c2: st.markdown("Developed by: [Christian Cachi](https://www.linkedin.com/in/christian-cachi/)")
st.divider()

#Zona sísmica
zona = {"Z4" : 0.45,
        "Z3" : 0.35,
        "Z2" : 0.25,
        "Z1" : 0.10}

#Tipo de suelo
suelos = {
    "Z4": {"S0": 0.80, "S1": 1.00, "S2": 1.05, "S3": 1.10},
    "Z3": {"S0": 0.80, "S1": 1.00, "S2": 1.15, "S3": 1.20},
    "Z2": {"S0": 0.80, "S1": 1.00, "S2": 1.20, "S3": 1.40},
    "Z1": {"S0": 0.80, "S1": 1.00, "S2": 1.60, "S3": 2.00}
        }

n = st.number_input("¿Cuánto espectros desea comparar?", min_value = 1, value = 1)

##NÚMERO DE ESPECTROS A COMPARAR

c = list(st.columns(n)) #Para convertir en una lista la cantidad de columnas
fig, ax = plt.subplots(nrows=1,ncols=1, figsize=(7,4))

st.divider()

#Elegir T y calcular su SaM correspondiente
Tt = st.slider("T: Periodo (s)",min_value=0.00,max_value=7.00,step=0.01,value=2.50)
for i in range(n):
    #Ingresar zona sísmica para el espectro "i"
    with c[i]: 
        
        Z = st.selectbox(f"Zona Sísmica {i+1}:", 
                    ("Z4", "Z3", "Z2", "Z1")
                    )

    #Ingresar tipo de Suelo para el espectro "i"
    with c[i]: 
        S = st.selectbox(f"Tipo de Suelo {i+1}:", 
                    ("S3", "S2", "S1", "S0")
                    )
    #Periodos Tp y Tl para el espectro "i"
    if S == "S0":
        Tp = 0.3
        Tl = 3.0
    elif S == "S1":
        Tp = 0.4
        Tl = 2.5
    elif S == "S2":
        Tp = 0.6
        Tl = 2.0
    elif S == "S3":
        Tp = 1.0
        Tl = 1.6
    
    #Función de espectro de pseudoaceleraciones  
    def get_SaM(T):
        U = 1
        if T < 0.2*Tp:
            C = 1+7.5*(T/Tp)
        elif T < Tp:
            C = 2.5   
        elif T < Tl:
            C = 2.5*(Tp/T)
        else:
            C = 2.5*(Tp*Tl/(T**2))
        SaM = 1.5*zona[Z]*U*C*suelos[Z][S] 
        return SaM  

    #Espectro de pseudoaceleraciones
    lista_1 = [i/1000 for i in range(0,7001,1)]
    lista_T = []
    lista_SaM = []
    for T in lista_1:
        get_SaM(T)
        lista_T.append(T)
        lista_SaM.append(get_SaM(T))
            
    #Gráfico espectro
    
    ax.set_xlim(0,7)
    ax.set_ylim(0,2)
    ax.plot(lista_T,lista_SaM, label=Z+S)

    #Línea horizontal SaM 
    SaM = get_SaM(Tt)
    ax.plot([0.00,7.00],[SaM,SaM], "--", color = 'black')
    ax.text(7.05,SaM+0.05,f"a{i+1} = {SaM:.2f} g", color = "black")

st.divider()

#Línea vertical T
ax.plot([Tt,Tt],[0,3], "--", color = 'r')
ax.text(Tt+0.05,1.8,f"T = {Tt:.2f} s", color = "r")

ax.grid()
ax.set_title(f'Espectro Sismo Máximo E.031 \n')
ax.set_xlabel('\n Periodo (s)')
ax.set_ylabel('Aceleración (g)\n')
ax.legend()

st.pyplot(fig)
