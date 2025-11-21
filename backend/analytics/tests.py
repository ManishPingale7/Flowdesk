from django.test import TestCase
from io import StringIO
from django.core.exceptions import ValidationError

from .utils import parse_csv, compute_summary


class UtilsTests(TestCase):
	def setUp(self):
		self.valid_csv = StringIO(
			"Equipment Name,Type,Flowrate,Pressure,Temperature\n"
			"Pump A,Pump,10.5,1.2,25.0\n"
			"Valve B,Valve,5.0,0.8,22.5\n"
			"Compressor C,Compressor,20.0,2.5,40.0\n"
		)

		self.missing_cols_csv = StringIO(
			"Name,Category,Flow,Press,Temp\n"
			"X, Y, 1, 2, 3\n"
		)

	def test_parse_csv_valid(self):
		df = parse_csv(self.valid_csv)
		self.assertEqual(len(df), 3)
		self.assertIn('Equipment Name', df.columns)

	def test_parse_csv_missing_columns_raises(self):
		with self.assertRaises(ValidationError):
			parse_csv(self.missing_cols_csv)

	def test_compute_summary_values(self):
		df = parse_csv(self.valid_csv)
		summary = compute_summary(df)
		self.assertEqual(summary['total_count'], 3)
		# averages
		self.assertAlmostEqual(summary['avg_flowrate'], (10.5 + 5.0 + 20.0) / 3)
		self.assertIn('Pump', summary['type_distribution'])

