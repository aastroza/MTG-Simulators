"""
Austin Herrick

This script uses simulators to determine the average payouts at various winrates of Magic Arena's (MTGA)
Traditional Best of 3 Drafts. In particular, I am examining the impact of the changes in prize support
described in the development blog here:
https://magic.wizards.com/en/articles/archive/magic-digital/mtg-arena-state-game-april-2020-04-13

The below classes allow users to run their own simulations, and the `generate_prize_distributions` function
automates the work needed to create the data used as an input to the provided charts.
"""

import numpy as np
import pandas as pd

class ClassicSimulator():

	def __init__(self, winrate):

		self.winrate = winrate

	def play_draft(self):

		record = {'Wins': 0, 'Losses': 0}

		while record['Wins'] < 5 and record['Losses'] < 2:
			win = np.random.random() < self.winrate

			if win:
				record['Wins'] += 1
			else:
				record['Losses'] += 1

		return record

	def prize_out(self, record, prizes):
		'''
		Given a draft record, updates prize dictionary

		Inputs:
			- record: Dictionary of wins/losses
			- prizes: Dictionary of historic prize payouts
		'''

		wins = record['Wins']

		# prize out
		prizes['Packs'] += 1 + wins
		if wins >= 2:
			prizes['Gems'] += 700
		if wins >= 3:
			prizes['Gems'] += 800
		if wins >= 4:
			prizes['Gems'] += 300
		if wins == 5:
			prizes['Gems'] += 300

		# deduct price
		prizes['Gems'] -= 1500

		# add rounds played
		prizes['Rounds'] += record['Wins'] + record['Losses']

		return prizes

	def simulate_n_drafts(self, n, winrate=None):
		'''
		Plays many drafts to determine average payouts

		Inputs:
			- n: Number of drafts to simulate
			- winrate: Allows user to pass custom winrates
		'''

		# if requested, update winrate
		if winrate:
			self.winrate = winrate

		# initiate prize counter
		prizes = {'Packs': 0, 'Gems': 0, 'Rounds': 0}

		for draft in range(n):
			record = self.play_draft()
			prizes = self.prize_out(record, prizes)

		# find average prizes
		prizes['Packs'] /= n
		prizes['Gems'] /= n
		prizes['Rounds'] /= n	

		return prizes

class NewSimulator():
	
	def __init__(self, winrate):
		self.winrate = winrate

	def play_draft(self):

		record = {'Wins': 0, 'Losses': 0}
		while record['Wins'] + record['Losses'] < 3:
			win = np.random.random() < self.winrate
			if win:
				record['Wins'] += 1
			else:
				record['Losses'] += 1

		return record

	def prize_out(self, record, prizes):
		'''
		Given a draft record, updates prize dictionary

		Inputs:
			- record: Dictionary of wins/losses
			- prizes: Dictionary of historic prize payouts
		'''

		wins = record['Wins']

		# prize out
		prizes['Packs'] += 1
		if wins >= 2:
			prizes['Gems'] += 1000
			prizes['Packs'] += 3
		if wins == 3:
			prizes['Gems'] += 2000
			prizes['Packs'] += 2

		# deduct price
		prizes['Gems'] -= 1500

		# add rounds
		prizes['Rounds'] += 3

		return prizes

	def simulate_n_drafts(self, n, winrate=None):
		'''
		Plays many drafts to determine average payouts

		Inputs:
			- n: Number of drafts to simulate
			- winrate: Allows user to pass custom winrates
		'''

		# if requested, update winrate
		if winrate:
			self.winrate = winrate

		# initiate prize counter
		prizes = {'Packs': 0, 'Gems': 0, 'Rounds': 0}

		for draft in range(n):
			record = self.play_draft()
			prizes = self.prize_out(record, prizes)

		# find average prizes
		prizes['Packs'] /= n
		prizes['Gems'] /= n
		prizes['Rounds'] /= n

		return prizes

class PremierSimulator():

	def __init__(self, winrate):

		self.winrate = winrate

	def play_draft(self):

		record = {'Wins': 0, 'Losses': 0}

		while record['Wins'] < 7 and record['Losses'] < 3:
			win = np.random.random() < self.winrate

			if win:
				record['Wins'] += 1
			else:
				record['Losses'] += 1

		return record

	def prize_out(self, record, prizes):
		'''
		Given a draft record, updates prize dictionary

		Inputs:
			- record: Dictionary of wins/losses
			- prizes: Dictionary of historic prize payouts
		'''

		wins = record['Wins']

		# prize out
		prizes['Packs'] += 1
		prizes['Gems'] += 50
		if wins >= 1:
			prizes['Gems'] += 50
		if wins >= 2:
			prizes['Gems'] += 150
			prizes['Packs'] += 1
		if wins >= 3:
			prizes['Gems'] += 750
		if wins >= 4:
			prizes['Gems'] += 400
			prizes['Packs'] += 1
		if wins == 5:
			prizes['Gems'] += 200
			prizes['Packs'] += 1
		if wins == 6:
			prizes['Gems'] += 200
			prizes['Packs'] += 1
		if wins == 7:
			prizes['Gems'] += 400
			prizes['Packs'] += 1

		# deduct price
		prizes['Gems'] -= 1500

		# add rounds played
		prizes['Rounds'] += record['Wins'] + record['Losses']

		return prizes

	def simulate_n_drafts(self, n, winrate=None):
		'''
		Plays many drafts to determine average payouts

		Inputs:
			- n: Number of drafts to simulate
			- winrate: Allows user to pass custom winrates
		'''

		# if requested, update winrate
		if winrate:
			self.winrate = winrate

		# initiate prize counter
		prizes = {'Packs': 0, 'Gems': 0, 'Rounds': 0}

		for draft in range(n):
			record = self.play_draft()
			prizes = self.prize_out(record, prizes)

		# find average prizes
		prizes['Packs'] /= n
		prizes['Gems'] /= n
		prizes['Rounds'] /= n	

		return prizes


def generate_prize_distributions(intervals = 100, simulator_size = 500000):
	'''
	Generates dataframe of average prize payouts at various winrates.

	Inputs:
		- intervals: Number of evenly-spaced winrates to simulate
		- simulator_size: Number of drafts to simulate per winrate per payout method
	'''

	# assign holders
	labels = ['Winrate', 'Packs-PRE', 'Packs-TRA', 'Gems-PRE', 'Gems-TRA', 'Rounds-PRE']
	result_holder = []

	# run simulations at chosen intervals
	premier_payout = PremierSimulator(0)
	traditional_payout = NewSimulator(0)	
	winrate = 0
	interval_size = 1 / intervals
	for i in range(intervals + 1):

		# run simulations
		prizes_premier = premier_payout.simulate_n_drafts(simulator_size, winrate=winrate)
		prizes_traditional = traditional_payout.simulate_n_drafts(simulator_size, winrate=winrate)

		# append results
		result_holder.append([
			winrate, 
			prizes_premier['Packs'], 
			prizes_traditional['Packs'], 
			prizes_premier['Gems'], 
			prizes_traditional['Gems'], 
			prizes_premier['Rounds']
		])

		# update winrate
		winrate += interval_size

	df = pd.DataFrame.from_records(result_holder, columns=labels)

	# calculate "effective" payout (using 200 gems per pack as previous sale price)
	# cards from the draft itself are valued at 600 gems, though this is likely an undercount
	df['NetGemsPRE'] = 600 + (df['Packs-PRE'] * 200) + df['Gems-PRE']
	df['NetGemsTRA'] = 600 + (df['Packs-TRA'] * 200) + df['Gems-TRA']
	

	return df	