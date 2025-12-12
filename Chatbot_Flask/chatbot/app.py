from flask import Flask, render_template, request, jsonify
import math
import random
from datetime import date

app = Flask(__name__, static_folder="static")
pending_task = None

# ---------------- FUNCTIONS ----------------
def rock_paper_scissors(user_choice):
    user_choice = user_choice.lower()
    options = ["rock", "paper", "scissors"]
    if user_choice not in options:
        return "Please choose: rock, paper, or scissors."
    bot_choice = random.choice(options)
    if user_choice == bot_choice:
        result = "It's a tie!"
    elif (user_choice=="rock" and bot_choice=="scissors") or \
         (user_choice=="paper" and bot_choice=="rock") or \
         (user_choice=="scissors" and bot_choice=="paper"):
        result = "You win! 🎉"
    else:
        result = "You lose! 😅"
    return f"You chose: {user_choice}\nBot chose: {bot_choice}\nResult: {result}"

def area_of_circle(radius):
    return math.pi * radius ** 2

def calculator(num1, operator, num2):
    if operator == '+': return num1 + num2
    elif operator == '-': return num1 - num2
    elif operator == '*': return num1 * num2
    elif operator == '/': return "Error: Division by zero" if num2 == 0 else num1 / num2
    else: return "Invalid operator!"

def vowel_or_consonant(char):
    char = char.lower()
    if char in 'aeiou': return "Vowel"
    elif char.isalpha(): return "Consonant"
    else: return "Invalid input"

def even_or_odd(number):
    return "Even" if number % 2 == 0 else "Odd"

def age_in_days(year, month, day):
    birth_date = date(year, month, day)
    today = date.today()
    return (today - birth_date).days

def day_by_number(day_num):
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return days[day_num-1] if 1 <= day_num <= 7 else "Invalid day number!"

def shortest_height(heights):
    return min(heights)

def avg_percentage_grade(marks):
    total = sum(marks)
    n = len(marks)
    average = total / n
    percentage = (total / (n*100)) * 100
    if percentage >= 90: grade = "A+"
    elif percentage >= 80: grade = "A"
    elif percentage >= 70: grade = "B"
    elif percentage >= 60: grade = "C"
    else: grade = "F"
    return average, percentage, grade

def discount_price(total, disc):
    return total * (1 - disc / 100)

def leap_year_check(year):
    if (year%4==0 and year%100!=0) or (year%400==0):
        return "Leap Year"
    else:
        return "Not a Leap Year"

def random_shayari():
    shayaris = [
        "Dil hi to hai na sang-o-khisht, dard se bhar na aaye kyun 💔 — Mirza Ghalib",
        "Shayad khuda ka iraada hai, hum akelay hi jeena seekh lein 😔 — Jaun Elia",
        "Aankhon me bas tu hai, baaki duniya ka kya hai? 🌙 — Modern",
        "Woh afsaana jise anjaam tak laana na ho mumkin, use ek khoobsurat modh dekar chhod do ✨ — Mirza Ghalib",
        "Tere jaane ka gham kam nahi hua, par tera intezar jeene ka bahaana ban gaya 💭 — Jaun Elia",
        "Tere bina adhura lagta hai har pal, Tu saath ho toh zindagi lage ek naya safar." 
        "Tum meri aakhri tamanna ho.\n" 
        "Mohabbat sirf lafzon ka khel nahi,\nYeh toh woh jazba hai jo rooh tak mehsoos hota hai",
        "Mohabbat Ko Mohabbat Se Mohabbat Ho gayi\nMohabbat Hi Mohabbat per Fida Ho Gai jab\nMohabbat Ko Mohabbat Se Mohabbat Na Mili 😢\nto Mohabbat Hi Mohabbat ki Maahabbat mein Fanaa ho gai 💔"
    ]
    return random.choice(shayaris)

def welcome_message():
    return (
        "Hi! My Name is Jamie and i am your assistant\n\n"
        "Main ye kaam kar sakta hoon:\n"
        "1️⃣ Find Area of Circle\n"
        "2️⃣ Calculate (+,-,*,/) step by step\n"
        "3️⃣ Vowel or Consonant Find\n"
        "4️⃣ Even or Odd Find\n"
        "5️⃣ Age in days Convert\n"
        "6️⃣ Name of day by number tell\n"
        "7️⃣ Shortest height student compare\n"
        "8️⃣ Average, Percentage and Grade find\n"
        "9️⃣ Discount on bill calculate\n"
        "1️⃣0️⃣ Leap Year Check\n"
        "1️⃣1️⃣ Rock–Paper–Scissors Game play🎮\n"
        "1️⃣2️⃣ Do poetry Shayari ❤️\n"
        "0️⃣ Exit\n\n"
        "Apna choice type karein (1-12) ya 0 to exit:\n"
        "So app kia karwana cahte hai 💭 ?? "
    )

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    global pending_task
    user_msg = request.form["msg"].strip()

    if pending_task is not None:
        task = pending_task['task']
        step = pending_task.get('step', None)
        try:
            if task == 'area':
                r = float(user_msg)
                pending_task = None
                reply = f"Area = {area_of_circle(r):.2f}"
            elif task == 'calculator':
                if step == 'operator':
                    if user_msg not in ['+', '-', '*', '/']:
                        return jsonify({"response":"Operator galat hai! (+,-,*,/). Try again:"})
                    pending_task['operator'] = user_msg
                    pending_task['step'] = 'num1'
                    return jsonify({"response":"Enter first number:"})
                elif step == 'num1':
                    pending_task['num1'] = float(user_msg)
                    pending_task['step'] = 'num2'
                    return jsonify({"response":"Enter second number:"})
                elif step == 'num2':
                    num1 = pending_task['num1']
                    num2 = float(user_msg)
                    operator = pending_task['operator']
                    result = calculator(num1, operator, num2)
                    pending_task = None
                    reply = f"Result: {result}"
            elif task == 'vowel':
                pending_task = None
                reply = f"{user_msg} is {vowel_or_consonant(user_msg)}"
            elif task == 'evenodd':
                pending_task = None
                reply = f"{user_msg} is {even_or_odd(int(user_msg))}"
            elif task == 'age':
                y, m, d = map(int, user_msg.split())
                pending_task = None
                reply = f"You are {age_in_days(y,m,d)} days old"
            elif task == 'day':
                pending_task = None
                reply = day_by_number(int(user_msg))
            elif task == 'shortest':
                heights = list(map(float, user_msg.split()))
                pending_task = None
                reply = f"Shortest = {shortest_height(heights)}"
            elif task == 'avg':
                marks = list(map(float, user_msg.split()))
                avg, perc, grade = avg_percentage_grade(marks)
                pending_task = None
                reply = f"Average: {avg:.2f}, Percentage: {perc:.2f}%, Grade: {grade}"
            elif task == 'discount':
                total, disc = map(float, user_msg.split())
                pending_task = None
                reply = f"Discounted: {discount_price(total, disc):.2f}"
            elif task == 'leap':
                pending_task = None
                reply = leap_year_check(int(user_msg))
            elif task == 'rps':
                pending_task = None
                reply = rock_paper_scissors(user_msg)
        except:
            reply = "Invalid input! Try again."
        return jsonify({"response": reply + "\n\n" + welcome_message()})

    # Normal commands
    if user_msg.lower() in ["hello","hi","salam"]:
        return jsonify({"response": welcome_message()})
    if user_msg == '1': pending_task = {'task':'area'}; return jsonify({"response":"Enter radius:"})
    if user_msg == '2': pending_task = {'task':'calculator','step':'operator'}; return jsonify({"response":"Enter operator (+,-,*,/):"})
    if user_msg == '3': pending_task = {'task':'vowel'}; return jsonify({"response":"Enter a character:"})
    if user_msg == '4': pending_task = {'task':'evenodd'}; return jsonify({"response":"Enter number:"})
    if user_msg == '5': pending_task = {'task':'age'}; return jsonify({"response":"Enter: year month day"})
    if user_msg == '6': pending_task = {'task':'day'}; return jsonify({"response":"Enter day number (1-7):"})
    if user_msg == '7': pending_task = {'task':'shortest'}; return jsonify({"response":"Enter heights separated by space:"})
    if user_msg == '8': pending_task = {'task':'avg'}; return jsonify({"response":"Enter marks separated by space:"})
    if user_msg == '9': pending_task = {'task':'discount'}; return jsonify({"response":"Enter: total discount%"})
    if user_msg == '10': pending_task = {'task':'leap'}; return jsonify({"response":"Enter year:"})
    if user_msg == '11': pending_task = {'task':'rps'}; return jsonify({"response":"rock, paper, scissors?"})
    if user_msg == '12': return jsonify({"response": random_shayari() + "\n\n❤️ Shayari by your bot ❤️"})
    if user_msg == '0': return jsonify({"response":"Bye! Khuda Hafiz 👋"})
    return jsonify({"response":"Sorry samajh nahi aaya.\n\n" + welcome_message()})

if __name__ == "__main__":
    app.run(debug=True)
