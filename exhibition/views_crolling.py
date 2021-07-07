from django.shortcuts import render, redirect
from django.contrib import messages


def reset_exhibitions(request):
    # messages.INFO()
    messages.add_message(request, messages.SUCCESS, "리셋 되었습니다.")
    # messages.add_message(request, messages.INFO, "리셋 되었습니다.")
    # messages.add_message(request, messages.WARNING, "리셋 되었습니다.")
    # messages.add_message(request, messages.WARNING, "리셋 되었습니다.")
    # messages.info(request, )
    # messages.success(request, "reset")
    return redirect('/info/')
