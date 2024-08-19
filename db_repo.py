from y_database.db_helper import DbHelper
from y_database.entitys import yEntity


def get_entity(f_id,f_type,f_db = DbHelper()) -> yEntity:
  f_res = f_db.get_row_by_coll(f_type.__name__, "id", f_id)

  return f_type(f_res)


def get_entity_by_coll(f_type,f_coll,f_vall, f_db=DbHelper()) -> yEntity:
  f_res = f_db.get_row_by_coll(f_type.__name__, f_coll, f_vall)
  if not f_res:
    return f_res
  return f_type(f_res)


def update_entity(f_entity: yEntity,f_db = DbHelper()):
  # Если айди -1 - сущность новая, функция добавить ее в базу и добавит новый айди в сущность
  if f_entity.id == -1:
    print(f'make new entity of signal')
    f_new_id = f_db.add_row(f_entity.__class__.__name__,
                 f_entity.get_data())
    f_entity.id = f_new_id
  else:
    print(f'upd exist entity')
    f_db.upd_row_by_coll(f_entity.__class__.__name__,
                         'id',
                         f_entity.id,
                         f_entity.get_data())
    f_new_id = f_entity.id

  return f_new_id