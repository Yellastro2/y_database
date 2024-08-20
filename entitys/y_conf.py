from y_database.entitys import yEntity


class yConf(yEntity):

  type: str
  value: str

  def __init__(self, params):
    super().__init__(params)