from django.shortcuts import render

# Create your views here.ArithmeticError
def main(request):
    return render(request, 'index.html')