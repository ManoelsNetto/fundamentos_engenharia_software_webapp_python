# Módulo de conexão entre a classe e banco de dados

from classes.plan import PlanType
from classes.run_sql import run_sql


# Função para obter todos os planos
def get_all():

    plan_types = []

    sql = "SELECT * FROM webuser.TB_PLANS;"
    results = run_sql(sql)

    for row in results:
        plan_type = PlanType(row['plan'], row['ident'])
        plan_types.append(plan_type)

    return plan_types


# Função para obter um plano
def get_one(id):

    plan_type = None
    sql = "SELECT * FROM webuser.TB_PLANS " \
          "WHERE ident = %s;"
    value = [id]
    result = run_sql(sql, value)

    if result is not None:
        for row in result:
            plan_type = PlanType(row["plan"], row["ident"])

    return plan_type


# Função para criar um tipo de plano
def new(plan_type):

    sql = "INSERT INTO webuser.TB_PLANS(plan) " \
          "VALUES (%s) " \
          "RETURNING *;"
    value = [plan_type.plan]
    result = run_sql(sql, value)
    plan_type.id = result[0]["ident"]

    return plan_type


# Função para deletar um plano
def delete_one(id):

    sql = "DELETE FROM webuser.TB_PLANS " \
          "WHERE ident = %s;"
    value = [id]

    run_sql(sql, value)


# Função para alterar um plano
def edit(plan_type):

    sql = "UPDATE webuser.TB_PLANS SET(plan) = (%s)" \
          "WHERE ident = %s;"
    value = [plan_type.plan, plan_type.ident]

    run_sql(sql, value)

