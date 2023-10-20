from psychopy import visual, core
from psychopy.hardware import keyboard
import pandas as pd
import random
import math

class trialInfo:
    def __init__(self, input_dict, num_valid_trials, num_invalid_trials):
        self.input_dict = input_dict
        self.num_valid_trials = num_valid_trials
        self.num_invalid_trials = num_invalid_trials
        self.trial_dict = self.full_dict_generator()
        self.shuffled_trial_dict = self.dict_shuffler()

    #this function generates a full (un-shuffled) dictionary containing all trials
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

    #this function shuffles the full dictionary
    def dict_shuffler(self):
        trial_order = list(range(len(self.trial_dict['flanker_text'])))
        random.shuffle(trial_order)

        shuffled_trial_dict = {'flanker_text': [], 'congruency': [], 'center_direction': []}
        for index in trial_order:
            shuffled_trial_dict['flanker_text'].append(self.trial_dict['flanker_text'][index])
            shuffled_trial_dict['congruency'].append(self.trial_dict['congruency'][index])
            shuffled_trial_dict['center_direction'].append(self.trial_dict['center_direction'][index])

        return shuffled_trial_dict

def user_input():
    while True:
        subnum = input("Enter subject number: ")
        if subnum.isdigit():
            break
        else:
            print("Please enter a valid number for subject number.")

    while True:
        arrow_vs_letter = input("Would you like to run an Arrow (A) or Letter (L) flanker task: ").lower()
        if arrow_vs_letter in ['l', 'a']:
            break
        else:
            print("Please enter 'A' for Arrow or 'L' for Letter.")

    return subnum, arrow_vs_letter

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

def main():
    subnum, arrow_vs_letter = user_input()

    output_file_format = "flanker_task_type_{}_subj_{}.csv".format(arrow_vs_letter, subnum)

    data = pd.DataFrame({
        'subnum': [],
        'flanker_text': [],
        'congruency': [],
        'direction': [],
        'Response_Time': [],
        'Response': [],
        'Accuracy': []
    })

    arrow_flankers_dict = {
        'flanker_text': ["< < < < <", "< < > < <", "> > > > >", "> > < > >"],
        'congruency': [0, 1, 0, 1], #i have this backwards coded 1 = incongruent and 0 = congruent
        'center_direction': [1, 0, 0, 1]
    }

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

    #set number of trials of each type that is desired
    num_valid_trials = 80
    num_invalid_trials = 20

    arrow_flankers = trialInfo(arrow_flankers_dict, num_valid_trials, num_invalid_trials)
    letter_flankers = trialInfo(letter_flankers_dict, num_valid_trials, num_invalid_trials)

    if arrow_vs_letter == 'A' or arrow_vs_letter == 'a':
        all_trials_shuffled = arrow_flankers.shuffled_trial_dict
    elif arrow_vs_letter == 'L' or arrow_vs_letter == 'l':
        all_trials_shuffled = letter_flankers.shuffled_trial_dict

    #set up psychopy window and keyboard
    win = visual.Window([800, 600], monitor="testMonitor", units="deg")
    kb = keyboard.Keyboard()

    #create fixation cross
    fixation_cross = visual.TextStim(win, text='+')

    for trialnum in range(len(all_trials_shuffled['flanker_text'])):
        #create flanker stim
        flanker_stim = visual.TextStim(win, text=all_trials_shuffled['flanker_text'][trialnum])

        #draw fixation cross
        fixation_cross.draw()
        win.flip()
        core.wait(0.5)

        #draw flanker stim
        flanker_stim.draw()
        win.flip()

        response, response_time = get_response(kb, max_response_time=3)

        # Process the response and response time
        if response == 'z':
            # Participant pressed 'z'
            print("Z key pressed.")
            print(response_time)
            response_correct = 1 if all_trials_shuffled['center_direction'][trialnum] == 1 else 0
        elif response == 'slash':
            # Participant pressed '/'
            print("/ key pressed")
            print(response_time)
            response_correct = 1 if all_trials_shuffled['center_direction'][trialnum] == 0 else 0
        else:
            # No response within the specified time
            print("No response")
            response_correct = -1

        data.loc[len(data.index)] = [subnum,
                                    all_trials_shuffled['flanker_text'][trialnum],
                                    all_trials_shuffled['congruency'][trialnum], 
                                    all_trials_shuffled['center_direction'][trialnum],
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