"""Perform credit card calculations."""
from argparse import ArgumentParser
import sys

def get_min_payment(total_balance, fees = 0):
    """Computes the minumum credit card payment
    
    Args: 
        total_balance (float number): The total amount of the balance left 
            in the account that needs to be paid
        fees (int number): Any associated charges with the credit
            card account
    
    Returns:
        min_payment (int): The calculated minimum payment that 
            needs to be paid 
    """
    #Formula for calculating the minimum payment
    min_payment = ((total_balance * .02) + fees)
    if min_payment < 25:
        min_payment = 25
    return min_payment

def interest_charged(credit_balance, annual_APR): 
    """Computes the amount of interest accrued in the next payment 
    
    Args: 
        credit_balance (float): The balance of the credit card
        
        annual_APR (int): The annual APR for the account
    
    Returns:
        The interest accrued in each payment
    """
    #Formula for calculating the interest based on the credit card balance
    percent_to_float = annual_APR/100
    interest = (percent_to_float/365)*credit_balance*30
    return interest

def remaining_payments(credit_balance, annual_APR, targetamount, 
                       credit_line = 5000, fees = 0):
    """Computes the number of payments needed to pay off 
    the credit card balance
    
    Args:
        credit_balance (float): The balance of the credit card
        
        annual_APR (int): The annual APR, integer between 0 and 100
        
        target_payment (int): The amount the user wants to pay per payment
        
        credit_line (int): The credit line, or maximum amount the account 
        holder can keep in their account
        
        fees (int): The amount of fees that will be charged in addition 
        to the minimum payment
    
    Returns:
        The number of payments required to pay off the balance, also returns 
        the counters for each time the balance remains over 25%, 50%, and 75%
        
    Side Effects: 
    Alters the value of the credit card balance, subtracting 
    the value until it is zero.
    """
    #Create a variable that changes each time an amount is subtracted
    balance = credit_balance
    #Initialize a payment counter and counters for credit utilization
    payment_counter = 0
    one_third_balance_counter = 0
    half_balance_counter = 0
    three_fourths_balance_counter = 0
    while balance > 0:
        #If the target payment was passed as none, get the minimum payment
        #and subtract the interest from it 
        if targetamount == None:
            payment_amount = get_min_payment(balance,fees) - interest_charged(balance,annual_APR)
        #If a target payment was passed, calculate the payment amount
        #using the number passed
        elif targetamount is not None:
            payment_amount = targetamount - interest_charged(balance,annual_APR)
        if payment_amount < 0:
            "Card balance cannot be paid off"
            exit
        #The new balance will be the balance minus the payment amount
        balance = balance - payment_amount
        #Calculate the credit utilization and check to see if the balance
        #is above any of the percentages below
        credit_percentage = (balance/credit_line) *100
        
        if credit_percentage > 75:
            three_fourths_balance_counter += 1
        if credit_percentage > 50:
            half_balance_counter +=1
        if credit_percentage > 25:
            one_third_balance_counter += 1
        payment_counter += 1
    return payment_counter, one_third_balance_counter,\
    half_balance_counter,three_fourths_balance_counter

def main(balance, APR, targetamount = None, credit_line = 5000, fees = 0):
    """Calls the get_min_payment() function and displays it to the user.
    Also calls remaining_payments() and calculates the number of payments needed
    to pay off the credit card
    
    Args:
        balance (float): The balance of the credit card
        
        APR (int): The annual APR for the card
        
        target_payment(int): The amount the user wants to pay per payment
        
        credit_line(int): The max balance the account holder can have on their card
        
        fees(float): Any fees associated with the credit card
    
    Returns:
        A string that tells the user how many payments will be above the 25%, 50%, 
        and 75% thresholds.
    """
    #Calculate and display the minimum payment to the user
    minimum_payment = get_min_payment(balance,fees)
    print("Your reccomended starting payment is $",minimum_payment)
    #Create a variable and set it to false as long as a target payment is passed
    pays_minimum = False
    if targetamount == None:
        pays_minimum = True
    elif targetamount < minimum_payment:
        print("Your  target payment  is  less  than  the  \
              minimum  payment  for  this  credit  card")
        quit
    #If no target payment was passed through, calculate and display the number
    #of payments needed to pay off the balance
    if pays_minimum == True:
        total_payments = remaining_payments(balance, APR, targetamount, 
                                            credit_line, fees)
        print("If you pay the minimum payments  each  month, \
you  will  pay  off  the  balance  in ",  total_payments[0], " payments.")
    #If a target payment was passed through, use that value instead of the
    #minimum payment and display the number of payments needed to the user
    if pays_minimum == False:
        total_payments = remaining_payments(balance,APR,
                                            targetamount,credit_line,fees)
        print(f"If you make payments of ${targetamount} you will pay off \
the balance in {total_payments[0]} payments.")
    return (f"You will spend a total of {total_payments[1]} months over 25% \
 of the credit line\n\
You will spend a total of {total_payments[2]} months over 50% of the credit line\n\
You will spend a total of {total_payments[3]} months over 75% of the credit line")
        
def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them 
    through as arguments
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type = float, help = 'The total \
                        amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 'The annual APR, \
                        should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum \
                        amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The \
                        amount the user wants to pay per payment, \
                        should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees \
                        that are applied monthly.')
     #parse and validate arguments
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args
if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print(main(arguments.balance_amount, arguments.apr, targetamount = arguments.payment, 
               credit_line = arguments.credit_line, fees = arguments.fees))