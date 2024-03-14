# Controlador de Membros

# Imports
from flask import request, redirect, render_template, Blueprint
from classes.member import Member
from connectors import member_connector, plan_connector
import psycopg2, os, academia
from werkzeug.utils import secure_filename

# Definindo o objeto blueprint (componente da aplicação)
members_blueprint = Blueprint("membros", __name__)


# Rota para index.html para buscar membros ativos
@members_blueprint.route("/membros")
def members_index():
    members = member_connector.get_all_active()
    return render_template("membros/index.html", membros=members, title='Membros')


# Rota para index.html para buscar membros inativos
@members_blueprint.route("/membros/inativo")
def members_inactives():
    members = member_connector.get_all_inactive()
    return render_template("membros/index.html", membros=members, title='Membros')


# Rota para a página de novo membro.
@members_blueprint.route("/membros/novo")
def new_member():
    plan_types = plan_connector.get_all()
    return render_template("membros/novo.html", tipos_planos=plan_types, title='Novo Membro')


# Rota para fazer o POST de criação.
@members_blueprint.route("/membros", methods=["POST"])
def create_member():

    name = request.form['name']
    surname = request.form['surname']
    birth_day = request.form['birth_day']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    plan_type = plan_connector.get_one(request.form['plan_type'])
    start_date = request.form['start_date']
    enabled = request.form['enabled']
    img = request.files['img']
    img_name = ''

    member = Member(name, surname, birth_day, address, phone, email, plan_type, start_date, enabled, img_name)
    member = member_connector.new(member)

    if img.filename != '':
        img_name = secure_filename('member_photo' + '_' + 'id' + '_' + member.ident.__str__())
        img.save(os.path.join(academia.app.config['UPLOAD_FOLDER'], img_name))

        member.img = img_name
        member_connector.edit(member)

    return redirect("/membros")


# Rota para edição
@members_blueprint.route('/membros/<id>/edit')
def edit_member(id):
    member = member_connector.get_one(id)
    plan_types = plan_connector.get_all()
    return render_template("membros/editar.html", membro=member, tipos_planos=plan_types,
                           title='Editar detalhes do membro')


# Rota para o POST da edição
@members_blueprint.route('/membro/<id>', methods=["POST"])
def update_member(id):

    member = member_connector.get_one(id)

    name = request.form['name']
    surname = request.form['surname']
    birth_day = request.form['birth_day']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    plan_type = plan_connector.get_one(request.form['plan_type'])
    start_date = request.form['start_date']
    enabled = request.form['enabled']
    img = request.files['img']

    if img.filename != '':
        img_name = secure_filename('member_photo' + '_' + 'id' + '_' + member.ident.__str__())
        img.save(os.path.join(academia.app.config['UPLOAD_FOLDER'], img_name))
    else:
        img_name = member.img

    try:
        updated_member = Member(name, surname, birth_day, address, phone, email, plan_type, start_date, enabled,
                                img_name, id)
        member_connector.edit(updated_member)
    except psycopg2.Error as e:
        error = "SQL Error: " + e
        member = member_connector.get_one(id)
        plan_types = plan_connector.get_all()
        return render_template("membros/editar.html", membro=member, tipos_planos=plan_types,
                               title='Editar detalhes do membro', error=error)

    return redirect("/membros")


# Rota para mostrar detalhes
@members_blueprint.route("/membros/<id>")
def show_details(id):
    member = member_connector.get_one(id)
    scheduled_activities = member_connector.get_activities(id)
    plan_type = plan_connector.get_one(member.plan_type.ident)

    return render_template('membros/mostrar.html', membro=member, plan_type=plan_type,
                           atividades_agendadas=scheduled_activities)


# Rota para deletar
@members_blueprint.route('/membros/<id>/delete')
def delete_member(id):
    member_connector.delete_one(id)

    return redirect("/membros")





