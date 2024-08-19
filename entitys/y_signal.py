import datetime

from backend.database.entitys.y_entity import yEntity


# from aiogram.types import User





class ySignal(yEntity):
  # `id` int(11) NOT NULL,
  #   `userid` text NOT NULL,
  #   `login` text DEFAULT NULL,
  #   `balance` int(11) NOT NULL DEFAULT 50,
  #   `pay` int(11) NOT NULL DEFAULT 0,
  #   `lang` text DEFAULT 'rus',
  #   `referrer_id` int(11) DEFAULT 0,
  #   `status_payment` int(11) NOT NULL DEFAULT 0,
  #   `days_payment` int(11) DEFAULT 0
  # id: int
  address_from: str
  address_to: str
  from_ton: float
  value1: float
  value2: float
  ton_result: float
  date: int


  def __init__(self,params):
    super().__init__(params)
    self.address_from = params[1]
    self.address_to = params[2]
    self.ton_result = float(params[3])
    self.date = params[4]
    self.from_ton = params[5]
    self.value1 = params[6]
    self.value2 = params[7]



def from_params(address_from: str,
                address_to: str,
                from_ton: float,
                value1: float,
                value2: float,
                ton_result: float,
                date: int) -> ySignal:
  return ySignal((-1,
                  address_from,
                  address_to,
                  ton_result,
                  date,
                  from_ton,
                  value1,
                  value2))