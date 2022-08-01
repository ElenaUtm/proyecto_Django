from django.shortcuts import render

#Accedemos al modelo Alumnos que contiene la estructura de la tabla.
from .models import Alumnos
#Accedemos a los modelos restantes
from .forms import ComentarioContactoForm
from .models import ComentarioContacto
#Genera en Http404 en lugar de la DoesNotExistexcepción del modelo. Solo se verá en modo de ejecución no en debug.
from django.shortcuts import get_object_or_404
import datetime

from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages 

# Create your views here.


def registros(request):
    alumnos=Alumnos.objects.all()
    #all recupera todos los objetos del modelo (registros de la tabla alumnos)
    return render(request, "registros/principal.html",{'alumnos':alumnos})
    #Indicamos el lugar donde se renderizará el resultado de esta vista
    # y enviamos la lista de alumnos recuparados

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): #Si los datos recibidos son correctos
            form.save() #inserta
            comentarios=ComentarioContacto.objects.all()
            return render(request,'registros/consultaContacto.html',{'comentarios':comentarios}) 
    form = ComentarioContactoForm()
    #Si algo sale mal se reenvian al formulario los datos ingresados
    return render(request,'registros/contacto.html',{'form': form}) 

def contacto(request):
	return render(request,"registros/contacto.html")
	#Indicamos el lugar donde se renderizará el resultado de esta vista
	# y enviamos la lista de alumnos recuparados.

def consultarComentarioContacto(request):
    comentarios=ComentarioContacto.objects.all()
    #all recupera todos los objetos del modelo (registros de la tabla 
    #comentariosContacto)
    return render(request,"registros/consultaContacto.html",{'comentarios':comentarios})
    #Indicamos el lugar donde se renderizará el resultado de esta vista
    # y enviamos la lista de comentarios recuparados.

def eliminarComentarioContacto(request, id, 	confirmacion='registros/confirmarEliminacion.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method=='POST':
        comentario.delete()
        comentarios=ComentarioContacto.objects.all()
        return render(request,"registros/consultaContacto.html",{'comentarios':comentarios})
    return render(request, confirmacion, {'object':comentario})

def consultarComentarioIndividual(request, id):
	comentario=ComentarioContacto.objects.get(id=id)
	#get permite establecer una condicionante a la consulta y recupera el objetos 
       #del modelo que cumple la condición (registro de la tabla ComentariosContacto.  
       #get se emplea cuando se sabe que solo hay un objeto que coincide con su
       #consulta.
	return render(request,"registros/formEditarComentario.html",
		{'comentario':comentario})
	#Indicamos el lugar donde se renderizará el resultado de esta vista
	# y enviamos la lista de alumnos recuparados.

def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    #Referenciamos que el elemento del formulario pertenece al comentario 
    # ya existente
    if form.is_valid():
        form.save() #si el registro ya existe, se modifica. 
        comentarios=ComentarioContacto.objects.all()
        return render(request,"registros/consultaContacto.html",{'comentarios':comentarios})
	#Si el formurio no es valido nos regresa al formulario para verificar
	#datos
    return render(request,"registros/formEditarComentario.html",{'comentario':comentario})

def consultar1(request):
    #con una sola condición
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
    #multiples condiciones adicionando .filter() se analiza #como AND
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
    #Si solo deseamos recuperar ciertos datos agregamos la #función only, listando los campos que queremos obtener de #la consulta emplear filter() o #en el ejemplo all()
    alumnos=Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
    alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar6(request):
    fechaInicio = datetime.date(2022, 7, 1)
    fechaFin = datetime.date(2022, 7, 13)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
    #Consultando entre modelos
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})


def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion=descripcion, archivo=archivo)
            insert.save()
            return render(request,"registros/archivos.html")
        else:
            messages.error(request, "Error al procesar el formulario")
    else:
        return render(request,"registros/archivos.html",{'archivo':Archivos})

def consultasSQL(request):
    alumnos=Alumnos.objects.raw('SELECT id, matricula,nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def seguridad(request, nombre=None):
	nombre = request.GET.get('nombre')
	return render(request,"registros/seguridad.html",
	{'nombre':nombre})
