from django.shortcuts import render
from core.models import Curso
from core.models import Disciplina

#Aqui estão as paginas views do template


def index(request):
	return render(request, "index.html")


def noticia(request):
	return render(request, "noticias.html")


def login(request):
	return render(request, "login.html")


def Cursos(request):
	contexto = {
		"cursos":Curso.objects.all()
	}
	return render(request,"lista_cursos.html", contexto)


def Disciplina(request):
	contexto = {
		"disciplinas":Disciplina.objects.all()
	}

	return render(request, "disciplinas.html")

def detalhe_de_cursos(request):
	return render(request, "detalhe_de_cursos.html")


def questionario(request):
	return render(request, "questionario.html")