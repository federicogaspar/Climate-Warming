"""
Created on Fri Apr  9 19:24:08 2021

@author: Federico G Vega
"""

import unittest
import numpy as np
import math
import main

TRAINING_INTERVAL = np.array(range(1961, 2010))
TESTING_INTERVAL = np.array(range(2010, 2016))

CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]


class TestClimate(unittest.TestCase):

	def test_generate_models(self):

		degs_msg = "generate_models should return one model for each given degree"
		list_type_msg = "generate_models should return a list of models"
		array_type_msg = "each model returned by generate_models should be of type pylab.array"
		coefficient_mismatch = "coefficients of returned model are not as expected"

		# simple y = x case.
		x = np.array(range(50))
		y = np.array(range(50))
		degrees = [1]
		models = main.generate_models(x, y, degrees)

		self.assertEquals(len(models), len(degrees), degs_msg)
		self.assertIsInstance(models, list, list_type_msg)
		self.assertIsInstance(models[0], np.ndarray, array_type_msg)
		self.assertListEqual(list(models[0]), list(np.polyfit(x, y, 1)), coefficient_mismatch)

		# two models for y = 2x case
		y = np.array(range(0,100,2))
		degrees = [1, 2]
		models = main.generate_models(x, y, degrees)
		self.assertEquals(len(models), len(degrees), degs_msg)
		self.assertIsInstance(models, list, list_type_msg)
		for m in models:
			self.assertIsInstance(m, np.ndarray, array_type_msg)
		for i in range(2):
			self.assertListEqual(list(models[i]), list(np.polyfit(x,y, degrees[i])), coefficient_mismatch)

		# three models
		degrees = [1,2,20]
		models = main.generate_models(x, y, degrees)
		self.assertEquals(len(models), len(degrees), degs_msg)
		self.assertIsInstance(models, list, list_type_msg)
		for m in models:
			self.assertIsInstance(m, np.ndarray, array_type_msg)
		for i in range(3):
			self.assertListEqual(list(models[i]), list(np.polyfit(x,y, degrees[i])), coefficient_mismatch)


	def test_r_squared(self):

		# basic case:
		# actual values    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
		# estimated values [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
		y = np.array(range(10))
		est = np.array([5]*10)
		r_sq = main.r_squared(y, est)
		self.assertIsInstance(r_sq, float, "r_squared should return a float")
		rounded = round(r_sq, 6)
		self.assertEquals(rounded, -0.030303)

		# another basic case:
		# actual values    [0, 1, 2, 3, 4, 5, 6, 7, 8]
		# estimated values [0, 2, 4, 6, 8, 10, 12, 14, 16]
		est = np.array(range(0,20,2))
		r_sq = main.r_squared(y, est)
		self.assertIsInstance(r_sq, float, "r_squared should return a float")
		rounded = round(r_sq, 6)
		self.assertEquals(rounded, -2.454545)

		# case where actual = estimated, so R^2=1
		r_sq = main.r_squared(y, y)
		self.assertIsInstance(r_sq, float, "r_squared should return a float")
		self.assertEquals(r_sq, 1.0)

	def test_gen_cities_avg(self):
		# test for just one city
		climate = main.Climate('data.csv')
		test_years = np.array(TESTING_INTERVAL)
		result = main.gen_cities_avg(climate, ['SEATTLE'], test_years)
		correct = [11.514383561643836,10.586849315068493,11.28319672,12.10643836,12.82917808,13.13178082]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "City averages do not match expected results")

		# multiple cities
		result = main.gen_cities_avg(climate, CITIES, test_years)
		correct = [16.75950424, 16.85749511,17.56180068,16.65717547,16.84499022,17.54460535]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "City averages do not match expected results")

		# years range
		# multiple cities
		result = main.gen_cities_avg(climate, ['TAMPA', 'DALLAS'], test_years)
		correct = [20.8040411,22.03910959,22.27206284,21.31136986,20.88123288,22.07794521]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "City averages do not match expected results")

	def test_moving_avg(self):
		y = [1, 2, 3, 4, 5, 6, 7]
		window_length = 3
		correct = np.array([1, 1.5, 2, 3, 4, 5, 6])
		result = main.moving_average(y, window_length)
		self.assertListEqual(list(result), list(correct), "Moving average values incorrect")

		y = [-1.5, 1.5, -3.0, 3.0, -4.5, 4.5]
		window_length = 2
		correct = [-1.5, 0, -.75, 0, -.75, 0]
		result = main.moving_average(y, window_length)
		self.assertListEqual(list(result), list(correct), "Moving average values incorrect")

	def test_rmse(self):
		y = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		estimate = [1, 4, 9, 16, 25, 36, 49, 64, 81]
		result = main.rmse(np.array(y), np.array(estimate))
		correct = 35.8515457593
		self.assertTrue(math.isclose(correct, result), "RMSE value incorrect")

		y = [1, 1, 1, 1, 1, 1, 1, 1, 1]
		estimate = [1, 4, 9, 16, 25, 36, 49, 64, 81]
		result = main.rmse(np.array(y), np.array(estimate))
		correct = 40.513372278
		self.assertTrue(math.isclose(correct, result), "RMSE value incorrect")

	def test_gen_std_devs(self):
		climate = main.Climate('data.csv')
		years = np.array(TRAINING_INTERVAL)
		result = main.gen_std_devs(climate, ['SEATTLE'], years)
		correct = [6.1119325255476635, 5.4102625076401125, 6.0304210441394801, 5.5823239710637846, 5.5908151965372177, 5.0347634736031583, 6.2485081784971772, 5.6752637253518703, 5.9822493041266327, 5.5376216719090898, 6.0339331562285095, 6.3471434661632733, 5.3872564859222782, 5.7528361897357705, 6.0117329392620285, 5.5922579610955854, 5.67888175212234, 5.7810899373043272, 5.7184178577664087, 5.3955809402004036, 5.1736886920193665, 5.8134229790176573, 5.1915733214759872, 5.4023314139519591, 6.7868442109830855, 5.2952870947334114, 5.6064597624296333, 5.4921097908102086, 6.1450202825415214, 6.3591021848005278, 5.4996866353350615, 5.6516820894310058, 5.7969983303071411, 5.8531227958031931, 5.2545492072097808, 6.0102701017450126, 5.5327493838092865, 5.7703034605336532, 5.0412624972468443, 5.2728662938897264, 5.0859211734722649, 5.5526426823734987, 5.8005720594546748, 5.7391426965165389, 5.5518538235632207, 5.8279562142168073, 5.9089508390885479, 5.9789908401877394, 6.5696153940105573]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "Standard deviations do not match expected results")

		result = main.gen_std_devs(climate, CITIES, years)
		correct = [6.80077295, 6.93447231, 7.29650045, 6.73045142, 6.50559487, 6.95908749, 6.48897992, 6.95104303, 7.05854311, 7.09774206, 6.83865798, 6.73134708, 6.66162258, 6.40923967, 6.62142171, 6.7136105 , 7.25754822, 7.26327636, 7.1787612 , 7.08593526, 6.87367413, 6.79570439, 7.08155492, 6.72499748, 7.21627296, 6.45603723, 6.72883068, 6.97209869, 6.92295834, 6.30336456, 6.53301708, 6.27774296, 6.84886294, 6.82578303, 6.78561011, 6.75927822, 6.66340501, 6.44863217, 6.3413249 , 6.76376744, 6.55199308, 6.68316545, 6.77515503, 6.74354111, 6.87205089, 6.38152825, 6.97079446, 6.75824573, 6.74513468]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "Standard deviations do not match expected results")

		result = main.gen_std_devs(climate, ['TAMPA', 'DALLAS'], years)
		correct = [6.6222742584336203, 7.0831603561201613, 7.7597469401129215, 7.0259613619453818, 6.5638542892147722, 7.2251974365928691, 6.1518558874089617, 7.0391602268356808, 7.1526420227632297, 7.2908275139292842, 6.270260767160857, 6.4782366919527483, 6.6679030134469448, 6.0219388710726411, 6.6228151175078525, 6.4353160709432649, 7.8465935407208427, 8.1048357980863859, 7.2582171660107786, 7.7051951164668244, 7.083156557719672, 6.6459102430953294, 7.3472808518990416, 6.7892304784646278, 7.4543972339551905, 6.3029047021487283, 6.6943381051857225, 6.9549273458644914, 7.0491429730256217, 6.0235494427214373, 6.3241265661686636, 6.125270864250882, 6.8769945045255714, 6.2418939236561259, 6.8146994668451102, 7.2018962701686169, 6.5761298971998094, 7.0293238787351466, 6.3457405064020591, 7.1321062259929908, 6.5963446478678387, 6.750967975464123, 6.839988834120371, 6.4423456425074255, 6.8283808762586897, 6.3536010884491958, 6.6492152503358843, 6.6265277854285625, 6.6375221251962317]
		self.assertTrue(len(correct) == len(result), "Expected length %s, was length %s" % (len(correct), len(result)))

		for index in range(len(correct)):
			good_enough = math.isclose(correct[index], result[index])
			self.assertTrue(good_enough, "Standard deviations do not match expected results")


if __name__ == '__main__':
    # Run the tests and print verbose output to stderr.
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestClimate))
    unittest.TextTestRunner(verbosity=2).run(suite)
