import random

def get_random_number():
    return random.randint(1, 100)

def get_guess_state_and_message(current_guess, thought_number):
    if current_guess == thought_number:
        return (True, f"И это правильно! Я загадал число <b>{thought_number}</b>.\nЯ загадал новое число, если " \
                      "хочешь продолжить - пиши новое число")
    elif current_guess > thought_number:
        return False, f"Меньше чем <b>{current_guess}</b>"
    else:
        return False, f"Больше чем <b>{current_guess}</b>"