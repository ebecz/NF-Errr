#!/usr/bin/python3
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import time
from nfe import validar_chave

def barcodeReader(image, bgr):
	gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	barcodes = decode(gray_img)

	for decodedObject in barcodes:
		print("bar code")
		points = decodedObject.polygon

		pts = np.array(points, np.int32)
		pts = pts.reshape((-1, 1, 2))
		cv2.polylines(image, [pts], True, (0, 255, 0), 3)

	for bc in barcodes:
		print("Barcode: {} - Type: {}".format(bc.data.decode("utf-8"), bc.type))
		if validar_chave(bc.data.decode("utf-8")):
			return bc.data.decode("utf-8")
		cv2.putText(image, bc.data.decode("utf-8") + " - " + bc.type, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, bgr, 2)
	return None

def scan_bar_code():
	bgr = (8, 70, 208)
	cap = cv2.VideoCapture(0)
	while (True):
		ret, frame = cap.read()
		barcode = barcodeReader(frame, bgr)
		cv2.imshow('Barcode reader', frame)
		code = cv2.waitKey(10)
		if code == ord('q'):
			return None
		if not barcode is None:
			cap.release()
			cv2.destroyAllWindows()
			return barcode
