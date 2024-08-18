import unittest
from random import randint
from project_appium_ahiya_hayisraeli.mobile_calc import MobileCalculator
from project_appium_ahiya_hayisraeli.factorization_calculator import FactorizationCalculator
from project_appium_ahiya_hayisraeli.simple_calculator import SimpleCalculator
from project_appium_ahiya_hayisraeli.decimal2fraction_calculator import DecimalToFractionCalculator
from selenium.webdriver import Edge
from appium.webdriver import Remote
appium_server_url_local = 'http://localhost:4723/wd/hub'
capabilities = dict(
    platformName="Android",
    deviceName="Pixel7a",
    udid="emulator-5554",
    appActivity='com.android.calculator2.Calculator',
    appPackage='com.google.android.calculator',
    platformVersion="35"
)


class TestCalculator(unittest.TestCase):
    def setUp(self):
        # mobile
        self.mobile_calculator = MobileCalculator(Remote(appium_server_url_local, capabilities))

        # web
        driver = Edge()
        driver.maximize_window()
        driver.implicitly_wait(5)
        self.factorization_calculator = FactorizationCalculator(driver)
        self.simple_calculator = SimpleCalculator(driver)
        self.decimal2fraction_calculator = DecimalToFractionCalculator(driver)

    def tearDown(self):
        if self.mobile_calculator.driver:
            self.mobile_calculator.driver.quit()
        self.factorization_calculator.driver.close()

    # tests for prime factorization calculator page

    def test_multiplying_by_prime_factors(self):
        """
        This test verifies that multiplying - using the calculator application -
         the prime factors of a given number, as provided by the website,
         results in the given number.
        """
        # sets a 3-digit random number
        num = randint(100, 999)

        # gets its prime factorization from the website into a list
        factors = self.factorization_calculator.calculation(num)

        # multiplies all the prime factors in the calculator application
        self.mobile_calculator.operation(factors, "mul")

        self.assertEqual(self.mobile_calculator.element("result_final").text.strip(), str(num))

    def test_prime_number(self):
        """
        This test verifies using the calculator application that a given number is a prime number,
         and using the website that it has one factor only
        """
        # sets a 3-digit prime number
        num = 101

        # verify that it is a prime number by the calculator application
        primes_sqrt_1000 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]  # all prime numbers to sqrt(1000)
        for prime in primes_sqrt_1000[:4]:  # continue when num is bigger
            dividing = self.mobile_calculator.operation([num, prime], "div")
            self.assertNotEqual(dividing, int(dividing))
            self.assertNotEqual(1, dividing)

        # gets its prime factorization from the website into a list
        factors = self.factorization_calculator.calculation(num)

        # verifies it has one factor - itself
        self.assertEqual(len(factors), 1)
        self.assertEqual(int(factors[0]), num)

    def test_dividing_by_each_prime_factor(self):
        """
        This test verifies that dividing using the calculator application
        a given number by every one from its prime factors,
        as provided by the website, results in an integer
        """
        # sets a 3-digit random number
        num = randint(100, 999)

        # gets its prime factorization from the website into a list
        factors = self.factorization_calculator.calculation(num)

        # in the calculator application verifies that dividing the given number by every prime factor results in integer
        for factor in set(factors):  # every different factor
            dividing = self.mobile_calculator.operation([num, factor.strip()], "div")
            self.assertEqual(dividing, int(dividing))

    def test_square_number(self):
        """
        Verifies the mobile calculator ability to square a given square number accurately,
        and the prime factorization calculator ability of this number and its square root.
        """
        # sets a square number
        num = 576

        # checks in the mobile calculator if the square root of num is integer
        sqrt = float(self.mobile_calculator.sqrt(num))
        self.assertEqual(int(sqrt), sqrt)

        # gets the prime factorization of the num and his square root from the website into 2 lists
        num_factors = self.factorization_calculator.calculation(num)
        sqrt_factors = self.factorization_calculator.calculation(sqrt)

        # verifies that every factor appears in the prime factorization of num
        # 2 times more than in the prime factorization of his square root
        for factor in set(num_factors):
            self.assertEqual(sqrt_factors.count(factor) * 2, num_factors.count(factor))

    # test for simple calculator page
    def test_log_negative_error(self):
        """
        test error message for an illegal calculation
        in both calculators
        """
        calc = self.simple_calculator
        calc.driver.get("https://www.calculator.net/")
        calc.clicks("'log'", randint(0, 9), "'+/-'", "'='")
        self.assertEqual(calc.output().text.lower().strip(), "error")

        calc = self.mobile_calculator
        calc.clicks("collapse_expand", "fun_log", "op_sub", randint(0, 9), "eq")
        self.assertEqual(calc.element("result_preview").text[-5:], "error")

    # test for fraction calculator page
    def test_decimal_to_fraction_calculator(self):
        """
        tests correct show of fraction in both calculators
        """
        calc = self.decimal2fraction_calculator
        calc.driver.get("https://www.calculator.net/fraction-calculator.html")
        calc.submit_button().click()  # there is a default value in the input field
        num, result = calc.before_calculation().text, calc.after_calculation()

        calc = self.mobile_calculator
        calc.operation([num, 1], "mul")  # multiplies in 1 so that the number's presentation will be converted
        self.assertEqual(result, calc.result_in_fraction())  # compares between the results
