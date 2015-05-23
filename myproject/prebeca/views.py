from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from models import User, Event, User_Event, Date_Act, Score, Comment, Image
from BeautifulSoup import BeautifulSoup
import urllib
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from prebeca.forms import LongDurForm, OrderForm, TypeForm, DateForm, UserForm, UserTitleForm, UserDescriptionForm, LoginForm, ScoreForm, CommentForm, ImageForm
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import logout
from django.contrib import auth

# Create your views here.


def logout_view(request):
    logout(request)
    login = False

    isUser = checkUser(request)
    if isUser:
        user = request.user.username
    else:
        user = None

    template = get_template("login.html")
    c = Context({'out': "Ya no estas registrado",
                 'form': LoginForm(),
                 'login': login,
                 'isUser': isUser,
                 'user': user})
    return HttpResponse(template.render(c))


@csrf_exempt
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                   username=form.cleaned_data["username"],
                   password=form.cleaned_data["password"])
            try:
                auth.login(request, user)
                return HttpResponseRedirect("/")
            except AttributeError:
                out = "Introduce un nombre de usuario o password correctos"
        else:
            out = "Introduce un nombre de usuario o password correctos"
    else:
        out = "Introduce tu nombre y clave para iniciar sesion"

    login = True

    isUser = checkUser(request)
    if isUser:
        user = request.user.username
    else:
        user = None

    template = get_template("login.html")
    c = Context({'out': out,
                 'form': LoginForm(),
                 'login': login,
                 'isUser': isUser,
                 'user': user})
    return HttpResponse(template.render(c))


def checkUser(request):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(name=request.user.username)
        except User.DoesNotExist:
            user = User(name=request.user.username, page=("Pagina de " + request.user.username))
            user.save()
        return(True)
    else:
        return(False)


def infoAdd(request, url, description):
        url = url.replace('amp;', '')
        soup = BeautifulSoup(urllib.urlopen(url).read())
        new_url = soup.find('a', {'class': 'punteado'})
        if new_url is None:
            info = description
        else:
            new_url = "http://www.madrid.es" + str(new_url).split('"')[3]
            new_url = new_url.replace('amp;', '')
            soup = BeautifulSoup(urllib.urlopen(new_url).read())
            info = soup.find('div', {'class': 'parrafo'})
            try:
                info = info.string.replace('acute;', '').replace('&', '').replace('quot;', '"')
            except AttributeError:
                info = description
        return(info)


def refresh(request):
    url = "http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=206974-0-agenda-eventos-culturales-100&mgmtid=6c0b6d01df986410VgnVCM2000000c205a0aRCRD"

    soup = BeautifulSoup(urllib.urlopen(url).read())
    events = soup.findAll('contenido')
    format = '%Y-%m-%d %H:%M:%S.%f'

    for i in range(len(events)):
        id_madrid = events[i].find('atributo', {'nombre': 'ID-EVENTO'}).string

        title = events[i].find('atributo', {'nombre': 'TITULO'}).string.encode('utf-8')

        try:
            type = events[i].find('atributo', {'nombre': 'TIPO'}).string
            type = type.split("/")[3]
        except AttributeError:
            type = "Sin clasificacion"

        free = events[i].find('atributo', {'nombre': 'GRATUITO'}).string
        if free == "0":
            try:
                price_descrip = events[i].find('atributo', {'nombre': 'PRECIO'}).string.encode('utf-8')
                price1 = price_descrip.split()[0].replace(",", ".")
                i = 1
                long = len(price_descrip.split())
                while (not price1.replace('.', '', 1).isdigit()) and (i < long):
                    price1 = price_descrip.split()[i].replace(",", ".")
                    i = i + 1
                if i >= long:
                    try:
                        float(price1)
                        price = price1
                    except ValueError:
                        price = 0
                else:
                    price = price1
            except AttributeError:
                price_descrip = "No gratuito. Preguntar precio en el evento"
                price = 0
        else:
            price_descrip = "Gratuito"
            price = 0

        date = events[i].find('atributo', {'nombre': 'FECHA-EVENTO'}).string
        date = datetime.strptime(date, format)
        hour = events[i].find('atributo', {'nombre': 'HORA-EVENTO'}).string
        hour = str(date).split()[0] + " " + hour + ":00.0"
        hour = datetime.strptime(hour, format)
        datef = events[i].find('atributo', {'nombre': 'FECHA-FIN-EVENTO'}).string
        datef = datetime.strptime(datef, format)
        duration = datef - hour
        duration = duration.total_seconds()

        try:
            longdur = events[i].find('atributo', {'nombre': 'EVENTO-LARGA-DURACION'}).string.encode('utf-8')
            if longdur == "0":
                long = False
            else:
                long = True
        except AttributeError:
            long = False

        try:
            description = events[i].find('atributo', {'nombre': 'DESCRIPCION'}).string.encode('utf-8')
            if description == " ":
                description = "Detalle en la URL"
        except AttributeError:
            description = "Detalle en la URL"

        url = events[i].find('atributo', {'nombre': 'CONTENT-URL'}).string
        url = url.replace('amp;', '')

        try:
            e = Event.objects.get(id_madrid=id_madrid)
        except Event.DoesNotExist:
            e = Event(id_madrid=id_madrid, title=title, type=type, price=price, price_descrip=price_descrip, date=str(hour), duration=str(duration), longdur=long, description=description, url=url)
            e.save()

    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = Date_Act(date=str(today))
    date.save()

    return HttpResponseRedirect("/todas")


@csrf_exempt
def all(request):
    import datetime

    isUser = checkUser(request)
    if isUser:
        user_name = request.user.username
    else:
        user_name = None

    if request.method == "POST":
        form_long = LongDurForm(request.POST)
        form_order = OrderForm(request.POST)
        form_type = TypeForm(request.POST)
        form_date = DateForm(request.POST)
        if form_long.is_valid():
            longdur = form_long.cleaned_data['Duracion']
            if longdur == "True":
                list = Event.objects.filter(longdur=True)
            else:
                list = Event.objects.filter(longdur=False)
        if form_order.is_valid():
            mode = form_order.cleaned_data['Ordenar']
            list = Event.objects.order_by(mode)
        if form_type.is_valid():
            type = form_type.cleaned_data['Tipo']
            list = Event.objects.filter(type=type)
        if form_date.is_valid():
            dateMax = form_date.cleaned_data['FechaMax']
            dateMin = form_date.cleaned_data['FechaMin']
            list = Event.objects.filter(date__range=[dateMin, dateMax])
    else:
        list = Event.objects.all()

    for i in list:
        i.duration = datetime.timedelta(seconds=i.duration)
    len_list = len(list)
    date = Date_Act.objects.order_by('-date')[0].date

    template = get_template("all.html")
    c = Context({'isUser': isUser,
                 'user': user,
                 'user_name': user_name,
                 'len_list': len_list,
                 'date': date,
                 'list': list,
                 'order_form': OrderForm(),
                 'type_form': TypeForm(),
                 'longdur_form': LongDurForm(),
                 'date_form': DateForm(),
                 'form': LoginForm()})
    return HttpResponse(template.render(c))


def root(request):
    import datetime

    isUser = checkUser(request)
    if isUser:
        user = request.user.username
    else:
        user = None

    today = datetime.datetime.now()
    list_event = Event.objects.order_by('date').filter(date__gte=(today))[:10]
    for i in list_event:
        i.duration = datetime.timedelta(seconds=i.duration)
    checkUser(request)

    list_user = User.objects.all()
    list_images = Image.objects.all()

    template = get_template("index.html")
    c = Context({'list_event': list_event,
                 'list_user': list_user,
                 'user': user,
                 'isUser': isUser,
                 'form': LoginForm(),
                 'list_images': list_images})
    return HttpResponse(template.render(c))


@csrf_exempt
def activity(request, id):
    import datetime

    isUser = checkUser(request)
    if isUser:
        user = request.user.username
    else:
        user = None

    if request.method == "POST":
        form_score = ScoreForm(request.POST)
        form_comment = CommentForm(request.POST)
        if form_score.is_valid():
            score = form_score.cleaned_data['Puntuacion']
            user_obj = User.objects.get(name=user)
            activ = Event.objects.get(id=id)
            today = datetime.datetime.now()
            score_obj = Score(event=activ, user=user_obj, score=score, date=today)
            score_obj.save()
        if form_comment.is_valid():
            comment = form_comment.cleaned_data['Comentario']
            user_obj = User.objects.get(name=user)
            activ = Event.objects.get(id=id)
            today = datetime.datetime.now()
            comment_obj = Comment(event=activ, user=user_obj, comment=comment, date=today)
            comment_obj.save()

    try:
        activ = Event.objects.get(id=id)
        activ.duration = datetime.timedelta(seconds=activ.duration)
        info = infoAdd(request, activ.url, activ.description)
        ok = True

        score_list = Score.objects.filter(event__id=id)
        if score_list:
            scores = len(score_list)
            votes = 0
            for i in score_list:
                votes = i.score + votes
            average = votes / float(scores)
            last_score = score_list.order_by('-date')[0]
        else:
            average = 0
            last_score = None
            scores = 0

        comments_list = Comment.objects.filter(event__id=id)
        if comments_list:
            last_comment = comments_list.order_by('-date')[0]
            comments = len(comments_list)
        else:
            last_comment = None
            comments = 0

        select_list = User_Event.objects.filter(event__id=id)
        if select_list:
            last_selection = select_list.order_by('-date')[0]
            selections = len(select_list)
        else:
            last_selection = None
            selections = 0

        try:
            User_Event.objects.filter(user__name=request.user.username).get(event__id=id)
            select = True
        except User_Event.DoesNotExist:
            select = False

    except Event.DoesNotExist:
        activ = None
        info = None
        score_list = None
        average = 0
        last_score = None
        scores = 0
        ok = False
        comments_list = None
        select = False
        last_comment = None
        comments = 0
        last_selection = None
        selections = 0
        select_list = None

    template = get_template("activity.html")
    c = Context({'isUser': isUser,
                 'user': user,
                 'ok': ok,
                 'activ': activ,
                 'id': id,
                 'info': info,
                 'form': LoginForm(),
                 'score_form': ScoreForm(),
                 'score_list': score_list,
                 'average': average,
                 'comment_form': CommentForm(),
                 'comments_list': comments_list,
                 'select_list': select_list,
                 'select': select,
                 'last_comment': last_comment,
                 'comments': comments,
                 'last_score': last_score,
                 'scores': scores,
                 'last_selection': last_selection,
                 'selections': selections})
    return HttpResponse(template.render(c))


@csrf_exempt
def help(request):
    isUser = checkUser(request)
    if isUser:
        user = request.user.username
    else:
        user = None

    par1 = "En esta pagina podras consultar los ultimos eventos tanto culturales como de ocio que te propone la Comunidad de Madrid. A partir del canal RSS que proporciona el ayuntamiento de Madrid en su web oficial obtenemos la informacion esencial para mostrarla toda en un unico lugar, esta web"
    par2 = "En la pagina principal encontraras los 10 proximos eventos para que no te los pierdas, con hora, lugar y descripcion. Si quieres ampliar la informacion para conocer mas detalles sobre el acto, solo tienes que pinchar en el enlace 'Ver detalle'"
    par3 = "Finalmente, si te gusta algun evento solo tienes que seleccionarlo e incluirlo a tu lista de favoritos, de este modo nunca olvidaras cual es tu proxima cita. Siempre podras modificar tu lista y consultar la de otros amigos. Ademas, tienes la posiblidad de obtener todos tus eventos guardados en formato rss para poder compartirlo con mayor facilidad"

    template = get_template("help.html")
    c = Context({'isUser': isUser,
                 'user': user,
                 'par1': par1,
                 'par2': par2,
                 'par3': par3,
                 'form': LoginForm()})
    return HttpResponse(template.render(c))


@csrf_exempt
def user(request, username):
    import datetime

    isUser = checkUser(request)
    if isUser and request.user.username == username:
        isThisUser = True
    else:
        isThisUser = False

    if request.method == "POST":
        form_user = UserForm(request.POST)
        form_title_user = UserTitleForm(request.POST)
        form_description_user = UserDescriptionForm(request.POST)
        form_image = ImageForm(request.POST, request.FILES)

        if form_title_user.is_valid():
            title = form_title_user.cleaned_data['Titulo']
            User.objects.filter(name=username).update(page=title)
        if form_description_user.is_valid():
            description = form_description_user.cleaned_data['Descripcion']
            User.objects.filter(name=username).update(description=description)
        if form_user.is_valid():
            letter_size = form_user.cleaned_data['Letra']
            letter_color = form_user.cleaned_data['ColorLetra']
            back_color = form_user.cleaned_data['ColorFondo']
            back_image = form_user.cleaned_data['Imagen']
            letter_title = form_user.cleaned_data['LetraTitulo']
            title_color = form_user.cleaned_data['ColorTitulo']
            User.objects.filter(name=username).update(letter_size=letter_size, letter_color=letter_color, back_color=back_color, back_image=back_image, title=letter_title, title_color=title_color)
            ruta = "templated-linear/css/" + username + ".css"
            f = open(ruta, "w")
            css = open("templated-linear/css/prueba.css", "r")
            content = css.read()
            code = content.replace("{{image}}", back_image).replace("{{back_color}}", back_color).replace("{{letter_size}}", letter_size).replace("{{letter_color}}", letter_color).replace("{{letter_title}}", letter_title).replace("{{title_color}}", title_color)
            f.write(code)
            f.close()
        if form_image.is_valid():
            user = User.objects.get(name=username)
            image_ant = Image.objects.filter(user=user)
            if image_ant:
                for i in image_ant:
                    i.delete()
            image = Image(user=user, imagen=request.FILES['imagen'])
            image.save()

    try:
        user = User.objects.get(name=username)
        ok = True
        list = User_Event.objects.filter(user=user)
        if list:
            for i in list:
                i.event.duration = datetime.timedelta(seconds=i.event.duration)

        score_list = Score.objects.filter(user=user)
        if score_list:
            scores = len(score_list)
            last_score = score_list.order_by('-date')[0]
        else:
            last_score = None
            scores = 0

        comments_list = Comment.objects.filter(user=user)
        if comments_list:
            last_comment = comments_list.order_by('-date')[0]
            comments = len(comments_list)
        else:
            last_comment = None
            comments = 0

        select_list = User_Event.objects.filter(user=user)
        if select_list:
            last_selection = select_list.order_by('-date')[0]
            selections = len(select_list)
        else:
            last_selection = None
            selections = 0

        images_list = Image.objects.filter(user=user)
        if images_list:
            last_image = images_list[0]
        else:
            last_image = None

    except User.DoesNotExist:
        user = None
        ok = False
        list = None
        score_list = None
        comments_list = None
        select_list = None
        last_score = None
        scores = 0
        last_comment = None
        comments = 0
        last_selection = None
        selections = 0
        images_list = None
        last_image = None

    template = get_template("user.html")
    c = Context({'isUser': isUser,
                 'isThisUser': isThisUser,
                 'user': user,
                 'user_name': request.user.username,
                 'user_page': username,
                 'ok': ok,
                 'list': list,
                 'usertitle_form': UserTitleForm(),
                 'userdescription_form': UserDescriptionForm(),
                 'user_form': UserForm(),
                 'form': LoginForm(),
                 'score_list': score_list,
                 'last_score': last_score,
                 'scores': scores,
                 'comments_list': comments_list,
                 'last_comment': last_comment,
                 'comments': comments,
                 'select_list': select_list,
                 'last_selection': last_selection,
                 'selections': selections,
                 'ImageForm': ImageForm(),
                 'images_list': images_list,
                 'last_image': last_image})
    return HttpResponse(template.render(c))


def add(request, id):
    isUser = checkUser(request)
    if isUser:
        try:
            event = Event.objects.get(id=id)
            try:
                User_Event.objects.filter(user__name=request.user.username).get(event=event)
            except User_Event.DoesNotExist:
                user = User.objects.get(name=request.user.username)
                today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_event = User_Event(user=user, event=event, date=str(today))
                save_event.save()
        except Event.DoesNotExist:
            out = "Evento no encontrado</br>"
            return HttpResponse(out)
    else:
        out = "No estas registrado"
        return HttpResponse(out)
    return HttpResponseRedirect("/actividad/" + str(id))


def remove(request, id):
    isUser = checkUser(request)
    if isUser:
        try:
            event = Event.objects.get(id=id)
            try:
                event_user = User_Event.objects.filter(user__name=request.user.username).get(event=event)
                event_user.delete()
            except User_Event.DoesNotExist:
                out = "El evento no estaba seleccionado"
                return HttpResponse(out)
        except Event.DoesNotExist:
            out = "Evento no encontrado</br>"
            return HttpResponse(out)
    else:
        out = "No estas registrado"
        return HttpResponse(out)
    return HttpResponseRedirect("/actividad/" + str(id))
