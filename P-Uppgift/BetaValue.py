class BetaValue:
    def __init__(self, company, beta_value):
        self.__company = company
        self.__beta_value = beta_value

    def __str__(self):
        return "{}: {}".format(self.__company, self.__beta_value)

    def __lt__(self, other):
        return self.__beta_value < other.__beta_value

    def __gt__(self, other):
        return other < self

    def get_company(self):
        return self.__company

    def get_beta_value(self):
        return self.__beta_value
