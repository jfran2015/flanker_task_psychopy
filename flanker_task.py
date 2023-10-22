from psychopy import visual, core, event, gui
from psychopy.hardware import keyboard
import pandas as pd
import random
import math

class trial_info:
    def __init__(self, input_dict, num_valid_trials, num_invalid_trials):
        self.input_dict = input_dict
        self.num_valid_trials = num_valid_trials
        self.num_invalid_trials = num_invalid_trials
        self.trial_dict = self.full_dict_generator()
        self.shuffled_trial_dict = self.dict_shuffler()

    # This function generates a full (un-shuffled) dictionary containing all trials
    def full_dict_generator(self):
        valid_inds = []
        invalid_inds = []

        trial_dict = {'flanker_text': [], 'congruency': [], 'center_direction': []}

        for x in range(len(self.input_dict['flanker_text'])):
            if self.input_dict['congruency'][x] == 0:
                valid_inds.append(x)
            elif self.input_dict['congruency'][x] == 1:
                invalid_inds.append(x)

        input_choice = [i for i in range(0, len(valid_inds))]
        num_reps = math.ceil(self.num_valid_trials / len(valid_inds))
        full_input_choice = input_choice*num_reps

        for valid_count in range(self.num_valid_trials):
            choice_index = full_input_choice[valid_count]  # Get the index from input_choice
            trial_dict['flanker_text'].append(self.input_dict['flanker_text'][valid_inds[choice_index]])
            trial_dict['congruency'].append(self.input_dict['congruency'][valid_inds[choice_index]])
            trial_dict['center_direction'].append(self.input_dict['center_direction'][valid_inds[choice_index]])

        input_choice = [i for i in range(0, len(valid_inds))]
        num_reps = math.ceil(self.num_valid_trials / len(valid_inds))
        full_input_choice = input_choice*num_reps

        for invalid_count in range(self.num_invalid_trials):
            choice_index = full_input_choice[invalid_count]  # Get the index from input_choice
            trial_dict['flanker_text'].append(self.input_dict['flanker_text'][invalid_inds[choice_index]])
            trial_dict['congruency'].append(self.input_dict['congruency'][invalid_inds[choice_index]])
            trial_dict['center_direction'].append(self.input_dict['center_direction'][invalid_inds[choice_index]])

        return trial_dict

    # This function shuffles the full dictionary
    def dict_shuffler(self):
        trial_order = list(range(len(self.trial_dict['flanker_text'])))
        random.shuffle(trial_order)

        shuffled_trial_dict = {'flanker_text': [], 'congruency': [], 'center_direction': []}
        for index in trial_order:
            shuffled_trial_dict['flanker_text'].append(self.trial_dict['flanker_text'][index])
            shuffled_trial_dict['congruency'].append(self.trial_dict['congruency'][index])
            shuffled_trial_dict['center_direction'].append(self.trial_dict['center_direction'][index])

        return shuffled_trial_dict

def get_subject_number():
    dlg = gui.Dlg(title="Subject Information")
    dlg.addField("Subject Number:")

    while True:
        dlg.show()
        if dlg.OK:
            subject_number = dlg.data[0]
            if type(subject_number) == int or float:
                return subject_number
            else:
                dlg.data = []  # Clear the input field
                dlg.error("Please enter a valid number.")
        else:
            core.quit()

def get_task_choice():
    dlg = gui.Dlg(title="Task Choice")
    dlg.addField("Arrow or Letter (A or L):", tip="Enter 'A' for Arrow or 'L' for Letter")

    while True:
        dlg.show()
        if dlg.OK:
            task_choice = dlg.data[0].strip().lower()
            if task_choice in ['a', 'l']:
                return task_choice
            else:
                dlg.data = []  # Clear the input field
                dlg.error("Please enter 'A' for Arrow or 'L' for Letter.")
        else:
            core.quit()

def get_response(key_board, max_response_time):
    response = None
    response_time = None
    max_response_time = max_response_time
    start_time = core.getTime()
    key_board.clock.reset()
    key_board.start()

    # Wait for either 'z' or '/'
    while (response is None) and ((core.getTime() - start_time) < max_response_time):
        keys = key_board.getKeys(keyList=['z', 'slash'])
        if keys:
            response = keys[0].name
            response_time = keys[0].rt

    key_board.stop()

    return response, response_time

def instructions(win, arrow_vs_letter):
    if arrow_vs_letter == 'a':
        instruction_text = 'In this task you will be shown an array of arrows. You will be asked to respond to the arrow in the center while ignoring the outside arrows. If you see a < arrow in the center respond with the z key and if you see a > arrow in the center respond with the / key.'
    elif arrow_vs_letter == 'l':
        instruction_text = 'In this task you will be shown an array of letters. You will be asked to respond to the letter in the center while ignoring the outside letters. If you see a X or C in the center respond with the z key and if you see a V or B in the center respond with the / key.'

    instruction_stim = visual.TextStim(win, text=instruction_text)

    instruction_stim.draw()
    win.flip()
    # Wait for a key press
    event.waitKeys()

def main():
    # Get input in a dialog box for what the subject number is
    subject_number = get_subject_number()
    # Get input in a dialog box for what task type (arrow or letter) is desired
    arrow_vs_letter = get_task_choice()
    # Using the user input create filename for output file
    output_file_format = "flanker_task_type_{}_subj_{}.csv".format(arrow_vs_letter, subject_number)

    # Create structure for the output file
    data = pd.DataFrame({
        'subject_number': [],
        'trial_number': [],
        'flanker_text': [],
        'congruency': [],
        'direction': [],
        'Response_Time': [],
        'Response': [],
        'Accuracy': []
    })

    # Create dictionary for arrow flanker task
    arrow_flankers_dict = {
        'flanker_text': ["< < < < <", "< < > < <", "> > > > >", "> > < > >"],
        'congruency': [0, 1, 0, 1], #i have this backwards coded 1 = incongruent and 0 = congruent
        'center_direction': [1, 0, 0, 1]
    }

    # Create dictionary for letter flanker task
    letter_flankers_dict = {
        'flanker_text':    ["X X X X X", "X X C X X", "X X V X X", "X X B X X", 
                            "C C X C C", "C C C C C", "C C V C C", "C C B C C",
                            "V V X V V", "V V C V V", "V V V V V", "V V B V V",
                            "B B X B B", "B B C B B", "B B V B B", "B B B B B"],
        'congruency':  [0, 0, 1, 1, 
                        0, 0, 1, 1,
                        1, 1, 0, 0,
                        1, 1, 0, 0],
        'center_direction':    [1, 1, 0, 0,
                                1, 1, 0, 0,
                                1, 1, 0, 0,
                                1, 1, 0, 0]
    }

    # Set number of trials of each type that is desired
    num_valid_trials = 80
    num_invalid_trials = 20

    # Create instances of the trial_info class. This could be done only once for the version 
    # desired but it isn't too computationally intensive so I will just do both
    arrow_flankers = trial_info(arrow_flankers_dict, num_valid_trials, num_invalid_trials)
    letter_flankers = trial_info(letter_flankers_dict, num_valid_trials, num_invalid_trials)

    # Set up psychopy window and keyboard
    win = visual.Window([800, 600], monitor="testMonitor", units="deg")
    kb = keyboard.Keyboard()

    if arrow_vs_letter == 'a':
        all_trials_shuffled = arrow_flankers.shuffled_trial_dict
    elif arrow_vs_letter == 'l':
        all_trials_shuffled = letter_flankers.shuffled_trial_dict

    # Create fixation cross
    fixation_cross = visual.TextStim(win, text='+')

    # Present instructions
    instructions(win, arrow_vs_letter)

    for trial_number in range(len(all_trials_shuffled['flanker_text'])):
        # Create flanker stim
        flanker_stim = visual.TextStim(win, text=all_trials_shuffled['flanker_text'][trial_number])

        # Draw fixation cross
        fixation_cross.draw()
        win.flip()
        core.wait(0.5)

        # Draw flanker stim
        flanker_stim.draw()
        win.flip()

        response, response_time = get_response(kb, max_response_time=3)

        # Process the response and response time
        if response == 'z':
            # Participant pressed 'z'
            print("Z key pressed.")
            print(response_time)
            response_correct = 1 if all_trials_shuffled['center_direction'][trial_number] == 1 else 0
        elif response == 'slash':
            # Participant pressed '/'
            print("/ key pressed")
            print(response_time)
            response_correct = 1 if all_trials_shuffled['center_direction'][trial_number] == 0 else 0
        else:
            # No response within the specified time
            print("No response")
            response_correct = -1

        data.loc[len(data.index)] = [subject_number,
                                    trial_number,
                                    all_trials_shuffled['flanker_text'][trial_number],
                                    all_trials_shuffled['congruency'][trial_number], 
                                    all_trials_shuffled['center_direction'][trial_number],
                                    response_time,
                                    response,
                                    response_correct]

    # Save the DataFrame to a CSV file
    data.to_csv('data/' + output_file_format, index=False)

    win.flip()
    core.wait(0.5)

    win.close()
    kb.clearEvents()

if __name__ == "__main__":
    main()