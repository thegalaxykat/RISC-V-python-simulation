from controller import Controller
from model import MVP_Model
from register_file import RegisterFile

model = MVP_Model(register_file=RegisterFile())
controller = Controller(model,view=None)
controller.run()
None