from apps.client.models import ClientPayRoles
from django.db.models import Q


class SalaryFinder():
    
    def __init__(self,payrole= None):
        self.payrole    = payrole
        self.salary     = self.payrole.pay_values

    def evaluate_expression(self,expr):
        total = 0
        for term in expr:
            total += self.salary.get(term,0)
        return total
    
    
    def extract_variables(self,expr):
        parts = expr.replace("(", "").replace(")", "").split("-")
        variables = [part.split("+") for part in parts]
        return variables


    def total_salary(self):
        
        if self.payrole is None or self.payrole.company is None:
            return None
        
        salary_str = self.payrole.company.pay_structure
        
        positive_vars, negative_vars = self.extract_variables(salary_str)
        result = self.evaluate_expression(positive_vars) - self.evaluate_expression(negative_vars)

        print("result",result)
        self.payrole.final_salary = result
        self.payrole.save()

        return  result
    

