import json
import logging
import traceback


class yEntity:
  id: int = -1

  def __init__(self,params):
    params = list(params)
    f_fields = self.list_attributes()
    f_anotated = self.__annotations__
    i = 0
    for q_field in f_fields:
      if len(params) > i:
        if q_field in f_anotated.keys() and f_anotated[q_field] == float and isinstance(params[i],str):
          try:
            params[i] = float(params[i])
          except:
            e = traceback.format_exc()
            logging.error('ERROR on parse float from string in yEntity')
        if q_field in f_anotated.keys() and f_anotated[q_field] in [list,dict,tuple] and isinstance(params[i],str):
          try:
            params[i] = json.loads(params[i])
          except:
            e = traceback.format_exc()
            logging.error('ERROR on parse json from string in yEntity')
        self.__dict__[q_field] = params[i]
      else:
        logging.warning(f'{self.__class__.__name__} init without enougth params')
        break
      i += 1

  def get_data(self) -> dict:
    f_data = self.__dict__.copy()
    f_data.pop('id')

    for q_d in f_data.keys():
      if isinstance(f_data[q_d],float):
        f_data[q_d] = str(f_data[q_d])

      if isinstance(f_data[q_d],list) or isinstance(f_data[q_d],dict) or isinstance(f_data[q_d],tuple):
        f_data[q_d] = json.dumps(f_data[q_d])

    return f_data

  def list_attributes(self):
    # Получаем все атрибуты, которые уже имеют значения
    attrs_with_values = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    # Получаем все аннотированные атрибуты
    annotations = list(self.__annotations__.keys()) if hasattr(self, '__annotations__') else []

    # Используем словарь для объединения списков без дубликатов, сохраняя порядок
    all_attrs_ordered = {}
    for attr in attrs_with_values + annotations:
      all_attrs_ordered[attr] = None

    return list(all_attrs_ordered.keys())
