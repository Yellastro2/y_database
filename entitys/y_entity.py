

class yEntity:
  # `id` int(11) NOT NULL
  # _id: int
  #
  # @property
  # def id(self):
  #   return self._id
  #
  # @id.setter
  # def id(self, newname):
  #   self._id = newname

  id: int = -1


  def __init__(self,params):
    self.id = params[0]


  def get_data(self):
    f_data = self.__dict__
    f_data.pop('id')
    return f_data