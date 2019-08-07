from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.conf import settings
import json
import random
import numpy as np
import re
import tensorflow as tf

modelchatbot = settings.MODELCHATBOT
tokenizer = settings.TOKENIZER
START_TOKEN = settings.START_TOKEN
END_TOKEN = settings.END_TOKEN
MAX_LENGTH = settings.MAX_LENGTH

def index(request):
    return render(request, 'chatbot/index.html', {})

def room(request, room_name):
    return render(request, 'chatbot/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def respond_to_websockets(message):
    
    if '!arxiv' in message:
        result_message = "http://www.arxiv-sanity.com/"
    
    elif '!music' in message:
    	result_message = "https://www.youtube.com/watch?v=BN1WwnEDWAM"

    else:
        temp_message = str(message)
        result_message = predict(temp_message)

    return result_message


def preprocess_sentence(sentence):
  sentence = sentence.lower().strip()
  # creating a space between a word and the punctuation following it
  # eg: "he is a boy." => "he is a boy ."
  sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
  sentence = re.sub(r'[" "]+', " ", sentence)
  # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
  sentence = re.sub(r"[^a-zA-Z?.!,]+", " ", sentence)
  sentence = sentence.strip()
  # adding a start and an end token to the sentence
  return sentence


def evaluate(sentence):
  sentence = preprocess_sentence(sentence)

  sentence = tf.expand_dims(
      START_TOKEN + tokenizer.encode(sentence) + END_TOKEN, axis=0)

  output = tf.expand_dims(START_TOKEN, 0)

  for i in range(MAX_LENGTH):
    predictions = modelchatbot(inputs=[sentence, output], training=False)

    # select the last word from the seq_len dimension
    predictions = predictions[:, -1:, :]
    predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

    # return the result if the predicted_id is equal to the end token
    if tf.equal(predicted_id, END_TOKEN[0]):
      break

    # concatenated the predicted_id to the output which is given to the decoder
    # as its input.
    output = tf.concat([output, predicted_id], axis=-1)

  return tf.squeeze(output, axis=0)


def predict(sentence):
  prediction = evaluate(sentence)

  predicted_sentence = tokenizer.decode(
      [i for i in prediction if i < tokenizer.vocab_size])

  print('Input: {}'.format(sentence))
  print('Output: {}'.format(predicted_sentence))

  return predicted_sentence