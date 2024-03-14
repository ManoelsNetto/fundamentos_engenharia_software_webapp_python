# Web App

from flask import Flask, render_template
from controllers.controller_member import members_blueprint
from controllers.controller_schedule import schedule_blueprint
from controllers.controller_instructor import instructors_blueprint
from controllers.controller_activities import activities_blueprint

# App
app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Registro dos blueprints (componentes da aplicação)
app.register_blueprint(members_blueprint)
app.register_blueprint(schedule_blueprint)
app.register_blueprint(instructors_blueprint)
app.register_blueprint(activities_blueprint)


# Rota para a página de entrada da aplicação
@app.route('/')
def home():
    return render_template('index.html', title='Home')


# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)
