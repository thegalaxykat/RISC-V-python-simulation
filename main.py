from controller import Controller
from cpu_view import TextView
from model import MVP_Model
from register_file import RegisterFile

model = MVP_Model(register_file=RegisterFile())
view = TextView(model)
controller = Controller(model, view)
# file = controller.prompt.get_file()
controller.run()  # file)
None
