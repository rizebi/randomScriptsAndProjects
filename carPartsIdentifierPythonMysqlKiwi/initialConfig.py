#!/usr/bin/python

# After MySQL was installed (and of course runnning), and we are sure
# that we can import MySQLdb module, we run this script, which is the
# initial script which create database, create the tables needed, and
# fill them by default

import MySQLdb
import os

# Open database connection 
db = MySQLdb.connect("localhost","root","mysqlpass")

# Prepare a cursor object using cursor() method
cursor = db.cursor()


# First we must drop the database if it exists
cursor.execute("DROP DATABASE IF EXISTS ProiectBD2")

# Then create the database
cursor.execute("CREATE DATABASE ProiectBD2")

# Use the database ProiectBD2
cursor.execute("USE ProiectBD2")

# Now we have to create the tables:

cursor.execute("""CREATE TABLE coduriPiese(
	codPiesa VARCHAR(10) PRIMARY KEY
	);""")

cursor.execute("""CREATE TABLE motoare(
	codMotor VARCHAR(10) PRIMARY KEY,
	codFiltruPolen VARCHAR(10) NOT NULL,
	codFiltruCombustibil VARCHAR(10) NOT NULL,
	codFiltruAer VARCHAR(10) NOT NULL,
	codFiltruUlei VARCHAR(10) NOT NULL,
	FOREIGN KEY (codFiltruPolen) REFERENCES coduriPiese(codPiesa),
	FOREIGN KEY (codFiltruCombustibil) REFERENCES coduriPiese(codPiesa),
	FOREIGN KEY (codFiltruAer) REFERENCES coduriPiese(codPiesa),
	FOREIGN KEY (codFiltruUlei) REFERENCES coduriPiese(codPiesa)
	); """)

cursor.execute("""CREATE TABLE masini(
	IDMasina INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	marcaMasina VARCHAR(20) NOT NULL,
	modelMasina VARCHAR(20) NOT NULL,
	combustibil VARCHAR(10) NOT NULL,
	capacitate SMALLINT UNSIGNED NOT NULL,
	codMotor VARCHAR(10) NOT NULL,
	FOREIGN KEY (codMotor) REFERENCES motoare(codMotor)
	);""")

cursor.execute("""CREATE TABLE piese(
	IDPiesa INT(6) UNSIGNED PRIMARY KEY,
	producator VARCHAR(15) NOT NULL,
	numePiesa VARCHAR(20) NOT NULL,
	codPiesa VARCHAR(10) NOT NULL,
	pretPiesa FLOAT NOT NULL,
	cantitateTotala INT(3),
	FOREIGN KEY (codPiesa) REFERENCES coduriPiese(codPiesa)
	);""")

cursor.execute("""CREATE TABLE magazine(
	IDMagazin INT(2) UNSIGNED PRIMARY KEY,
	numeMagazin VARCHAR(20) NOT NULL,
	adresaMagazin VARCHAR(50) NOT NULL
	);""")

cursor.execute("""CREATE TABLE stocuri(
	IDStoc INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	IDPiesa INT(6) UNSIGNED NOT NULL,
	IDMagazin INT(2) UNSIGNED NOT NULL,
	cantitateMagazin INT(3) NOT NULL,
	FOREIGN KEY (IDPiesa) REFERENCES piese(IDPiesa),
	FOREIGN KEY (IDMagazin) REFERENCES magazine(IDMagazin)
	);""")

# Now we have to create a trigger to update the total quantity of the parts
# from all the shops. In other words, when in table "stocuri" there is an
# insert or update, this trigger must trigger

cursor.execute("""CREATE TRIGGER after_stocuri_insert
					AFTER INSERT ON stocuri
					FOR EACH ROW
				BEGIN
					UPDATE piese
						SET cantitateTotala = (SELECT sum(cantitateMagazin) FROM stocuri WHERE IDPiesa = NEW.IDPiesa)
						WHERE IDPiesa = NEW.IDPiesa;
				END ;""")

cursor.execute("""CREATE TRIGGER after_stocuri_update
					AFTER UPDATE ON stocuri
					FOR EACH ROW
				BEGIN
					UPDATE piese
						SET cantitateTotala = (SELECT sum(cantitateMagazin) FROM stocuri WHERE IDPiesa = NEW.IDPiesa)
						WHERE IDPiesa = NEW.IDPiesa;
				END ;""")

# Now we create function returnCodMotor which receives 4 parameters: marcaMasina VARCHAR(20), modelMasina VARCHAR(20),
# combustibil VARCHAR(10), capacitate SMALLINT UNSIGNED and returns codMotor VARCHAR(10)

cursor.execute("""CREATE FUNCTION returnCodMotor (p_marcaMasina VARCHAR(20), p_modelMasina VARCHAR(20),
					p_combustibil VARCHAR(10), p_capacitate SMALLINT UNSIGNED)
				RETURNS VARCHAR(10) DETERMINISTIC
				RETURN (SELECT codMotor
							FROM masini 
							WHERE UPPER(p_marcaMasina) = UPPER(marcaMasina) AND
								UPPER(p_modelMasina) = UPPER(modelMasina) AND
								UPPER(p_combustibil) = UPPER(combustibil) AND
								p_capacitate = capacitate);""")



# Now we create a procedure that from 4 parameters: marcaMasina VARCHAR(20), modelMasina VARCHAR(20),
# combustibil VARCHAR(10), capacitate SMALLINT UNSIGNED, finds the codMotor and all the parts compatible
# with that car

cursor.execute("""CREATE PROCEDURE coduriPiese (IN marcaMasina VARCHAR(20), IN modelMasina VARCHAR(20),
												IN combustibil VARCHAR(10), IN capacitate SMALLINT UNSIGNED)
						BEGIN
							SELECT * FROM motoare WHERE codMotor = returnCodMotor(marcaMasina, modelMasina, combustibil, capacitate);
						END;""")

# Now we create another procedure which will show all the choices for a given codPiesa

cursor.execute("""CREATE PROCEDURE varianteCodPiesa (IN codulPiesei VARCHAR(10))
						BEGIN
							SELECT * FROM piese WHERE codPiesa = codulPiesei;
						END;""")

# Now we create another procedure which will show all the places where IDPiese is found

cursor.execute("""CREATE PROCEDURE locatiePiesa (IN IDPiesei INT(6))
						BEGIN
							SELECT s.IDStoc, s.IDPiesa, s.cantitateMagazin, m.numeMagazin, m.adresaMagazin
							FROM stocuri s, magazine m
							WHERE IDPiesa = IDPiesei AND s.IDMagazin = m.IDMagazin;
						END;""")

cursor.execute("""CREATE PROCEDURE cantitateDisponibila (IN IDulStoc INT(6))
						BEGIN
							SELECT cantitateMagazin FROM stocuri WHERE IDStoc = IDulStoc;
						END;""")

cursor.execute("""CREATE PROCEDURE updateStoc (IN IDulStoc INT(6))
						BEGIN
							UPDATE stocuri SET cantitateMagazin = cantitateMagazin - 1  WHERE IDStoc = IDulStoc;
						END;""")

cursor.execute("""CREATE PROCEDURE raport1 ()
						BEGIN
							SELECT codPiesa, numePiesa, sum(cantitateTotala) FROM piese GROUP BY codPiesa, numePiesa;
						END""")

cursor.execute("""CREATE PROCEDURE raport2 ()
						BEGIN
							SELECT a.IDMagazin, b.numeMagazin, b.adresaMagazin, count(a.cantitateMagazin)
							FROM stocuri a, magazine b
							WHERE a.IDMagazin = b.IDMagazin
							GROUP BY IDMagazin;
						END;""")

cursor.execute("""CREATE PROCEDURE ceACumparat (IN IDulStoc INT(6), IN IDMasinaCurenta VARCHAR(20))
						BEGIN
							SELECT mas.marcaMasina, mas.modelMasina, mas.combustibil, mas.capacitate, mas.codMotor,
									pie.codPiesa, pie.numePiesa, pie.producator, mag.numeMagazin
							FROM masini mas, piese pie, motoare mot, magazine mag, stocuri sto
							WHERE sto.IDStoc = IDulStoc AND
									sto.IDMagazin = mag.IDMagazin AND
									sto.IDPiesa = pie.IDPiesa AND
									(pie.codPiesa = mot.codFiltruPolen OR pie.codPiesa = mot.codFiltruCombustibil OR
										pie.codPiesa = mot.codFiltruAer OR pie.codPiesa = mot.codFiltruUlei) AND
									mot.codMotor = mas.codMotor AND mas.IDMasina = IDMasinaCurenta;
						END;""")

cursor.execute("""CREATE PROCEDURE daMiIDMasina (IN p_marcaMasina VARCHAR(20), IN p_modelMasina VARCHAR(20),
												IN p_combustibil VARCHAR(10), IN p_capacitate SMALLINT UNSIGNED)
						BEGIN
							SELECT IDMasina
							FROM masini 
							WHERE UPPER(p_marcaMasina) = UPPER(marcaMasina) AND
								UPPER(p_modelMasina) = UPPER(modelMasina) AND
								UPPER(p_combustibil) = UPPER(combustibil) AND
								p_capacitate = capacitate;
						END;""")


# Delete user guest@localhost which we will use in application
cursor.execute("DROP USER IF EXISTS BDuser@localhost")

# Create user to use on application (limited privileges)
cursor.execute("CREATE USER 'BDuser'@'localhost' IDENTIFIED BY 'BDuser';")

# Grant privileges
cursor.execute("GRANT ALL PRIVILEGES ON ProiectBD2.* TO BDuser@localhost;")

# Flush privileges
cursor.execute("FLUSH PRIVILEGES;")

# Disconnect from server
db.close()

# Run the script to populate the tables
os.system("./populateTables.py")