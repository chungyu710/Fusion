import pyautogui
from drivers import state_lookup

class Agent:
    def __init__(self):
        self.velocity_x = 0
        self.velocity_y = 0
        
    def perform_action(self, state):

        default = "Error"

        getattr(self, 'state_' + str(state), lambda: default)()
        pyautogui.move(self.velocity_x, self.velocity_y)

    def state_start(self):
        self.velocity_x = 0
        self.velocity_y = 0
        return None
    def state_move_left(self):
        self.velocity_x = max(-100, self.velocity_x - 2)
        return True
    def state_move_right(self):
        self.velocity_x = min(100, self.velocity_x + 2)
        return True
    def state_move_up(self):
        self.velocity_y = min(100, self.velocity_y + 2)
        return True
    def state_move_down(self):
        self.velocity_y =  max(-100, self.velocity_y - 2)
        return True


# def driver():
#     agent = Agent()
#     try:
#         while True:
#             # TODO: pass in acceleration array
#             state = state_lookup.get_state_based_on_accel("pass in acceleration array here")
#             agent.perform_action(state.lower())
#     except KeyboardInterrupt:
#         print('\n')

# driver()
