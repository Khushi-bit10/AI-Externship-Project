from flask import Flask, render_template, request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import requests

app = Flask(__name__, template_folder="templates")
model = load_model('nutrition.h5')
print("Loaded model from disk")


@ app.route('/')
def home():
    return render_template('home.html')


@ app.route('/image', methods=['GET', 'POST'])
def image():
    return render_template("image.html")


@ app.route('/predict', methods=['GET', 'POST'])
def lanuch():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname('__file__')
        filepath = os.path.join(basepath, "uploads", f.filename)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(64, 64))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        pred = np.argmax(model.predict(x), axis=1)
        print("prediction", pred)
        index = ['APPLE', 'BANANA', 'ORANGE', 'PINEAPPLE', 'WATERMELON']

        result = str(index[pred[0]])
        print(result)
        x = result
        result = nutrition(result)
        print(result)

        return render_template("empty.html", showcase=(result), showcase1=(x))


def nutrition(index):
    import requests
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = {"query": index}
    response = requests.get(
        api_url + query, headers={'0gR+jLs5Z6Fii4sGu8eCTA==OC0RSXE6rmJhHxHb'})

    if response.status_code == requests.codes.ok:
        print(response.text)
        return response.json()["items"]
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":

    app.run(debug=True)
