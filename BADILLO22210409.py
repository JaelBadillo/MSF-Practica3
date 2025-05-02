""" Practica 3: Sistema Cardiovascular


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México


Nombre del alumno:  Jael Badillo Cruz
Número de control: 22210409
Correo institucional: l22210409@tectijuana.edu.mx


Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerias en consola
#!pip install control
#!pip install slycot
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tend, dt, w, h = 0, 0, 10, 1E-3, 10, 5
N = round((tend - t0) / dt) + 1
t = np.linspace(t0, tend, N)
u = np.sin (2*m.pi*95/60*t) + 0.8

# Función de transferencia sistema cardiovascular
def cardio(Z, C, R, L):
    num = [L * R, R * Z]        
    den = [C * L * R * Z, L * (R + Z), R * Z]
    sys = ctrl.tf(num, den)
    return sys

# Casos
Z, C, R, L = 0.020, 0.250, 0.600, 0.005
sysHipotenso = cardio(Z, C, R, L)

Z, C, R, L = 0.033, 1.500, 0.950, 0.010
sysNormotenso = cardio(Z, C, R, L)

Z, C, R, L = 0.050, 2.500, 1.400, 0.020
sysHipertenso = cardio(Z, C, R, L)

# Colores
#Colores
Amarillo = [1,0.7,0]
Rojo = [1,0,0]
Morado = [0.6,0.3,0.7]
Azul = [0.1,0.5,0.7]
# Datos de la simulación
x0,t0,tF,dt,w,h =0,0,30,1E-3,10,5
N = round((tF-t0)/dt)+1
t = np.linspace(t0,tF,N)
t = np.linspace(t0,tF,N)
u = np.sin(2*m.pi*95/60*t) + 0.8
signal = ['Hipotenso', 'Normotenso', 'Hipertenso']

def sys_cardio(Z,C,R,L):
        num = [L*R,R*Z]
        den = [C*L*R*Z,L*R+L*Z,R*Z]
        sys = ctrl.tf(num,den)
        return sys

# Hipotenso
Z, C, R, L = 0.020, 0.250, 0.600, 0.005
sysHipo = sys_cardio(Z,C,R,L)
print('Individuo: Hipotenso')
print(sysHipo)

#  Normotenso (control)
Z, C, R, L = 0.033, 1.500, 0.950, 0.010
sysN = sys_cardio(Z,C,R,L)
print('Individuo: Normotenso')
print(sysN)

#Hipertenso
Z, C, R, L = 0.050, 2.500, 1.400, 0.020
sysHiper = sys_cardio(Z,C,R,L)
print('Individuo: Hipertenso')
print(sysHiper)


#LAZO CERRADO


def plotsignals(u, sysHipo, sysN, sysHiper, signal):
    fig = plt.figure()
    ts,Vs = ctrl.forced_response(sysHipo,t,u,x0)
    plt.plot(t,Vs, ':', color = Amarillo, label = '$P_P(t): Hipotenso$')
   
    ts,Ve = ctrl.forced_response(sysN,t,u,x0)
    plt.plot(t,Ve,'-', color = Azul, label = '$P_P(t): Normotenso$')
    ts,pid = ctrl.forced_response(sysHiper,t,Vs,x0)
    fig.set_size_inches(w,h)
    fig.tight_layout()
    namepng = 'python_' + signal + '.png'
    namepdf = 'python_' + signal + '.pdf'
   
    plt.plot(t,pid, ':', linewidth = 2, color = Rojo,label = '$P_P(t): Hipertenso$')
    plt.grid(False)
   
    plt.xlim(0, 10)
    plt.ylim(-0.5, 1.5)
    plt.xticks(np.arange(0, 10, 1))
    plt.yticks(np.arange(-0.5, 2.5, 0.5))
    plt.xlabel('$t$ [s]')
    plt.ylabel('$V(t)$ [V]')
    plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol = 4,
               fontsize = 8, frameon = False)
    plt.show()
    fig.savefig(namepng,dpi = 600, bbox_inches = 'tight')
    fig.savefig(namepdf,bbox_inches ='tight')
    return sysHipo, sysN, sysHiper

plotsignals(u, sysHipo, sysN, sysHiper, 'señal')



# CONTROLADOR I

kP = 0.00206
kI = 1033.333



def tratamiento_PI(sysCaso):
    num = [kP, kI]
    den = [1, 0]
    controlador_PI = ctrl.tf(num, den)
    lazo = ctrl.series(controlador_PI, sysCaso)
    sistema_control = ctrl.feedback(lazo, 1, sign=-1)
    return sistema_control


sysHipertenso = tratamiento_PI(sysHiper)

fig2 = plt.figure()
_, respN = ctrl.forced_response(sysN, t, u, x0)
plt.plot(t, respN, '-', color=Azul, label='Normotenso')
_, respHiper = ctrl.forced_response(sysHiper, t, u, x0)
plt.plot(t, respHiper, '-', color=Amarillo, label='Hipertenso')
_, respTratado = ctrl.forced_response(sysHipertenso, t, u, x0)
plt.plot(t, respTratado, ':', linewidth=2, color=Rojo,
label='Tratamiento:Hipertenso')
plt.xlim(0, 10)
plt.ylim(-0.5, 2)
plt.xlabel('t [s]')
plt.ylabel('V(t) [V]')
plt.xticks(np.arange(0, 10, 1))
plt.yticks(np.arange(-0.5, 2.5, 0.5))
plt.legend(bbox_to_anchor=(0.5, -0.3), loc='center', ncol=4,
fontsize=8, frameon=False)
plt.title('HIPERTENSO')
plt.show()
#hipo
sysHipotenso = tratamiento_PI(sysHipo)
#normo
fig3 = plt.figure()
_, respN = ctrl.forced_response(sysN, t, u, x0)
plt.plot(t, respN, '-', color=Azul, label='Normotenso')
_, respHipo = ctrl.forced_response(sysHipo, t, u, x0)
plt.plot(t, respHipo, '-', color=Amarillo, label='Hipotenso')
_, respTratado = ctrl.forced_response(sysHipotenso, t, u, x0)
plt.plot(t, respTratado, ':', linewidth=2, color=Rojo,
label='Tratamiento:Hipotenso')
plt.xlim(0, 10)
plt.ylim(-0.5, 2)
plt.xlabel('t [s]')
plt.ylabel('V(t) [V]')
plt.xticks(np.arange(0, 10, 1))
plt.yticks(np.arange(-0.5, 2.5, 0.5))
plt.legend(bbox_to_anchor=(0.5, -0.3), loc='center', ncol=4,
fontsize=8, frameon=False)
plt.title('HIPOTENSO')
plt.show()
