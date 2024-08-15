from selenium.webdriver.common.by import By
from selenium.webdriver import Edge


class DecimalToFractionCalculator:
    def __init__(self, driver: Edge):
        self.driver = driver

    def form(self):
        """return the form of this specific calculator in the page"""
        return self.driver.find_element(By.NAME, "calform2")

    def input(self):
        """return the element of the input field"""
        return self.form().find_element(By.ID, "c2d1")

    def submit_button(self):
        """return the element of the submit button"""
        return self.form().find_element(By.NAME, "x")

    def result(self):
        """return the element of the table that describes the result"""
        return self.driver.find_element(By.ID, "fcoutput")

    def before_calculation(self):
        """return the number as it is before the calculation"""
        return self.result().find_elements(By.TAG_NAME, "td")[0]

    def after_calculation(self):
        """
        return a dictionary of the parts of the number after calculation:
        the integer part, numerator and denominator.
        """
        return {"integer": self.result().find_elements(By.TAG_NAME, "td")[-4].text,
                "numerator": self.result().find_elements(By.TAG_NAME, "td")[-3].text,
                "denominator": self.result().find_elements(By.TAG_NAME, "td")[-1].text}
