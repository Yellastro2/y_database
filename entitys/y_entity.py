

class yEntity:

  id: int = -1


  def __init__(self,params):
    self.id = params[0]


  def get_data(self) -> dict:
    f_data = self.__dict__
    f_data.pop('id')
    return f_data