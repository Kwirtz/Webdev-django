<h1>Web developement with django</h1>

<p>Advanced example of different applications like GAN/Chatbot/Dash implemented in django.</p>
<p>Here is some ressources I used to build this repository:<br>
- https://pythonprogramming.net/django-web-development-python-tutorial/<br>
- https://www.youtube.com/watch?v=-RbkNcDwKbc<br>
- https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/ <br>
- https://community.plot.ly/t/django-and-dash-eads-method/7717/2 (for the dashboard)<br>
 </p>

<h2>Pre-requisite</h2>

<p>You will need redis-server to run the chatbot. You can download it there: https://redis.io/ <br></p>

<p>Install requirements either with the yml file (conda environment) or the requirements.txt </p>

```
pip install -r requirements.txt
```

<p>Install tinymce</p>

```
python -m pip install django-tinymce4-lite
```

<p>You will also need to create your own keys in mysite/dashboard/Tweets.py (line 14-17) to create the database required for the dashboard. You can follow this tutorial to create your keys https://www.youtube.com/watch?v=pUUxmvvl2FE (note that I followed this tutorial a long time ago and things might have change from the UI shown in the video). Once this is done run this next cmd line until you think you have enough data.</p>

```
python Tweets.py
```

<p>Once all of this is done, run the redis-server (if you have redis on your path you can just run redis-server from a terminal).<br>
Go to mysite/ and run</p>

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
<p> Go to http://127.0.0.1:8000/ and have fun ! </p>


<h2>Overall</h2>

<p>The bone of the website. Mainly created by following the tutorial of Sentdex(see on top of the README). I might use this website in the future to do tutorials in machine learning hence the tutorial stuff.</p>
<img src="https://raw.githubusercontent.com/Kwirtz/Webdev-django/master/demogif/overall.gif" width="800" height="400" />

<h2>Dashboard (sentiment analysis)</h2>
<p>Sentiment analysis on e-sport games. For the moment the number of game is limited (if you want to add games you'll need to add some things in mysite/dashboard/Tweets.py and mysite/dashboard/dashapp.py). <br>
I only use the vaderSentiment module provided in python but it is not the best solution since I use some french data (e.g sentiment is all wrong). I intend to move on to BERT at some point. </p>
<img src="https://raw.githubusercontent.com/Kwirtz/Webdev-django/master/demogif/dashboard.gif" width="800" height="400" />

<h2>GAN</h2>
<p>Basic implementation of a DCGAN on pokemons. I will soon release the repository for the gan with additionnal ressources on how to implement it in Keras. I intend to improve the model by using ProGAN or styleGAN.</p>
<img src="https://raw.githubusercontent.com/Kwirtz/Webdev-django/master/demogif/gan.gif" width="800" height="400" />

<h2>Chatbot</h2>
<p>Implementation of a chatbot using the transformer model on reddit data. As the GAN, I will soon release the repository for it. I still need to work on hyperparameters (you can see the limitation of the chatbot in the demo below). </p>
<img src="https://raw.githubusercontent.com/Kwirtz/Webdev-django/master/demogif/chatbot.gif" width="800" height="400" />