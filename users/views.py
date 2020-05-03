from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegForm, DeleteAccountForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

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

@user_passes_test(lambda u: u.is_superuser)
def delete_account(request):
    # Delete User Account
    if request.method != 'POST':
        form = DeleteAccountForm()
    else:
        form = DeleteAccountForm(request.POST)

        if form.is_valid():
            data = request.POST.copy()
            username_delete = data.get('username')
            User.objects.filter(username=username_delete).delete()
            return redirect('book_keeping:index')

    context = {'form' : form}
    return render(request, 'users/delete_account.html', context)

# @user_passes_test(lambda u: u.is_superuser)
# def summary_report(request):
# 	# Summary Report
# 	if request.method != 'POST':
# 		form = SummaryForm()
# 	else:
# 		form = SummaryForm(request.POST)

# 		if form.is_valid():
# 			data = request.POST.copy()
# 			username_report = data.get('username')
# 			d = Donation.objects.filter(username=username_report)
# 			print('\n')
# 			print(d)
# 			print('\n')

# 			return redirect('book_keeping:summary_report')

# 	context = {'form' : form }
# 	return render(request, 'users/summary_report.html', context)





