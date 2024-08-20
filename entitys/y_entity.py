

class yEntity:

  id: int = -1


  def __init__(self,params):
    f_fields = self.list_attributes()
    i = 0
    for q_field in f_fields:
      if len(params) > i:
        self.__dict__[q_field] = params[i]
      else:
        print(f'{self.__name__} init without enougth params')
      i += 1



  def get_data(self) -> dict:
    f_data = self.__dict__
    f_data.pop('id')
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
