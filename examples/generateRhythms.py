# -*- coding: utf-8 -*-
"""
Created on Sun Feb  6 11:36:59 2022

@author: olehe

Should be an example of using the groove generator
"""

#%% Imports

import groovegenerator as gg


#%% Generate patterns

# This makes a random rhythm
# The output is a 3x32 numpy array, with events for Hihat, Snare, and Kick
random_rhythm = gg.generateRandomPattern()


# This makes a random rhythm with some constraints
random_rhythm_two = gg.generateRandomPattern(minEvents=10,
											 maxEvents=30,
											 avoidMultiples=True,
											 maxMultiples=3)

# This makes a constrainted rhythm
constrained_rhythm = gg.generateConstrainedPattern()

# You can specify some constraints
constrained_rhythm_two = gg.generateConstrainedPattern(minSnare=5,
													   maxSnare=15,
													   minKick=5,
													   maxKick=20,
													   avoidMultiples=False)


#%% Calculate metrics

# Syncopation index
witek_SI = gg.syncopationIndexWitek(random_rhythm)
print('This rhythm has a syncopation index of ' + str(witek_SI) + ' as measured with Witek\'s SI')

hoesl_SI = gg.syncopationIndexHoesl(random_rhythm)
print('This rhythm has a syncopation index of ' + str(hoesl_SI) + ' as measured with Hoesl\'s SI')

# Entropy
# This takes a single stream, i.e. snare OR kick
snare = random_rhythm[1,:]
entropy_value = gg.entropy(snare)
print('Entropy value is ' + str(entropy_value))

# Kolmogorov complexity
# This takes the entire pattern, but calculates between snare and kick
k_complexity = gg.kComplexity(random_rhythm)


#%% Make audio

# Generate a .wav file of the pattern
gg.generate_wav(random_rhythm,
				tempo=120,
				loops=5,
				saveName='my_rhythm.csv')

# There's also additional settings here
gg.generate_wav(random_rhythm,
				tempo=130,
				loops=2,
				saveName='my_fancy_rhythm.wav',
				fs=44100,
				dynamics=True,
				customSound='amen')
