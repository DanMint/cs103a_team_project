'''
gptwebapp shows how to create a web app which ask the user for a prompt
and then sends it to openai's GPT API to get a response. You can use this
as your own GPT interface and not have to go through openai's web pages.

We assume that the APIKEY has been put into the shell environment.
Run this server as follows:

On Mac
% pip3 install openai
% pip3 install flask
% export APIKEY="......."  # in bash
% python3 gptwebapp.py

On Windows:
% pip install openai
% pip install flask
% $env:APIKEY="....." # in powershell
% python gptwebapp.py
'''
from flask import request,redirect,url_for,Flask, render_template
from gpt import GPT
import openai
import os

app = Flask(__name__)
gptAPI = GPT(os.environ.get('APIKEY'))

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q789789uioujkkljkl...8z\n\xec]/'

@app.route('/')
def index():
    ''' display a link to the general query page '''
    print('processing / route')
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/index')
def index_page():
    return render_template("index.html")

@app.route('/gptdemo', methods=['GET', 'POST'])
def gptdemo():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.getResponse(prompt)
        return f'''
        <h1>GPT Demo</h1>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('gptdemo')}> make another query</a>
        '''
    else:
        return '''
        <h1>GPT Demo App</h1>
        Enter your query below
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''
    
@app.route('/ian', methods=['GET', 'POST'])
def ian():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        or_prompt = prompt
        prompt = "Translate the following into French; pay attention to proper grammar while doing so. Explain the grammar of the translated sentence. At the end, gloss the French words to English. \"" + prompt + "\""
        answer = gptAPI.getResponse(prompt)
        return render_template("ian.html", show_answer=True, prompt=prompt, answer=answer, or_prompt=or_prompt)
    else:
        return render_template("ian.html", show_answer=False)

    
@app.route('/veronika', methods=['GET', 'POST'])
def veronika():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        new_prompt = "Translate the following into Russian.\n Have a glossary of the Russian words to English at the end: \n" + prompt
        answer = gptAPI.getResponse(new_prompt)
        answer_split = answer.split("Glossary:")
        answer_split = answer_split[0] + "\n" + answer_split[1]
        return render_template("veronika.html", show_answer=True, prompt=prompt, answer=answer_split)
    else:
        return render_template("veronika.html", show_answer=False)
    
    
@app.route('/daniel', methods=['GET', 'POST'])
def daniel():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        or_prompt = prompt
        prompt = "Translate the following into Hebrew\"" + prompt + "\""
        answer = gptAPI.getResponse(prompt)
        return render_template("daniel.html", show_answer=True, prompt=prompt, answer=answer, or_prompt=or_prompt)
    else:
        return render_template("daniel.html", show_answer=False)


if __name__=='__main__':
    # run the code on port 5001, MacOS uses port 5000 for its own service :(
    app.run(debug=True,port=5001)
