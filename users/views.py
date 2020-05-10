from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.forms import DeleteAccountForm, UserAccountForm, UserForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

# Create your views here.


# def register(request):
#     # Register a new user
#     if request.method != 'POST':
#         form = RegForm()
#
#     else:
#         form = RegForm(data=request.POST)
#
#         if form.is_valid():
#             new_user = form.save()
#             login(request, new_user)
#             return redirect('book_keeping:index')
#     context = {'form': form}
#     return render(request, 'users/register.html', context)

def register(request):
    """ Register a new user """

    # Set registered to false by default
    registered = False
    if request.method != 'POST':  # This SHOULD always be post
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
            print("Something broke!")  # TODO: Debugging, delete this
            print(form.errors, account_form.errors)
    context = {'form': form, 'account_form': account_form,
               'registered': registered}
    return render(request, 'users/register.html', context)


@user_passes_test(lambda u: u.is_superuser)
def list_accounts(request):
    """ Lists user accounts so that they may be deleted """
    users = User.objects.order_by('username')
    users_dict = {'users': users}
    return render(request, 'users/user_list.html', users_dict)


@user_passes_test(lambda u: u.is_superuser)
def delete_account(request):
    """ Delete User Account """
    if request.method != 'POST':  # This means they clicked the delete button
        form = DeleteAccountForm()
        username = request.GET['delete']
        context = {'form': form, 'username': username}
        return render(request, 'users/delete_account.html', context)
    else:
        form = DeleteAccountForm(request.POST) 
        if form.is_valid():
            data = request.POST.copy()
            username_delete = data.get('username')
            User.objects.filter(username=username_delete).delete()
            return redirect('book_keeping:admin_index')

    context = {'form': form}
    return render(request, 'users/delete_account.html', context)
