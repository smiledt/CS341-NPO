from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.forms import DeleteAccountForm, UserAccountForm, UserForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

# Create your views here.


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
            print(form.errors, account_form.errors)
    context = {'form': form, 'account_form': account_form,
               'registered': registered}
    return render(request, 'users/register.html', context)


@user_passes_test(lambda u: u.is_superuser)
def list_accounts(request):
    """ Lists user accounts so that they may be deleted """
    users = User.objects.order_by('username')
    error = ''
    users_dict = {'users': users, 'error': error}
    return render(request, 'users/user_list.html', users_dict)


@user_passes_test(lambda u: u.is_superuser)
def delete_account(request):
    """ Delete User Account """
    if request.method != 'POST':  # This means they clicked the delete button
        form = DeleteAccountForm()
        username = request.GET['delete']
        context = {'form': form, 'username': username, }
        return render(request, 'users/delete_account.html', context)
    else:
        form = DeleteAccountForm(data=request.POST)
        initial_user = User.objects.get(username=request.POST['delete'])
        if form.is_valid():
            users = User.objects.order_by('username')
            data = request.POST.copy()
            username_delete = data.get('username')
            print(username_delete)
            print(initial_user.username)
            if (username_delete == initial_user.username):
                message = 'User was deleted.'
                User.objects.filter(username=username_delete).delete()
                users_dict = {'users': users, 'message': message}
                return render(request, 'users/user_list.html', users_dict)
            else:  # The usernames did not match
                error = 'Usernames did not match. No user was deleted.'
                users_dict = {'users': users, 'message': error}
                return render(request, 'users/user_list.html', users_dict)

    context = {'form': form}
    return render(request, 'users/delete_account.html', context)
