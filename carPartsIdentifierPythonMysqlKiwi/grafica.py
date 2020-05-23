#!/usr/bin/python

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.config import Config 						# For window size
from kivy.graphics import Color, Rectangle		  # For background
from kivy.uix.button import Button
from functools import partial

import MySQLdb

cosCumparaturi = ""
IDMasinaCurenta = ""
fmt = "{0:7} {1:7} {2:9} {3:6} {4:8} {5:8} {6:20} {7:13} {8:20}"
cosCumparaturi = cosCumparaturi + fmt.format("Marca", "Model", "Comb.", "Capac", "codMotor", "codPiesa",
	"numePiesa", "producator", "magazin")
cosCumparaturi = cosCumparaturi + "\n" + "-"*93 + "\n"

# Adaugat fiecare persoana ce cumpara


# Open database connection 
# Connect with user after implementation TODO
db = MySQLdb.connect("localhost","BDuser","BDuser")

# Prepare a cursor object using cursor() method
cursor = db.cursor()

# Use the database ProiectBD2
cursor.execute("USE ProiectBD2")

class Grafica(BoxLayout):

	def __init__(self, **kwargs):
		super(Grafica, self).__init__(**kwargs)
		self.orientation='vertical'
		self.padding=[400, 50, 400, 20]
		self.spacing=10
		self.ok1 = 1

		self.campNull=Label(text='Nu ai introdus date intr-un camp, mai incearca!',
					   italic=True,
					   font_size=46,
					   color=(0,0.2,0.2,1))

		self.capacitateNumar=Label(text='Capacitatea motorului este numar, nu text! Mai incearca!',
					   italic=True,
					   font_size=46,
					   color=(0,0.2,0.2,1))

		self.introduNumar=Label(text='Valoarea trebuie sa fie numar, nu text! Mai incearca!',
					   italic=True,
					   font_size=46,
					   color=(0,0.2,0.2,1))

		self.autoturismNeidentificat=Label(text='Autoturism neidentificat in baza de date. Mai incearca!',
					   italic=True,
					   font_size=46,
					   color=(0,0.2,0.2,1))

		self.stocNeidentificat=Label(text='IDStoc neidentificat in baza de date. Mai incearca!',
					   italic=True,
					   font_size=46,
					   color=(0,0.2,0.2,1))

		self.stocZero=Label(text='Din pacate piesa nu mai este disponibila in magazin. Mai incearca!',
					   italic=True,
					   font_size=40,
					   color=(0,0.2,0.2,1))

		self.rezervareCompleta=Label(text="""Felicitari!! Ai rezervat cu success piesa in magazin.\n
Apasa click pentru a rezerva alta piesa sau a vedea rapoarte\n
sau exit pentru a iesi""",
					   italic=True,
					   font_size=40,
					   markup=True,
					   color=(0,0.2,0.2,1))

		self.piesaNeidentificata=Label(text='IDPiesa introdus nu a fost gasit in baza de date. Mai incearca!',
					   italic=True,
					   font_size=46,
					   color=(0,0.2,0.2,1))

		self.variantaIncorecta=Label(text='Ai introdus un numar gresit. Mai incearca!',
					   italic=True,
					   font_size=46,
					   color=(0,0.2,0.2,1))

		self.codPiesaNeidentificat=Label(text='Din pacate nu s-a identificat codul piesa in baza de date. Mai incearca!',
					   italic=True,
					   font_size=35,
					   color=(0,0.2,0.2,1))

		t1=""
		t2=""
		self.primulMeniu(t1, t2)


	def primulMeniu(self, t1, t2):

		self.padding=[400, 50, 400, 20]		
		self.clear_widgets()
		self.titlu=Label(text='Program identificare piese auto',
					   italic=True,
					   font_size=46,
					   color=(0,0.2,0.2,1))
		self.add_widget(self.titlu)

		self.informatii=Label(text='Pentru a cauta piesele disponibile va rugam introduceti urmatoarele detalii:',
					   font_size=30,
					   color=(1,0.2,0.2,0.8))
		self.add_widget(self.informatii)

		self.add_widget(Label(text='Marca autoturism:'))
		self.marcaWidget = TextInput(multiline=False, write_tab=False)
		self.add_widget(self.marcaWidget)

		self.add_widget(Label(text='Model autoturism:'))
		self.modelWidget = TextInput(multiline=False, write_tab=False)
		self.add_widget(self.modelWidget)

		self.add_widget(Label(text='Combustibil autoturism:'))
		self.combustibilWidget = TextInput(multiline=False, write_tab=False)
		self.add_widget(self.combustibilWidget)

		self.add_widget(Label(text='Capacitate cilindrica autoturism:'))
		self.capacitateWidget = TextInput(multiline=False, write_tab=False)
		self.add_widget(self.capacitateWidget)
		self.capacitateWidget.bind(on_text_validate=self.cautaDetalii)
		
		self.verificaDetalii = Button(text="Apasa pentru cautare")
		self.add_widget(self.verificaDetalii)
		self.verificaDetalii.bind(on_press=self.cautaDetalii)

		self.raport1B = Button(text="Raport total piese grupat dupa codPiesa")
		self.add_widget(self.raport1B)
		self.raport1B.bind(on_press=self.raport1)

		self.raport2B = Button(text="Raport total piese grupat dupa magazine")
		self.add_widget(self.raport2B)
		self.raport2B.bind(on_press=self.raport2)

		self.raport3B = Button(text="Raport piese rezervate")
		self.add_widget(self.raport3B)
		self.raport3B.bind(on_press=self.raport3)

		self.iesire = Button(text="Apasa pentru inchidere aplicatie")
		self.add_widget(self.iesire)
		self.iesire.bind(on_press=self.inchidere)

	def raport1(self, t):
		self.clear_widgets()
		self.raport1L=Label(text='Mai jos se pot vedea toate piesele grupate dupa codPiesa',
					   font_size=30,
					   color=(1,0.2,0.2,0.8))
		self.add_widget(self.raport1L)
		cursor.execute("CALL raport1();")

		text=""
		fmt = "{0:15} {1:30} {2:10}"
		text = text + fmt.format("codPiesa", "numePiesa", "CantitateTotala")
		text = text + "\n" + "-"*65 + "\n"
		
		for linie in cursor.fetchall():
			text = text + fmt.format(linie[0], linie[1], linie[2])
			text = text + '\n'
		self.add_widget(Label(text=text,
								markup=True,
								font_size=22,
								font_name='DroidSansMono'))

		self.inapoiLa1 = Button(text="Apasa pentru te intoarce la pagina initiala", size_hint=[1,0.3])
		self.add_widget(self.inapoiLa1)
		t1=""
		self.inapoiLa1.bind(on_press=partial(self.primulMeniu, t1))

		self.iesire = Button(text="Apasa pentru inchidere aplicatie", size_hint=[1,0.4])
		self.add_widget(self.iesire)
		self.iesire.bind(on_press=self.inchidere)

	def raport2(self, t):
		self.clear_widgets()

		
		self.raport2L=Label(text='Mai jos se pot vedea toate piesele grupate dupa magazine',
							font_size=30,
							color=(1,0.2,0.2,0.8))
		self.add_widget(self.raport2L)
		cursor.execute("CALL raport2();")

		text=""
		fmt = "{0:10} {1:20} {2:40} {3:15}"
		text = text + fmt.format("IDMagazin", "numeMagazin", "adresaMagazin", "totalPieseDinMagazin")
		text = text + "\n" + "-"*95 + "\n"
		
		for linie in cursor.fetchall():
			text = text + fmt.format(linie[0], linie[1], linie[2], linie[3])
			text = text + '\n'

		self.add_widget(Label(text=text,
								markup=True,
								font_size=22,
								font_name='DroidSansMono'))

		self.inapoiLa1 = Button(text="Apasa pentru te intoarce la pagina initiala", size_hint=[1,0.3])
		self.add_widget(self.inapoiLa1)
		t1=""
		self.inapoiLa1.bind(on_press=partial(self.primulMeniu, t1))

		self.iesire = Button(text="Apasa pentru inchidere aplicatie", size_hint=[1,0.4])
		self.add_widget(self.iesire)
		self.iesire.bind(on_press=self.inchidere)

	def raport3(self, t):
		self.clear_widgets()

		
		self.raport3L=Label(text='Mai jos se pot vedea toate piesele rezervate din magazine',
							font_size=30,
							color=(1,0.2,0.2,0.8))
		self.add_widget(self.raport3L)

		self.add_widget(Label(text=cosCumparaturi,
								markup=True,
								font_size=18,
								font_name='DroidSansMono'))

		self.inapoiLa1 = Button(text="Apasa pentru te intoarce la pagina initiala", size_hint=[1,0.3])
		self.add_widget(self.inapoiLa1)
		t1=""
		self.inapoiLa1.bind(on_press=partial(self.primulMeniu, t1))

		self.iesire = Button(text="Apasa pentru inchidere aplicatie", size_hint=[1,0.4])
		self.add_widget(self.iesire)
		self.iesire.bind(on_press=self.inchidere)




	def cautaDetalii(self, t):

		marcaText = self.marcaWidget.text
		modelText = self.modelWidget.text
		combustibilText = self.combustibilWidget.text
		capacitateText = self.capacitateWidget.text
		self.ok1 = 1

		if (marcaText == "" or modelText == "" or combustibilText == "" or capacitateText == ""):
			self.clear_widgets()
			self.add_widget(self.campNull)
			self.campNull.bind(on_touch_down=self.primulMeniu)
			self.ok1 = 0

		else:
			try:
				capacitateText = int(capacitateText)
			except ValueError:
				self.clear_widgets()
				self.add_widget(self.capacitateNumar)
				self.capacitateNumar.bind(on_touch_down=self.primulMeniu)
				self.ok1 = 0

		
		if self.ok1 == 1:
			cursor.execute("CALL coduriPiese('%s', '%s', '%s', %s);" % (marcaText, modelText, combustibilText, capacitateText))
			self.coduriPiese = cursor.fetchall()

			if not self.coduriPiese:
				self.clear_widgets()
				self.add_widget(self.autoturismNeidentificat)
				self.autoturismNeidentificat.bind(on_touch_down=self.primulMeniu)
			else:
				# Here we will make second menu
				self.infoMasina = 'Marca masina:'.ljust(29) + marcaText.upper() + '\nModel masina:'.ljust(30) + modelText.upper() \
							+ '\nCombustibil:'.ljust(30) + combustibilText.upper() + '\nCapcitate:'.ljust(30) + str(capacitateText) + ' cc\n'

				global IDMasinaCurenta
				
				cursor.execute("CALL daMiIDMasina('%s', '%s', '%s', %s);" % (marcaText, modelText, combustibilText, capacitateText))
				raspuns = cursor.fetchone()
				IDMasinaCurenta = raspuns[0]
				t1=""
				t2=""
				self.doileaMeniu(t1, t2)


	def doileaMeniu(self, t1, t2):
		self.clear_widgets()
		self.padding=[400, 0, 400, 20]
		self.titlu=Label(text='Masina identificata!',
					   italic=True,
					   font_size=40,
					   color=(1,0.2,0.2,0.8))
		self.add_widget(self.titlu)

		self.dateMasina=Label(text=self.infoMasina ,
					   italic=True,
					   font_size=27,
					   color=(0,0,0,1),
					   markup=True,
					   font_name='DroidSansMono')
		self.add_widget(self.dateMasina)

		textPiese = 'Codul motor al masinii:'.ljust(40) + self.coduriPiese[0][0] \
				+ '\nCodul filtrului de polen:'.ljust(40) + self.coduriPiese[0][1] \
				+ '\nCodul filtrului de combustibil:'.ljust(40) + self.coduriPiese[0][2] \
				+ '\nCodul filtrului de aer:'.ljust(40) + self.coduriPiese[0][3] \
				+ '\nCodul filtrului de ulei:'.ljust(40) + self.coduriPiese[0][4]

		self.testPieseLabel=Label(text=textPiese,
					   font_size=28,
					   color=(0,0.2,0.2,1),
					   markup=True,
					   font_name='DroidSansMono')
		self.add_widget(self.testPieseLabel)

		textPiese = """Pentru a cauta variantele pentru filtru de polen         introdu 1
Pentru a cauta variantele pentru filtru de combustibil   introdu 2
Pentru a cauta variantele pentru filtru de aer           introdu 3
Pentru a cauta variantele pentru filtru de ulei          introdu 4"""

		self.add_widget(Label(text=textPiese, font_size=20, markup=True, font_name='DroidSansMono'))
		
		self.varianteWidget = TextInput(multiline=False, write_tab=False, size_hint=[1,0.3])
		self.add_widget(self.varianteWidget)
		self.varianteWidget.bind(on_text_validate=self.cautaVariante)

		self.cautaVarianteW = Button(text="Apasa pentru a vedea variantele disponibile", size_hint=[1,0.3])
		self.add_widget(self.cautaVarianteW)
		self.cautaVarianteW.bind(on_press=self.cautaVariante)

		self.inapoiLa1 = Button(text="Apasa pentru a cauta alta masina", size_hint=[1,0.3])
		self.add_widget(self.inapoiLa1)
		t1=""
		self.inapoiLa1.bind(on_press=partial(self.primulMeniu, t1))

		self.iesire = Button(text="Apasa pentru inchidere aplicatie", size_hint=[1,0.4])
		self.add_widget(self.iesire)
		self.iesire.bind(on_press=self.inchidere)

	def cautaVariante(self, t):
		varianta = self.varianteWidget.text

		if varianta == '1' or varianta == '2' or varianta == '3' or varianta == '4':
			self.codPiesaAleasa = self.coduriPiese[0][int(varianta)]
			t1=""
			self.treileaMeniu(self, t1)
		else:
			self.clear_widgets()
			self.add_widget(self.variantaIncorecta)
			self.variantaIncorecta.bind(on_touch_down=self.doileaMeniu)

	def treileaMeniu(self, t1, t2):
		self.clear_widgets()
		# Now we have the self.cofPiesaAleasa which is a value from piese.codPiesa column.
		# We need to search in piese table and show all the alternatives

		cursor.execute("CALL varianteCodPiesa('%s');" % (self.codPiesaAleasa))
		self.variantePiese = cursor.fetchall()
		if not self.variantePiese:
			self.clear_widgets()
			self.add_widget(self.codPiesaNeidentificat)
			self.codPiesaNeidentificat.bind(on_touch_down=self.doileaMeniu)
		else:
			# Now we need to parse all the information for that codPiesaAleasa

			self.titlu=Label(text='Cod piesa identificat!\nMai jos se pot vedea variantele de piese care au acest cod',
						   italic=True,
						   halign='center',
						   font_size=40,
						   markup=True,
						   color=(1,0.2,0.2,0.8))
			self.add_widget(self.titlu)

			textVariante=""
			fmt = "{0:10} {1:10} {2:20} {3:10} {4:10} {5:15}"
			textVariante = textVariante + fmt.format("IDPiesa", "Producator", "NumePiesa", "CodPiesa", "PretPiesa", "CantitateTotala")
			textVariante = textVariante + "\n" + "-"*80 + "\n"
			
			for variante in self.variantePiese:
				textVariante = textVariante + fmt.format(variante[0], variante[1], variante[2], variante[3], str(variante[4]) + " lei", variante[5])
				textVariante = textVariante + '\n'

			self.add_widget(Label(text=textVariante,
									markup=True,
									font_size=22,
									font_name='DroidSansMono'))




			textPiese = """Pentru a vedea disponibilitatea pieselor in magazinele partenere introdu IDPiesa"""

			self.add_widget(Label(text=textPiese, font_size=20))
			
			self.disponiblitateWidget = TextInput(multiline=False, write_tab=False, size_hint=[1,0.3])
			self.add_widget(self.disponiblitateWidget)
			self.disponiblitateWidget.bind(on_text_validate=self.disponibilitate)

			self.cautaDisponibiltateW = Button(text="Apasa pentru a vedea disponibilitatea in magazine", size_hint=[1,0.3])
			self.add_widget(self.cautaDisponibiltateW)
			self.cautaDisponibiltateW.bind(on_press=self.disponibilitate)

			self.inapoiLa2 = Button(text="Apasa pentru a cauta alta piesa", size_hint=[1,0.3])
			self.add_widget(self.inapoiLa2)
			t1=""
			self.inapoiLa2.bind(on_press=partial(self.doileaMeniu, t1))

			self.raport3B = Button(text="Raport piese rezervate", size_hint=[1,0.4])
			self.add_widget(self.raport3B)
			self.raport3B.bind(on_press=self.raport3)

			self.iesire = Button(text="Apasa pentru inchidere aplicatie", size_hint=[1,0.4])
			self.add_widget(self.iesire)
			self.iesire.bind(on_press=self.inchidere)

	def disponibilitate(self, t):
		piesaAleasa = self.disponiblitateWidget.text
		self.ok2 = 1
		try:
			piesaAleasa = int(piesaAleasa)
		except ValueError:
			self.clear_widgets()
			self.add_widget(self.introduNumar)
			self.introduNumar.bind(on_touch_down=self.treileaMeniu)
			self.ok2 = 0

		if self.ok2 == 1:
			cursor.execute("CALL locatiePiesa('%s');" % (piesaAleasa))
			locatiiPiese = cursor.fetchall()

			if not locatiiPiese:
				self.clear_widgets()
				self.add_widget(self.piesaNeidentificata)
				self.piesaNeidentificata.bind(on_touch_down=self.treileaMeniu)
			else:
				# Here we will make the fourth menu
				self.locatiiParsat=""
				fmt = "{0:8} {1:8} {2:12} {3:20} {4:30}"
				self.locatiiParsat = self.locatiiParsat + fmt.format("IDStoc", "IDPiesa", "CantMagazin", "numeMagazin", "adresaMagazin")
				self.locatiiParsat = self.locatiiParsat + "\n" + "-"*95 + "\n"
				
				for locatii in locatiiPiese:
					self.locatiiParsat = self.locatiiParsat + fmt.format(locatii[0], locatii[1], locatii[2], locatii[3], locatii[4])
					self.locatiiParsat = self.locatiiParsat + '\n'
				
				t1=""
				t2=""
				self.patruleaMeniu(t1, t2)

	def patruleaMeniu(self, t1, t2):

		self.clear_widgets()

		self.titlu=Label(text='IDpiesa identificat!\nMai jos se poate vedea disponibilitatea in magazine pentru aceasta piesa',
					   italic=True,
					   halign='center',
					   font_size=35,
					   markup=True,
					   color=(1,0.2,0.2,0.8))
		self.add_widget(self.titlu)
		self.add_widget(Label(text=self.locatiiParsat,
								font_size=20,
								markup=True,
								font_name='DroidSansMono'))

		textPiese = "Introdu IDStoc pentru a rezerva piesa in magazin"

		self.add_widget(Label(text=textPiese, font_size=35, color=(1,0.2,0.2,0.8)))
		
		self.rezervaWidget = TextInput(multiline=False, write_tab=False, size_hint=[1,0.3])
		self.add_widget(self.rezervaWidget)
		self.rezervaWidget.bind(on_text_validate=self.rezervaMagazin)

		self.rezervaMagazinB = Button(text="Apasa pentru a rezerva in magazin", size_hint=[1,0.3])
		self.add_widget(self.rezervaMagazinB)
		self.rezervaMagazinB.bind(on_press=self.rezervaMagazin)

		self.inapoiLa3 = Button(text="Apasa pentru alege alta varianta de piesa", size_hint=[1,0.3])
		self.add_widget(self.inapoiLa3)
		t1=""
		self.inapoiLa3.bind(on_press=partial(self.treileaMeniu, t1))

		self.iesire = Button(text="Apasa pentru inchidere aplicatie", size_hint=[1,0.4])
		self.add_widget(self.iesire)
		self.iesire.bind(on_press=self.inchidere)

	def rezervaMagazin(self, t):
		
		stocAles = self.rezervaWidget.text
		self.ok3 = 1

		try:
			stocAles = int(stocAles)
		except ValueError:
			self.clear_widgets()
			self.add_widget(self.introduNumar)
			self.introduNumar.bind(on_touch_down=self.patruleaMeniu)
			self.ok3 = 0

		if self.ok3 == 1:
			cursor.execute("CALL cantitateDisponibila('%s');" % (stocAles))
			disponibil = cursor.fetchone()

			if not disponibil:
				self.clear_widgets()
				self.add_widget(self.stocNeidentificat)
				self.stocNeidentificat.bind(on_touch_down=self.patruleaMeniu)
			else:
				disponibil = int(disponibil[0])

				if disponibil == 0:
					self.clear_widgets()
					self.add_widget(self.stocZero)
					self.stocZero.bind(on_touch_down=self.patruleaMeniu)
				else:
					# We have to update that row
					cursor.execute("CALL updateStoc('%s');" % (stocAles))
					db.commit()

					# Aici trebuie sa adaugam in string ce am cumparat##################################
					fmt = "{0:7} {1:7} {2:9} {3:6} {4:8} {5:8} {6:20} {7:13} {8:20}"
					global cosCumparaturi
					cursor.execute("CALL ceACumparat(%s, '%s');" % (stocAles, IDMasinaCurenta))
					ceACumparat = cursor.fetchall()

					for entry in ceACumparat:
						cosCumparaturi += fmt.format(entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7], entry[8])
						cosCumparaturi += '\n'

					print cosCumparaturi


					self.clear_widgets()
					self.add_widget(self.rezervareCompleta)
					self.rezervareCompleta.bind(on_touch_down=self.treileaMeniu)

					self.continuare = Button(text="Apasa pentru continuare cumparaturi", size_hint=[1,0.4])
					self.add_widget(self.continuare)
					t1=""
					self.continuare.bind(on_press=partial(self.treileaMeniu, t1))

					self.iesire = Button(text="Apasa pentru inchidere aplicatie", size_hint=[1,0.4])
					self.add_widget(self.iesire)
					self.iesire.bind(on_press=self.inchidere)

	def inchidere(self, t):
		App.get_running_app().stop()


class Start(App):
	def build(self):
		root = Grafica()
		root.bind(size=self._update_rect, pos=self._update_rect)
		with root.canvas.before:
			Color(0.2, 0.2, 0.6, 1)  # blue;
			self.rect = Rectangle(size=root.size, pos=root.pos)
		return root

	def _update_rect(self, instance, value):

		self.rect.pos = instance.pos

		self.rect.size = instance.size


class main():
	def main(self):
		# Set the dimensions of the window
		Config.set('graphics', 'width', '1100')
		Config.set('graphics', 'height', '700')


		Start().run()

if __name__ == "__main__":

	main().main()
	# disconnect from server
	db.close()