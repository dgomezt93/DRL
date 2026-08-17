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
ruta_df = "C:/Users/Daniela G/Desktop/PruebaDicom/dfConvencional" + str(fecha_actual) + ".xlsx"#asigno una ruta para archivo 


# Defino los identificadores globales DICOM
tagEdad = (0x0010, 0x1010)
tagkVp= (0x0018, 0x0060)
tagExpTime = (0x0018, 0x1150)
tagmAs = (0x0018, 0x1153)
tagPDA = (0x0018, 0x115E)
tagStudyDescrip = (0x0008, 0x1030)
tagRegion= (0x0018,0x0015)
tagModality = (0x0008, 0x0060)
tagManufacture = (0x0008, 0x0070)
tagModel = (0x0008,0x1090)	
tagProyeccion = (0x0018, 0x5101)
tagLocalizacion = (0x0008, 0x1010)
tagEntranceDose = (0x0040,0x8302)
tagSerial = (0x0018,0x1000)

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
    # Extraer la edad de manera segura
    edad_element = ds.get(tagEdad, None)
    edad_value = edad_element.value if edad_element and hasattr(edad_element, "value") else "NA"

    # Inicializar variable para la edad como número o NA
    result_integer = "NA"

    # Si la edad no es 'NA' y contiene 'Y', procesarla
    if edad_value != "NA" and 'Y' in edad_value:
        # Remover la letra 'Y'
    
        string_without_y =  ds.PatientAge.replace('Y', '')
        try:

            # Convierte la cadena resultante en un entero
            result_integer = int(string_without_y)
        except ValueError:
            result_integer = "NA"  # Si no se puede convertir, asignar NA
    if result_integer == "NA" or result_integer > 17:# si el paciente es adulto agregelo
            
            
            #Agrego los identificadores globales a metadata
            metadata.append(nombre_archivo)
            kvp_element = ds.get(tagkVp, "N/A")
            kvp_value = kvp_element.value if hasattr(kvp_element, "value") else kvp_element
            metadata.append(kvp_value)
            time_element = ds.get(tagExpTime, None)
            time_value = time_element.value if hasattr(time_element, "value") else time_element
            metadata.append(time_value)
            mAs_element = ds.get(tagmAs, None)
            mAs_value = mAs_element.value if hasattr(mAs_element, "value") else mAs_element
            metadata.append(mAs_value)
           

            pda_element = (ds.get(tagPDA, None))
            pda_value = pda_element.value if hasattr(pda_element, "value") else pda_element
            if(pda_value!=None):
               pda_value = float(pda_value)*0.1
            metadata.append(pda_value)
           
            dosis_element = ds.get(tagEntranceDose, None)
            dosis_value = dosis_element.value if hasattr(dosis_element, "value") else dosis_element
            metadata.append(dosis_value)
    
            region_element = ds.get(tagRegion, None)
            region_value = region_element.value if hasattr(region_element, "value") else region_element
            metadata.append(region_value)
            metadata.append(result_integer)
            fabricante_element = ds.get(tagManufacture, None)
            fabricante_value = fabricante_element.value if hasattr(fabricante_element, "value") else fabricante_element
            metadata.append(fabricante_value)
            modelo_element = ds.get(tagModel, None)
            modelo_value = modelo_element.value if hasattr(modelo_element, "value") else modelo_element
            metadata.append(modelo_value)
            proyection_element = ds.get(tagProyeccion, None)
            proyection_value = proyection_element.value if hasattr(proyection_element, "value") else proyection_element
            metadata.append(proyection_value)    
            localizacion_element = ds.get(tagLocalizacion, None)
            localizacion_value = localizacion_element.value if hasattr(localizacion_element, "value") else localizacion_element      
            metadata.append(localizacion_value)
            serial_element = ds.get(tagSerial, None)
            serial_value = serial_element.value if hasattr(serial_element, "value") else serial_element
            metadata.append(serial_value)
            
    
       
    return metadata
   

  
#lo primero que necesito es sacar los nombres de los archivos en la carpeta con las imagene dicom
nombres_archivos = listar_archivos_en_carpeta(ruta_carpeta)

# Definir las columnas del DataFrame en el mismo orden en que se agregan a metadata

columnas = ['Archivo','kV', 'Tiempo de Exposición mSec', 'mAs', "Producto dosis Área", 'Dosis de Entrada','Region', 'Edad','Fabricante','Modelo','Proyeccion','localizacion','Serial' ]#el mismo orden del arreglo con la informacion de la imagen dicom 

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

carpeta_destino = sg.popup_get_folder("Seleccione la carpeta donde desea guardar el archivo Excel")
# Verificar si el usuario seleccionó una carpeta
if carpeta_destino:
    ruta = f"{carpeta_destino}/Convencional_{fecha_actual}.xlsx"
    
    # Guardar el DataFrame en el archivo seleccionado
    df.to_excel(ruta, index=False)
    
    print("Datos guardados en el archivo Excel:", ruta)
else:
    sg.popup_error("No se seleccionó una carpeta. No se guardará el archivo.")

sg.popup_ok("Tarea realizada")
#print("# de Archivos con EntranceDoseInmGy = ", contador)




# se ejecuta la interfaz
# 1. selecciona el serial que identifica el equipo
# 2. 
while True:
    try:
        
        T1 = df['localizacion'].unique()
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
            df1=df[df['localizacion']==Model]#en DF1 dataframe filtrado por modelo del equipo
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
                    dfresultados_3=df3
                # Agrupar por 'NOMBRE' y sumar los valores de 'DLP'
                #dfresultado = df2.groupby('Nombre Imagen', as_index=False).agg({'DLP': 'sum','CTDIvol_name': 'sum'})

                # Mostrar el resultado
                    print(dfresultados)
                    print("entrando a consulta PDA")
                        # Verificar si al menos un valor en la columna NO está vacío (NaN, None o "")
                    if dfresultados['Producto dosis Área'].apply(lambda x: x != "" and not pd.isna(x)).any():
                        print("Entro a if PDA")
                        # Crear un nuevo DataFrame solo con las filas donde la columna NO esté vacía
                        dfresultados_2 = dfresultados[dfresultados['Producto dosis Área'] != ""]
                        total_dap_np = dfresultados_2['Producto dosis Área'].to_numpy()
                        #total_dap_np = dfresultados_2[dfresultados_2['Producto dosis Área'].apply(lambda x: x != "" and not pd.isna(x))]
                        
                    
                        # Calculate percentiles and statistics
                        fq_dap = np.percentile(total_dap_np, 25)
                        sq_dap = np.percentile(total_dap_np, 50)
                        tq_dap = np.percentile(total_dap_np, 75)
                        max_dap = np.max(total_dap_np)
                        min_dap = np.min(total_dap_np)
                        RIQ = tq_dap - fq_dap


                        print("fq_ed:", fq_dap)
                        print("sq_ed:", sq_dap)
                        print("tq_ed:", tq_dap)
                        print("max_ed:", max_dap)
                        print("min_ed:", min_dap)
                        print("Ran_intercuartil", RIQ)
                        columnas2 = ['Estadística','PDA (Gy*cm^2)']#,'1st Quartile' ,'2nd Quartile','3rd Quartile' ,'IQR' ,'Min' ,'Max' , 'KAP (Gy*cm^2)' , 'Air Kerma (mGy)' ,'Fluoroscopy time (min)' ,'Exposure images' ]#el mismo orden del arreglo con la informacion de la imagen dicom 
                        #'1st Quartile', '2nd Quartile' ,'3rd Quartile' ,'IQR','Min', 'Max',
                        dataFrame = pd.DataFrame(columns=columnas2)# creo un dataframe y nombro las columnas del como sea requerido

                        # Append statistics to DataFrame
                        dataFrame.loc[len(dataFrame)] = ['1er Cuartil', "{:.2f}".format(fq_dap)]
                        dataFrame.loc[len(dataFrame)] = ['2do Cuartil', "{:.2f}".format(sq_dap)]
                        dataFrame.loc[len(dataFrame)] = ['3er Cuartil', "{:.2f}".format(tq_dap)]
                        dataFrame.loc[len(dataFrame)] = ['Min', "{:.2f}".format(min_dap)]
                        dataFrame.loc[len(dataFrame)] = ['Max', "{:.2f}".format(max_dap)]
                        dataFrame.loc[len(dataFrame)] = ['Rango Intercuartílico ', "{:.2f}".format(RIQ)]

                        print(dataFrame)  # Display DataFrame
                        # Pedir al usuario seleccionar la carpeta donde guardar el archivo
                        carpeta_destino = sg.popup_get_folder("Seleccione la carpeta donde desea guardar el archivo Excel")

                        # Verificar si el usuario seleccionó una carpeta
                        if carpeta_destino:
                            ruta_DE = f"{carpeta_destino}/NivelReferencia_{est}_{fecha_actual}.xlsx"
                            
                            # Guardar el DataFrame en el archivo seleccionado
                            dataFrame.to_excel(ruta_DE, index=False)
                            
                            print("Datos guardados en el archivo Excel:", ruta_DE)
                        else:
                            sg.popup_error("No se seleccionó una carpeta. No se guardará el archivo.")

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
                        window = sg.Window("Nivel de Referencia en Proyección " +est, layout, resizable=True)

                        # Event loop to process events and get values from the inputs
                        while True:
                            event, values = window.read()
                            if event == sg.WIN_CLOSED or event == 'Exit':
                                break

                        # Close the window
                        window.close()


                    elif dfresultados_3['Dosis de Entrada'].apply(lambda x: x != "" and not pd.isna(x)).any():
                        print("Entro a if DOsis de entrada")
                        # Crear un nuevo DataFrame solo con las filas donde la columna NO esté vacía
                        dfresultados_2 = dfresultados_3[dfresultados_3['Dosis de Entrada'] != ""]
                        total_dap_np = dfresultados_2['Dosis de Entrada'].to_numpy()
                        #total_dap_np = dfresultados_2[dfresultados_2['Producto dosis Área'].apply(lambda x: x != "" and not pd.isna(x))]
                        
                    
                        # Calculate percentiles and statistics
                        fq_dap = np.percentile(total_dap_np, 25)
                        sq_dap = np.percentile(total_dap_np, 50)
                        tq_dap = np.percentile(total_dap_np, 75)
                        max_dap = np.max(total_dap_np)
                        min_dap = np.min(total_dap_np)
                        RIQ = tq_dap - fq_dap


                        print("fq_ed:", fq_dap)
                        print("sq_ed:", sq_dap)
                        print("tq_ed:", tq_dap)
                        print("max_ed:", max_dap)
                        print("min_ed:", min_dap)
                        print("Ran_intercuartil", RIQ)
                        

                        columnas2 = ['Estadística','Dosis de Entrada (mGy)']#,'1st Quartile' ,'2nd Quartile','3rd Quartile' ,'IQR' ,'Min' ,'Max' , 'KAP (Gy*cm^2)' , 'Air Kerma (mGy)' ,'Fluoroscopy time (min)' ,'Exposure images' ]#el mismo orden del arreglo con la informacion de la imagen dicom 
                        #'1st Quartile', '2nd Quartile' ,'3rd Quartile' ,'IQR','Min', 'Max',
                        dataFrame = pd.DataFrame(columns=columnas2)# creo un dataframe y nombro las columnas del como sea requerido

                        # Append statistics to DataFrame
                        dataFrame.loc[len(dataFrame)] = ['1er Cuartil', "{:.2f}".format(fq_dap)]
                        dataFrame.loc[len(dataFrame)] = ['2do Cuartil', "{:.2f}".format(sq_dap)]
                        dataFrame.loc[len(dataFrame)] = ['3er Cuartil', "{:.2f}".format(tq_dap)]
                        dataFrame.loc[len(dataFrame)] = ['Min', "{:.2f}".format(min_dap)]
                        dataFrame.loc[len(dataFrame)] = ['Max', "{:.2f}".format(max_dap)]
                        dataFrame.loc[len(dataFrame)] = ['Rango Intercuartílico ', "{:.2f}".format(RIQ)]

                        print(dataFrame)  # Display DataFrame
                        dataFrame.to_excel(ruta_df, index=False)#creo un archivo excel apartir del df, con nombre DatosFechahora.xlsx

                        print("Datos guardados en el archivo Excel:", ruta_df)

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
                        window = sg.Window("Nivel de Referencia en Proyeccion "+est, layout)

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

# Guardar el DataFrame en un archivo Excel
df.to_excel(ruta_archivo, index=False)#creo un archivo excel apartir del df, con nombre DatosFechahora.xlsx

print("Datos guardados en el archivo Excel:", ruta_archivo)

