from OCR_APP.interface import my_ocr
import sys, json

try:
	result = my_ocr(sys.argv[1])
except:
	result = my_ocr('ocr_app/test_imgs/addr2.png')
print(result)
with open('static/tmp/result.txt', 'w', encoding='utf-8') as f:
	f.write(json.dumps(result))