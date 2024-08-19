import datetime

from aiogram.types import User

from backend.database.entitys.y_entity import yEntity


def from_tg(f_tg_user: User):

  return yUser((-1,
                f_tg_user.id,
                f_tg_user.username,
                ''))
class yUser(yEntity):

  userid: int
  login: str
  memo: str

  def __init__(self, params):
    super().__init__(params)
    self.userid = params[1]
    self.login = params[2]
    self.memo = params[3]

