"ZoekHetMonstertje" ("Find the little monster") is a probabilistic, reversal learning task that is developmentally 
appropriate for infant populations (8-12 months). The task's duration is around 4 minutes. It is designed to run on Python (PsychoPy 2022 for best compatibility).

**Paradigm Description**
On each trial, a colourful fixation spinner is presented for 1000±250ms, after which the cues (two white rectangles) are
displayed for 1000±250ms. The target animation (a dancing "little monster" figure) appears in one of the two cued locations. 
The probabilistic nature of the task means that one side always has a higher (90%) probability of displaying the target animation.
On the rest of the trials (10%), the animation appears in the other location.
The task consists of 70 trials with a stable acquisition block and multiple reversals, during which the side most likely to
contain the target animation switches. 

**Compatability with EEG and eyetracking**
The task is designed to be used with EEG: the EEG component can be enabled in the pop-up menu, in which
case the task runs as a simple behavioural paradigm. 

The paradigm can also be used with a Tobii eye tracker. Eyetracking functionality can 
be added using the existing psychopy_tobii_infant package, which provides an 
interface between PsychoPy and Tobii eye trackers and includes infant-friendly calibration functionality
(https://github.com/yh-luo/psychopy_tobii_infant). 

**How to start the task**
Download the entire folder "ZoekHetMonstertje". To run the task, open the "Monstertjes_Taak.py" in PsychoPy (or another Python shell). 
When you start the task, you will be prompted to enter a participant number, as well as select the session settings.
Indicate if the session is a practice (in which case, a shorter sequence will be run), and whether there is an EEG system connected.
When prompted, press SPACE to begin the task. You can pause the task at any moment by pressing **SPACE**. 
In case the infant is distracted, press **9** to start an attention grabber. 

