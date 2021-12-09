import requests, shutil, os, base64, random, string, datetime, math
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', '--style', dest='style')
args = parser.parse_args()

style = args.style 
if style is None: style = 1

url = 'http://ec2-34-219-219-11.us-west-2.compute.amazonaws.com:443/'

headers = {
	"Accept": "*/*",
	"Accept-Encoding": 'gzip, deflate',
	"Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6",
	"Connection": "keep-alive",
	"Host": "ec2-54-214-184-243.us-west-2.compute.amazonaws.com:443",
	"Origin": "http://gaugan.org",
	"Referer": "http://gaugan.org/",
	'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
}

with open('./masked_edgemap.png', "rb") as m_e :
	masked_edgemap = 'data:image/png;base64,' + str(base64.b64encode(m_e.read()))[2:-1]
with open('./masked_image.png', 'rb') as m_i:
	masked_image = 'data:image/png;base64,' + str(base64.b64encode(m_i.read()))[2:-1]

for img in os.listdir('./in/'):
	if(not img.endswith('.png')): continue
	
	print(f'Processing image \'{img}\'')

	# get b64 encoded image
	with open('./in/' + img, "rb") as f:
		imgb64 = 'data:image/png;base64,' + str(base64.b64encode(f.read()))[2:-1]

	# generate name for requests
	now = datetime.datetime.now()
	date = '{}. {}. {}.'.format(now.year, now.month, now.day)
	milli = math.ceil(now.timestamp() * 1000)
	key = ''.join(random.choices(string.digits, k=9))
	name = '{},{}-{}'.format(date, milli, key)


	# send map img to server
	payload = {
		'name': name,
		'masked_segmap': imgb64,
		'masked_edgemap': masked_edgemap,
		'masked_image': masked_image,
		'style_name': style,
		'caption': '',
		'enable_seg': 'true',
		'enable_edge': 'false',
		'enable_caption': 'false',
		'enable_image': 'false',
		'use_model2': 'false',
	}

	response = requests.post(url + 'gaugan2_infer', data = payload, headers=headers)

	payload = {
		'name': (None, name),
	}
	r = requests.post(url + 'gaugan2_receive_output', files = payload, stream = True, headers = headers)
	r.raw.decode_content = True

	# write image to out folder
	with open('out/' + img.split('.')[0] + '.jpg', 'wb') as f:
		shutil.copyfileobj(r.raw, f)