#Importando librerías
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.title("Espectro Sismo Máximo según E.031")
st.markdown(
    "[Christian Cachi](https://www.linkedin.com/in/christian-cachi/)"
)
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

#Ingresar zona sísmica
Z = st.selectbox("Ingrese Zona Sísmica:", 
                 ("Z4", "Z3", "Z2", "Z1")
                 )

#Ingresar tipo de Suelo
S = st.selectbox("Ingrese Zona Sísmica:", 
                 ("S3", "S2", "S1", "S0")
                 )

#Periodos Tp y Tl
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

#Elegir T y calcular su SaM correspondiente
T = st.slider("T: Periodo (s)",min_value=0.00,max_value=7.00,step=0.01,value=2.50)
SaM = get_SaM(T)

#Gráfico espectro
fig, ax = plt.subplots(nrows=1,ncols=1, figsize=(7,4))
ax.set_xlim(0,7)
ax.set_ylim(0,2)
ax.plot(lista_T,lista_SaM, color = 'b')

#Línea vertical T
ax.plot([T,T],[0,3], color = 'r')

#Línea horizontal SaM 
ax.plot([0.00,7.00],[SaM,SaM], color = 'g')
ax.text(T+0.05,SaM+0.05,f"a = {SaM:.2f} g", color = "black")

ax.grid()
ax.set_title(f'Espectro Sismo Máximo {Z}{S}')
ax.set_xlabel('Periodo (s)')
ax.set_ylabel('Aceleración (g)')

st.pyplot(fig)
