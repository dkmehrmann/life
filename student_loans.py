# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 19:01:42 2016

@author: andrew
"""

import datetime
import pandas as pd

class loan:
    def __init__(self, name, princ, i_rate, i_start_date, today=datetime.date.today()):
        self.name = name
        self.princ = princ
        self.i_rate = i_rate
        self.i_start_date = i_start_date
        self.today = today
        
        days = (today-i_start_date).days
        if days <= 0:
            days = 0
            
        self.i_accrued = self.calc_interest(i_start_date, today)
        self.total = self.princ + self.i_accrued
        
    def calc_interest(self, start, end):
        if start < self.i_start_date:
            return 0
        days = (end - start).days
        if days <= 0:
            days = 0
        return days * self.i_rate * self.princ / 365        
    
    def pass_month(self):
        days_per_month = 365.25/12
        next_time = self.today + datetime.timedelta(days = days_per_month)
        
        self.i_accrued += self.calc_interest(self.today, next_time)
        
        self.today = next_time
        self.total = self.princ + self.i_accrued        
        
    
    def make_payment(self, amt):
        
        if amt > self.i_accrued:
            amt -= self.i_accrued
            self.i_accrued = 0
            if amt > self.princ:
                amt -= self.princ
                self.princ = 0
            else:
                self.princ -= amt
                amt = 0
        else:
            self.i_accrued -= amt
            amt = 0
        
        self.total = self.princ + self.i_accrued
        
            
        return amt
            
        
    def __str__(self):
        q = 'Name: {0}\nPrincipal: {1}\nInterest Rate: {2:0.2%}\nTotal: {3:0.2f}'
        return q.format(self.name, self.princ, self.i_rate, self.total)
    
    
class portfolio:
    def __init__(self):
        self.loans = []
        self.total = 0
        self.payments_made = 0
    
    def add_loan(self, one_loan):
        self.loans.append(one_loan)
        self.total += one_loan.total
        
    def __str__(self):
        for l in self.loans:
            print(l, "\n")
            
        total = sum([x.total for x in self.loans])
        return "Total Portfolio Size: {0:0.2f}".format(total)
    
    def pass_month(self):
        for x in self.loans:
            x.pass_month()
        self.total = sum([x.total for x in self.loans])
        
        return self
    
    def make_payment(self, amt):
        
        df = pd.DataFrame({
            'interest': [x.i_rate for x in self.loans],
            'principal': [x.princ for x in self.loans]
        })
        
        priorities = df.sort(['interest', 'principal'], ascending=False).index
        
        self.total = sum([x.total for x in self.loans])
        
        for l in priorities:
            amt = self.loans[l].make_payment(amt)
            self.total = sum([x.total for x in self.loans])
            if amt == 0 or self.total <= 0:
                break
                
        self.payments_made += 1

        return self
    
    def pay_loans(self, monthly):
        
        while self.total > 0:
            prev_tot = self.total
            self.make_payment(monthly).pass_month()

        print("Paid off in {0} months at ${1} per month".format(self.payments_made, monthly))
        print("Total paid ${0}".format(self.payments_made * monthly -(monthly - prev_tot)))