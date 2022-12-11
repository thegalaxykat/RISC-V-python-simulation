from abc import ABC


#########################big TODO TODO TODO need to choose what the state of a wire/bus is 


#TODO the abc stuff for me i forgor how
class PsudoFFModel():
    #######TODO add rst and ena to this
    def __init__(self):
        # do stuff here
        self.module_inputs = {
            # the inputs and output go here in the form
            # "named input (for this module only)" : (module class, "named output (output name from module in same tuple)")
        }
        #set state to uknonwn
        self._state = None
        self._next_state = None
        # collect all module to iter through for clock pulses
        self.sub_modules = []
        for module, _ in self.module_io:
            if module not in self.sub_module:
                self.sub_modules.append(module)
        

    def do_clock_cycle(self):
        self._get_all_next_state()
        self._set_all_next_state()
        pass

    def _get_all_next_state(self):
        #iter through subs and set their get next states
        for module in self.sub_modules:
            module._get_next_state()
        self._get_next_state()
        pass

    def _set_all_next_state(self):
        #iter through subs and set their get next states
        for module in self.sub_modules:
            module._set_next_state()
        self._set_next_state()
        pass
    
    def _get_next_state(self):
        input_next_state = {}
        for wire, (module, module_wire) in self.module_inputs:
            input_next_state[wire] = module.state[module_wire]
        self._next_state = self.simulation(input_next_state)
    
    def _set_next_state(self):
        self._state = self._next_state
        self._next_state = None

    # TODO the property thing
    def state(self):
        return self._state()



    def simulation(self, input_state):
        """calcs what the next state of the module should be
        inputs dict of module
        outputs dict of next state"""
        # you should call other sub functions from here if you want to make it cleaner
        #eg for an alu it would be
        # a = input_state["a"]
        # b = input_state["b"]
        # out = {}
        # out["equal"] = a is b
        # rest of bs
        # return out
