import win32gui #Me permite controlar el comportamiento de las aplicaciones de windows
import win32con #Me permite controlar el comportamiento de las aplicaciones de windows
import PySimpleGUIQt as sg #Me permite hacer aplicaciones con interfaz grafica
import threading #Me permite manejar hilos
import time #Libreria con herramientas relacionadas al tiempo
import subprocess
import openpyscad as ops

########Diseño de componentes#####
def crearDimensiones(base, altura, grosor): #Esto solo ayuda a crear el cuerpo del dron
    cuboFrente = ops.Cube([base/2, base/2, grosor+5], center = True)
    cuboFrente = cuboFrente.translate([0,altura/2,grosor/2+1])
    cuboDer = ops.Cube([altura - base/2, altura - base/2, grosor+5], center = True)
    cuboDer = cuboDer.translate([(altura - base/2)/2+base/2-base/4,0,grosor/2+1])
    dimensiones = cuboFrente + cuboDer
    return dimensiones

def crearBateria(base, altura, grosor):
    bateria = ops.Cube([base/2, altura - base/2, base/10], center=True)
    bateria = bateria .translate([0,0,base/20 + grosor/2])
    bateria = bateria.color("Blue")
    return bateria

def crearPerno(diametro,altura):
    perno = ops.Cylinder(r = diametro/2, h = altura,  _fn=30)
    return perno

def pernosBrazo(base, altura, dimensionZ):
    #cuadrado ficticio base= 2*base/3
    lado = base/12
    brazoParte2 = ops.Cube([base/4, base/4, dimensionZ*0.2]) #Parte de union entre brazo y cuerpo
    brazoParte2 = brazoParte2.translate([base/4, altura/2-base/4, grosor])

    perno1 = ops.Cylinder(r=1.6, h=dimensionZ, _fn=30)
    perno1 = perno1.translate([lado, lado, -5])
    perno2 = perno1.mirror([1, 0, 0])

    perno34 = (perno1 + perno2).mirror([0, 1, 0])

    pernos1 = (perno1 + perno2 + perno34).translate([base/8, base/8, 0])
    pernos1 = pernos1.translate([base/4, altura/2-base/4, grosor])

    pernos2 = pernos1.mirror([1,0,0])
    pernos34 = (pernos1 + pernos2).mirror([0,1,0])

    pernos = pernos1 + pernos2 + pernos34
    
    return pernos

def crearPernosCirculares(diamPerno, alturaPerno, diametro):
    perno = crearPerno(diamPerno,alturaPerno)
    perno1 = perno.translate([diametro/2,diametro/2,0])
    perno2 = perno1.mirror([1,0,0])
    perno34 = (perno1+perno2).mirror([0,1,0])
    return perno1+perno2+perno34

########Diseño del dron#####
def crearDimensiones(base, altura, grosor): #Esto solo ayuda a crear el cuerpo del dron
    cuboFrente = ops.Cube([base/2, base/2, grosor+5], center = True)
    cuboFrente = cuboFrente.translate([0,altura/2,grosor/2+1])
    cuboDer = ops.Cube([altura - base/2, altura - base/2, grosor+5], center = True)
    cuboDer = cuboDer.translate([(altura - base/2)/2+base/2-base/4,0,grosor/2+1])
    dimensiones = cuboFrente + cuboDer
    return dimensiones

def crearCuerpoSuperior(base, altura, grosor):
    cubo = ops.Cube([base, altura, grosor], center = True)
    cubo = cubo.translate([0,0,grosor/2])

    circuloFrente = ops.Cylinder(r=base/4, h=grosor+5)
    circuloFrente = circuloFrente.translate([0,altura/2,-1])
    circuloAtras = circuloFrente.mirror([0,1,0])

    circuloDer = ops.Cylinder(r=(altura - base/2)/2, h=grosor+5)
    circuloDer = circuloDer.translate([(altura - base/2)/2+base/2-base/4,0,-1])
    circuloIzq = circuloDer.mirror([1,0,0])

    cuerpo = cubo-circuloFrente-circuloAtras-circuloDer-circuloIzq
    cuerpo = cuerpo.translate([0,0,grosor + base*0.1])
    cuerpo = cuerpo.color([0.8, 0.0, 0.0]) #color rojo ironman
    #cuerpo = cuerpo.color("yellow")

    return cuerpo

def crearCuerpoInferior(base, altura, grosor):
    cubo = ops.Cube([base, altura, grosor], center = True)
    cubo = cubo.translate([0,0,grosor/2])

    circuloFrente = ops.Cylinder(r=base/4, h=grosor+5)
    circuloFrente = circuloFrente.translate([0,altura/2,-1])
    circuloAtras = circuloFrente.mirror([0,1,0])

    circuloDer = ops.Cylinder(r=(altura - base/2)/2, h=grosor+5)
    circuloDer = circuloDer.translate([(altura - base/2)/2+base/2-base/4,0,-1])
    circuloIzq = circuloDer.mirror([1,0,0])

    cuerpo = cubo-circuloFrente-circuloAtras-circuloDer-circuloIzq
    cuerpo = cuerpo.color([0.8, 0.0, 0.0]) #color rojo ironman
    #cuerpo = cuerpo.color("yellow")

    return cuerpo

def crearBrazo(base, altura, grosor):
    dimensionX = base*0.2
    dimensionY = altura*0.5
    dimensionZ = base*0.1

    brazoParte1 = ops.Cube([dimensionX, dimensionY, dimensionZ]) #Parte mas alargada
    brazoParte1 = brazoParte1.translate([-dimensionX/2, 0, grosor]) 
    brazoParte1 = brazoParte1.rotate([0,0,-45])
    brazoParte1 = brazoParte1.translate([base/2-dimensionX/2, altura/2-dimensionX/2,0])

    brazoParte2 = ops.Cube([base/4, base/4, dimensionZ]) #Parte de union entre brazo y cuerpo
    brazoParte2 = brazoParte2.translate([base/4, altura/2-base/4, grosor])

    brazo =  brazoParte2 + brazoParte1
    brazo = brazo.color([1.0, 0.84, 0.0]) #color amarillo ironman
    # brazo = brazo.color("gray")

    return brazo

def crearBaseMotor(diametro=28, altura=15, grosorBase=3, grosorPared=0, diamPerno1= 19, diamPerno2=16):
  
    cilindro1 = ops.Cylinder(r = diametro/2+grosorPared, h =  altura, _fn=100)
    
    if grosorPared == 0:
        cilindro2 = ops.Cylinder(r = diametro/2+1, h =  altura, _fn=100)
    else:
        cilindro2 = ops.Cylinder(r = diametro/2, h =  altura, _fn=100)
    
    cilindro2 = cilindro2.translate([0,0,grosorBase])
    
    cilindro3 = ops.Cylinder(r = diametro/6, h =  altura, _fn=100)
    cilindro3 = cilindro3.translate([0,0,-altura/2])

    perno1 = crearPerno(3.1,altura).translate([diamPerno1/2,0,-altura/2]).rotate([0,0,45])
    perno2 = crearPerno(3.1,altura).translate([-diamPerno1/2,0,-altura/2]).rotate([0,0,45])
    perno3 = crearPerno(3.1,altura).translate([0,diamPerno2/2,-altura/2]).rotate([0,0,45])
    perno4 = crearPerno(3.1,altura).translate([0,-diamPerno2/2,-altura/2]).rotate([0,0,45])

    baseMotor = cilindro1-cilindro2-cilindro3-(perno1+perno2+perno3+perno4)

    baseMotor = baseMotor.color([0.8, 0.0, 0.0]) #color rojo ironman

    return baseMotor

########Herramientas de la interfaz##############################
def on_button_click():
    hilo2 = threading.Thread(target=mostrarFigura)
    hilo3 = threading.Thread(target=redimensionarAplicacion, args=(3,"prueba.scad - OpenSCAD"))
    hilo2.start()
    hilo3.start()


########Diseño de interfaz#####
def mostrarInterfaz():
    
    # themes = ["Default", "Dark", "Dark2", "DarkBlue", "DarkAmber", "DarkGreen", "DarkTeal", "DarkPurple", "DarkOrange", "DarkRed", 
    #     "LightGreen", "LightTeal", "LightBlue", "LightYellow", "LightGray", "LightBrown", "LightPurple", "LightPink", "LightCyan", 
    #     "LightBlueMono", "GreenMono", "BlueMono", "BrownMono", "PurpleMono", "PinkMono", "CyanMono", "YellowMono", "GrayMono", 
    #     "DarkAqua", "DarkMinimal", "LightMinimal", "GrayMinimal", "DarkBrown", "LightBrown2", "DarkPurple2", "LightPurple2", 
    #     "DarkGreen2", "LightGreen2", "DarkBlue2", "LightBlue2", "DarkRed2", "LightRed2", "DarkOrange2", "LightOrange2", 
    #     "DarkTeal2", "LightTeal2", "DarkCyan", "LightCyan"]

    sg.theme("DarkAmber")

    menu_def = [
        ['Archivo', ['Abrir', "Cambiar Tema", 'Guardar', 'Guardar como...']],
        ['Editar', ['Copiar', 'Pegar', 'Cortar']],
        ['Ver', ['Ver barra de herramientas']],
        ['Ayuda', ['Acerca de...']]
    ]

    #Columnas de Componentes
    layoutControlador = [ #Columan de seleccion del controlador
        [sg.Text('Controlador', font=("Helvetica", 10, "bold"), justification='center')],
        [sg.Radio('Pixhawk', 3, key='controlador_1', change_submits=True)],
        [sg.Radio('The Cube Orange', 3, key='controlador_2', change_submits=True)],
        [sg.Radio('Omnibus F4 V3', 3, key='controlador_3', change_submits=True)],
        [sg.Radio('Matek CTR F405', 3, key='controlador_4', change_submits=True)],
        [sg.Radio('Arduino', 3, key='controlador_5', change_submits=True)],
        #[sg.Text("Dimensiones: ", tooltip="Poner valores x,y,z"),sg.InputText(key='controladores')]
    ]

    layoutBatería = [ #Columan de seleccion de la bateria
        [sg.Text('Bateria', font=("Helvetica", 10, "bold"), justification='center')],
        [sg.Radio('Bateria 2S, 2200mAh', 4, key='bateria_1', change_submits=True)],
        [sg.Radio('Bateria 2S, 2700mAh', 4, key='bateria_2', change_submits=True)],
        [sg.Radio('Bateria 3S, 2200mAh ', 4, key='bateria_3', change_submits=True)],
        [sg.Radio('Bateria 3S, 2200mAh', 4, key='bateria_4', change_submits=True)],
        [sg.Radio('Bateria 4S, 3700mAh', 4, key='bateria_5', change_submits=True)],
        #[sg.Text("Dimensiones: ", tooltip="Poner valores x,y,z"),sg.InputText(key='baterias')]
    ]

    layoutMotor = [ #Columan de seleccion del motor
        [sg.Text('Motor', font=("Helvetica", 10, "bold"), justification='center')],
        [sg.Radio('2204 2300kv', 5, key='motor_1', change_submits=True)],
        [sg.Radio('2213 935kv', 5, key='motor_2', change_submits=True)],
        [sg.Radio('2212 920kv', 5, key='motor_3', change_submits=True)],
        [sg.Radio('2312 920kv', 5, key='motor_4', change_submits=True)],
        [sg.Radio('3508 700kv', 5, key='motor_5', change_submits=True)],
        #[sg.Text("Dimensiones: ", tooltip="Poner valores x,y,z"),sg.InputText(key='motores')]
    ]

    layoutMaterial = [ #Columna de seleccion del material
        [sg.Text('Material', font=("Helvetica", 10, "bold"))],
        [sg.Radio('Material 1', 6, key='material_1')],
        [sg.Radio('Material 2', 6, key='material_2')],
        [sg.Radio('Material 3', 6, key='material_3')],
        [sg.Text("Esfuerzo: ", tooltip="Escribir el esfuerzo maximo de ruptura"),sg.InputText()]
    ]    

    layoutResultados1 = [ #Columna de resultados 1
        [sg.Text('Diseño del dron:')],
        [sg.InputText(key="resultado1")],
        [sg.Text('Material:')],
        [sg.InputText(key="resultado2")],
        [sg.Text('Controlador:')],
        [sg.InputText(key='resultado3')],
        [sg.Text('Batería:')],
        [sg.InputText(key="resultado4")],
        [sg.Text('Motor:')],
        [sg.InputText(key="resultado5")],
    ]
    
    layoutResultados2 = [ #Columna de resultados 2
        [sg.Text('Dimensiones:')],
        [sg.InputText(key="resultado6")],
        [sg.Text('Diametro motor a motor:')],
        [sg.InputText(key="resultado7")],
        [sg.Text('Peso del chasis:')],
        [sg.InputText(key="resultado8")],
        [sg.Text('Peso total:')],
        [sg.InputText(key="resultado9")],
        [sg.Text('Duración de vuelo:')],
        [sg.InputText(key="resultado10")],

    ]
   
    layout1 = [
        [sg.Text('Modelo del dron',font=("Arial", 14, "bold"))], #Modelo del dron
        [sg.HSeperator()],
        [sg.Radio('Modelo 1', 1, key='option_1', font=("Helvetica", 10, "bold")), 
        sg.Radio('Modelo 2', 1, key='option_2', font=("Helvetica", 10, "bold")),
        ],
        [sg.Text(' ',font=("Arial", 14))],
        [sg.Text('Tamaño del dron',font=("Arial", 14))], #Tamaño del dron
        [sg.HSeperator()],
        [sg.Radio('Dron Pequeño', 2, key='option_3', font=("Helvetica", 10, "bold")),
        sg.Radio('Dron Mediano', 2, key='option_4', font=("Helvetica", 10, "bold")),
        sg.Radio('Dron Grande', 2, key='option_5', font=("Helvetica", 10, "bold")),
        ],
        [sg.Text('13 a 23 cm'),
        sg.Text('23 a 33 cm'),
        sg.Text('33 a 60 cm'),
        ],
        [sg.Text(' ',font=("Arial", 14))],
        [sg.Text('Componentes',font=("Arial", 14, "bold"))],
        [sg.HSeperator()],
        [sg.Column(layoutControlador),
        sg.Column(layoutBatería),
        sg.Column(layoutMotor),],
        [sg.Text(' ',font=("Arial", 14))],
        [sg.Text('Resultados',font=("Arial", 14, "bold"))],
        [sg.HSeperator()],
        #[sg.Text('Diseño del dron:', justification='right'),sg.InputText()],
        [sg.Column(layoutResultados1),
        sg.Column(layoutResultados2),],

        [sg.Button('Renderizar', size=(200, 50))]
    ]

    layout2 = [
        [sg.Graph(canvas_size=(300, 300), graph_bottom_left=(0, 0), graph_top_right=(300, 300))]
    ]

    layoutPrincipal = [
        [sg.Menu(menu_def, tearoff=True, background_color="white"),
        sg.Column(layout1), 
        sg.Column(layout2),]
    ]

    window = sg.Window("DronCAD.py", layoutPrincipal, resizable=True, size=(700, 600))

    while True:
        event, values = window.read()
        if event in (None, 'Cancelar'):
            break
        if event == 'Renderizar':
            on_button_click()
            window["resultado1"].update("Modelo 1")
            window["resultado2"].update("PLA: ácido poliláctico")
            window["resultado3"].update("The Cube Orange")
            window["resultado4"].update("3S, 11.1V, 2200mAh")
            window["resultado5"].update("2212 920kv")
            window["resultado6"].update("aprox: 160x, 180y, 26z mm")
            window["resultado7"].update("aprox: 19 mm")
            window["resultado8"].update("aprox: 300 gr")
            window["resultado9"].update("aprox: 940 gr")
            window["resultado10"].update("aprox: 30 min")
        
        # if values["controlador_1"]:
        #     window["controladores"].update("x1,y1,z1")
        # if values["controlador_2"]:
        #     window["controladores"].update("x2,y2,z2")
        # if values["controlador_3"]:
        #     window["controladores"].update("x3,y3,z3")
        # if values["controlador_4"]:
        #     window["controladores"].update("x4,y4,z4")  
        # if values["controlador_5"]:
        #     window["controladores"].update("x5,y5,z5")   
         
        # if values["bateria_1"]:
        #     window["baterias"].update("x1,y1,z1")
        # if values["bateria_2"]:
        #     window["baterias"].update("x2,y2,z2")
        # if values["bateria_3"]:
        #     window["baterias"].update("x3,y3,z3")
        # if values["bateria_4"]:
        #     window["baterias"].update("x4,y4,z4")
        # if values["bateria_5"]:
        #     window["baterias"].update("x5,y5,z5")
        
        # if values["motor_1"]:
        #     window["motores"].update("x1,y1,z1")
        # if values["motor_2"]:
        #     window["motores"].update("x2,y2,z2")
        # if values["motor_3"]:
        #     window["motores"].update("x3,y3,z3")
        # if values["motor_4"]:
        #     window["motores"].update("x4,y4,z4")
        # if values["motor_5"]:
        #     window["motores"].update("x5,y5,z5")

    window.close()



"""
dimensionx
dimensiony
dimensionz
grosor
"""

base = 80
altura = 100
grosor = 4
diametroMotor = 28

ParteInferior = crearCuerpoInferior(base,altura,grosor)
ParteSuperior = crearCuerpoSuperior(base,altura,grosor)
Brazo1 = crearBrazo(base,altura,grosor)
Brazo2 = Brazo1.mirror([1,0,0])
Piernas = (Brazo1 + Brazo2).mirror([0,1,0])

baseMotor1 = crearBaseMotor(grosorPared=2,altura=20, diametro=diametroMotor)
baseMotor1 = baseMotor1.translate([0,altura*0.5,0])
baseMotor1 = baseMotor1.rotate([0,0,-45])
baseMotor1 = baseMotor1.translate([base/2-base*0.2/2+diametroMotor/2-4,altura/2-base*0.2/2+diametroMotor/2-4,0])

baseMotor2 = crearBaseMotor(grosorPared=2,altura=20, diametro=diametroMotor)
baseMotor2 = baseMotor2.translate([0,altura*0.5,0])
baseMotor2 = baseMotor2.rotate([0,0,45])
baseMotor2 = baseMotor2.translate([-(base/2-base*0.2/2+diametroMotor/2-4),altura/2-base*0.2/2+diametroMotor/2-4,0])

baseMotor3 = crearBaseMotor(grosorPared=2,altura=20, diametro=diametroMotor)
baseMotor3 = baseMotor3.translate([0,altura*0.5,0])
baseMotor3 = baseMotor3.rotate([0,0,135])
baseMotor3 = baseMotor3.translate([-(base/2-base*0.2/2+diametroMotor/2-4),-(altura/2-base*0.2/2+diametroMotor/2-4),0])

baseMotor4 = crearBaseMotor(grosorPared=2,altura=20, diametro=diametroMotor)
baseMotor4 = baseMotor4.translate([0,altura*0.5,0])
baseMotor4 = baseMotor4.rotate([0,0,-135])
baseMotor4 = baseMotor4.translate([(base/2-base*0.2/2+diametroMotor/2-4),-(altura/2-base*0.2/2+diametroMotor/2-4),0])




bateria = crearBateria(base, altura, grosor)
pernos = pernosBrazo(base, altura, 50 )

#Dron = CuerpoDron + Brazo1 + Brazo2 + Piernas + bateria
#Dron = ParteInferior + Brazo1 + Brazo2 + Piernas - pernos
#Dron = ParteInferior + ParteSuperior + Brazo1 + Brazo2 + Piernas + baseMotor1 + baseMotor2 + baseMotor3 + baseMotor4 + bateria - pernos
#Dron =  Brazo1 + baseSupDer - pernosBrazo(base, altura, 30)
#Dron = Brazo1 + Brazo2
#Dron = baseSupDer
Dron = ParteInferior - pernos
#Dron = baseMotor1 + Brazo1 - pernos

Dron.write("prueba.scad")



########Herramientas##############################

def mostrarFigura():
    # Especificamos el nombre de la aplicación y cualquier argumento necesario
    app_name = "C:\Program Files\OpenSCAD\openscad.exe"
    app_args = ["prueba.scad"]

    # Ejecutamos la aplicación
    subprocess.run([app_name] + app_args)

def expandirAplicacion(tiempoEspera, nomAplicacion):
    #Espera un tiempo a que abra la aplicacion
    time.sleep(tiempoEspera)
    # Obtener la ventana de la aplicación que quieres maximizar
    hwnd = win32gui.FindWindow(None, nomAplicacion)
    print(hwnd)
    # Maximizar la ventana
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    print("se deberia agrandar")

def redimensionarAplicacion(tiempoEspera, nomAplicacion):
    #Espera un tiempo a que abra la aplicacion
    time.sleep(tiempoEspera)
    # Obtener la ventana de la aplicación que quieres maximizar
    hwnd = win32gui.FindWindow(None, nomAplicacion)
    # Maximizar la ventana
    #win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    
    # Redimensionamos la ventana
    win32gui.MoveWindow(hwnd, 1000, 90, 875, 900, True)

    # Establece la ventana como siempre visible
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
    #print(hwnd)


# Creamos una instancia de la clase Thread y le pasamos la función que queremos ejecutar
hilo1 = threading.Thread(target=mostrarInterfaz)
hilo4 = threading.Thread(target=expandirAplicacion, args=(2,"DronCAD.py"))

# Iniciamos el hilo
hilo1.start()
hilo4.start()






















































#