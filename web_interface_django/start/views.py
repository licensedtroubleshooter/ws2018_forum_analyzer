from django.shortcuts import render, redirect


def choice(request):
    return render(request, 'choice.html')
