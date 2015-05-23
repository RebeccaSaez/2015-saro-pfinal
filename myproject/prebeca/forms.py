from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from models import Image


longdur_choices = (('True', 'Larga duracion'),
                   ('False', 'Corta duracion'))

order_choices = (('date', 'Fecha ascendente'),
                 ('-date', 'Fecha descendente'),
                 ('duration', 'Duracion ascendente'),
                 ('-duration', 'Duracion descendente'),
                 ('price', 'Precio ascendente'),
                 ('-price', 'Precio descendente'),
                 ('title', 'Titulo ascendente'),
                 ('-title', 'Titulo descendente'))

type_choices = (('ActividadesInfantiles', 'Actividades infantiles'),
                 ('Circos', 'Circos'),
                 ('ComemoracionesHomenajes', 'Comemoraciones y homenajes'),
                 ('Conciertos', 'Conciertos'),
                 ('ConcursosCertamenes', 'Concursos y certamenes'),
                 ('ConferenciasColoquios', 'Conferencias y coloquios'),
                 ('CuentacuentosTiteresMarionetas', 'Cuentacuentos y marionetas'),
                 ('CursosTalleres', 'Cursos y talleres'),
                 ('DanzaBallet', 'Ballet'),
                 ('EspectaculosHumorMagia', 'Humor y magia'),
                 ('Exposiciones', 'Exposiciones'),
                 ('FeriasMuestras', 'Ferias y muestras'),
                 ('FiestasActividadesCalle', 'Actividades callejeras'),
                 ('FiestasSanIsidro', 'San Isidro'),
                 ('Flamenco', 'Flamenco'),
                 ('ItinerariosOtrasActividadesAmbientales', 'Actividades ambientales'),
                 ('Jazz', 'Jazz'),
                 ('MusicaClasica', 'Musica clasica'),
                 ('ObrasTeatro', 'Teatro'),
                 ('Opera', 'Opera'),
                 ('Peliculas', 'Peliculas'),
                 ('PerformancesEspectaculosAudiovisuales', 'Performances y espectaculos'),
                 ('RecitalesPresentacionesActosLiterarios', 'Actos literarios'),
                 ('VisitasTuristicas', 'Visitas turisticas'),
                 ('Zarzuelas', 'Zarzuelas'))

size_leter_choices = (('11pt', 'Original'),
                      ('large', 'Grande'),
                      ('medium', 'Mediana'),
                      ('small', 'Peque'))

color_leter_choices = (('#000', 'Negro'),
                       ('#014B16', 'Verde oscuro'),
                       ('#1D0363', 'Azul Oscuro'),
                       ('#F52C2C', 'Rojo'),
                       ('#FFF', 'Blanco'))

color_back_choices = (('#B8D9F7', 'Azul'),
                      ('#84FBA6', 'Verde'),
                      ('#E7FEA4', 'Amarillo'),
                      ('#B9ADAD', 'Gris'),
                      ('#FFF', 'Blanco'))

image_choices = (('madrid1.jpg', 'Gran Via Metro'),
                 ('madrid2.jpg', 'Gran Via noche'),
                 ('madrid3.jpg', 'Lago del Retiro'),
                 ('madrid4.jpg', 'Madrid antiguo'),
                 ('madrid5.jpg', 'Gran Via atardecer'),
                 ('madrid6.jpg', 'Gran Via'),
                 ('madrid7.jpg', 'Cuatro Torres'),
                 ('madrid8.jpg', 'Puerta del Sol'),
                 ('madrid9.jpg', 'Plaza Mayor'),
                 ('madrid10.jpg', 'Parque del Retiro'))

title_choices = (('"Roboto", sans-serif', 'Original'),
                 ('"Lucida Sans Unicode", "Lucida Grande", sans-serif', 'Lucida'),
                 ('"Courier New", Courier, monospace', 'Mediana'),
                 ('"Lobster", cursive', 'Lobster'))

color_title_choices = (('#FFF', 'Blanco'),
                       ('#F53291', 'Rosa'),
                       ('#F9FF3C', 'Amarillo'),
                       ('#F52C2C', 'Rojo'),
                       ('#000', 'Negro'),
                       ('#72CEFF', 'Azul'),
                       ('#6CFA89', 'Verde'))

score_choices = (('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'),
                 ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                 ('8', '8'), ('9', '9'), ('10', '10'))


class LongDurForm(forms.Form):
    Duracion = forms.ChoiceField(widget=forms.Select, choices=longdur_choices)


class OrderForm(forms.Form):
    Ordenar = forms.ChoiceField(widget=forms.Select, choices=order_choices)


class TypeForm(forms.Form):
    Tipo = forms.ChoiceField(widget=forms.Select, choices=type_choices)


class DateForm(forms.Form):
    FechaMin = forms.DateField(widget=forms.extras.widgets.SelectDateWidget)
    FechaMax = forms.DateField(widget=forms.extras.widgets.SelectDateWidget)


class UserTitleForm(forms.Form):
    Titulo = forms.CharField(max_length=64)


class UserDescriptionForm(forms.Form):
    Descripcion = forms.CharField(max_length=300, widget=forms.Textarea)


class UserForm(forms.Form):
    Letra = forms.ChoiceField(widget=forms.Select, choices=size_leter_choices)
    ColorLetra = forms.ChoiceField(widget=forms.Select, choices=color_leter_choices)
    ColorFondo = forms.ChoiceField(widget=forms.Select, choices=color_back_choices)
    Imagen = forms.ChoiceField(widget=forms.Select, choices=image_choices)
    LetraTitulo = forms.ChoiceField(widget=forms.Select, choices=title_choices)
    ColorTitulo = forms.ChoiceField(widget=forms.Select, choices=color_title_choices)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class ScoreForm(forms.Form):
    Puntuacion = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizontalRadioRenderer), choices=score_choices)


class CommentForm(forms.Form):
    Comentario = forms.CharField(max_length=500, widget=forms.Textarea, initial="Escribe tu comentario...")


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['imagen']
