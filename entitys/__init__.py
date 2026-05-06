from y_database.entitys.y_entity import yEntity
from y_database.entitys.y_conf import yConfig


class yConf(yEntity):
  """Обратная совместимость со старым именем конфигурационной entity."""

  type: str
  value: str
