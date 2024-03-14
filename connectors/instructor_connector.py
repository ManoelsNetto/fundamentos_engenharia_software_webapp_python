# Módulo de conexão entre a classe e o banco de dados.
from classes.run_sql import run_sql
from classes.instructor import Instructor
from classes.activity import Activity


# Função para listar todos os instrutores
def get_all():

    instructors = list()

    sql = "SELECT * FROM webuser.TB_INSTRUCTORS " \
          "ORDER BY ident ASC;"
    results = run_sql(sql)

    for row in results:
        instructor = Instructor(row['name'],
                                row['surname'],
                                row['birth_day'],
                                row['address'],
                                row['phone'],
                                row['img'],
                                row['ident'])

        instructors.append(instructor)

    return instructors


# Função para retornar um instrutor
def get_one(id):

    sql = "SELECT * FROM webuser.TB_INSTRUCTORS " \
          "WHERE ident = %s;"
    value = [id]
    instructor = run_sql(sql, value)

    if instructor is not None:
        for row in instructor:
            instructor = Instructor(row['name'],
                                    row['surname'],
                                    row['birth_day'],
                                    row['address'],
                                    row['phone'],
                                    row['img'],
                                    row['ident'])

    return instructor


# Função para listar todas as atividade de um instrutor
def get_activities(instuctor_id):

    activities = []
    sql = "SELECT * FROM webuser.TB_ACTIVITIES " \
          "WHERE instructor = %s;"
    value = [instuctor_id]
    results = run_sql(sql, value)

    for row in results:
        activity = Activity(row['name'],
                            row['instructor'],
                            row['date'],
                            row['time_length'],
                            row['capacity'],
                            row['plan_type'],
                            row['enabled'],
                            row['ident'])

        activities.append(activity)

    return activities


# Função para cadastrar um instrutor
def new(instructor):

    sql = "INSERT INTO webuser.TB_INSTRUCTORS(name, surname, birth_day, address, phone, img) " \
          "VALUES (%s, %s, %s, %s, %s, %s) " \
          "RETURNING *;"
    values = [instructor.name, instructor.surname, instructor.birth_day, instructor.address, instructor.phone,
              instructor.img]
    result = run_sql(sql, values)

    instructor.ident = result[0][0]

    return instructor


# Função para deletar um instrutor
def delete_one(id):

    sql = "DELETE FROM webuser.TB_INSTRUCTORS " \
          "WHERE ident = %s;"
    values = [id]

    run_sql(sql, values)


# Função para editar um instrutor
def edit(instructor):

    sql = "UPDATE webuser.TB_INSTRUCTORS " \
          "SET(name, surname, birth_day, address, phone, img) = (%s, %s, %s, %s, %s, %s) " \
          "WHERE ident = %s;"
    values = [instructor.name, instructor.surname, instructor.birth_day, instructor.address, instructor.phone,
              instructor.img, instructor.ident]

    run_sql(sql, values)

