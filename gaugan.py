import requests, re, shutil, os, base64, random, string
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', '--style', dest='style')
args = parser.parse_args()

style = args.style

def getUrl():
	print('Getting new server address...')
	r = requests.get('http://34.216.122.111/gaugan/demo.js')
	urls = re.findall(r'\'(http.*?://.*?/)\'', re.search(r'urls=.*?;', r.text)[0])
	return urls[0]

url = getUrl()

for img in os.listdir('./in/'):
	print(f'Processing image \'{img}\'')

	# get b64 encoded image
	with open('./in/' + img, "rb") as f:
		imgb64 = 'data:image/png;base64,' + str(base64.b64encode(f.read()))[2:-1]

	# generate name for requests
	name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


	while True:
		try:
			# send map img to server
			POSTdata = {
				'imageBase64': imgb64,
				'name': name
			}

			requests.post(url + 'nvidia_gaugan_submit_map', data = POSTdata)

			# get generated img from server
			POSTdata = {
				'name': name,
				'style_name': str(style)
			}
			r = requests.post(url + 'nvidia_gaugan_receive_image', data = POSTdata, stream = True)
			break
		except:
			url = getUrl() # if there is an error getting the image, get a new server URL and try again

	r.raw.decode_content = True

	# write image to out folder
	with open('out/' + img.split('.')[0] + '.jpg','wb') as f:
		shutil.copyfileobj(r.raw, f)