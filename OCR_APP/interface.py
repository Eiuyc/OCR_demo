import numpy as np
from PIL import Image
import cv2
import os
import sys
app_dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(app_dir_path)
sys.path.append(app_dir_path + '/advancedeast')
from AdvancedEAST.predict import predict as adeast_predict
from AdvancedEAST.network import East
east = East()
east_detect = east.east_network()
from AdvancedEAST.cfg import train_task_id
east_detect.load_weights(app_dir_path + f'/AdvancedEast/saved_model/east_model_weights_{train_task_id}.h5')
sys.path.append(app_dir_path + '/crnn_ctc')
from ocr.model import predict as ocr_predict

def adjusted(img_path):
	# 灰度
	raw = cv2.imread(img_path, 0)
	ret, mask = cv2.threshold(raw, 127, 255, cv2.THRESH_BINARY)
	# 获取黑色像素坐标
	coords = np.column_stack(np.where(mask == 0))
	# 计算旋转角度
	angle = cv2.minAreaRect(coords)[-1]
	if angle < -45:
		angle = -(90+ angle)
	else:
		angle = -angle
	h, w = mask.shape[:2]
	center = (w//2, h//2)
	# 获取旋转矩阵
	M = cv2.getRotationMatrix2D(center, angle, 1.0)
	# 旋转
	rotated = cv2.warpAffine(cv2.imread(img_path), M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

	cv2.imwrite(img_path + '_adjusted.jpg', rotated)
	return img_path + '_adjusted.jpg'

def my_ocr(img_path):
	img_path = adjusted(img_path)
	recs_ = adeast_predict(east_detect, img_path, 0.9)
	recs = list(map(lambda x: [x[0],x[1],x[6],x[7],x[2],x[3],x[4],x[5]], recs_))

	raw = cv2.imread(img_path)
	cuts = []
	for i in recs:
		cols = (int(i[0]), int(i[2]), int(i[4]), int(i[6]))
		rows = (int(i[1]), int(i[3]), int(i[5]), int(i[7]))
		cuts.append(raw[min(rows):max(rows), min(cols):max(cols)])

	cnt = 0
	result = {}
	if not os.path.exists(app_dir_path + '/tmp'):
		os.mkdir(app_dir_path + '/tmp')
	for i, img in enumerate(cuts):
		img = Image.fromarray(img).convert('L')
		txt = ocr_predict(img)
		result[i] = txt
		img.save(f'{app_dir_path}/tmp/{i}.png')

	return result

