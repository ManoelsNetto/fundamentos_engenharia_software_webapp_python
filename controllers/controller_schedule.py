# Controlador de agendamentos

from flask import render_template, redirect, Blueprint, request
from connectors import member_connector, schedule_connector, activity_connector, plan_connector
from classes.schedule import Schedule

# Definindo o objeto blueprint (componente da aplicação)
schedule_blueprint = Blueprint('agendamentos', __name__)


# Rota para a página index.html
@schedule_blueprint.route("/agendamentos")
def schedule_index():

    schedules = schedule_connector.get_all()
    return render_template('agendamentos/index.html', agendamentos=schedules, title='Agendamentos')


# Rota para novo agendamento a partir da visão do membro
@schedule_blueprint.route('/agendamentos/novo/membro/<id>')
def new_member_schedule(id):

    member = member_connector.get_one(id)
    activities = activity_connector.get_all_active()  # Apenas atividade ativas
    return render_template('agendamentos/novo_membro.html', membro=member, atividades=activities,
                           title='Novo agendamento')


# Rota para novo agendamento a partir da visão da atividade
@schedule_blueprint.route('/agendamentos/novo/atividade/<id>')
def new_activity_schedule(id):

    activity = activity_connector.get_one(id)
    members = member_connector.get_all_active()  # Apenas membros ativos
    return render_template('agendamentos/nova_atividade.html', atividade=activity, membros=members,
                           title='Novo Agendamento')


# Rota para criar agendamento a partir de membro
@schedule_blueprint.route('/agendamentos/membro', methods=['POST'])
def create_member_schedule():
    activity_id = request.form['activity']
    member_id = request.form['member']

    activity = activity_connector.get_one(activity_id)
    member = member_connector.get_one(member_id)

    member_plan = plan_connector.get_one(member.plan_type.ident)
    activity_plan = plan_connector.get_one(activity.plan_type.ident)

    current_schedules = len(activity_connector.get_members(activity_id))
    activities_active = activity_connector.get_all_active()

    if schedule_connector.check_schedule(activity_id, member_id):
        error = 'Não foi possível realizar esta ação: o membro já está cadastrado nessa atividade.'
        return render_template('agendamentos/novo_membro.html', atividades=activities_active,
                               membro=member, title='Novo agendamento', error=error)
    elif member_plan.ident != activity_plan.ident:
        error = f'Não foi possível realizar esta ação: o plano do membro deve ser {activity_plan.plan.lower()}.'
        return render_template('agendamentos/novo_membro.html', atividades=activities_active,
                               membro=member, title='Novo agendamento', error=error)
    elif current_schedules >= activity.capacity:
        error = 'Não foi possível realizar esta ação: a atividade já está lotada.'
        return render_template('agendamentos/novo_membro.html', atividades=activities_active,
                               membro=member, title='Novo agendamento', error=error)
    else:
        new_schedule = Schedule(activity_id, member_id)
        schedule_connector.new(new_schedule)
        return redirect('/membros/' + member_id)  # Redirecionará o usuário para a página de detalhes do membro.


# Rota para criar agendamento a partir da atividade
@schedule_blueprint.route('/agendamentos/atividade', methods=['POST'])
def create_activity_schedule():
    activity_id = request.form['activity']
    member_id = request.form['member']

    activity = activity_connector.get_one(activity_id)
    member = member_connector.get_one(member_id)

    member_plan = plan_connector.get_one(member.plan_type.ident)
    activity_plan = plan_connector.get_one(activity.plan_type.ident)

    current_schedules = len(activity_connector.get_members(activity_id))
    members_active = member_connector.get_all_active()

    if schedule_connector.check_schedule(activity_id, member_id):
        error = 'Não foi possível realizar essa ação: o membro já está cadastrado nessa atividade.'
        return render_template('agendamentos/nova_atividade.html', atividade=activity,
                               membros=members_active, title='Novo agendamento', error=error)
    elif member_plan.ident != activity_plan.ident:
        error = f'Não foi possível realizar essa ação: o plano do membro deve ser {activity_plan.plan.lower()}.'
        return render_template('agendamentos/nova_atividade.html', atividade=activity,
                               membros=members_active, title='Novo agendamento', error=error)
    elif current_schedules >= activity.capacity:
        error = 'Não foi possível realizar essa ação: a atividade já está lotada.'
        return render_template('agendamentos/nova_atividade.html', atividade=activity,
                               membros=members_active, title='Novo agendamento', error=error)
    else:
        new_schedule = Schedule(activity_id, member_id)
        schedule_connector.new(new_schedule)
        return redirect('/atividades/' + activity_id)  # Redirecionará o usuário para a página de detalhes da atividade.


# Rota para deletar agendamento
@schedule_blueprint.route('/agendamentos/<id>/delete')
def delete_schedule(id):
    schedule_connector.delete_one(id)
    return redirect('/agendamentos')


# Rota para deletar agendamento da visão do membro
@schedule_blueprint.route('/agendamentos/delete/membro/<member_id>/<activity_id>')
def delete_schedule_member(member_id, activity_id):
    schedule_connector.delete_schedule(member_id, activity_id)
    return redirect('/membros/' + member_id)


# Rota para deletar agendamento da visão da atividade
@schedule_blueprint.route('/agendamentos/delete/atividade/<member_id>/<activity_id>')
def delete_schedule_activity(member_id, activity_id):
    schedule_connector.delete_schedule(member_id, activity_id)
    return redirect('/atividades/' + activity_id)

