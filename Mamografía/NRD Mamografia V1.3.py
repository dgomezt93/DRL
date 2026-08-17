import pandas as pd
import pydicom
import os
import numpy as np
from datetime import datetime
import PySimpleGUI as sg
sg.theme('LightGrey')

ruta_carpeta = sg.popup_get_folder("Seleccionar carpeta")
print(ruta_carpeta)

contador = 0

# Obtener la fecha y hora actual
fecha_hora_actual = datetime.now()
fecha_actual = str(fecha_hora_actual.date()) + "_" + str(fecha_hora_actual.hour) + str(fecha_hora_actual.minute)
print("Fecha actual:", fecha_actual)

# Especificar la ruta del archivo Excel

ruta_archivo = "C:/Users/Daniela G/Desktop/PruebaDicom/Mamografia" + str(fecha_actual) + ".xlsx"#asigno una ruta para archivo 

ruta_dt = "C:/Users/Daniela G/Desktop/PruebaDicom/Nivel de Referencia DT" + str(fecha_actual) + ".xlsx"#asigno una ruta para archivo 


# Define the tags
tagEdad = (0x0010, 0x1010)
tagkVp = (0x0018, 0x0060)
tagExpTime = (0x0018, 0x1150)
tagmAs = (0x0018, 0x1152)
tagOrganDose = (0x0040, 0x0316)
tagEntranceDose = (0x0040, 0x8302)
tagStudyDescrip = (0x0008, 0x1030)
tagImageLaterality = (0x0020, 0x0060)  # Corregido el tag de '002,0016' a '0020,0060'
tagViewPosition = (0x0018, 0x5101)
tagThickness = (0x0018, 0x11A0)
tagManufacture = (0x0008, 0x0070)
tagModel= (0x0008, 0x1090)
tagInstitutionName = (0x0008,0x0080)
tagUID = (0x0020,0x000D)
tagserial = (0x0018,0x1000)
tagLaterality = (0x0020,0x0062)
tagLocalizacion = (0x0008, 0x1010)

# Definir funciones
def listar_archivos_en_carpeta(ruta_carpeta):
    nombres_archivos = []
    if os.path.isdir(ruta_carpeta):
        archivos_en_carpeta = os.listdir(ruta_carpeta)
        for archivo in archivos_en_carpeta:
            ruta_absoluta = os.path.join(ruta_carpeta, archivo)
            if os.path.isfile(ruta_absoluta):
                nombres_archivos.append(archivo)
    else:
        print("La ruta proporcionada no es una carpeta.")
    return nombres_archivos


def extract_dicom_metadata(dicom_file):
    global contador
    ds = pydicom.dcmread(dicom_file,force=True)
    metadata = []

    
    espesor_element = ds.get(tagThickness, "N/A")
    espesor_value = espesor_element.value if hasattr(espesor_element, "value") else espesor_element
    print(float(espesor_value))

    if 40 < espesor_value < 60:



        # Metadata appending
        metadata.append(nombre_archivo)

        descripcion_element = ds.get(tagStudyDescrip, "N/A")
        descripcion_value = descripcion_element.value if hasattr(descripcion_element, "value") else descripcion_element
        metadata.append(descripcion_value)

        kvp_element = ds.get(tagkVp, "N/A")
        kvp_value = kvp_element.value if hasattr(kvp_element, "value") else kvp_element
        metadata.append(kvp_value )

        tiempo_element = ds.get(tagExpTime, "N/A")
        tiempo_value = tiempo_element.value if hasattr(tiempo_element, "value") else tiempo_element
        metadata.append(tiempo_value )
        
        
        mAs_element = ds.get(tagmAs, "N/A")
        mAs_value = mAs_element.value if hasattr(mAs_element, "value") else mAs_element
        metadata.append(mAs_value)

        #metadata.append(ds[tagOrganDose].value*100)

        dose_element = ds.get(tagEntranceDose, "N/A")
        dose_value = dose_element.value if hasattr(dose_element, "value") else dose_element
        metadata.append(dose_value)

        organ_dose_element = ds.get(tagOrganDose, "N/A")
        organ_dose_value = organ_dose_element.value if hasattr(organ_dose_element, "value") else organ_dose_element
        organ_dose_value = float(organ_dose_value)*100
        metadata.append(organ_dose_value)
        
        proyeccion_element = ds.get(tagViewPosition, "N/A")
        proyeccion_value = proyeccion_element.value if hasattr(proyeccion_element, "value") else proyeccion_element
        valproyeccion = proyeccion_value
        if valproyeccion == 'ML':
            valproyeccion = 'MLO'
        metadata.append(valproyeccion)

        metadata.append(float(espesor_value))
        
        fabricante_element = ds.get(tagManufacture, "N/A")
        fabricante_value = fabricante_element.value if hasattr(fabricante_element, "value") else fabricante_element
        metadata.append(fabricante_value)
        
        modelo_element = ds.get(tagModel, "N/A")
        modelo_value = modelo_element.value if hasattr(modelo_element, "value") else modelo_element
        metadata.append(modelo_value)
        
        institucion_element = ds.get(tagInstitutionName, "N/A")
        institucion_value = institucion_element.value if hasattr(institucion_element, "value") else institucion_element
        metadata.append(institucion_value)
    
        UID_element = ds.get(tagUID, "N/A")
        UID_value = UID_element.value if hasattr(UID_element, "value") else UID_element
        metadata.append(UID_value)
        
        serial_element = ds.get(tagserial, "N/A")
        serial_value = serial_element.value if hasattr(serial_element, "value") else serial_element
        metadata.append(serial_value)
        
        lateralidad_element = ds.get(tagLaterality, "N/A")
        lateralidad_value = lateralidad_element.value if hasattr(lateralidad_element, "value") else lateralidad_element
        metadata.append(lateralidad_value)

        localizacion_element = ds.get(tagLocalizacion, None)
        localizacion_value = localizacion_element.value if hasattr(localizacion_element, "value") else localizacion_element      
        metadata.append(localizacion_value)
    

    return metadata



# Ruta de la carpeta con imágenes DICOM
nombres_archivos = listar_archivos_en_carpeta(ruta_carpeta)

# Definir las columnas del DataFrame
columnas = ['Archivo', 'Estudio', 'kV', 'Tiempo de Exposición mSec', 'mAs', 'Dosis de Entrada [mGy]','Dosis Glandular [mGy]', 'Proyección', 'Espesor', 'Fabricante','Modelo','Institución', 'UID','Serial','Laterality','Localización']
#se crea el dataframe con las columnas definidas
df = pd.DataFrame(columns=columnas)

index = 0
for nombre_archivo in nombres_archivos: # recorre todo el arreglo con los nombres y nombre por nombre lo usa 
    print(nombre_archivo)#imprimo nombre del archivo al que le voy a extraer la informacion de interes
    index=index+1
    sg.one_line_progress_meter("Current Progress", index+1, len(nombres_archivos))
    #dicom_file = "C:/Users/Daniela G/Desktop/PruebaDicom/IMAGENES/" + nombre_archivo# la ruta del archivo es la ruta de la carpeta + el nombre del archivo
    dicom_file = ruta_carpeta + '/' + nombre_archivo
    metadata = extract_dicom_metadata(dicom_file)#extraigo la informacion de interes de la imagen
    print(metadata)#imprimo la informacion 
    #print(len(metadata))


    # 
    if len(metadata) != 0:
        df.loc[len(df)] = metadata# agrego al dataframe una fila con los valores de la informacion de la imagen dicom
   
        print("****************************")# caracteres para separar un archivo de otro y repito el for hasta lea todos los archivos existentes en la carpeta
    else:
        print("Espesor fuera de rango")
print(df)#muestro el dataframe






# Guardar el DataFrame en un archivo Excel
carpeta_destino = sg.popup_get_folder("Seleccione la carpeta donde desea guardar el archivo Excel")
# Verificar si el usuario seleccionó una carpeta
if carpeta_destino:
    ruta_DE = f"{carpeta_destino}/Mamografía_{fecha_actual}.xlsx"
    
    # Guardar el DataFrame en el archivo seleccionado
    df.to_excel(ruta_DE, index=False)
    
    print("Datos guardados en el archivo Excel:", ruta_DE)
else:
    sg.popup_error("No se seleccionó una carpeta. No se guardará el archivo.")


sg.popup_ok("Tarea realizada")
#print("# de Archivos con EntranceDoseInmGy = ", contador)


while True:
    try:
        T1 = df['Localización'].unique()
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
            Loc=selected_option
            window.close()
        if event == sg.WIN_CLOSED:
            exit()
        
        if Loc in T1:
            df1=df[df['Localización']==Loc]#en DF1 dataframe filtrado por modelo del equipo
            print("\n",df1,"\n")
            unique_strings = df1['Proyección'].unique()

            
            

            print(unique_strings)
            unique_strings_2 = [s.strip() for s in unique_strings]  # Eliminar espacios extra
            print(unique_strings_2)

        
            for est in unique_strings_2:
                print("Nivel de Referencia proyección " + est)
                df2=df1[df1['Proyección']==est]#dentro del Dataframe para un modelo de equipo filtro por descripcion de la serie ej: "Torax simple"
                dfresultado=df2
                # Agrupar por 'NOMBRE' y sumar los valores de 'DLP'
                #dfresultado = df2.groupby('Nombre Imagen', as_index=False).agg({'DLP': 'sum','CTDIvol_name': 'sum'})

                # Mostrar el resultado
                #print(dfresultado)

                Entrance_Dose_np = dfresultado['Dosis de Entrada [mGy]'].to_numpy()  # Convert to NumPy array if needed
                    
                # Calculate percentiles and statistics
                fq_ed = np.percentile(Entrance_Dose_np, 25)
                sq_ed = np.percentile(Entrance_Dose_np, 50)
                tq_ed = np.percentile(Entrance_Dose_np, 75)
                max_ed = np.max(Entrance_Dose_np)
                min_ed = np.min(Entrance_Dose_np)
                RIQ_ED = tq_ed - fq_ed


                print("fq_ed:", fq_ed)
                print("sq_ed:", sq_ed)
                print("tq_ed:", tq_ed)
                print("max_ed:", max_ed)
                print("min_ed:", min_ed)
                print("Ran_intercuartil", RIQ_ED)

                Organ_dose_np = dfresultado['Dosis Glandular [mGy]'].to_numpy()  # Convert to NumPy array if needed
                    
                # Calculate percentiles and statistics
                fq_dg = np.percentile(Organ_dose_np, 25)
                sq_dg = np.percentile(Organ_dose_np, 50)
                tq_dg = np.percentile(Organ_dose_np, 75)
                max_dg = np.max(Organ_dose_np)
                min_dg = np.min(Organ_dose_np)
                RIQ_DG = tq_dg - fq_dg


                print("fq_ed:", fq_dg)
                print("sq_ed:", sq_dg)
                print("tq_ed:", tq_dg)
                print("max_ed:", max_dg)
                print("min_ed:", min_dg)
                print("Ran_intercuartil", RIQ_DG)

                    

                columnas2 = ['Estadística','Dosis de entrada [mGy]', 'Dosis Glandular [mGy]']#,'1st Quartile' ,'2nd Quartile','3rd Quartile' ,'IQR' ,'Min' ,'Max' , 'KAP (Gy*cm^2)' , 'Air Kerma (mGy)' ,'Fluoroscopy time (min)' ,'Exposure images' ]#el mismo orden del arreglo con la informacion de la imagen dicom 
                #'1st Quartile', '2nd Quartile' ,'3rd Quartile' ,'IQR','Min', 'Max',
                dataFrame = pd.DataFrame(columns=columnas2)# creo un dataframe y nombro las columnas del como sea requerido

                # Append statistics to DataFrame
                dataFrame.loc[len(dataFrame)] = ['1er Cuartil', "{:.2f}".format(fq_ed),"{:.2f}".format(fq_dg)]
                dataFrame.loc[len(dataFrame)] = ['2do Cuartil', "{:.2f}".format(sq_ed),"{:.2f}".format(sq_dg)]
                dataFrame.loc[len(dataFrame)] = ['3er Cuartil', "{:.2f}".format(tq_ed), "{:.2f}".format(tq_dg)]
                dataFrame.loc[len(dataFrame)] = ['Min', "{:.2f}".format(min_ed),"{:.2f}".format(min_dg)]
                dataFrame.loc[len(dataFrame)] = ['Max', "{:.2f}".format(max_ed),"{:.2f}".format(max_dg)]
                dataFrame.loc[len(dataFrame)] = ['Rango Intercuartílico ', "{:.2f}".format(RIQ_ED), "{:.2f}".format(RIQ_DG)]

               

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
                window = sg.Window("Nivel de Referencia "+est, layout)
                

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
print('df1:::::::::::::::::')
print(df1)


df_dosis_proyeccion = df.groupby(['UID', 'Laterality', 'Proyección'], as_index=False)['Dosis de Entrada [mGy]'].sum()
df_dosis_mama = df_dosis_proyeccion.groupby(['UID', 'Laterality'], as_index=False)['Dosis de Entrada [mGy]'].sum()
df_dosis_total = df_dosis_mama.groupby('UID', as_index=False)['Dosis de Entrada [mGy]'].sum()
df_dosis_total['Dosis Total'] = df_dosis_total['Dosis de Entrada [mGy]'] / 2  # Promedio de ambas mamas
print('Dosis total')
print(df_dosis_total)

Dosis_total_np = df_dosis_total['Dosis de Entrada [mGy]'].to_numpy()  # Convert to NumPy array if needed
                    
# Calculate percentiles and statistics
fq_ed = np.percentile(Dosis_total_np, 25)
sq_ed = np.percentile(Dosis_total_np, 50)
tq_ed = np.percentile(Dosis_total_np, 75)
max_ed = np.max(Dosis_total_np)
min_ed = np.min(Dosis_total_np)
RIQ = tq_ed - fq_ed

print("fq_ed:", fq_ed)
print("sq_ed:", sq_ed)
print("tq_ed:", tq_ed)
print("max_ed:", max_ed)
print("min_ed:", min_ed)
print("Ran_intercuartil", RIQ)


    

columnas3 = ['Estadística','Dosis total [mGy]']#,'1st Quartile' ,'2nd Quartile','3rd Quartile' ,'IQR' ,'Min' ,'Max' , 'KAP (Gy*cm^2)' , 'Air Kerma (mGy)' ,'Fluoroscopy time (min)' ,'Exposure images' ]#el mismo orden del arreglo con la informacion de la imagen dicom 
#'1st Quartile', '2nd Quartile' ,'3rd Quartile' ,'IQR','Min', 'Max',
dataFrameDT = pd.DataFrame(columns=columnas3)# creo un dataframe y nombro las columnas del como sea requerido

# Append statistics to DataFrame
dataFrameDT.loc[len(dataFrameDT)] = ['1er Cuartil', "{:.2f}".format(fq_ed)]
dataFrameDT.loc[len(dataFrameDT)] = ['2do Cuartil', "{:.2f}".format(sq_ed)]
dataFrameDT.loc[len(dataFrameDT)] = ['3er Cuartil', "{:.2f}".format(tq_ed)]
dataFrameDT.loc[len(dataFrameDT)] = ['Min', "{:.2f}".format(min_ed)]
dataFrameDT.loc[len(dataFrameDT)] = ['Max', "{:.2f}".format(max_ed)]
dataFrameDT.loc[len(dataFrameDT)] = ['Rango Intercuartílico ', "{:.2f}".format(RIQ)]
print(dataFrameDT)  # Display DataFrame

# Pedir al usuario seleccionar la carpeta donde guardar el archivo
carpeta_destino = sg.popup_get_folder("Seleccione la carpeta donde desea guardar el archivo Excel")

# Verificar si el usuario seleccionó una carpeta
if carpeta_destino:
    ruta_DE = f"{carpeta_destino}/NivelReferencia_DosisTotal_{fecha_actual}.xlsx"
    
    # Guardar el DataFrame en el archivo seleccionado
    dataFrameDT.to_excel(ruta_DE, index=False)
    
    print("Datos guardados en el archivo Excel:", ruta_DE)
else:
    sg.popup_error("No se seleccionó una carpeta. No se guardará el archivo.")

# Convert the DataFrame to a list of lists
data_list = dataFrameDT.values.tolist()
header_list = dataFrameDT.columns.tolist()

# Define the layout for PySimpleGUI
layout = [
    [sg.Table(values=data_list, headings=header_list,
            auto_size_columns=True, display_row_numbers=False,
            justification='center', num_rows=min(25, len(data_list)))],
    [sg.Button('Exit')]
]

# Create the window
window = sg.Window('Nivel de Referencia Dosis Total', layout)


# Event loop to process events and get values from the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

# Close the window
window.close()
