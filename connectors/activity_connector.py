# Módulo de conexão entre a classe e o banco de dados.
from classes.run_sql import run_sql
from classes.activity import Activity
from classes.member import Member
import connectors.plan_connector as plan


# Função para listar todas as atividades.
def get_all():

    activities = []
    sql = 'SELECT * FROM webuser.TB_ACTIVITIES ' \
          'ORDER BY ident ASC;'
    results = run_sql(sql)

    for row in results:

        plan_type = plan.get_one(row['ident'])
        activity = Activity(row['name'],
                            row['instructor'],
                            row['date'],
                            row['time_length'],
                            row['capacity'],
                            plan_type,
                            row['enabled'],
                            row['ident'])
        activities.append(activity)

    return activities


# Função para obter membros de atividades agendadas.
def get_members(activity_id):

    members = []

    sql = 'SELECT tb_members.* FROM webuser.tb_members ' \
          'INNER JOIN webuser.tb_schedule ' \
          'ON tb_members.ident = tb_schedule.member ' \
          'WHERE tb_schedule.activity = %s;'

    value = [activity_id]
    results = run_sql(sql, value)

    for row in results:

        member = Member(row['name'],
                        row['surname'],
                        row['birth_day'],
                        row['address'],
                        row['phone'],
                        row['email'],
                        row['plan_type'],
                        row['start_date'],
                        row['enabled'],
                        row['img'],
                        row['ident'])
        members.append(member)

    return results


# Função para obter atividades ativas ordenadas por data.
def get_all_active():

    activities = []

    sql = 'SELECT * FROM webuser.TB_ACTIVITIES ' \
          'WHERE enabled = TRUE ' \
          'ORDER BY date ASC;'
    results = run_sql(sql)

    for row in results:

        plan_type = plan.get_one(row['plan_type'])
        activity = Activity(row['name'],
                            row['instructor'],
                            row['date'],
                            row['time_length'],
                            row['capacity'],
                            plan_type,
                            row['enabled'],
                            row['ident'])
        activities.append(activity)

    return activities


# Função para obter atividades inativas.
def get_all_inactive():

    activities = []

    sql = 'SELECT * FROM webuser.TB_ACTIVITIES ' \
          'WHERE enabled = FALSE;'
    results = run_sql(sql)

    for row in results:

        plan_type = plan.get_one(row['plan_type'])
        activity = Activity(row['name'],
                            row['instructor'],
                            row['date'],
                            row['time_length'],
                            row['capacity'],
                            plan_type,
                            row['enabled'],
                            row['ident'])
        activities.append(activity)

    return activities


# Função para obter uma atividade.
def get_one(activity_id):

    activity = None
    sql = 'SELECT * FROM webuser.TB_ACTIVITIES ' \
          'WHERE ident = %s;'
    value = [activity_id]
    result = run_sql(sql, value)

    if result is not None:
        for row in result:

            plan_type = plan.get_one(row['plan_type'])
            activity = Activity(row['name'],
                                row['instructor'],
                                row['date'],
                                row['time_length'],
                                row['capacity'],
                                plan_type,
                                row['enabled'],
                                row['ident'])

    return activity


# Função para cadastrar nova atividade.
def new(activity):

    sql = 'INSERT INTO webuser.TB_ACTIVITIES(name, instructor, date, time_length, capacity, plan_type, enabled) ' \
          'VALUES ' \
          '(%s, %s, %s, %s, %s, %s, %s) RETURNING *;'

    values = [activity.name,
              activity.instructor,
              activity.date,
              activity.time_length,
              activity.capacity,
              activity.plan_type,
              activity.enabled]

    result = run_sql(sql, values)
    activity.ident = result[0][0]

    return activity


# Função para deletar uma atividade.
def delete_one(id):

    sql = 'DELETE FROM webuser.tb_activities ' \
          'WHERE ident = %s;'
    value = [id]

    run_sql(sql, value)


# Função para editar uma atividade.
def edit(activity):

    sql = 'UPDATE webuser.tb_activities ' \
          'SET (name, instructor, date, time_length, capacity, plan_type, enabled) = (%s, %s, %s, %s, %s, %s, %s) ' \
          'WHERE ident = %s;'
    value = [activity.name,
             activity.instructor,
             activity.date,
             activity.time_length,
             activity.capacity,
             activity.plan_type,
             activity.enabled,
             activity.ident]

    run_sql(sql, value)
