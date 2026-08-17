#importar las librerias necesarias
import PySimpleGUI as sg
sg.theme('LightGrey')
import pandas as pd
import pydicom
import os
from datetime import datetime
import numpy as np

ruta_carpeta = sg.popup_get_folder("Seleccionar carpeta")	

print(ruta_carpeta)


#la ejecucion del programa inicia aca, las funciones no se ejecutan por si mismas



contador= 0

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now()
# Extraer la fecha y la hora por separado
fecha_actual = str(fecha_hora_actual.date())+ "_" + str(fecha_hora_actual.hour) +  str(fecha_hora_actual.minute)  # Extraer solo la fecha
# Imprimir la fecha y la hora
print("Fecha actual:", fecha_actual)


# Especificar la ruta del archivo Excel
ruta_archivo = "C:/Users/Daniela G/Desktop/PruebaDicom/Convencional" + str(fecha_actual) + ".xlsx"#asigno una ruta para archivo 


# Defino los identificadores globales DICOM
tagEdad = (0x0010, 0x1010)
tagkVp= (0x0018, 0x0060)
tagExpTime = (0x0018, 0x1150)
tagmAs = (0x0018, 0x1153)
tagPDA = (0x0018, 0x115E)
tagStudyDescrip = (0x0008, 0x1030)
tagRegion= (0x0018,0x0015)
tagSex = (0x0010, 0x0040)
tagModality = (0x0008, 0x0060)
tagManufacture = (0x0008, 0x0070)
tagPosition = (0x0018, 0x5101)
tagLocalizacion = (0x0008, 0x1010)
tagEntranceDose = (0x0040,0x8302)

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
    # Carga los archivos DICOM 
    ds = pydicom.dcmread(dicom_file)
    
    
    metadata=[] 

    #Filtro pacientes pediátricos

    if 'Y' in ds[tagEdad].value:
        # Remueve la letra 'Y' del  string
        string_without_y =  ds.PatientAge.replace('Y', '')

        # Convierte la cadena resultante en un entero
        result_integer = int(string_without_y)

        if result_integer >17:# si el paciente es adulto agregelo 
            
            #Agrego los identificadores globales a metadata
          
            metadata.append(nombre_archivo)
            metadata.append(ds[tagkVp].value)
            metadata.append(ds[tagExpTime].value)
            metadata.append(ds[tagmAs].value)
            if tagPDA in ds:
                productDose=float((ds[tagPDA].value)*10)
                metadata.append(productDose)
            else:
                 metadata.append(ds[tagEntranceDose])
            
            metadata.append(ds[tagRegion].value)
            metadata.append(ds[tagSex].value)
           
            metadata.append(result_integer)
            
            metadata.append(ds[tagManufacture].value)
            metadata.append(ds.ManufacturerModelName)
            # output_ViewPosition = extraerViewPosition(ds.ViewPosition)
            metadata.append(ds[tagPosition].value)             
            metadata.append(ds[tagLocalizacion].value)
   
            metadata.append(ds.DeviceSerialNumber)
    
       
    return metadata
   

  
#lo primero que necesito es sacar los nombres de los archivos en la carpeta con las imagene dicom
nombres_archivos = listar_archivos_en_carpeta(ruta_carpeta)

# Definir las columnas del DataFrame en el mismo orden en que se agregan a metadata

columnas = ['Archivo','kV', 'Tiempo de Exposición mSec', 'mAs', "Producto dosis Área", 'Region', 'Sexo', 'Edad','Fabricante','Modelo','Proyeccion','localizacion','Serial' ]#el mismo orden del arreglo con la informacion de la imagen dicom 

# creo un dataframe y nombro las columnas 
df = pd.DataFrame(columns=columnas)

#se itera con un for para recorrer cada archivo
index = 0
for nombre_archivo in nombres_archivos: # recorre todo el arreglo con los nombres y nombre por nombre lo usa 
    print(nombre_archivo)#imprimo nombre del archivo al que le voy a extraer la informacion de interes
    index=index+1
    sg.one_line_progress_meter("Current Progress", index+1, len(nombres_archivos))
    dicom_file = ruta_carpeta + '/' + nombre_archivo
    #extraigo la informacion de interes de la imagen
    metadata = extract_dicom_metadata(dicom_file)
    #imprimo la informacion
    print(metadata) 
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




# se ejecuta la interfaz
# 1. selecciona el serial que identifica el equipo
# 2. 
while True:
    try:
        T1 = df['Serial'].unique()
        layout = [
        [sg.Text('Seleccione una opción:')],
        [sg.Combo(T1, default_value=T1[0], key='-COMBO-', size=(30,1))],
        [sg.Button('Seleccionar')]
        ]
         # Create the window
        window = sg.Window('Seleccionar equipo de interés', layout)
        
        event, values = window.read()
        # If the user clicks the Submit button
        if event == 'Seleccionar':
            selected_option = values['-COMBO-']
            Model=selected_option
            window.close()
        if event == sg.WIN_CLOSED:
            exit()
        
        if Model in T1:
            df1=df[df['Serial']==Model]#en DF1 dataframe filtrado por modelo del equipo
            print("\n",df1,"\n")
            unique_strings = df1['Region'].unique()
            

            unique_strings_2 =(unique_strings)
           # unique_strings_2 = [s.strip() for s in unique_strings]  # Eliminar espacios extra
            print(unique_strings_2)


            layout1 = [
            [sg.Text('Seleccionar una opción:')],
            [sg.Combo(unique_strings_2, default_value=unique_strings_2[0], key='-COMBO-', size=(30,1))],
            [sg.Button('Seleccionar')]
            ]

            # Create the window
            window2 = sg.Window('Seleccionar Estudio', layout1)


            event, values = window2.read()
            # If the user clicks the Submit button
            if event == 'Seleccionar':
                selected_option = values['-COMBO-']
                region=selected_option
                print("+++++++++++++++++++")
                print(selected_option)
                window2.close()
            if event == sg.WIN_CLOSED:
                exit()    
            
            if region in unique_strings_2:
                print(df1)
                df2=df1[df1['Region']==region]#dentro del Dataframe para un modelo de equipo filtro por descripcion de la serie ej: "Torax simple"
                
                unique_strings = df2['Proyeccion'].unique()
                print("Valores de estudio existentes para la localizacion ", "\n" )
                print(unique_strings)
                unique_strings_2 = [s.strip() for s in unique_strings] 
              
                for est in unique_strings_2:
                    df3=df2[df2["Proyeccion"]==est]
                    dfresultados=df3
                # Agrupar por 'NOMBRE' y sumar los valores de 'DLP'
                #dfresultado = df2.groupby('Nombre Imagen', as_index=False).agg({'DLP': 'sum','CTDIvol_name': 'sum'})

                # Mostrar el resultado
                    print(dfresultados)

                    total_dap_np = dfresultados['Producto dosis Área'].to_numpy()  # Convert to NumPy array if needed
                        
                    # Calculate percentiles and statistics
                    fq_dap = np.percentile(total_dap_np, 25)
                    sq_dap = np.percentile(total_dap_np, 50)
                    tq_dap = np.percentile(total_dap_np, 75)
                    max_dap = np.max(total_dap_np)
                    min_dap = np.min(total_dap_np)


                    print("fq_ed:", fq_dap)
                    print("sq_ed:", sq_dap)
                    print("tq_ed:", tq_dap)
                    print("max_ed:", max_dap)
                    print("min_ed:", min_dap)

                        

                    columnas2 = ['Estadística','PDA (mGy*cm^2)']#,'1st Quartile' ,'2nd Quartile','3rd Quartile' ,'IQR' ,'Min' ,'Max' , 'KAP (Gy*cm^2)' , 'Air Kerma (mGy)' ,'Fluoroscopy time (min)' ,'Exposure images' ]#el mismo orden del arreglo con la informacion de la imagen dicom 
                    #'1st Quartile', '2nd Quartile' ,'3rd Quartile' ,'IQR','Min', 'Max',
                    dataFrame = pd.DataFrame(columns=columnas2)# creo un dataframe y nombro las columnas del como sea requerido

                    # Append statistics to DataFrame
                    dataFrame.loc[len(dataFrame)] = ['1st Quartile', "{:.1f}".format(fq_dap)]
                    dataFrame.loc[len(dataFrame)] = ['2nd Quartile', "{:.1f}".format(sq_dap)]
                    dataFrame.loc[len(dataFrame)] = ['3rd Quartile', "{:.1f}".format(tq_dap)]
                    dataFrame.loc[len(dataFrame)] = ['Min', "{:.1f}".format(min_dap)]
                    dataFrame.loc[len(dataFrame)] = ['Max', "{:.1f}".format(max_dap)]

                    print(dataFrame)  # Display DataFrame

                    # Convert the DataFrame to a list of lists
                    data_list = dataFrame.values.tolist()
                    header_list = dataFrame.columns.tolist()

                    # Define the layout for PySimpleGUI
                    layout = [
                        [sg.Table(values=data_list, headings=header_list,
                                auto_size_columns=True, display_row_numbers=False,
                                justification='center', num_rows=min(25, len(data_list)))],
                        [sg.Button('Exit')]
                    ]

                    # Create the window
                    window = sg.Window("Proyeccion "+est, layout)

                    # Event loop to process events and get values from the inputs
                    while True:
                        event, values = window.read()
                        if event == sg.WIN_CLOSED or event == 'Exit':
                            break

                    # Close the window
                    window.close()


    except Exception as e:
        # Handle any other unexpected errors
        print("Error try: ")
        print(e)

    break