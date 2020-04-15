from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegForm

# Create your views here.


def register(request):
    # Register a new user
    if request.method != 'POST':
        form = RegForm()

    else:
        form = RegForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('book_keeping:index')
    context = {'form': form}
    return render(request, 'users/register.html', context)
