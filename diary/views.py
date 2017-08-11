# diary/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Diary
from django.contrib.auth.decorators import login_required
from .forms import DiaryForm
from django.utils import timezone
from django.contrib import messages


@login_required
def diary_list(request):
    user_idx = request.user.id
    diary = Diary.objects.filter(user_id=user_idx, created_at__day=timezone.now().day)  #오늘것만에 대해서 다이어리 보여주기

    week = ('월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일')
    #한글 안먹으면 아래 week로 해보세요
    #week = ('MONDAY','THESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY')
    now=timezone.now()
    month=now.month
    day=now.day
    week_day=week[now.weekday()]
    #그날의 날짜와 요일을 보여줌
    ctx = {
        'diary': diary,
        'month':month,
        'day':day,
        'week_day':week_day,
    }
    return render(request, 'diary/diary_list.html', ctx)

@login_required
def diary_search_title(request):
    if request.GET.get('search_title'):
        search_title=request.GET.get('search_title')
        search_diary_title = Diary.objects.filter(title__icontains=search_title,user=request.user)

        if search_diary_title.count()==0:
            messages.info(request, '검색결과가 없습니다')
            return redirect('diary:diary_search_title')

        return render(request, 'diary/diary_search_title.html',{
            'search_diary_title':search_diary_title,
            'search_title':search_title,
        })
    else:
        return render(request, 'diary/diary_search_title.html')


@login_required
def diary_search_content(request):
    if request.GET.get('search_content'):
        search_content=request.GET.get('search_content')
        search_diary_content = Diary.objects.filter(content__icontains=search_content,user=request.user)

        if search_diary_content.count()==0:
            messages.info(request, '검색결과가 없습니다')
            return redirect('diary:diary_search_content')

        return render(request, 'diary/diary_search_content.html',{
            'search_diary_content':search_diary_content,
            'search_content':search_content,
        })
    else:
        return render(request, 'diary/diary_search_content.html')

@login_required
def diary_search_day(request):
    if request.GET.get('search_day'):
        search_day=request.GET.get('search_day')
        daylist=search_day.split('-')
        if daylist[1]<'10':
            daylist[1]=list(daylist[1])[1]
        if daylist[2]<'10':
            daylist[2]=list(daylist[2])[1]
        search_diary_day=Diary.objects.filter(created_at__year=daylist[0],created_at__month=daylist[1],created_at__day=daylist[2],user=request.user)

        if search_diary_day.count()==0:
            messages.info(request, '검색결과가 없습니다')
            return redirect('diary:diary_search_day')

        return render(request, 'diary/diary_search_day.html',{
            'search_diary_day':search_diary_day,
            'search_day':search_day,
        })
    else:
        return render(request, 'diary/diary_search_day.html')
    #제목,내용,날짜 검색으로 자신이 쓴 다이어리만 검색이 가능



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

    diary_num=Diary.objects.filter(user=request.user,created_at__year=timezone.now().year,created_at__month=timezone.now().month,created_at__day=timezone.now().day).count()

    if diary_num >= 5 :
        messages.info(request, ' 오늘 입력 가능한 다이어리 수를 초과했습니다.')
        return redirect('diary:diary_list')


    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('diary:diary_list')

    else:
        form = DiaryForm()

    week = ('월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일')
    #한글 안먹으면 아래 week로 해보세요
    #week = ('MONDAY','THESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY')
    now=timezone.now()
    month=now.month
    day=now.day
    week_day=week[now.weekday()]
    #그날의 날짜와 요일을 보여줌
    ctx = {
        'form': form,
        'month':month,
        'day':day,
        'week_day':week_day,
    }
    return render(request, 'diary/diary_new.html', ctx)


@login_required
def diary_edit(request, pk):
    diary = get_object_or_404(Diary, id=pk)
    diary_title=diary.title
    diary_content=diary.content

    # 글의 유저인덱스와 로그인한 유저인덱스의 값이 다를 경우 되돌려보냄
    if diary.user_id != request.user.id:
        return redirect('diary:diary_list')

    # 질문 등록 날짜와 현재 날짜가 다르면 수정 불가
    if diary.created_at.day != timezone.now().day:
        return redirect('diary:diary_list')

    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES, instance=diary)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('diary:diary_list')
    else:
        form = DiaryForm()

        week = ('월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일')
        # 한글 안먹으면 아래 week로 해보세요
        # week = ('MONDAY','THESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY')
        now = timezone.now()
        month = now.month
        day = now.day
        week_day = week[now.weekday()]
        # 그날의 날짜와 요일을 보여줌

        ctx = {
            'form': form,
            'diary_title':diary_title,
            'diary_content':diary_content,
            'month': month,
            'day': day,
            'week_day': week_day,
        }
        return render(request, 'diary/diary_new.html', ctx)


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
