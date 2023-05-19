

class CalculatorRule:
    def __init__(self, id=0,
                 expression='',
                 cause='',
                 rec='',
                 var='',
                 val='',
                 spr=True,
                 aut=True):
        self.db_id =id
        self.expression =expression
        self.cause = cause
        self.recommendation = rec
        self.variable = var
        self.value = val
        self.for_autumn = aut
        self.for_spring = spr

    def __str__(self):
        return self.expression

