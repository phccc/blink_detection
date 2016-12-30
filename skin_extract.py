import numpy as np
import cv2

def gen_comb_non_skin_ratio(block1, block2):
	ratio1 = gen_non_skin_ratio(block1)
	ratio2 = gen_non_skin_ratio(block2)
	return ratio1 * ratio2

def gen_non_skin_ratio(block):
	total = (block.shape[1]*block.shape[0])*1.0
	non_skin_map = gen_skin_map(block)
	num_of_non_skin = np.sum(non_skin_map)
	print (num_of_non_skin, total)
	return num_of_non_skin / total

def gen_skin_map(block):
	block_YCrCb = cv2.cvtColor(block, cv2.COLOR_BGR2YCR_CB)
	block_Cr = block_YCrCb[:,:,1]
	block_Cb = block_YCrCb[:,:,2]

	skin_map = (block_Cb>=80) & (block_Cb<=120) & (block_Cr>=133) & (block_Cr<=173)
	return skin_map

def create_skin_image(block, skin_map):
	width = block.shape[1]
	height = block.shape[0]

	img = np.zeros((height, width), dtype=np.uint8)

	img[skin_map] = 255
	return img
