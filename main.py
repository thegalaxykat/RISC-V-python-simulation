from controller import Controller
from model import MVP_Model
from register_file import RegisterFile
from cpu_view import TextView

model = MVP_Model(register_file=RegisterFile())
view = TextView(model)
controller = Controller(model,view)
#addaddi file = controller.prompt.get_file()
controller.run()#file)
None