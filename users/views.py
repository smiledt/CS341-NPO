from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserForm, UserAccountForm

# Create your views here.


def register(request):
    """ Register a new user """

    registered = False
    if request.method != 'POST':
        form = UserForm()
        account_form = UserAccountForm()
    else:
        form = UserForm(data=request.POST)
        account_form = UserAccountForm(data=request.POST)

        if form.is_valid() and account_form.is_valid():
            new_user = form.save()
            new_user.set_password(new_user.password)
            new_user.save()
            account = account_form.save(commit=False)
            account.user = new_user
            account.save()

            registered = True
            login(request, new_user)
            return redirect('book_keeping:index')
        else:
            print(form.errors, account_form.errors)
    context = {'form': form, 'account_form': account_form,
               'registered': registered}
    return render(request, 'users/register.html', context)
