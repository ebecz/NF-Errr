#!/usr/bin/python3
import tkinter as tk
from tkinter import *
import locale
from nfe import download_json, download_png_path as nfe
from datetime import datetime
from scan_webcam import scan_bar_code
import pyperclip

def set_text(entry, text):
	entry.delete(0,END)
	entry.insert(0,text)
	return

def processar_nfe():
	chave = chave_tk_entry.get()
	print("NF-E: %s" % chave)

	data = download_json(chave)
	if data is None:
		return

	serie=data["Dados da NF-e"]["Série"]
	numero=data["Dados da NF-e"]["Número"]

	dataEmissao=datetime.strptime(data["Dados da NF-e"]["Data de Emissão"], '%d/%m/%Y %H:%M:%S-%U:00')

	locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
	valor=locale.atof(data["Dados da NF-e"]["Valor Total da Nota Fiscal"])

	set_text(serie_tk_entry, serie)
	set_text(numero_tk_entry, str(numero))
	set_text(data_tk_entry, dataEmissao.strftime("%d/%m/%Y"))
	set_text(valor_tk_entry, str(valor))

def scanear_code():
	chave = scan_bar_code()
	set_text(chave_tk_entry, chave)
	processar_nfe()

def copiar_serie():
	pyperclip.copy(serie_tk_entry.get())

def copiar_numero():
	pyperclip.copy(numero_tk_entry.get())

def copiar_valor():
	pyperclip.copy(int(float(valor_tk_entry.get())*100))

def copiar_data():
	text_date=data_tk_entry.get();
	dataEmissao=datetime.strptime(text_date, '%d/%m/%Y')
	pyperclip.copy(dataEmissao.strftime("%d%m%Y"))

master = tk.Tk()

tk.Label(master, text="Chave NF-E:").grid(row=0)

chave_tk_entry = tk.Entry(master, width = 44)
chave_tk_entry.grid(row=0, column=1)

web_cam_photo = PhotoImage(file = "icon_web_camera.png") 
web_cam_photo = web_cam_photo.subsample(5)

#, heigh = 50, width = 50,
tk.Button(master, 
          text='Scanear Web Cam', image = web_cam_photo,
          command=scanear_code).grid(row=0,
                                    column=2)
tk.Button(master, 
          text='Processar', 
          command=processar_nfe).grid(row=1,
                                    column=1)

tk.Label(master, text="Serie:").grid(row=2)
serie_tk_entry = tk.Entry(master)
serie_tk_entry.grid(row=2, column=1)
tk.Button(master, text="copiar", command=copiar_serie).grid(row=2, column=2);

tk.Label(master, text="Número:").grid(row=3)
numero_tk_entry = tk.Entry(master)
numero_tk_entry.grid(row=3, column=1)
tk.Button(master, text="copiar", command=copiar_numero).grid(row=3, column=2);

tk.Label(master, text="Data da Emissão:").grid(row=4)
data_tk_entry = tk.Entry(master)
data_tk_entry.grid(row=4, column=1)
tk.Button(master, text="copiar", command=copiar_data).grid(row=4, column=2);

tk.Label(master, text="Valor Total da Nota:").grid(row=5)
valor_tk_entry = tk.Entry(master)
valor_tk_entry.grid(row=5, column=1)
tk.Button(master, text="copiar", command=copiar_valor).grid(row=5, column=2);

tk.mainloop()
