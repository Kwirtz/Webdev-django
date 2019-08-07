from django.shortcuts import render
from django.conf import settings
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse, JsonResponse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import math
from io import BytesIO
import base64
from django.contrib.auth.decorators import login_required

# Create your views here.

#import tensorflow as tf
#from keras.models import load_model

#graph = tf.get_default_graph()
#modelwhite = load_model('C:/Users/kevin/OneDrive/Bureau/Sentdex/WebDev/mysite/dcgan/checkpoint/gen_model_125_w.h5')
#modelwhite._make_predict_function()
#modelblack = load_model('C:/Users/kevin/OneDrive/Bureau/Sentdex/WebDev/mysite/dcgan/checkpoint/gen_model_1_b.h5')
#modelblack._make_predict_function()
#MODEL = model

modelwhite = settings.MODELWHITE
modelblack = settings.MODELBLACK

@login_required(login_url='/login')
def index(request):
    return render(request, 'dcgan/form.html')


@login_required(login_url='/login')
def generate(request):
    if request.method == 'POST':
        num_images = int(request.POST.get('textfield', None))
        noise = np.random.normal(0, 1,size=(num_images,) + (1, 1, 100))
        background = request.POST.get('background',None)
        if background == "white":
            generated_images = modelwhite.predict(noise) 
        else:
            generated_images = modelblack.predict(noise) 
        fig = plt.figure(figsize = (5,5))
        dim = math.ceil(math.sqrt(num_images))
                
        for i in range(num_images):
            ax = plt.subplot(dim,dim,i+1)
            image = generated_images[i, :, :, :]
            image += 1
            image *= 127.5
            im = ax.imshow(image.astype(np.uint8))
            plt.axis('off')
                    
        plt.tight_layout()


        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        return render(request, 'dcgan/generate.html',{'graphic':graphic})
    else:
        return render(request, 'dcgan/form.html')




