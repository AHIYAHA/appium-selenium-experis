from selenium.webdriver.common.by import By
from selenium.webdriver import Edge


class FactorizationCalculator:
    def __init__(self, driver: Edge):
        self.driver = driver

    def calc_line(self):
        """return the element of the input field"""
        return self.driver.find_element(By.CSS_SELECTOR, "input.infull")

    def submit_button(self):
        """click it to get factorization"""
        return self.driver.find_element(By.NAME, "x")

    def enter_num(self, num):
        """performs factorization in the site using the required elements"""
        self.calc_line().clear()
        self.calc_line().send_keys(num)
        self.submit_button().click()

    def result(self):
        """the element of the result message"""
        return self.driver.find_element(By.CLASS_NAME, "bigtext")

    def factors(self, num):
        """
        returns a list of the number's factors
        according to the result message
        whether the number is prime or not
        """
        if self.result().text.strip()[-18:] == "is a prime number.":
            return [self.result().text.strip()[:-18]]

        # split the message in num location, take the second half without the ": " and convert it to list
        return self.result().text.split(f"{num}")[1][2:].split(", ")

    def calculation(self, num):
        """all the operation of calculator, return a list of factors"""
        self.driver.get("https://www.calculator.net/prime-factorization-calculator.html/")
        self.enter_num(num)
        return self.factors(num)
