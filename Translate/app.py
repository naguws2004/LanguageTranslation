from flask import Flask, render_template, request
import deepl

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def translate(source_text, source_lang, target_lang):
  translator = deepl.Translator(auth_key="380c8d16-91c0-460e-8d68-cb19a189ea00:fx")
  result = translator.translate_text(text=source_text, source_lang=source_lang, target_lang=target_lang)
  return result.text

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
          <title>Language Translator</title>
        </head>
        <body>
          <h1>Language Translator</h1>
          <form action="/translate_page" method="POST">
            Enter Text to Translate: <br>
            <textarea name="source_text" rows="5" cols="80"></textarea><br><br>
            Source Language: <br>
            <select name="source_lang">
              <option value="en">English</option>
              <option value="fr">French</option>
              <option value="es">Spanish</option>
            </select><br><br>
            Target Language: <br>
            <select name="target_lang">
              <option value="en-US">English</option>
              <option value="fr">French</option>
              <option value="es">Spanish</option>
            </select><br><br>
            <button type="submit">Translate</button>
          </form>
        </body>
        </html>
    '''

@app.route('/translate_page', methods=['POST'])
def translate_page():
    source_text = request.form['source_text']
    source_lang = request.form['source_lang']
    target_lang = request.form['target_lang']
    translated_text = translate(source_text, source_lang, target_lang)
    return render_template('translate.html', translated_text=translated_text)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
