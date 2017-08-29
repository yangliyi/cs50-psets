import cs50 

while True:
    print("O hai! How much change is owed?")
    cents = cs50.get_float();
    if cents >= 0:
        break

float_dollar = cents * 100;
dollar = round(float_dollar);
number_of_coins = 0
while(dollar >= 25):
    dollar -= 25
    number_of_coins += 1

while(dollar >= 10):
    dollar -= 10
    number_of_coins += 1
    
while(dollar >= 5):
    dollar -= 5;
    number_of_coins += 1;

print("{}".format(number_of_coins + dollar))