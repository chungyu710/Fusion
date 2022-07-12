import pyautogui
from drivers import state_lookup

class Agent: 
    def perform_action(self, state):

        default = "Error"

        return getattr(self, 'state_' + str(state), lambda: default)()

    def state_start(self):
        return None
    def state_move_left(self):
        pyautogui.move(-30, 0) 
        return True
    def state_move_right(self):
        pyautogui.move(30, 0) 
        return True
    def state_move_up(self):
        pyautogui.move(0, -30)
        return True
    def state_move_down(self):
        pyautogui.move(0, 30) 
        return True

def driver():
    agent = Agent()
    try:
        while True:
            # TODO: pass in acceleration array 
            state = state_lookup.get_state_based_on_accel("pass in acceleration array here")
            agent.perform_action(state.lower())
    except KeyboardInterrupt:
        print('\n')

driver()

