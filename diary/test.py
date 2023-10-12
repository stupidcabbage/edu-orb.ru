import dateparser

a = dateparser.parse("11.03",
                     settings={
                         "TIMEZONE": "Asia/Yekaterinburg",
                         "PREFER_DATES_FROM": "future"})
print(a)
