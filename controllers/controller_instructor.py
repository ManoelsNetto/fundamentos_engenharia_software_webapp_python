# Controlador de instrutores

# Imports
from flask import render_template, request, redirect, Blueprint
from classes.instructor import Instructor
from connectors import instructor_connector
from werkzeug.utils import secure_filename
import os, academia, psycopg2

# Definindo o objeto blueprint (componente da aplicação)
instructors_blueprint = Blueprint("instrutores", __name__)


# Características dos componentes
# Rota para a página index.html
@instructors_blueprint.route("/instrutores")  # criação de rota, que é igual a caminho da página de instrutores em
# templates.
def instructors_index():
    instructors = instructor_connector.get_all()
    return render_template("instrutores/index.html", instrutores=instructors, title="Instrutores")


# Rota para a página de cadastro de instrutor
@instructors_blueprint.route("/instrutores/novo")
def new_instructor():
    return render_template("instrutores/novo.html", title="Novo Instrutor")


# Método para envio dos dados de um novo instrutor via POST
@instructors_blueprint.route('/instrutores', methods=["POST"])
def create_instructor():

    name = request.form['name']
    surname = request.form['surname']
    birth_day = request.form['birth_day']
    phone = request.form['phone']
    address = request.form['address']
    img = request.files['img']
    img_name = ''

    instructor = Instructor(name, surname, birth_day, address, phone, img_name)
    instructor_connector.new(instructor)

    if img.filename != '':
        img_name = secure_filename('instructor_photo' + '_' + 'id' + '_' + instructor.ident.__str__())
        img.save(os.path.join(academia.app.config['UPLOAD_FOLDER'], img_name))

        instructor.img = img_name
        instructor_connector.edit(instructor)

    return redirect('/instrutores')


# Rota para a página de edição de um instrutor
@instructors_blueprint.route('/instrutores/<id>/edit')
def edit_instructor(id):
    instructor = instructor_connector.get_one(id)
    return render_template("instrutores/editar.html", instrutor=instructor, title="Editar Instrutor")


# Método para envio dos dados de alteração de um instrutor via POST
@instructors_blueprint.route('/instrutores/<id>', methods=["POST"])
def update_instructor(id):

    instructor = instructor_connector.get_one(id)

    name = request.form['name']
    surname = request.form['surname']
    birth_day = request.form['birth_day']
    phone = request.form['phone']
    address = request.form['address']
    img = request.files['img']

    if img.filename != '':
        img_name = secure_filename('instructor_photo' + '_' + 'id' + '_' + instructor.ident.__str__())
        img.save(os.path.join(academia.app.config['UPLOAD_FOLDER'], img_name))
    else:
        img_name = instructor.img

    try:
        updated_instructor = Instructor(name, surname, birth_day, address, phone, img_name, id)
        instructor_connector.edit(updated_instructor)
    except psycopg2.Error as e:
        error = "SQL Error: " + e
        instructor = instructor_connector.get_one(id)

        return render_template("instrutores/editar.html", instrutor=instructor, title="Editar Instrutor", error=error)

    return redirect("/instrutores")


# Rota para a página de visualização de instrutores
@instructors_blueprint.route('/instrutores/<id>')
def show_details(id):

    instructor_activities = instructor_connector.get_activities(id)
    instructor = instructor_connector.get_one(id)
    return render_template('instrutores/mostrar.html', instrutor=instructor, instrutor_atividades=instructor_activities,
                           title="Detalhes do Instrutor")


@instructors_blueprint.route('/instrutores/<id>/delete')
def delete_instructor(id):
    instructor_connector.delete_one(id)
    return redirect("/instrutores")
