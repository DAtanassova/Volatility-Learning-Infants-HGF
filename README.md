# VolatilityLearningInfants_HGF

**What is this?**
This repository provides everything you need to study how infants learn in a 
changing, uncertain world: from the experimental task to a step-by-step guide 
for extracting the hidden computational processes driving their behavior.

**The task**
This developmentally appropriate probabilistic task allows for an investigation
of how infants (aged 8–12 months, though it works well with older children too) 
learn and adapt in volatile conditions. The task is a short passive viewing
paradigm where a reward (animation) appears reliably on one side until it 
switches. By tracking infants' anticipatory looks (where they expect the reward
to appear next), we can measure how quickly and how well they detect and adapt 
to these hidden changes.

The task takes ~4 minutes, making it suitable for infant attention spans, and 
is fully compatible with EEG and eye-tracking setups.
See the Probabilistic-Reversal-Task folder for the script and instructions 
on running it.

**The computational modelling**

While behavioral data can provide insights on how infants adapt (e.g. average
accuracy, win-stay, lose-shift rates), we use the Hierarchical Gaussian Filter 
(HGF) to extract an estimate of how they learn in changing conditions. The HGF 
(model available here: https://github.com/translationalneuromodeling/tapas/) is
considered the best mathematical approximation of how humans learn under
uncertainty and in volatile (changing) conditions.

The model allows for an estimate of how predictions or beliefs (i.e. about the 
side where a target would appear) are generated, and how fast these beliefs
update in response to new information. It also quantifies various latent 
parameters representing individual differences in this process (i.e. how 
sensitive or reactive someone is to change). These hidden quantities cannot be
observed directly but the model creates an estimate based on observed behaviour
(in this case: the anticipatory looking behaviour).

The "Computational-Modelling"" folder includes a full tutorial for applying this 
model to infant data, using anticipatory looking behavior as the behavioral 
signal.

