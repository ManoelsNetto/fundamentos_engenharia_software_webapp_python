# Módulo para conexão entre a classe e o banco de dados.
from classes.run_sql import run_sql
from classes.schedule import Schedule


# Função para consultar agendamentos.
def get_all():

    schedules = list()
    sql = 'SELECT * FROM webuser.TB_SCHEDULE;'
    results = run_sql(sql)

    for row in results:
        schedule = Schedule(row['activity'],
                            row['member'],
                            row['ident'])
        schedules.append(schedule)

    return schedules


# Função para retornar um agendamento com base em um ID.
def get_one(id):

    schedule = None
    sql = 'SELECT * FROM webuser.TB_SCHEDULE ' \
          'WHERE ident = %s;'
    value = [id]
    result = run_sql(sql, value)

    if result is not None:
        for row in result:
            schedule = Schedule(row['activity'],
                                row['member'],
                                row['ident'])

    return schedule


# Função para criar novo agendamento.
def new(schedule):

    sql = 'INSERT INTO webuser.TB_SCHEDULE(activity, member) ' \
          'VALUES (%s, %s) ' \
          'RETURNING *;'
    values = [schedule.activity, schedule.member]
    result = run_sql(sql, values)

    schedule.ident = result[0]['ident']

    return schedule


# Função para deletar um agendamento com base no ID.
def delete_one(id):

    sql = 'DELETE FROM webuser.TB_SCHEDULE ' \
          'WHERE ident = %s;'
    value = [id]

    run_sql(sql, value)


# Função para verificar se um agendamento existe.
def check_schedule(activity_id, member_id):

    sql = 'SELECT * FROM webuser.TB_SCHEDULE ' \
          'WHERE activity = %s AND member = %s;'
    values = [activity_id, member_id]
    results = run_sql(sql, values)

    if not results:
        return False
    else:
        return True


# Função para deletar um agendamento com base no ID e no membro.
def delete_schedule(member_id, activity_id):

    sql = 'DELETE FROM webuser.TB_SCHEDULE ' \
          'WHERE member = %s AND activity = %s;'
    values = [member_id, activity_id]

    run_sql(sql, values)
