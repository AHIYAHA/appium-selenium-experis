from selenium.webdriver.common.by import By
from selenium.webdriver import Edge


class SimpleCalculator:
    def __init__(self, driver: Edge):
        self.driver = driver

    def all_calc(self):
        return self.driver.find_element(By.CSS_SELECTOR, "table#sciout")

    def keys(self):
        return self.all_calc().find_elements(By.TAG_NAME, "tr")[1]

    def output(self):
        return self.driver.find_element(By.ID, "sciOutPut")

    def button(self, name):
        """
        optional names of buttons:
        'sin', 'cos', 'tan',
        'asin', 'acos', 'atan', 'pi', 'e',
        'pow', 'x3', 'x2', 'ex', '10x',
        'apow', '3x', 'sqrt', 'ln', 'log',
        '(', ')', '1/x', 'pc', 'n!'
        7, 8, 9, '+', 'bk'
        4, 5, 6, '-', 'ans'
        1, 2, 3, '*', 'M+'
        0, '.', 'EXP', '/', 'M-'
        '+/-', 'RND', 'C', '=', 'MR'
        """
        return self.driver.find_element(By.CSS_SELECTOR, f"""[onclick="r({name})"]""")

    def clicks(self, *buttons):
        self.button("'C'").click()
        for button in buttons:
            self.button(button).click()

