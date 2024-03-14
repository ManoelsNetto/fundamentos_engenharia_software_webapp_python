# Módulo de conexão entre a classe e o banco de dados
from classes.run_sql import run_sql
from classes.member import Member
from classes.activity import Activity
from connectors import plan_connector


# Função para retornar a lista de todos os membros
def get_all():

    members = list()
    sql = 'SELECT * FROM webuser.tb_members ' \
          'ORDER BY name ASC;'
    results = run_sql(sql)

    for row in results:
        plan_type = plan_connector.get_one(row['plan_type'])
        member = Member(row['name'],
                        row['surname'],
                        row['birth_day'],
                        row['address'],
                        row['phone'],
                        row['email'],
                        plan_type,
                        row['start_date'],
                        row['enabled'],
                        row['img'],
                        row['ident'])
        members.append(member)

    return members


# Função para obter um membro
def get_one(id):

    member = None
    sql = 'SELECT * FROM webuser.tb_members ' \
          'WHERE ident = %s;'
    value = [id]
    result = run_sql(sql, value)

    if result is not None:
        for row in result:
            plan_type = plan_connector.get_one(row['plan_type'])
            member = Member(row['name'],
                            row['surname'],
                            row['birth_day'],
                            row['address'],
                            row['phone'],
                            row['email'],
                            plan_type,
                            row['start_date'],
                            row['enabled'],
                            row['img'],
                            row['ident'])

    return member


# Função para obter a lista de atividades de um membro
def get_activities(member_id):

    activities = list()
    sql = 'SELECT TB_ACTIVITIES.* FROM webuser.TB_ACTIVITIES INNER JOIN webuser.TB_SCHEDULE ' \
          'ON TB_SCHEDULE.activity = TB_ACTIVITIES.ident ' \
          'WHERE member = %s ' \
          'ORDER BY date;'
    value = [member_id]
    results = run_sql(sql, value)

    for row in results:

        plan_type = plan_connector.get_one(row['plan_type'])
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


# Função para retornar todos os membros ativos ordenados por nome
def get_all_active():

    members = list()
    sql = "SELECT * FROM webuser.TB_MEMBERS " \
          "WHERE enabled = TRUE " \
          "ORDER BY name;"
    results = run_sql(sql)

    for row in results:
        plan_type = plan_connector.get_one(row['plan_type'])
        member = Member(row['name'],
                        row['surname'],
                        row['birth_day'],
                        row['address'],
                        row['phone'],
                        row['email'],
                        plan_type,
                        row['start_date'],
                        row['enabled'],
                        row['img'],
                        row['ident'])
        members.append(member)

    return members


# Função para retornar todos os membros inativos ordenados por nome
def get_all_inactive():

    members = list()
    sql = "SELECT * FROM webuser.TB_MEMBERS " \
          "WHERE enabled = FALSE " \
          "ORDER BY name;"
    results = run_sql(sql)

    for row in results:
        plan_type = plan_connector.get_one(row['plan_type'])
        member = Member(row['name'],
                        row['surname'],
                        row['birth_day'],
                        row['address'],
                        row['phone'],
                        row['email'],
                        plan_type,
                        row['start_date'],
                        row['enabled'],
                        row['img'],
                        row['ident'])
        members.append(member)

    return members


# Função para cadastrar um novo membro
def new(member):

    sql = 'INSERT INTO webuser.TB_MEMBERS ' \
          '(name, surname, birth_day, address, phone, email, plan_type, start_date, enabled, img) ' \
          'VALUES ' \
          '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ' \
          'RETURNING *;'
    values = [member.name,
              member.surname,
              member.birth_day,
              member.address,
              member.phone,
              member.email,
              member.plan_type.ident,
              member.start_date,
              member.enabled,
              member.img]

    result = run_sql(sql, values)

    member.ident = result[0][0]

    return member


# Função para deletar um membro
def delete_one(id):

    sql = 'DELETE FROM webuser.TB_MEMBERS ' \
          'WHERE ident = %s;'
    value = [id]

    run_sql(sql, value)


# Função parar atualizar um membro
def edit(member):

    sql = "UPDATE webuser.TB_MEMBERS " \
          "SET (name, surname, birth_day, address, phone, email, plan_type, start_date, enabled, img) = " \
          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) " \
          "WHERE ident = %s;"
    values = [member.name,
              member.surname,
              member.birth_day,
              member.address,
              member.phone,
              member.email,
              member.plan_type.ident,
              member.start_date,
              member.enabled,
              member.img,
              member.ident]

    run_sql(sql, values)
