from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.db.models.functions import Length, ExtractHour
import datetime, requests, json, hmac, hashlib, secrets
from dateutil import relativedelta
import emoji, editdistance
from collections import Counter
from os import getenv

# from .title_gen_inference import generate_text, load_generator_model, getRandomChar

from .models import Entry, APIData, EntryFilter

CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
USER_ID = "71092938" # xQc Twitch ID
TIMEZONES = ["UTC", "CET", "US/Pacific", "US/Central", "US/Eastern", "Asia/Hong_Kong", "Australia/Sydney"]

def getAccessToken():
    return getattr(APIData.objects.last(), "accessToken", None)

def Percent(a, b):
    if b == 0: return 0
    return round(a / b * 100)

def GetFilterIDs(name: str):
    try:
        ids = EntryFilter.objects.get(name=name).entryIDs
    except:
        ids = []
    return ids

def GetFilterDate(name="Duplicates"):
    try:
        lastChanged = getattr(EntryFilter.objects.get(name=name), "lastChanged", "N/A")
    except:
        return "N/A"

    if lastChanged != "N/A":
        return timezone.localtime(lastChanged).strftime('%d/%m/%Y')

duplicates = False

def Entries(includeDuplicates = None, ordering = "-time", years = None, months = None):
    if includeDuplicates is None: includeDuplicates = duplicates
    if includeDuplicates:
        res =  Entry.objects
    else:
        res = Entry.objects.exclude(id__in=GetFilterIDs("Duplicates"))

    if years is not None:
        res = res.filter(time__year__in=years)
    if months is not None:
        res = res.filter(time__month__in=months)

    if isinstance(ordering, list):
        return res.order_by(*ordering)
    else:
        return res.order_by(ordering)

# ----------------------- Index -----------------------

def index(request):
    if "timezone" in request.GET:
        request.session['django_timezone'] = request.GET['timezone']
        return HttpResponse("done")
    if 'json' in request.GET:
        return JsonResponse([{
            "time": timezone.localtime(entry.time).strftime('%d/%m/%Y | %H:%M'),
            "title": f'<div class="text-break">{entry.title}</div>',
            "category": entry.category} for entry in Entries(request.GET.get("duplicates", "no") == "yes")], safe=False)

    return render(request, 'main/index.html', {'timezones': TIMEZONES,
                                                "context": {"ndLastReview": GetFilterDate(),
                                                            "entryCount": Entry.objects.all().count(),
                                                            "filterCount": len(GetFilterIDs("Duplicates"))}})

# ----------------------- Statistics -----------------------

def GetWordList(string: str, lowercase = True):
    titles = string.translate(str.maketrans('?!\n"()[]{}|;/<>&=',
                                            "                 "))
    more_filters = ['. ', ' .', '..', '...', '....', '^ ', ' ^', '* ', ' *', ', ', ' ,', '- ', ' -', '_ ', ' _', ' : ', ' # ', '@ ', '— ', ' —', ' ~ ', ' + ', ' - ', ' $ ']
    while True:
        action = False
        for f in more_filters:
            n = titles.replace(f, " ")
            if n != titles:
                action = True
                titles = n
        if not action:
            break

    emoji.replace_emoji(titles, replace=' ')
    titles = titles.encode("ascii", "ignore").decode()
    if lowercase:
        titles = titles.lower()

    return titles.split()

def s8Data(entries, div):
    entryCount = entries.count()
    titles = " ".join(list(entries.values_list("title", flat=True)))
    charCount = len(titles) - entryCount
    return {"entryCount": round(entryCount / div, 1),
            "charCount": round(charCount / div),
            "emojiCount": round(emoji.emoji_count(titles, unique=False) / div, 1),
            "timePeriod": div}

def s1(params:QueryDict = None, init = False):
    if init:
        years = [d.year for d in Entries().dates("time", "year")]
        return {"years": years,
                "cardContentID": params.get("cardContentID", "0")}

    titles = " ".join(list(Entries(years=params.getlist("years[]"), months=params.getlist("months[]")).values_list("title", flat=True)))
    return [{"word": f'<div class="text-break">{r[0]}</div>', "count": r[1]} for r in Counter(GetWordList(titles)).most_common()]

def s2(params:QueryDict = None, init = False):
    if init:
        years = [d.year for d in Entries().dates("time", "year")]
        return {"years": years,
                "cardContentID": params.get("cardContentID", "0")}

    titles = " ".join(list(Entries(years=params.getlist("years[]"), months=params.getlist("months[]")).values_list("title", flat=True)))
    titles = [e["emoji"] for e in emoji.emoji_list(titles)]
    return [{"word": f'<div class="text-break">{r[0]}</div>', "count": r[1]} for r in Counter(titles).most_common()]

def s3(params:QueryDict = None, init = False):
    if init:
        years = [d.year for d in Entries().dates("time", "year")]
        return {"years": years,
                "cardContentID": params.get("cardContentID", "0")}

    entries = Entries(years=params.getlist("years[]"), months=params.getlist("months[]"))
    titles = " ".join(list(entries.values_list("title", flat=True)))

    entryCount = entries.count()
    charCount = len(titles) - len(entries)
    letterCount = 0
    capitalLetterCount = 0
    for char in titles:
        if char.isalpha():
            letterCount += 1
            if char.isupper():
                capitalLetterCount += 1

    return {"entryCount": entryCount,
            "days": entries.dates("time", "day").count(),
            "charCount": charCount,
            "letterUsage": Percent(letterCount, charCount),
            "capitalLetterUsage": Percent(capitalLetterCount, charCount),
            "emojiCount": emoji.emoji_count(titles)}

def s4(params:QueryDict = None, init = False):
    if init:
        years = [d.year for d in Entries().dates("time", "year")]
        return {"years": years,
                "cardContentID": params.get("cardContentID", "0")}

    categories = list(Entries(years=params.getlist("years[]"), months=params.getlist("months[]")).values_list("category", flat=True))
    c = Counter(categories).most_common()
    other = [i for i in c[10:]]
    labels = [r[0] for r in c[:8]]
    data = [r[1] for r in c[:8]]
    if other:
        labels.append("Other")
        data.append(sum([r[1] for r in other]))
    return {"labels": labels,
            "data": data,
            "other": [f"{r[0]} ({r[1]})" for r in other[:10]] + (["..."] if len(other) > 10 else [])}

def s5(params:QueryDict = None, init = False):
    if init:
        return {"cardContentID": params.get("cardContentID", "0")}

    entries = Entries(ordering=[Length("title").desc(), "-time"])
    return [{
            "time": timezone.localtime(entry.time).strftime('%d/%m/%Y | %H:%M'),
            "title": f'<div class="text-break">{entry.title}</div>',
            "length": len(entry.title)} for entry in entries]

def s6(params:QueryDict = None, init = False):
    if init:
        return {"cardContentID": params.get("cardContentID", "0")}
    entries = sorted(Entries(),
                    key=lambda e: (Percent(sum(1 for c in e.title if c.isupper()), sum(1 for c in e.title if c.isalpha())),
                                sum(1 for c in e.title if c.isalpha())), reverse=True)
    amounts = [(sum(1 for c in entry.title if c.isupper()), sum(1 for c in entry.title if c.isalpha())) for entry in entries]
    return [{
            "time": timezone.localtime(entry.time).strftime('%d/%m/%Y | %H:%M'),
            "title": f'<div class="text-break">{entry.title}</div>',
            "capsAmount": amounts[i][0],
            "caps%": Percent(amounts[i][0], amounts[i][1])} for i, entry in enumerate(entries)]

def s7(params:QueryDict = None, init = False):
    if init:
        years = [d.year for d in Entries().dates("time", "year")]
        return {"years": years,
                "cardContentID": params.get("cardContentID", "0")}

    data = Entries(years=params.getlist("years[]"), months=params.getlist("months[]")
    ).annotate(
        hour = ExtractHour('time'),
    ).values(
        'hour'
    ).annotate(
        n=Count('pk')
    ).order_by('hour')

    data = Counter({d['hour']: d['n'] for d in data})
    return {"data": [data[i] for i in range(24)]}

def s8(params:QueryDict = None, init = False):
    entries = Entries()

    # Weekly stats
    latestDate = entries.first().time.date()
    dateFrom = datetime.date(2020, 12, 28)
    dateTo = latestDate - datetime.timedelta(days=latestDate.weekday())
    div = (dateTo - dateFrom).days // 7
    weekData = s8Data(entries.filter(time__range=(dateFrom, dateTo)), div)

    # Monthly stats
    dateFrom = datetime.date(2021, 1, 1)
    dateTo = datetime.date(latestDate.year, latestDate.month, 1)
    delta = relativedelta.relativedelta(dateTo, dateFrom)
    div = delta.years * 12 + delta.months
    monthData = s8Data(entries.filter(time__range=(dateFrom, dateTo)), div)

    # Yearly stats
    dateTo = datetime.date(latestDate.year, 1, 1)
    div = dateTo.year - dateFrom.year
    yearData = s8Data(entries.filter(time__range=(dateFrom, dateTo)), div)

    return {"weekData": weekData,
            "monthData": monthData,
            "yearData": yearData,
            "cardContentID": params.get("cardContentID", "0")}

def s9(params:QueryDict = None, init = False):
    if init:
        years = [d.year for d in Entries().dates("time", "year")]
        return {"years": years,
                "cardContentID": params.get("cardContentID", "0")}

    titleList = list(Entries(years=params.getlist("years[]"), months=params.getlist("months[]")).values_list("title", flat=True))
    chars = Counter("".join(titleList).lower()).most_common()
    cWords = Counter(map(lambda w: w[0], GetWordList(" ".join(titleList))))
    cTitles = Counter(map(lambda t: t[0], titleList))
    data = []
    for char, count in chars:
        if char == "": continue
        data.append({"character": char,
                    "count": count,
                    "1word": cWords.get(char),
                    "1title": cTitles.get(char)})
    return data

statArgs = {
    "1": s1,
    "2": s2,
    "3": s3,
    "4": s4,
    "5": s5,
    "6": s6,
    "7": s7,
    "8": s8,
    "9": s9,
}

def statistics(request):
    if request.method == "POST":
        if "duplicates" in request.POST:
            global duplicates
            duplicates = request.POST.get("duplicates") == "false"
            print(duplicates)
            return HttpResponse(duplicates)

        id = request.POST.get("id")
        return render(request, f'main/stats/{id}.html', statArgs[id](request.POST, True))
    else:
        if "timezone" in request.GET:
            request.session['django_timezone'] = request.GET['timezone']
            return HttpResponse("done")
        if "json" in request.GET:
            return JsonResponse(statArgs[request.GET.get("json", "1")](request.GET), safe=False)

        return render(request, 'main/statistics.html', {"timezones": TIMEZONES,
                                                        "context": {"ndLastReview": GetFilterDate(),
                                                                    "entryCount": Entry.objects.all().count(),
                                                                    "filterCount": len(GetFilterIDs("Duplicates"))},
                                                        "t": request.GET.get("t", 0)})

# ----------------------- Generator -----------------------
# model = None

# def generator(request):
#     if request.method == "POST":
#         global model
#         if not model:
#             model = load_generator_model()

#         try:
#             startString = request.POST.get("startInput")
#             minLength = int(request.POST.get("minLength"))
#             temperature = float(request.POST.get("temperature"))
#         except Exception as e:
#             return JsonResponse({"result": str(e)}, safe=False)

#         if not startString:
#             startString = getRandomChar()

#         result = generate_text(model, startString, temperature, minLength)
#         entries = sorted(Entries(False).exclude(id__in=GetFilterIDs("AI")), key=lambda e: editdistance.eval(result, e.title))[:3]
#         distances = [editdistance.eval(result, e.title) for e in entries]
#         similars = [
#             {"time": timezone.localtime(entry.time).strftime('%d/%m/%Y | %H:%M'),
#             "title": f'<div class="text-break">{entry.title}</div>',
#             "distance": distances[i]} for i, entry in enumerate(entries)]

#         return JsonResponse({"result": result,
#                             "similars": similars}, safe=False)

#     return render(request, 'main/generator.html')

# ----------------------- Admin -----------------------

@user_passes_test(lambda u: u.is_superuser)
def get_token(request):
    url = "https://id.twitch.tv/oauth2/token"
    body = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            "grant_type": "client_credentials"}

    response = requests.post(url, body)
    if 200 <= response.status_code < 300:
        try:
            content = json.loads(response.content.decode('utf-8'))
            token = content["access_token"]
            expires = int(content["expires_in"])
        except Exception as e:
            return HttpResponse(f"Unexpected Error: {e} | STATUS: {response.status_code} | Content: {response.content}")

        if APIData.objects.exists():
            APIData.objects.all().update(accessToken = token, accessTokenExpireDate = datetime.datetime.fromtimestamp(datetime.datetime.timestamp(datetime.datetime.now())+expires))
        else:
            new = APIData(accessToken = token, accessTokenExpireDate = datetime.datetime.fromtimestamp(datetime.datetime.timestamp(datetime.datetime.now())+expires))
            new.save()

        return HttpResponse(f"Success | STATUS: {response.status_code} | Expires: {content['expires_in']}")
    else:
        return HttpResponse(f"Unexpected Error | STATUS: {response.status_code} | Content: {response.content}")

@user_passes_test(lambda u: u.is_superuser)
def subscribe(request):
    url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    headers = {"Client-ID": CLIENT_ID,
            "Authorization": "Bearer " + getAccessToken(),
            "Content-Type": "application/json"}

    mode = request.GET.get("mode")
    if mode == "subscribe":
        callback_url = "https://terraa.eu.pythonanywhere.com/callback/"

        secret = secrets.token_hex(32)
        APIData.objects.all().update(verificationSecret = secret)

        body = {"type": "channel.update",
                "version": "1",
                "condition": {"broadcaster_user_id": USER_ID},
                "transport": {"method": "webhook",
                                "callback": callback_url,
                                "secret": secret}}

        response = requests.post(url, data=json.dumps(body), headers=headers)
        return HttpResponse(f'STATUS: {response.status_code} | Content: {response.content}')
    elif mode == "unsubscribe":
        if APIData.objects.exists():
            sub_id = getattr(APIData.objects.last(), "subscriptionID", None)
            response = requests.delete(url, params={"id": sub_id}, headers=headers)
            return HttpResponse(f'STATUS: {response.status_code} | Content: {response.content}')
    else:
        return HttpResponse("Unknown request")

@user_passes_test(lambda u: u.is_superuser)
def list_subs(request):
    url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    headers = {"Client-ID": CLIENT_ID,
            "Authorization": "Bearer " + getAccessToken()}

    response = requests.get(url, headers=headers)
    return HttpResponse(f'STATUS: {response.status_code} | Content: {response.content}')

@user_passes_test(lambda u: u.is_superuser)
def duplicate_filter(request):
    if "filterEntry" in request.GET:
        filter = EntryFilter.objects.get(name="Duplicates")
        entryID = int(request.GET["filterEntry"])
        if entryID not in filter.entryIDs:
            filter.entryIDs.append(entryID)
        else:
            filter.entryIDs.remove(entryID)

        filter.lastChanged = datetime.datetime.now()
        filter.save()
        return HttpResponse(f"Filter updated (Entry {request.GET['filterEntry']})")

    if "json" in request.GET:
        if request.GET.get("json", "1") == "1":
            data = []
            t0 = None
            ed = 999
            for entry in Entries(False):
                if t0:
                    ed = editdistance.eval(t0, entry.title)
                t0 = entry.title
                data.append({"id": entry.id,
                    "time": timezone.localtime(entry.time).strftime('%d/%m/%Y | %H:%M'),
                    "title": f'<div class="text-break">{entry.title}</div>',
                    "distance": ed})
        else:
            entries = Entry.objects.filter(id__in=GetFilterIDs("Duplicates"))
            data = [
                {"id": entry.id,
                "time": timezone.localtime(entry.time).strftime('%d/%m/%Y | %H:%M'),
                "title": f'<div class="text-break">{entry.title}</div>'} for entry in entries]
        return JsonResponse(data, safe=False)

    return render(request, 'main/duplicateFilter.html', {'timezones': TIMEZONES})


@user_passes_test(lambda u: u.is_superuser)
def AI_filter(request):
    if "filterEntry" in request.GET:
        filter = EntryFilter.objects.get(name="AI")
        entryID = int(request.GET["filterEntry"])
        if entryID not in filter.entryIDs:
            filter.entryIDs.append(entryID)
        else:
            filter.entryIDs.remove(entryID)

        filter.lastChanged = datetime.datetime.now()
        filter.save()
        return HttpResponse(f"Filter updated (Entry {request.GET['filterEntry']})")

    if "json" in request.GET:
        if request.GET.get("json", "1") == "1":
            entries = Entries(False).exclude(id__in=GetFilterIDs("AI"))
        else:
            entries = Entry.objects.filter(id__in=GetFilterIDs("AI"))

        data = [
            {"id": entry.id,
            "time": timezone.localtime(entry.time).strftime('%d/%m/%Y | %H:%M'),
            "title": f'<div class="text-break">{entry.title}</div>'} for entry in entries]
        return JsonResponse(data, safe=False)

    return render(request, 'main/AIFilter.html', {'timezones': TIMEZONES})

# ----------------------- Twitch API -----------------------

@csrf_exempt
def callback(request):
    if request.method == "POST":
        headers = request.headers
        data = json.loads(request.body.decode('utf-8'))
        if not 'Twitch-Eventsub-Message-Id' in headers:
            return HttpResponse("Unknown request")

        verificationSecret = getattr(APIData.objects.last(), "verificationSecret", None)
        hmac_message = headers['Twitch-Eventsub-Message-Id'] + headers['Twitch-Eventsub-Message-Timestamp']
        expected_signature = "sha256=" + hmac.new(bytes(verificationSecret, encoding='utf8'), msg=bytes(hmac_message, encoding='utf8') + request.body, digestmod=hashlib.sha256).hexdigest()
        if not hmac.compare_digest(headers["Twitch-Eventsub-Message-Signature"], expected_signature):
            print(f"Unknown signature, {headers['Twitch-Eventsub-Message-Signature']}, {expected_signature}")
            return HttpResponse("Unknown signature", status=400)

        if "challenge" in data:
            APIData.objects.all().update(subscriptionID=data["subscription"]["id"])
            return HttpResponse(data["challenge"])
        elif "event" in data:
            title = data["event"]["title"]
            category = data["event"]["category_name"]

            if Entry.objects.latest("time").title == title:
                return HttpResponse("Repeated notification")
            else:
                new = Entry(time=timezone.now(), title=title, category=category)
                new.save()
                return HttpResponse("Success - Database Updated")
        else:
            return HttpResponse("Revocation successful")
