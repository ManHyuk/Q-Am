import time


def get_today_id():
    #지금 시간에 해당하는 question id  return하는 함수
    now = time.localtime()
    year_now = now.tm_year  #올해 몇년?
    is_leap_year = False    #윤년
    if year_now%4 == 0:
        is_leap_year = True
        if year_now&100 == 0:
            is_leap_year = False
            if year_now%400 == 0:
                is_leap_year = True
    if is_leap_year:
        today_id = now.tm_yday
    else:
        if now.tm_mon <= 2:
            today_id = now.tm_yday
        else:
            today_id = now.tm_yday + 1
    if now.tm_hour < 4:     #새벽4시에 업데이트, so 그 전에는 같은 질문으로 뜨도록
        today_id = today_id - 1
    if not today_id:    #위 때문에 0이 되면 id가 366으로 리턴이 되게 함
        today_id = 366
    return today_id
