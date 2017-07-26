# diary/views.py
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from .models import Diary
from django.contrib.auth.decorators import login_required
from .forms import DiaryForm
from django.utils import timezone


@login_required
def diary_list(request):

    user_idx = request.user.id
    diary = Diary.objects.filter(user_id=user_idx, created_at__day=timezone.now().day)  #오늘것만에 대해서 다이어리 보여주기

    ctx = {
        'diary': diary,
    }
    return render(request, 'diary/diary_list.html', ctx)


@login_required
def diary_detail(request, pk):
    diary = get_object_or_404(Diary, pk=pk)

    # 글의 유저인덱스와 로그인한 유저인덱스의 값이 다를 경우 되돌려보냄
    if diary.user_id != request.user.id:
        return redirect('diary:diary_list')

    ctx = {
        'diary': diary
    }
    return render(request, 'diary/diary_detail.html', ctx)


@login_required
def diary_new(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('diary:diary_list')

    else:
        form = DiaryForm()

    ctx = {
        'form': form
    }
    return render(request, 'diary/diary_new.html', ctx)


@login_required
def diary_edit(request, pk):
    diary = get_object_or_404(Diary, id=pk)

    # 글의 유저인덱스와 로그인한 유저인덱스의 값이 다를 경우 되돌려보냄
    if diary.user_id != request.user.id:
        return redirect('diary:diary_list')

    # 질문 등록 날짜와 현재 날짜가 다르면 수정 불가
    if diary.created_at.day != timezone.now().day:
        return redirect('diary:diary_detail', pk)

    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES, instance=diary)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('diary:diary_detail', pk)
    else:
        form = DiaryForm()

        ctx = {
            'form': form
        }
        return render(request, 'diary/diary_edit.html', ctx)


@login_required
def diary_delete(request, pk):
    diary = get_object_or_404(Diary, id=pk)

    # 글의 유저인덱스와 로그인한 유저인덱스의 값이 다를 경우 되돌려보냄
    if diary.user_id != request.user.id:
        return redirect('diary:diary_list')

    # 질문 등록 날짜와 현재 날짜가 다르면 수정 불가
    if diary.created_at.day != timezone.now().day:
        return redirect('diary:diary_detail', pk)
    else:
        diary.delete()
        return redirect('diary:diary_list')
