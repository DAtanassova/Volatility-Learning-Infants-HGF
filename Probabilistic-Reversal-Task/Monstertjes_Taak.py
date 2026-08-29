#!/usr/bin/env python3

import os
import sys
import csv
import random
from datetime import datetime

import numpy as np
import pandas as pd
import psychtoolbox as ptb
import psychtoolbox.audio

from psychopy import core, visual, event, sound, gui, prefs

sys.path.append("../")

# =============================================================================
# PsychoPy audio settings
# =============================================================================
prefs.hardware['audiolib'] = ['ptb']


# =============================================================================
# Paths
# =============================================================================
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'stimuli')


# =============================================================================
# Experiment functions
# =============================================================================

def getSession(isPractice):

    if isPractice:
        print("Currently running the Practice Run.")
        filename = os.path.join(script_dir, 'schedule_practice.csv')
    else:
        print("Currently running the Full Task Run.")
        filename = os.path.join(script_dir, 'schedule_volatile.csv')

    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        trials = list(reader)

    return trials


def sendMarker(isEEG, cc, markerNumber):

    if isEEG:
        cc.sendMarker(val=markerNumber)
        core.wait(0.002)
        cc.sendMarker(val=0)
    else:
        print('[EEG MOCK] sent marker {}'.format(markerNumber))


# =============================================================================
# Run task
# =============================================================================

def runtrials(win, writer, expData, Task):

    trials = getSession(isPractice)

    BlockNumberIndex = 0
    TrialNumberIndex = 1
    RewLeft = 2
    RewRight = 3
    ProbLeft = 4
    VideoPresent = 5

    # -------------------------------------------------------------------------
    # Participant/session information
    # -------------------------------------------------------------------------

    expData['Participant'] = participant
    expData['Practice'] = isPractice
    expData['EEG'] = isEEG

    # -------------------------------------------------------------------------
    # Visual stimuli
    # -------------------------------------------------------------------------

    fixation = visual.MovieStim(
        win,
        os.path.join(image_path, 'fixation_spinner.mp4'),
        units="cm",
        size=(5, 5),
        pos=(0, 0),
        flipVert=False,
        flipHoriz=False,
        loop=True,
        noAudio=False,
        volume=0.1,
        autoStart=True
    )

    target_left = visual.ImageStim(
        win,
        pos=(-17, 0),
        size=12.5,
        interpolate=True
    )
    target_left.setImage(
        os.path.join(image_path, 'white_rectangle_v3.png')
    )

    target_right = visual.ImageStim(
        win,
        pos=(17, 0),
        size=12.5,
        interpolate=True
    )
    target_right.setImage(
        os.path.join(image_path, 'white_rectangle_v3.png')
    )

    # -------------------------------------------------------------------------
    # Outcome audio
    # -------------------------------------------------------------------------

    audio_stimuli_left = [
        os.path.join(image_path, 'squeak1_left_48.wav'),
        os.path.join(image_path, 'squeak2_left_48.wav'),
        os.path.join(image_path, 'squeak3_left_48.wav'),
        os.path.join(image_path, 'squeak4_left_48.wav')
    ]

    audio_stimuli_right = [
        os.path.join(image_path, 'squeak1_right_48.wav'),
        os.path.join(image_path, 'squeak2_right_48.wav'),
        os.path.join(image_path, 'squeak3_right_48.wav'),
        os.path.join(image_path, 'squeak4_right_48.wav')
    ]

    # -------------------------------------------------------------------------
    # Attention grabbers
    # -------------------------------------------------------------------------

    attention_grabbers = [
        os.path.join(image_path, 'dog.mp4'),
        os.path.join(image_path, 'fox.mp4'),
        os.path.join(image_path, 'penguin.mp4'),
        os.path.join(image_path, 'bear.mp4'),
        os.path.join(image_path, 'bee.mp4')
    ]

    # NOTE:
    # These sounds are defined because they are part of your stimulus set,
    # but they are NOT played. The grabber videos have no audio.
    attention_grabbers_sounds = [
        os.path.join(image_path, 'jump_attention_grabber_looped.wav'),
        os.path.join(image_path, 'sparkle_attention_grabber_looped.wav'),
        os.path.join(image_path, 'sparkle2_attention_grabber_looped.wav'),
        os.path.join(image_path, 'twinkle_attention_grabber_looped.wav'),
        os.path.join(image_path, 'twinkle2_attention_grabber_looped.wav')
    ]

    # -------------------------------------------------------------------------
    # Instructions
    # -------------------------------------------------------------------------

    instructions = visual.TextStim(
        win,
        pos=(0, -10),
        text='Press SPACE to start task'
    )

    instructions_image = visual.ImageStim(
        win,
        pos=(0, 0),
        size=12.5,
        interpolate=True
    )

    instructions_image.setImage(
        os.path.join(image_path, 'instructions_image.png')
    )

    instructions.draw()
    instructions_image.draw()
    win.flip()

    event.waitKeys(keyList=['space'])

    # -------------------------------------------------------------------------
    # Experiment clock
    # -------------------------------------------------------------------------

    expClock = core.Clock()

    expData['StartExperiment'] = expClock.getTime()
    expData['StartDate'] = start_date
    expData['StartTime'] = start_time

    # =========================================================================
    # TRIAL LOOP
    # =========================================================================

    for i, trial in enumerate(trials):

        trialClock = expClock.getTime()

        expData['Block'] = trial[BlockNumberIndex]
        expData['StartTrial'] = trialClock
        expData['Trial'] = trial[TrialNumberIndex]
        expData['ProbLeft'] = trial[ProbLeft]

        # ---------------------------------------------------------------------
        # Timing
        # ---------------------------------------------------------------------

        fixation_time = random.uniform(0.75, 1.25)
        cues_presentation_time = random.uniform(0.75, 1.25)
        outcome_pres_time = 1.25

        # ---------------------------------------------------------------------
        # Fixation
        # ---------------------------------------------------------------------

        expData['fixation_duration'] = fixation_time
        expData['fixation_start_time'] = expClock.getTime()

        timer_fixation = core.Clock()

        sendMarker(isEEG, cc, 10)

        while timer_fixation.getTime() < fixation_time:

            fixation.draw()
            win.flip()

        # ---------------------------------------------------------------------
        # Cues
        # ---------------------------------------------------------------------

        target_left.draw()
        target_right.draw()
        win.flip()
        sendMarker(isEEG, cc, 20)

        core.wait(cues_presentation_time)

        expData['cues_pres_duration'] = cues_presentation_time
        expData['cues_start_time'] = expClock.getTime()

        # ---------------------------------------------------------------------
        # Outcome video
        # ---------------------------------------------------------------------

        selected_video = os.path.join(
            image_path,
            f"dancing_monster{trial[VideoPresent]}.mp4"
        )

        outcome = visual.MovieStim(
            win,
            selected_video,
            units="cm",
            size=12.5,
            loop=False,
            noAudio=True,
            autoStart=False
        )

        expData['VideoPresented'] = selected_video

        # ---------------------------------------------------------------------
        # Outcome audio
        # ---------------------------------------------------------------------

        selected_sound_left = random.choice(audio_stimuli_left)
        selected_sound_right = random.choice(audio_stimuli_right)

        sound_left = sound.Sound(
            selected_sound_left,
            stereo=True
        )

        sound_right = sound.Sound(
            selected_sound_right,
            stereo=True
        )

        # ---------------------------------------------------------------------
        # Present outcome
        # ---------------------------------------------------------------------

        if trial[RewLeft] == '1':

            timer_outcome = core.Clock()

            outcome.play()

            expData['outcome_start_time'] = expClock.getTime()

            sendMarker(isEEG, cc, 100)

            sound_left.play()

            while timer_outcome.getTime() < outcome_pres_time:

                target_left.draw()
                target_right.draw()

                outcome.pos = target_left.pos
                outcome.draw()

                win.flip()

            expData['RewLeft'] = 1
            expData['RewRight'] = 0
            expData['AudioPresented'] = selected_sound_left

        elif trial[RewRight] == '1':

            timer_outcome = core.Clock()

            outcome.play()

            expData['outcome_start_time'] = expClock.getTime()

            sendMarker(isEEG, cc, 100)

            sound_right.play()

            while timer_outcome.getTime() < outcome_pres_time:

                target_left.draw()
                target_right.draw()

                outcome.pos = target_right.pos
                outcome.draw()

                win.flip()

            expData['RewLeft'] = 0
            expData['RewRight'] = 1
            expData['AudioPresented'] = selected_sound_right

        # ---------------------------------------------------------------------
        # Experiment controls
        # ---------------------------------------------------------------------

        key_pressed = event.getKeys(
            keyList=['escape', 'space', '9']
        )

        # ---------------------------------------------------------------------
        # ESCAPE
        # ---------------------------------------------------------------------

        if 'escape' in key_pressed:

            # Stop audio first
            try:
                sound_left.stop()
                sound_right.stop()
            except Exception:
                pass

            # Save current data
            writer.writerow(expData)
            datafile.flush()
            datafile.close()

            # Close window
            win.close()

            # Quit PsychoPy
            core.quit()

        # ---------------------------------------------------------------------
        # PAUSE
        # ---------------------------------------------------------------------

        elif 'space' in key_pressed:

            pause_text = visual.TextStim(
                win,
                pos=(0, -10),
                text='Task paused. Press SPACE to re-start.'
            )

            pause_image = visual.ImageStim(
                win,
                pos=(0, 0),
                size=12.5,
                interpolate=True
            )

            pause_image.setImage(
                os.path.join(image_path, 'instructions_image.png')
            )

            pause_text.draw()
            pause_image.draw()
            win.flip()

            event.waitKeys(keyList=['space'])

        # ---------------------------------------------------------------------
        # ATTENTION GRABBER
        # ---------------------------------------------------------------------

        elif '9' in key_pressed:

            attention_grabber_selected = random.choice(
                attention_grabbers
            )

            grabber_movie = visual.MovieStim(
                win,
                attention_grabber_selected,
                pos=(0, 0),
                size=(20, 11.25),
                units="cm",
                loop=False,
                noAudio=True
            )

            grabber_timer = core.Clock()

            sendMarker(isEEG, cc, 9)

            while (
                grabber_timer.getTime() < 2
                and grabber_movie.status != visual.FINISHED
            ):

                grabber_movie.draw()
                win.flip()

            grabber_movie.stop()
            grabber_movie.unload()

        # ---------------------------------------------------------------------
        # Save trial
        # ---------------------------------------------------------------------

        writer.writerow(expData)
        datafile.flush()

        # Stop outcome audio
        try:
            sound_left.stop()
            sound_right.stop()
        except Exception:
            pass

        # Release outcome movie
        try:
            outcome.stop()
            outcome.unload()
        except Exception:
            pass

    # =========================================================================
    # GOODBYE
    # =========================================================================

    goodbye = visual.TextStim(
        win,
        text="Thank you for participating",
        pos=(0, 0)
    )

    goodbye.draw()
    win.flip()

    core.wait(1.000)

    # IMPORTANT:
    # Do NOT call win.close() or core.quit() here.
    # Return to __main__ for cleanup.


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    # =========================================================================
    # Session setup
    # =========================================================================

    expInfo = {
        'Practice mode': False,
        'EEG connected': False,
        'Participant number': ''
    }

    dlg = gui.DlgFromDict(
        dictionary=expInfo,
        title='Experiment Settings',
        order=[
            'Participant number',
            'Practice mode',
            'EEG connected'
        ]
    )

    if not dlg.OK:
        core.quit()

    isPractice = expInfo['Practice mode']
    isEEG = expInfo['EEG connected']
    participant = expInfo['Participant number']

    # =========================================================================
    # Date/time
    # =========================================================================

    start_datetime = datetime.now()

    start_date = start_datetime.strftime('%Y-%m-%d')
    start_time = start_datetime.strftime('%H:%M:%S')

    # =========================================================================
    # EEG buttonbox
    # =========================================================================

    if isEEG:

        try:
            from rusocsci import buttonbox

            cc = buttonbox.Buttonbox(
                port='com3'
            )

        except ImportError:

            print(
                "\nERROR: EEG compatibility is designed to work with "
                "the Buttonbox from the rusocsci package.\n"
            )

            core.quit()

    else:

        cc = None

    # =========================================================================
    # Data directory
    # =========================================================================

    data_dir = os.path.join(
        script_dir,
        'data'
    )

    os.makedirs(
        data_dir,
        exist_ok=True
    )

    # =========================================================================
    # Data file
    # =========================================================================

    filename = (
        f"sub-{participant}_"
        f"{'practice' if isPractice else 'task'}.csv"
    )

    data_filename = os.path.join(
        data_dir,
        filename
    )

    datafile = open(
        data_filename,
        'w',
        newline=''
    )

    # =========================================================================
    # Data fields
    # =========================================================================

    fieldnames = [
        'Participant',
        'Practice',
        'EEG',
        'StartDate',
        'StartTime',
        'StartExperiment',
        'Block',
        'Trial',
        'StartTrial',
        'fixation_start_time',
        'fixation_duration',
        'cues_start_time',
        'cues_pres_duration',
        'outcome_start_time',
        'RewLeft',
        'RewRight',
        'ProbLeft',
        'VideoPresented',
        'AudioPresented'
    ]

    writer = csv.DictWriter(
        datafile,
        fieldnames=fieldnames
    )

    writer.writeheader()

    # =========================================================================
    # Experiment data
    # =========================================================================

    expData = {}

    # =========================================================================
    # Window
    # =========================================================================

    win = visual.Window(
        fullscr=True,
        allowGUI=False,
        monitor="testMonitor",
        units='cm',
        color='#656565',
        gammaErrorPolicy="ignore"
    )

    win.mouseVisible = False

    # =========================================================================
    # Run experiment
    # =========================================================================

    try:

        runtrials(
            win,
            writer,
            expData,
            "VolatilityLearning"
        )

    except Exception as e:

        print("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("EXPERIMENT ERROR:")
        print(e)

        import traceback
        traceback.print_exc()

        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")

    finally:

        # Close data file
        if not datafile.closed:
            datafile.close()

        # Close PsychoPy window
        try:
            win.close()
        except Exception:
            pass

        # End PsychoPy
        core.quit()