#PROYECTO PYTHON CON BBDD POSTGRES
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
try:
    db = psycopg2.connect(
        dbname="proyectopython",
        user="raulhr",
        password="raulhr",
        host="localhost"
    )
except psycopg2.Error as e:
    print("No puedo conectar a la base de datos:", e)
    sys.exit(1)


eleccion=0
texto=''
def EscribirCentrado(texto):
    anchura=80
    longitud=len(texto)
    texto=("MENU\n1.Listar información\n2.Buscar información\n3.Búsqueda relacionada\n4.Insertar información\n5.Borrar centrales solares fotovoltaicas\n6.Actualizar información\n7.Salir")
    centrado=(' '*36 + texto)
    print("-"*anchura)
    print(centrado)
    print("-"*anchura)

def ejlistar(db):
	sql="SELECT * FROM CENTRALES"
	sql_hidro="SELECT * FROM HIDROELECTRICA"
	sql_solar="SELECT * FROM SOLAR"
	sql_termica="SELECT * FROM TERMICA"
	sql_eolicas="SELECT * FROM EOLICAS"
	cursor = db.cursor()
	print("-"*68)
	print("Centrales totales"," "*3+"Hidroelectricas"," "*3+"Solar"," "*3+"Termica"," "*3+"Eolicas")
	try:
		cursor.execute(sql)
		centrales=cursor.rowcount
		cursor.execute(sql_hidro)
		hidro=cursor.rowcount
		cursor.execute(sql_solar)
		solar=cursor.rowcount
		cursor.execute(sql_termica)
		termica=cursor.rowcount
		cursor.execute(sql_eolicas)
		eolicas=cursor.rowcount
		print(centrales," "*17,hidro," "*16,solar," "*6,termica," "*8,eolicas)
	except:
		print("Error en la consulta")
	

def ejbuscar(db):
	cap_max=input("Introduce la primera capacidad maxima: ")
	while not cap_max.isdigit():
		cap_max=input("No has introducido un valor numerico\nIntroduce la primera capacidad maxima: ")
	cap_max=int(cap_max)
	cap_max2=input("Introduce la segunda capacidad maxima: ")
	while not cap_max2.isdigit():
		cap_max2=input("No has introducido un valor numerico\nIntroduce la segunda capacidad maxima: ")
	cap_max2=int(cap_max2)
	while cap_max>cap_max2:
		cap_max=input("Has introducido la primera cantidad maxima mayor que la segunda\nIntroduce la primera capacidad maxima: ")
		while not cap_max.isdigit():
			cap_max=input("No has introducido un valor numerico\nIntroduce la primera capacidad maxima: ")
		cap_max=int(cap_max)
		cap_max2=input("Introduce la segunda capacidad maxima: ")
		while not cap_max2.isdigit():
			cap_max2=input("No has introducido un valor numerico\nIntroduce la segunda capacidad maxima: ")
		cap_max2=int(cap_max2)
	sql="SELECT * FROM CENTRALES"
	cursor = db.cursor(cursor_factory=RealDictCursor)
	print("-"*40)
	print("Código de las centrales"," "*5+"Ubicación")
	print("-"*40)
	validacion=0
	try:
		cursor.execute(sql)
		registros=cursor.fetchall()
		for registro in registros:
			cap_max_centrales=registro["capacidad_max"]
			if cap_max_centrales>=cap_max and cap_max_centrales<=cap_max2:
				print(registro["cod_centrales"]," "*20,registro["ubicacion"])
				validacion=1		
	except:
		print("Error en la consulta")
	if validacion==0:
		print("No hay datos para los valores introducidos")	
	

def ejrelacionado(db):
	nom_empresa=input("Introduce el nombre de la empresa que quieras buscar: ")
	while not nom_empresa.replace(" ","").isalpha():
		nom_empresa=input("No has introducido el nombre de la empresa \nIntroduce el nombre de la empresa que quieras buscar: ")
	sql="SELECT * FROM EMPRESA"
	sql_central="SELECT * FROM CENTRALES"
	cursor = db.cursor(cursor_factory=RealDictCursor)
	cursor_centrales= db.cursor(cursor_factory=RealDictCursor)
	validacion=0
	validacion2=0
	try:
		cursor.execute(sql)
		registros=cursor.fetchall()
		cursor_centrales.execute(sql_central)
		for registro in registros:
			if registro["nombre"]==nom_empresa:
				validacion=1
				validacion2=1
				nom_propietario=input("Introduce el nombre del propietario de dicha empresa: ")
				while not nom_propietario.replace(" ","").isalpha():
					nom_propietario=input("No has introducido el nombre del propietario \nIntroduce el nombre del propietario de dicha empresa: ")
				if registro["propietario"]==nom_propietario:
					validacion2=2
					cif_empresa=registro["cif"]
					cursor_centrales.execute(sql_central)
					centrales=cursor_centrales.fetchall()
					for central in centrales:
						if cif_empresa==central["cif"]:
							print("-"*65)
							print("Código de las centrales"," "*5+"Ubicación"," "*5+"Capacidad Máxima")
							print(central["cod_centrales"]," "*20,central["ubicacion"]," "*(13-len(central["ubicacion"])),central["capacidad_max"])
	except:
		print("Error en la consulta")
	if validacion==0:
		print("No hay ninguna empresa que se llame asi")
	if validacion2==1:
		print("El propietario introducido no es el propietario de dicha empresa")


def insertar(db):
	cursor = db.cursor()
	cif=input("Introduce el CIF de la empresa, tiene que ser una letra y 8 números: ")
	cod_pe=input("Introduce un codigo de producción de empresa por hora: ")
	while not cod_pe.isdigit():
		cod_pe=input("No has introducido un numero\nIntroduce un codigo de producción de empresa por hora: ")
	cod_pe=int(cod_pe)
	nombre=input("Introduce el nombre de la empresa: ")
	while not nombre.replace(" ","").isalpha():
		nombre=input("No has introducido una palabra\nIntroduce el nombre de la empresa: ")
	propietario=input("Introduce el nombre del propietario de la empresa: ")
	while not propietario.replace(" ","").isalpha():
		propietario=input("No has introducido un propietario\nIntroduce el nombre de la empresa: ")
	sql="INSERT INTO EMPRESA VALUES('%s','%d','%s','%s')"%(cif,cod_pe,nombre,propietario)
	try:
		cursor.execute(sql)
		db.commit()
		print("Se han introducido los datos correctamente ")
	except:
		db.rollback()
		print("No se han introducido los datos correctamente ")
	

def borrar(db):
	cursor=db.cursor()
	sql="DELETE FROM SOLAR WHERE TIPO_S='FOTOVOLTAICA'"
	try:
		cursor.execute(sql)
		db.commit()
		print("Has borrado todos los datos de las centrales Solares de tipo Fotovoltaicas")
	except:
		db.rollback()
		print("No has borrado nada")

def actualizar(db):
	cursor=db.cursor(cursor_factory=RealDictCursor)
	cursor_centrales=db.cursor(cursor_factory=RealDictCursor)
	cif=input("Introduce el CIF de la empresa, tiene que ser una letra y 8 números: ")
	sql="SELECT * FROM EMPRESA"
	validacion=0
	try:
		cursor.execute(sql)
		registros=cursor.fetchall()
		for registro in registros:
			if cif==registro["cif"]:
				validacion=1
				capacidad_max=input("Introduce la nueva capacidad máxima: ")
				while not capacidad_max.isdigit():
					capacidad_max=input("No has introducido una capacidad maxima valida\nIntroduce la nueva capacidad máxima: ")
				capacidad_max=int(capacidad_max)
				sql_central="UPDATE CENTRALES SET CAPACIDAD_MAX = '%d' WHERE CIF='%s'"%(capacidad_max,cif)
				try:
					cursor_centrales.execute(sql_central)
					db.commit()
					print("Has actualizado los datos con exito")
				except:
					db.rollback()
					print("No has actualizado los datos con exito")
	except:
		print("Error en la consulta")
	if validacion==0:
		print("No has introducido un CIF valido")

def salir(db):
	db.close
	print("Muchas gracias por su tiempo!!")

while eleccion!=7:
    if eleccion==1:
        ejlistar(db)
    elif eleccion==2:
        ejbuscar(db)
    elif eleccion==3:
        ejrelacionado(db)
    elif eleccion==4:
        insertar(db)
    elif eleccion==5:
        borrar(db)
    elif eleccion==6:
        actualizar(db)
    EscribirCentrado(texto)
    eleccion=int(input("Introduce lo que quieras hacer "))
    while not (eleccion==1 or eleccion==2 or eleccion==3 or eleccion==4 or eleccion==5 or eleccion==6 or eleccion==7):
        eleccion=int(input("No has introducido un numero valido, introduce lo que quieras hacer "))
salir(db)