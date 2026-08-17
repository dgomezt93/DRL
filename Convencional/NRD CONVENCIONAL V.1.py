import PySimpleGUI as sg
sg.theme('LightGrey')
#al inicio de un programa siempre importo las librerias necesarias
import pandas as pd
import pydicom
import os
from datetime import datetime
import numpy as np

ruta_carpeta = sg.popup_get_folder("Seleccionar carpeta")	

print(ruta_carpeta)

#ruta_archivo = sg.popup_get_folder("Select Folder")	

#la ejecucion del programa inicia aca, las funciones no se ejecutan por si mismas



contador= 0

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now()
# Extraer la fecha y la hora por separado
fecha_actual = str(fecha_hora_actual.date())+ "_" + str(fecha_hora_actual.hour) +  str(fecha_hora_actual.minute)  # Extraer solo la fecha
# Imprimir la fecha y la hora
print("Fecha actual:", fecha_actual)

#ruta_carpeta = "C:/Users/Daniela G/Desktop/PruebaDicom/IMAGENES"# Reemplaza con la ruta de tu carpeta

# Especificar la ruta del archivo Excel
ruta_archivo = "C:/Users/Daniela G/Desktop/PruebaDicom/Convencional" + str(fecha_actual) + ".xlsx"#asigno una ruta para archivo 


# Define the tag
tagEdad = (0x0010, 0x1010)
tagkVp= (0x0018, 0x0060)
tagExpTime = (0x0018, 0x1150)
tagmAs = (0x0018, 0x1152)
tagPDA = (0x0018, 0x115E)
tagStudyDescrip = (0x0008, 0x1030)
tagRegion= (0x0018,0x0015)
tagSex = (0x0010, 0x0040)
tagModality = (0x0008, 0x0060)
tagManufacture = (0x0008, 0x0070)
tagPosition = (0x0018, 0x5101)
tagLocalizacion = (0x0008, 0x1010)

#defino funciones variables etc
def listar_archivos_en_carpeta(ruta_carpeta):
    nombres_archivos = []
    # Verificar si la ruta es una carpeta
    if os.path.isdir(ruta_carpeta):
        # Listar los archivos en la carpeta
        archivos_en_carpeta = os.listdir(ruta_carpeta)
        # Filtrar solo los archivos regulares
        for archivo in archivos_en_carpeta:
            ruta_absoluta = os.path.join(ruta_carpeta, archivo)
            if os.path.isfile(ruta_absoluta):
                nombres_archivos.append(archivo)
    else:
        print("La ruta proporcionada no es una carpeta.")

    return nombres_archivos


def extract_dicom_metadata(dicom_file):
    global contador
    # Load the DICOM file
    ds = pydicom.dcmread(dicom_file)
    # Print all attributes
    #print(dir(ds))

    
    # Extract metadata el mismo orden debe ser el mismo del las columnas de dataframe
    metadata=[] 

    # Check if the tag is in the DICOM file and print its value
    if tagEdad in ds:
        print(f"Attribute (0010,1010): {ds[tagEdad].value}")
    else:
        print("Tag (0010,1010) not found in the DICOM file.")

    # Check if the tag is in the DICOM file and print its value
    if tagkVp in ds:
        print(f"Attribute (0018,0060): {ds[tagkVp].value}")
    else:
        print("Tag (0018,0060) not found in the DICOM file.")
    
    if tagExpTime in ds:
        print(f"Attribute (0018,1150): {ds[tagExpTime].value}")
    else:
        print("Tag (0018,1150) not found in the DICOM file.")
    
    if tagmAs in ds:
        print(f"Attribute (0018,1152): {ds[tagmAs].value}")
    else:
        print("Tag (0018,1152) not found in the DICOM file.")
    
    if tagPDA in ds:
        print(f"Attribute (0018,115E): {ds[tagPDA].value}")
    else:
        print("Tag (0018,115E) not found in the DICOM file.")
    
    if tagStudyDescrip in ds:
        print(f"Attribute (0008,1030): {ds[tagStudyDescrip].value}")
    else:
        print("Tag (0008,1030) not found in the DICOM file.")
        
    if tagRegion in ds:
        print(f"Attribute (0018,0015): {ds[tagRegion].value}")
    else:
        print("Tag (0018,0015) not found in the DICOM file.")        
    
    if tagSex in ds:
        print(f"Attribute (0010,0040): {ds[tagSex].value}")
    else:
        print("Tag (0010,0040) not found in the DICOM file.")
    
    if tagModality in ds:
        print(f"Attribute (0008,0060): {ds[tagModality].value}")
    else:
        print("Tag (0008,0060) not found in the DICOM file.")
    
    if tagManufacture in ds:
        print(f"Attribute (0008,0070): {ds[tagManufacture].value}")
    else:
        print("Tag (0008,0070) not found in the DICOM file.")
    
    if tagPosition in ds:
        print(f"Attribute (0018,5101): {ds[tagPosition].value}")
    else:
        print("Tag (0018,5101) not found in the DICOM file.")
    
    if tagLocalizacion in ds:
        print(f"Attribute (0008,1010): {ds[tagLocalizacion].value}")
    else:
        print("Tag (0008,1010) not found in the DICOM file.")


    if 'Y' in ds[tagEdad].value:
        # Remove the letter 'Y' from the string
        string_without_y =  ds.PatientAge.replace('Y', '')

        # Cast the resulting string to an integer
        result_integer = int(string_without_y)

        if result_integer >17:# si el paciente es adulto agregelo 
            if 'EntranceDoseInmGy' in ds:
                contador += 1

            metadata.append(nombre_archivo)
            metadata.append(ds[tagkVp].value)
            metadata.append(ds[tagExpTime].value)
            metadata.append(ds[tagmAs].value)
            productDose=float((ds[tagPDA].value)*10)
            metadata.append(productDose)
            output_string = split_and_remove_first_two(ds[tagStudyDescrip].value)
            metadata.append(output_string)
            metadata.append(ds[tagRegion].value)
            metadata.append(ds[tagSex].value)
            #metadata.append(ds.EntranceDoseInmGy)
            metadata.append(result_integer)
            metadata.append(ds[tagModality].value)
            metadata.append(ds[tagManufacture].value)
            #metadata.append(ds.ManufacturerModelName)
            # output_ViewPosition = extraerViewPosition(ds.ViewPosition)
            metadata.append(ds[tagPosition].value)       
            
            output_place =extraerLocalizacion(ds[tagLocalizacion].value)
            metadata.append(output_place)
            metadata.append(ds.DeviceSerialNumber)
    
       
    return metadata
   

def extraerLocalizacion(input_place):
    if input_place=="RX_CENTRAL":
      place="Medellín/Bloque12"
    elif input_place=="DiDiMedellin":
      place="Medellín/Urgencias"
    elif input_place=="DIDI IMAGENES":
      place="Rionegro/Imaginología"
    elif input_place=="DiDiEleva01":
      place="Rionegro/Urgencias"
    return place
        
def split_and_remove_first_two(input_string):
    # Split the input string by ' ' (space) SE verifica que el nombre del estudio y si tiene  las dos primeras palabras radiografia de lasborra y deja solo el nombre restante
    words = input_string.split(' ')
    
    # Check if there are at least two words
    if len(words) >= 2:
        # Check if the first two words are 'word1' and 'word2'
        if words[0] == 'RADIOGRAFIA' and words[1] == 'DE':
            # Delete the first two words
            del words[0]
            del words[0]
    
    # Join the remaining words back into a string
    exam = ' '.join(words)
    
    if exam=="Tórax" or exam=="Torax" or exam=="TÃ³rax" or exam=="TORAX (PA O AP Y" or exam=="TORAX (PA O AP Y LATERAL, DECUBITO LATERAL, OBLICUAS O LATERAL CON BARIO)":
      exam="Tórax"
    elif exam=="Humero" or exam=="Húmero" or exam=="HÃºmero":
      exam="Húmero"
    elif exam=="Fémur" or exam=="Femur" or exam=="FÃ©mur":
      exam="Fémur"
    elif exam=="Tibia/Peroné" or exam=="Tibia/peroné" or exam=="Tibia/Perone" or exam=="Tibia/peronÃ©":
      exam="Tibia/Peroné"
    elif exam=="RADIOGRAFIA DE RODILLA AP, LATER":
      exam="Rodilla"
    elif exam=="RADIOGRAFIA DE DEDOS EN MANO" or exam=="DEDOS EN MANO":
      exam="Mano"
    elif exam=="ANTEBRAZO":
      exam="Antebrazo"
    elif exam=="CODO":
      exam="Codo"        
    elif exam=="CRANEO SIMPLE":
      exam="Craneo"
    elif exam=='Rodillas bilaterales sin flexionar':
        exam= 'Rodillas'
    elif exam=='RADIOGRAFIA DINAMICA DE COLUMNA VERTEBRAL':
        exam='Columna'

    output_string = exam
    return output_string



nombres_archivos = listar_archivos_en_carpeta(ruta_carpeta)#lo primero que necesito es sacar los nombres de los archivos en la carpeta con las imagene dicom
#print("Archivos en la carpeta:", nombres_archivos)

# Definir las columnas del DataFrame
columnas = ['Archivo','kV', 'Tiempo de Exposición mSec', 'mAs', "Producto dosis Área", 'Estudio', 'Region', 'Sexo', 'Edad','modalidad','Fabricante','Proyeccion','localizacion', 'ID Equipo' ]#el mismo orden del arreglo con la informacion de la imagen dicom 

df = pd.DataFrame(columns=columnas)# creo un dataframe y nombro las columnas del como sea requerido

#queremos con todos esos nombres extraer los datos que nos interesan pero de cada uno
#para eso necesitamos un for
index = 0
for nombre_archivo in nombres_archivos: # recorre todo el arreglo con los nombres y nombre por nombre lo usa 
    print(nombre_archivo)#imprimo nombre del archivo al que le voy a extraer la informacion de interes
    index=index+1
    sg.one_line_progress_meter("Current Progress", index+1, len(nombres_archivos))
    dicom_file = "C:/Users/Daniela G/Desktop/PruebaDicom/IMAGENES/" + nombre_archivo# la ruta del archivo es la ruta de la carpeta + el nombre del archivo
    metadata = extract_dicom_metadata(dicom_file)#extraigo la informacion de interes de la imagen
    print(metadata)#imprimo la informacion 
    # 
    if len(metadata) != 0:
        df.loc[len(df)] = metadata# agrego al dataframe una fila con los valores de la informacion de la imagen dicom
   
        print("****************************")# caracteres para separar un archivo de otro y repito el for hasta lea todos los archivos existentes en la carpeta
    else:
        print("paciente pediatrico")
print(df)#muestro el dataframe

# Guardar el DataFrame en un archivo Excel
df.to_excel(ruta_archivo, index=False)#creo un archivo excel apartir del df, con nombre DatosFechahora.xlsx

print("Datos guardados en el archivo Excel:", ruta_archivo)

sg.popup_ok("Tarea realizada")
#print("# de Archivos con EntranceDoseInmGy = ", contador)






while True:
    try:
        T1 = df['localizacion'].unique()
        T1 = np.append(T1, "SanVicente")
        
        print("\n","Copie y pegue una opción de las siguientes en el cuadro de ingreso:","\n","\n",T1,"\n")
        layout = [
        [sg.Text('Seleccione una opción:')],
        [sg.Combo(T1, default_value=T1[0], key='-COMBO-')],
        [sg.Button('Seleccionar')]
        ]

        # Create the window
        window = sg.Window('Seleccionar institución de interés', layout)


        event, values = window.read()
        # If the user clicks the Submit button
        if event == 'Seleccionar':
            selected_option = values['-COMBO-']
            Hosp=selected_option
            window.close()
        if event == sg.WIN_CLOSED:
            exit()

        

        if Hosp in T1:
            if Hosp == "SanVicente":
                df1=df
                print("Toda la institucion")
                print("\n",df1,"\n")
            else:

                df1=df[df['localizacion']==Hosp]
                print("\n",df1,"\n")
            unique_strings = df1['Region'].unique()

            print("Valores de estudio existentes para la localizacion ", Hosp,"\n" )
            print(unique_strings)
            
            
            layout1 = [
            [sg.Text('Seleccionar una opción:')],
            [sg.Combo(unique_strings, default_value=unique_strings[0], key='-COMBO-', size=(20,1))],
            [sg.Button('Seleccionar')]
            ]

            # Create the window
            window2 = sg.Window('Seleccionar región anatomica', layout1)


            event, values = window2.read()
            # If the user clicks the Submit button
            if event == 'Seleccionar':
                selected_option = values['-COMBO-']
                est=selected_option
                window2.close()
            if event == sg.WIN_CLOSED:
                exit()

            if est in unique_strings:
                df2=df1[df1["Region"]==est]
                if est =="CHEST":
                    unique_strings = df2['Proyeccion'].unique()
                    print("Valores de estudio existentes para la localizacion ", "\n" )
                    print(unique_strings)

                    layout3 = [
                    [sg.Text('Seleccionar una proyección:')],
                    [sg.Combo(unique_strings, default_value=unique_strings[0], key='-COMBO-')],
                    [sg.Button('Seleccionar')]
                    ]

                    # Create the window
                    window3 = sg.Window('Seleccionar Proyeccion', layout3)


                    event, values = window3.read()
                    # If the user clicks the Submit button
                    if event == 'Seleccionar':
                        selected_option = values['-COMBO-']
                        proyeccion=selected_option
                        window3.close()
                    if event == sg.WIN_CLOSED:
                        exit()
                    
                    df3=df2[df2["Proyeccion"]==proyeccion]

                    
                    layout5 = [[sg.Text('Nivel de referencia en: '),sg.Text(str(est)), sg.Text(' : '),sg.Text(str(df3["Producto dosis Área"].median())), sg.Text(' mGy*cm2')],
                    # THIS is the newly added combination. Note (None, None) is default and not really needed
                    [sg.Text('Producto dosis-área promedio para estudio: '),sg.Text(str(df3["Producto dosis Área"].mean())), sg.Text(' mGy*cm2')],
                    [sg.Text('Primer percentil: '),sg.Text(str(np.percentile(df3["Producto dosis Área"], [50]))),sg.Text('  Segundo percentil: '),sg.Text(str(np.percentile(df3["Producto dosis Área"], [50]))),sg.Text(' Tercer percentil: '),sg.Text(str(np.percentile(df3["Producto dosis Área"], [75])))],
                    [sg.Text('Kv de nivel de referencia: '),sg.Text(str(df3["kV"].median())), sg.Text(' Kv')],
                    [sg.Text('mAs de nivel de referencia: '),sg.Text(str(df3["mAs"].median())), sg.Text(' mAs')],
                    [sg.Text('Kv promedio: '),sg.Text(str(df3["kV"].mean())), sg.Text(' kV')],
                    [sg.Text('mAs promedio: '),sg.Text(str(df3["mAs"].mean())), sg.Text(' mAs')],
                    [sg.Button('Realizar otro'), sg.Button('Exit')]
                    ]

                    window5 = sg.Window('Niveles de referencia', layout5)
                    event, values = window5.read()
                    if event == sg.WIN_CLOSED or event == 'Exit':
                        exit()
                    window5.close()
                else:
                    layout5 = [[sg.Text('Nivel de referencia en: '),sg.Text(str(est)), sg.Text(' : '),sg.Text(str(df2["Producto dosis Área"].median())), sg.Text(' mGy*cm2')],
                    # THIS is the newly added combination. Note (None, None) is default and not really needed
                    [sg.Text('Producto dosis-área promedio para estudio: '),sg.Text(str(df2["Producto dosis Área"].mean())), sg.Text(' mGy*cm2')],
                    [sg.Text('Primer percentil: '),sg.Text(str(np.percentile(df2["Producto dosis Área"], [25]))),sg.Text('  Segundo percentil: '),sg.Text(str(np.percentile(df2["Producto dosis Área"], [50]))),sg.Text(' Tercer percentil: '),sg.Text(str(np.percentile(df2["Producto dosis Área"], [75])))],
                    [sg.Text('Kv de nivel de referencia: '),sg.Text(str(df2["kV"].median())), sg.Text(' Kv')],
                    [sg.Text('mAs de nivel de referencia: '),sg.Text(str(df2["mAs"].median())), sg.Text(' mAs')],
                    [sg.Text('Kv promedio: '),sg.Text(str(df2["kV"].mean())), sg.Text(' kV')],
                    [sg.Text('mAs promedio: '),sg.Text(str(df2["mAs"].mean())), sg.Text(' mAs')],
                    [sg.Button('Realizar otro'), sg.Button('Exit')]
                    ]

                    window5 = sg.Window('Niveles de referencia', layout5)
                    event, values = window5.read()
                    if event == sg.WIN_CLOSED or event == 'Exit':
                        exit()
                    window5.close()
                    """
                    window5['-T-'].update(str(est))                        
                    window5['-T1-'].update(str(df2["Producto dosis Área"].median()))
                    window5['-T2-'].update(str(df2["Producto dosis Área"].mean()))
                    window5['-T3-'].update(str(np.percentile(df2["Producto dosis Área"], [25])))
                    window5['-T4-'].update(str(np.percentile(df2["Producto dosis Área"], [50])))
                    window5['-T5-'].update(str(np.percentile(df2["Producto dosis Área"], [75])))
                    window5['-T6-'].update(str(df2["kV"].median()))
                    window5['-T7-'].update(str(df2["mAs"].median()))
                    window5['-T8-'].update(str(df2["kV"].mean()))
                    window5['-T9-'].update(str(df2["mAs"].mean())
                    """                
                    print("Valores para estudio completo ",est,"\n")
                    print("\n",df2,"\n")
                    print("\n","Nivel de Referencia en:",est,":",df2["Producto dosis Área"].median(),"mGy*cm2","\n","Producto dosis-área promedio para estudio",est,":",df2["Producto dosis Área"].mean(),"mGy*cm2","\n")
                    print("primer percentil ", np.percentile(df2["Producto dosis Área"], [25]), "     Segundo percentil ", np.percentile(df2["Producto dosis Área"], [50]), "     Tercer percentil ", np.percentile(df2["Producto dosis Área"], [75]) )

                    print("\n","Kv de nivel de referencia en:",est,":",df2["kV"].median(),"kV","\n","mAs de nivel de referencia en",est,":",df2["mAs"].median(),"mAs","\n","Kv promedio en:",est,":",df2["kV"].mean(),"kV","\n","mAs promedio en",est,":",df2["mAs"].mean(),"mAs","\n")
                #elif est not in a:
                #    print("\n","Estudio inválido","\n")
                #    break

        elif Hosp not in T1:
            print("\n",Hosp,"No pertenece a San Vicente Fundación","\n")
            break
    except Exception as e:
        # Handle any other unexpected errors
        print("Error try: ")
        print(e)

