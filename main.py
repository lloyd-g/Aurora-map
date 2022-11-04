
import urllib.request
import json
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
#from matplotlib import cm
#from matplotlib.ticker import LinearLocator
#import numpy as np
from flask import Flask
from flask import send_file
#from PIL import Image, ImageFont, ImageDraw, ImageColor
#import io
def buildimage():
  # Let's then open the data we got (it acts like a file) and get the data
  url = 'https://services.swpc.noaa.gov/json/ovation_aurora_latest.json'
  req = urllib.request.urlopen(url).read().decode()
  # The we can load the json recived from the call
  data = json.loads(req)
  # Print the data to view it
  #"Observation Time": "2022-06-08T08:01:00Z", "Forecast Time": "2022-06-08T09:22:00Z", "Data Format": "[Longitude, Latitude, Aurora]", "coordinates":
  print(data['Observation Time'])
  print(data['Forecast Time'])
  print(data['Data Format'])
  #print(data['coordinates'])
  fig = plt.figure()
  fig.set_figheight(6)
  fig.set_figwidth(10)
  #ax = fig.add_subplot(111, projection='3d')
  ax = fig.add_subplot(111)
  x =[]
  y =[]
  z =[]
  for points in data['coordinates']: 
    #print(points)
    x.append(points[0])
    y.append(points[1])
    filt = points[2] if points[2] > 2 else 0
    z.append(filt)
  print(max(z)) 
  print(min(z))
  #from wiki
  im = plt.imread('World_Distribution_Map.jpeg')
  #implot = plt.imshow(im)
  ax.imshow(im, extent=[-180, 180, -90, 90])
  ax.imshow(im, extent=[180, 540, -90, 90])
  ax.scatter(x, y, z, marker='o',cmap='hot',c=z)
  ax.azim = 90
  ax.dist = 10
  ax.elev = 80
  ax.roll = 30
  ax.set_xlabel('Longitude')
  ax.set_ylabel('Latitude')
  ax.set_title('Aurora at '+data['Forecast Time'])
  plt.xlim( [ 0, 360 ] )          # Plot from x=0 to x=80.
  plt.ylim( [ -90, 90 ] )         # Plot from y=0 to y=250.
  plt.xticks( range(0,360,10) )   # Put x axis ticks every 10 units.
  plt.yticks( range(-90,90,10) )  # Y ticks every 50.  You can provide any list.
  plt.xticks(rotation = 90) # Rotates X-Axis Ticks by 90-degrees
  fig.savefig('temp.png', dpi=fig.dpi)
  #plt.show()

buildimage()
app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)


@app.route('/')
def serve_img():
  #img = Image.new('RGB', (60, 30), color = 'red')
  #img.save('pil_red.png')
  #print(img.format)
  #return serve_pil_image(img) 
  return send_file( 'temp.png', mimetype='image/png')
if __name__ == "__main__": 

  app.run(host='0.0.0.0',port=9000)