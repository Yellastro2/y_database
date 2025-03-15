from typing import TypeVar, Generic, Type

from y_database.db_helper import DbHelper
from y_database.entitys import yEntity

T = TypeVar("T", bound="yEntity")


def get_entity(f_type: Type[T],
               f_id,
               f_db=DbHelper()) -> T:
  f_res = f_db.get_row_by_coll(f_type.__name__, "id", f_id)

  return f_type(**f_res)


def get_all(f_type: Type[T],
            f_db=DbHelper()) -> list[T]:
  f_res = f_db.get_table(f_type.__name__)
  f_all = []
  for q_it in f_res:
    f_all.append(f_type(**q_it))
  return f_all


def get_entity_by_coll(f_type: Type[T], f_coll, f_vall, f_db=DbHelper()) -> T:
  f_res = f_db.get_row_by_coll(f_type.__name__, f_coll, f_vall)
  if not f_res:
    return f_res
  return f_type(**f_res)


def get_entities_by_coll(f_type: Type[T], f_coll, f_vall, f_db=DbHelper()) -> list[T]:
  f_res = f_db.get_rows_by_coll(f_type.__name__, f_coll, f_vall)
  if not f_res:
    return f_res
  f_res_list = []
  for q_res in f_res:
    f_res_list.append(f_type(**q_res))
  return f_res_list


def remove_entity(f_entity: yEntity, f_db=DbHelper()) -> int:
  if f_entity.id == -1:
    print(f'make new entity of signal')
    return -1
  else:
    print(f'upd exist entity')
    f_db.delete_row(f_entity.__class__.__name__,
                    f_entity.id)

  return f_entity.id


def update_entity(f_entity: yEntity, f_db=DbHelper()) -> int:
  # Если айди -1 - сущность новая, функция добавить ее в базу и добавит новый айди в сущность
  if f_entity.id == -1:
    print(f'make new entity of {f_entity.__class__.__name__}')
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
