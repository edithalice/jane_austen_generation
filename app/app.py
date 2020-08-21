import os
from flask import Flask, request, render_template, escape
import text_generator as tg
import sys



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def homepage():
        return render_template('austen.html')

    @app.route("/get_nouns")
    def get_ppns():
        output_str, ppns = tg.get_ppns()
        ppn_keys = ' '.join([ppn[0] for ppn in ppns])
        return render_template('ask_for_ppns.html', ppns=ppns,
                                ppn_keys=ppn_keys, output_str = output_str)


    @app.route("/print_text", methods=('GET', 'POST'))
    def final_string():
        user_defined_nouns = request.args.items()
        output_str = request.form["GeneratedText"]
        ppn_keys = request.form["PPNKeys"]
        user_given_ppns = []
        for key in ppn_keys.split():
            key = key.strip('[]\',')
            user_given_ppns.append((key, request.form[key]))
        output_str = tg.replace_ppn_keys(output_str, user_given_ppns)
        output_str = escape(output_str)
        return render_template('results.html', output_str=output_str)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
