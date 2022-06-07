from flask.helpers import url_for
from app import app
import os
from flask import render_template, request, redirect, jsonify, make_response
from datetime import datetime

import spacy
import os
import pathlib
import ocr
import score
import shutil

date = datetime.utcnow()
my_html = "<h1>This is some HTML</h1>"
suspicious = "<script>alert('NEVER TRUST USER INPUT!')</script>"

users = {
    "mitsuhiko": {
        "name": "Armin Ronacher",
        "bio": "Creator of of the Flask framework",
        "twitter_handle": "@mitsuhiko"
    },
    "gvanrossum": {
        "name": "Guido Van Rossum",
        "bio": "Creator of the Python programming language",
        "twitter_handle": "@gvanrossum"
    },
    "elonmusk": {
        "name": "Elon Musk",
        "bio": "technology entrepreneur, investor, and engineer",
        "twitter_handle": "@elonmusk"
    }
}



@app.route("/jinja")
def jinja():

    # Strings
    my_name = "MPC"

    # Integers
    my_age = 21

    # Lists
    langs = ["Python", "JavaScript", "Bash", "Ruby", "C", "Rust"]

    # Dictionaries
    friends = {
        "Tony": 43,
        "Cody": 28,
        "Amy": 26,
        "Clarissa": 23,
        "Wendell": 39
    }

    # Tuples
    colors = ("Red", "Blue")

    # Booleans
    cool = True

    # Classes
    class GitRemote:
        def __init__(self, name, description, domain):
            self.name = name
            self.description = description 
            self.domain = domain

        def pull(self):
            return f"Pulling repo '{self.name}'"

        def clone(self, repo):
            return f"Cloning into {repo}"

    my_remote = GitRemote(
        name="Learning Flask",
        description="Learn the Flask web framework for Python",
        domain="https://github.com/Julian-Nash/learning-flask.git"
    )

    # Functions
    def repeat(x, qty=1):
        return x * qty

    return render_template(
        "public/jinja.html", my_name=my_name, my_age=my_age, langs=langs,
        friends=friends, colors=colors, cool=cool, GitRemote=GitRemote, 
        my_remote=my_remote, repeat=repeat,my_html=my_html
    )















@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        req = request.form
        username = req.get('username')
        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Missing fields for {', '.join(missing)}"
            return render_template("public/sign_up.html", feedback=feedback)

        return redirect(url_for('profile', username=username))

    return render_template("public/sign_up.html")



@app.route("/profile/<username>")
def profile():

    args = request.args
    print(args)
    if "username" in args:
        username = args["foo"]
    return render_template("public/profile.html", username=username)



@app.route("/json", methods=["POST"])
def json_example():

    if request.is_json:

        req = request.get_json()

        response_body = {
            "message": "JSON received!",
            "sender": req.get("name")
        }

        res = make_response(jsonify(response_body), 200)

        return res

    else:

        return make_response(jsonify({"message": "Request body must be JSON"}), 400)



@app.route("/guestbook")
def guestbook():
    return render_template("public/guestbook.html")


@app.route("/guestbook/create-entry", methods=["POST"])
def create_entry():

    req = request.get_json()

    print(req)

    res = make_response(jsonify(req), 200)

    return res


@app.route("/query")
def query():

    print(app.config)

    return "No query string received", 200



app.config["IMAGE_UPLOADS"] = "C:/College/BE_Project/Project/spacy3/uploads/pdf"

def resume_score():

    for filename in os.listdir("C:/College/BE_Project/Project/spacy3/uploads/pdf"):
        with open(os.path.join("C:/College/BE_Project/Project/spacy3/uploads/pdf/", filename), 'r') as f:
            path = os.path.join("C:/College/BE_Project/Project/spacy3/uploads/pdf/", filename)
            ocr.pdf_to_text(path)

    nlp_ner = spacy.load("C:/College/BE_Project/Project/spacy3/model-best/")

    text_list = os.listdir("C:/College/BE_Project/Project/spacy3/uploads/text/")
    text_path = "C:/College/BE_Project/Project/spacy3/uploads/text/"
    text = ''
    try:
        if len(text_list) != 0:
            for filename in text_list :
                with open(text_path + filename, 'r') as f:
                    resume_text = f.readlines()
                    text = text.join(resume_text)
                    doc = nlp_ner(text)
                                
                    output = doc.to_json()
                    entities = {'NAME': [], 'SKILL': [], 'EMAIL': [], 'CONTACT': [], 'POSITION': [], 'LOCATION': [], 'EDUCATION': [], 'ORG': [], 'COLLEGE': []}
                    for ent in doc.ents:
                        entities[ent.label_].append(ent.text)
                    
                    with open('final_scores.txt', 'a') as f:
                        final = score.score(entities)
                        f.write('Score for ' + filename + ' is ' + str(final))
                        f.write('\n')
    except Exception as e:
        print(e)

@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            print("Image saved")
            
            resume_score()

            return redirect(request.url)
        else:
            print('H')

    return render_template("public/upload_image.html")