from django.shortcuts import render

# Create your views here.
number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
operator = ["+", "-", "*", "/"]
equal = "="
maxDispLength = 19

def compute(a, b, operator):
    result = 0
    if operator == "+":
        result = int(a) + int(b)
    elif operator == "-":
        result = int(a) - int(b)
    elif operator == "*":
        result = int(a) * int(b)
    elif operator == "/":
        try:
            result = int(a) / int(b)
        except ZeroDivisionError:
            result = "Error"
    return result


def initDisp():
    return {"result": 0, "a": 0, "operator": "+", "b": 0, "error": 0}


def errorDisp():
    return {"error": 1, "result": "Error"}


def resultDisp(request, button):
    a = request.POST["firstArg"]
    b = request.POST["secondArg"]
    operator = request.POST["operator"]

    result = compute(a, b, operator)
    if result == "Error":
        disp = errorDisp();
    else:
        a = 0
        b = 0
        operator = "+"
        disp = {"firstArg": a, "secondArg": b, "operator": operator, "result": result}
    return disp;


def requestHandler(request):
    if request.method == "GET":
        disp = {"result": 0, "firstArg": 0, "operator": "+", "secondArg": 0, "error": 0}
        return render(request, "calculator/calculator.html", disp)
    if request.method == "POST":
        if request.POST["error"] == "1":
            disp = errorDisp()
        else:
            for key in request.POST.keys():
                if key in number:
                    disp = argHandler(request, key)
                elif key in operator:
                    disp = operatorHandler(request, key)
                elif key == equal:
                    disp = resultDisp(request, key)
        return render(request, "calculator/calculator.html", disp)


def argHandler(request, val):
    firstArg = request.POST["firstArg"]
    secondArg = request.POST["secondArg"]
    operator = request.POST["operator"]

    if secondArg == "0":
        secondArg = val
    elif len(secondArg) < maxDispLength:
        secondArg += val
    context = {"firstArg": firstArg, "secondArg": secondArg, "operator": operator, "result": secondArg}
    return context


def operatorHandler(request, key):
    a = request.POST["firstArg"]
    b = request.POST["secondArg"]
    operator = request.POST["operator"]
    a = compute(a, b, operator)

    if a == "Error":
        disp = errorDisp();
    else:
        b = 0
        operator = key
        disp = {"firstArg": a, "secondArg": b, "operator": operator, "result": a}
    return disp;
