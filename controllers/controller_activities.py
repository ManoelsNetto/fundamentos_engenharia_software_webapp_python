# Controlador de Atividades

from flask import render_template, redirect, request, Blueprint
from connectors import activity_connector, instructor_connector, plan_connector
from classes.activity import Activity

# Definindo o objeto blueprint (componente da aplicação)
activities_blueprint = Blueprint('atividades', __name__)


# Rota para index.html com atividades ativas
@activities_blueprint.route('/atividades')
def activities_index():

    activities = activity_connector.get_all_active()
    return render_template('atividades/index.html', atividades=activities, title='Atividades')


# Rota para index.html com atividades inativas
@activities_blueprint.route('/atividades/inativas')
def inactive_activities():

    activities = activity_connector.get_all_inactive()
    return render_template('atividades/index.html', atividades=activities, title='Atividades Inativas')


# Rota para nova atividade
@activities_blueprint.route('/atividades/novo')
def new_activity():

    instructors = instructor_connector.get_all()
    plan_types = plan_connector.get_all()
    return render_template('atividades/novo.html', instrutores=instructors,
                           tipos_planos=plan_types, title='Nova Atividade')


# Rota para cadastro
@activities_blueprint.route('/atividades', methods=['POST'])
def create_activity():

    name = request.form['name']
    instructor = request.form['instructor']
    date = request.form['date']
    time_length = request.form['time_length']
    capacity = request.form['capacity']
    plan_type = request.form['plan_type']
    enabled = request.form['enabled']

    activity = Activity(name, instructor, date, time_length, capacity, plan_type, enabled)
    activity_connector.new(activity)
    return redirect('/atividades')


# Rota para renderização da página de edição
@activities_blueprint.route('/atividade/<id>/edit')
def edit_activity(id):

    activity = activity_connector.get_one(id)
    instructors = instructor_connector.get_all()
    plan_types = plan_connector.get_all()
    return render_template('atividades/editar.html', atividade=activity,
                           instrutores=instructors, tipos_planos=plan_types,
                           title='Editar Atividade')


# Rota para dá post da edição
@activities_blueprint.route('/atividades/<id>', methods=['POST'])
def update_activity(id):

    name = request.form['name']
    instructor = request.form['instructor']
    date = request.form['date']
    time_length = request.form['time_length']
    capacity = request.form['capacity']
    plan_type = request.form['plan_type']
    enabled = request.form['enabled']

    updated_activity = Activity(name, instructor, date, time_length, capacity, plan_type, enabled, id)
    activity_connector.edit(updated_activity)
    return redirect('/atividades')


# Rota para mostrar detalhes
@activities_blueprint.route('/atividades/<id>')
def show_details(id):

    activity = activity_connector.get_one(id)
    instructor = instructor_connector.get_one(activity.instructor)
    plan_type = plan_connector.get_one(activity.plan_type.ident)
    activity_members = activity_connector.get_members(id)
    no_members_booked = len(activity_members)

    return render_template('atividades/mostrar.html', atividade=activity,
                           instrutor=instructor, title='Detalhes da atividade',
                           tipo_plano=plan_type, membros_atividades=activity_members,
                           no_members_booked=no_members_booked)


# Rota para apagar atividade
@activities_blueprint.route('/atividades/<id>/delete')
def delete_activity(id):

    activity_connector.delete_one(id)
    return redirect('/atividades')
