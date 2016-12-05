# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 18:59:01 2016

@author: andrew
"""

import numpy as np

class mortgage:
    def __init__(self, value, down, interest, term, tax_rate, 
                 maintenance_rate, insurance_rate, HOA_fees):
        
        if type(down) == float:
            down = down * value
        
        self.P = value - down
        
        self.value = value
        self.down = down
            
        self.N = term * 12
        self.i = interest/12
        
        self.mortgage_payment = self.calculate_mortgage_payment()
        
        self.monthly_tax = tax_rate * value / 12
        self.monthly_insurance = insurance_rate * value / 12
        self.monthly_upkeep = maintenance_rate * value / 12
        self.monthly_hoa = HOA_fees
        
        self.total_monthly = self.calculate_monthly_cost()
        
        self.total_cost = self.total_monthly * self.N + down
        
    def calculate_mortgage_payment(self):
        
        m_payment = self.i * (self.P*(1+self.i)**self.N)/( (1+self.i)**self.N - 1)
        
        return m_payment
    
    def calculate_monthly_cost(self):
        
        total = sum([self.mortgage_payment, self.monthly_tax, self.monthly_insurance,
                   self.monthly_upkeep, self.monthly_hoa])
        
        return total
        
    def __str__(self):
        
        fmt = '{0:30} $ {1:,.2f}'
        long_string = [
            'Monthly Breakdown',
            '-'*50,
            fmt.format('Mortgage Payment', self.mortgage_payment),
            fmt.format('Property Taxes', self.monthly_tax),
            fmt.format('Insurance', self.monthly_insurance),
            fmt.format('Maintenance Cost', self.monthly_upkeep),
            fmt.format('HOA Fees', self.monthly_hoa),
            "",
            fmt.format('Total Monthly Payment', self.total_monthly),
            "",
            "Total Costs",
            "-"*50,
            fmt.format('Total Cost of Home', self.total_cost),
            fmt.format('Total Cost minus Value', self.total_cost - self.value)
        ]

        return '\n'.join(long_string)
    
    def compare_with_rental(self, monthly_rent):
        
        print(self)
        
        rental_cost = monthly_rent * self.N
        print('\n')
        print('Comparison with Renting')
        print('-'*50)
        print('{0:30} $ {1:,.2f}'.format("Comparable Monthly Rent", monthly_rent))
        print('{0:30} $ {1:,.2f}'.format("Total Cost of Rental", rental_cost))
        # total savings
        print('{0:30} $ {1:,.2f}'.format("Savings over Renting", rental_cost - self.total_cost + self.value))
        
    def create_burndown(self):
        
        P = [self.P]
        I = [0]
        princ_contribution = [0]
        
        for i in range(self.N):
            interest = self.i * P[i]
            amt_to_principal = self.mortgage_payment - interest         
            P.append(P[i]-amt_to_principal)
            I.append(interest)
            princ_contribution.append(amt_to_principal)
            
        return princ_contribution, I
        
        
def inverse_payment_calculator(payment, 
                               down=.20, 
                               interest=0.04, 
                               term=30, 
                               tax_rate=0.02, 
                               maintenance_rate=0.01, 
                               insurance_rate=0.0035, 
                               HOA_fees=0):
    i = interest/12
    N = term * 12
    
    numerator = payment - HOA_fees
    denom = i*(1-down)*(1+i)**N/((1+i)**N - 1) + (tax_rate + insurance_rate + maintenance_rate)/12
    
    return numerator/denom