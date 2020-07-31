from OCR_APP.interface import my_ocr
img_path = 'ocr_app/AdvancedEast/demo/front_01_gray.png'
result = my_ocr(img_path)
for i in result.values():
	print(i)