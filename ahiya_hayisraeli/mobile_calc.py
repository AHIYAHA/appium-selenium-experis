from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver


class MobileCalculator:
    def __init__(self, driver: webdriver.Remote):
        self.driver = driver

    def digit(self, d):
        return self.element(f'digit_{d}')

    def enter_num(self, num):
        """clicks on all the required keys to enter a given num"""
        num = str(num)
        for d in num:
            if d == '.':
                self.element("dec_point").click()
            else:
                self.digit(d).click()

    def op(self, operator: str):
        """
        returns one button of operator from these:
        div, pct, mul, sub, add, fact, pow, sqrt
        """
        return self.element(f'op_{operator}')

    def element(self, name):
        """
        return one element of the calculator from these:
        clr, parens, eq, del, dec_point, collapse_expand, const_pi, const_e
        result_final, result_container, result_preview, formula, symbolic
        """
        return self.driver.find_element(by=AppiumBy.ID, value=f'com.google.android.calculator:id/{name}')

    def fun(self, function):
        """
        return one button of operator from these: log, ln, sin, cos, tan
        """
        return self.element(f"fun_{function}")

    def operation(self, a, b, op: str):
        """
        clicks on all the required buttons on a calculator to perform an operation and returns the result.
        the optional operations: div, mul, sub, add, pow
        """
        self.element("clr").click()
        a, b = str(a), str(b)
        self.enter_num(a)
        self.op(op).click()
        self.enter_num(b)
        self.element("eq").click()
        return float(self.element("result_final").text)

    def sqrt(self, num):
        """calculates a square root of a given num and returns the result"""
        self.element("clr").click()
        self.op("sqrt").click()
        self.enter_num(num)
        self.element("eq").click()
        return float(self.element("result_final").text)

    def result_in_fraction(self):
        """
        return a dictionary of the parts of the result in fraction:
        the integer part, numerator and denominator.
        """
        result = self.element("symbolic").text
        space, slash = result.index(" "), result.index("⁄")
        return {"integer": result[:space],
                "numerator": result[space + 1: slash],
                "denominator": result[slash+1:]}
