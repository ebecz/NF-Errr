#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time
import json

def nfe_read(driver):
	nfe_dict = {}
	for fieldset in driver.find_elements_by_tag_name("fieldset"):
		try:
			legend = fieldset.find_element_by_tag_name("legend")
			table = fieldset.find_element_by_tag_name("table")
			tbody = table.find_element_by_tag_name("tbody")
			section = legend.get_attribute('textContent').strip()
			section_dict = {}
			for tr in tbody.find_elements_by_tag_name("tr"):
				for td in tr.find_elements_by_tag_name("td"):
					try:
						label = td.find_element_by_tag_name("label")
						span = td.find_element_by_tag_name("span")
						attribute = label.get_attribute('textContent').strip()
						value = span.get_attribute('textContent').strip()
						section_dict[attribute] = value
					except BaseException as Argument:
						continue;
			if len(section_dict) > 0:
				nfe_dict[section] = section_dict
		except BaseException as Argument:
			continue;
		
	return nfe_dict

def nfe_print_png(driver, filename):
	driver.find_element_by_id("ctl00_ContentPlaceHolder1_hplImprimirAba").click()
	driver.switch_to_window(driver.window_handles[1])
	driver.get_screenshot_as_file(filename)


def nfe_navigate(driver, chave):
	driver.get("http://www.nfe.fazenda.gov.br/portaL/consultaRecaptcha.aspx")
	driver.find_element_by_link_text("Serviços").click()
	driver.find_element_by_link_text("Consultar NF-e Completa").click()
	txtChave=driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtChaveAcessoCompleta')
	txtChave.send_keys(chave)
	try:
		element = WebDriverWait(driver, 120).until(
			EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_btnVoltar"))
		)
		print("Detected NF-E screen, waiting it to load")
		time.sleep(1)
	except:
		print("Timeout on NF-E captcha screen")

def validar_chave(chave):
	n = 2;
	soma = 0
	digitos =  list(chave);
	if len(digitos) != 44:
		print("Comprimento inválido (%s)" % len(digitos))
		return False;

	for i in digitos[0:43]:
		soma = soma + int(i) * (n + 2)
		n = (n + 7) % 8

	resto = (soma % 11)
	if resto == 0 or resto == 1:
		dv = 0
	else:
		dv = 11 - resto

	if (dv == int(digitos[-1])):
		return True
	else:
		print("Digito de verificação inválido %s != %s" % (dv, int(digitos[-1])))
		return False

def decode_chave(chave):
	if not validar_chave(chave):
		print("Chave invalida")
		return None;

	self = {}
	self["UF"] = chave[0:2]
	self["YY"] = chave[2:4]
	self["MM"] = chave[4:6]
	self["cnpj"] = chave[6:20]
	self["model"] = chave[20:22]
	self["serie"] = chave[22:25]
	self["numero"] = chave[25:34]
	self["emissao"] = chave[35]
	self["codigo"] = chave[35:43];
	self["dv"] = chave[43];
	return self

def nfe_download_json(driver, filename):
	data = nfe_read(driver)
	print(data["Dados da NF-e"]["Série"])
	print(data["Dados da NF-e"]["Número"])
	print(data["Dados da NF-e"]["Data de Emissão"])
	print(data["Dados da NF-e"]["Valor Total da Nota Fiscal"])
	print("Saving it")
	with open(filename, 'w') as f:
		json.dump(data, f)

def cache_path(chave, ext):
	chave_fields = decode_chave(chave)
	if chave_fields is None:
		return False

	return "cache/%s/%s/%s.%s" % (chave_fields["YY"], chave_fields["MM"], chave, ext)


def nfe_download_to_cache(chave):

	chave_fields = decode_chave(chave)
	if chave_fields is None:
		return False

	newpath = "cache/%s/%s" % (chave_fields["YY"], chave_fields["MM"])
	if not os.path.exists(newpath):
	    os.makedirs(newpath)

	if os.path.isfile(cache_path(chave, "json")) and os.path.isfile(cache_path(chave, "png")):
		print("%s hit cache" % chave)
		return True

	print("Starting selenium with Firefox")
	driver = webdriver.Firefox()

	nfe_navigate(driver, chave)

	print("Downloading values")
	nfe_download_json(driver, cache_path(chave, "json"))

	print("Saving SnapShot")
	nfe_print_png(driver, cache_path(chave, "png"))

	print("Finishing section")
	driver.quit()

	return True

def download_json(chave):
	if not nfe_download_to_cache(chave):
		return None

	with open(cache_path(chave, "json"), 'r') as f:
		return json.load(f)

def download_png_path(chave):
	if nfe_download_to_cache(chave):
		return False
	return cache_path(chave, "png")

