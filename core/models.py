# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def _criar_usuario(self, ra, password, **campos):
        if not ra:
            raise ValueError('RA deve ser declarado!')
        user = self.model(ra=ra, **campos)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, ra, password=None, **campos):
        return self._criar_usuario(ra,password,**campos)

    def create_superuser(self, ra, password=None, **campos):
        campos.setdefault('perfil','Coordenador')
        return self._criar_usuario(ra,password,**campos)

class Curso(models.Model):
    sigla = models.CharField("Sigla do curso",db_column='Sigla', unique=True, max_length=5)  # Field name made lowercase.
    nome = models.CharField("Nome", db_column='Nome', unique=True, max_length=50)  # Field name made lowercase.
    slug = models.SlugField('Link')
    imagem = models.ImageField("Imagem do curso",upload_to='image', null=True, blank=True)
    
    sobre = models.TextField('Sobre o Curso', blank=True)
    ativo = models.BooleanField("Ativo?",default=True)

    def __str__(self):
        return self.nome

    @models.permalink
    def get_absolute_url(self):
        return ('detalhe_de_cursos.html', (), {'slug': self.slug})

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nome']     

class Disciplina(models.Model):
    nome = models.CharField(db_column='Nome', unique=True, max_length=240)  # Field name made lowercase.
    cargahoraria = models.SmallIntegerField(db_column='CargaHoraria')  # Field name made lowercase.
    teoria = models.DecimalField(db_column='Teoria', max_digits=3, decimal_places=0)  # Field name made lowercase.
    pratica = models.DecimalField(db_column='Pratica', max_digits=3, decimal_places=0)  # Field name made lowercase.
    ementa = models.TextField(db_column='Ementa')  # Field name made lowercase. This field type is a guess.
    competencias = models.TextField(db_column='Competencias')  # Field name made lowercase. This field type is a guess.
    habilidades = models.TextField(db_column='Habilidades')  # Field name made lowercase. This field type is a guess.
    conteudo = models.TextField(db_column='Conteudo')  # Field name made lowercase. This field type is a guess.
    bibliografia_basica = models.TextField(db_column='Bibliografia_Basica')  # Field name made lowercase. This field type is a guess.
    biblioteca_complementar = models.TextField(db_column='Biblioteca_complementar')  # Field name made lowercase. This field type is a guess.

    def __str__(self):
        return self.nome

    
class Usuario(AbstractBaseUser):
    ra = models.IntegerField(db_column='RA', unique=True)
    password = models.CharField(db_column='Senha',max_length=200)
    nome = models.CharField(db_column='Nome',max_length=100)
    email = models.EmailField(db_column='E-mail',max_length=50)
    

    perfil = models.CharField(db_column='Perfil',max_length=50)
    ativo = models.BooleanField(db_column='Ativo',default=True)
    
    USERNAME_FIELD = 'ra'
    REQUIRED_FIELDS = ['nome','email']
    objects = UsuarioManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nome']     

    def get_full_name(self):
        return self.nome

    def get_short_name(self):
        return self.nome

    def __str__(self):
        return self.nome

    @property
    def is_staff(self):
        return self.perfil == "Coordenador"

    def has_module_perms(self, package_name):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm_list, obj=None):
        return True

class Aluno(Usuario):
    sigla_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Sigla_Curso')  # Field name made lowercase.
    imagemAluno = models.ImageField("Imagem do Aluno",upload_to='image', null=True, blank=True)
    celular = models.CharField(db_column='Celular', max_length=11)  # Field name made lowercase.
    
    def __str__(self):
        return str(self.ra)


class Gradecurricular(models.Model):
    sigla_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Sigla_Curso')  # Field name made lowercase.
    ano = models.SmallIntegerField(db_column='Ano',unique=True)  # Field name made lowercase.
    semestre = models.CharField(db_column='Semestre', max_length=1)  # Field name made lowercase.

    def __str__(self):
        return str(self.ano)
 

    class Meta:
        verbose_name = 'Grade Curricular'
        verbose_name_plural = 'Grades Curriculares'
        ordering = ['sigla_curso'] 

class Periodo(models.Model):
    sigla_curso = models.ForeignKey(Curso, models.DO_NOTHING, related_name="Curso", db_column='Sigla_Curso')  # Field name made lowercase.
    ano_grade = models.ForeignKey(Gradecurricular, models.DO_NOTHING, related_name="Ano")  # Field name made lowercase.
    semestre_grade = models.IntegerField(db_column='Semestre_Grade')  # Field name made lowercase.
    numeroperiodo = models.SmallIntegerField(db_column='NumeroPeriodo', unique=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Periodo'
        verbose_name_plural = 'Periodos'
        ordering = ['sigla_curso'] 


class Periododisciplina(models.Model):
    sigla_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Sigla_Curso')  # Field name made lowercase.
    ano_grade = models.ForeignKey(Gradecurricular, models.DO_NOTHING, related_name='Ano_Grade_periodo_dis')  # Field name made lowercase.
    semestre_grade = models.ForeignKey(Gradecurricular, models.DO_NOTHING, db_column='Semestre_Grade')  # Field name made lowercase.
    numero_periodo = models.ForeignKey(Periodo, models.DO_NOTHING, db_column='Numero_Periodo')  # Field name made lowercase.
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Disciplina')  # Field name made lowercase.

    class Meta:
        verbose_name = 'Periodo e Disciplina'
        verbose_name_plural = 'Periodos e Disciplinas'
        ordering = ['sigla_curso'] 


class Disciplinaofertada(models.Model):
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Disciplina')  # Field name made lowercase.
    anoofertado = models.SmallIntegerField(db_column='AnoOfertado', unique=True)  # Field name made lowercase.
    semestreofertado = models.CharField(db_column='SemestreOfertado', unique=True, max_length=1)  # Field name made lowercase.

                

class Professor(Usuario):
    apelido = models.CharField("Apelido",db_column='Apelido', unique=True, max_length=30)  # Field name made lowercase.
    celular = models.CharField(db_column='Celular', max_length=11)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
        ordering = ['apelido']

    def __str__(self):
        return str(self.ra)


class Turma(models.Model):
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, related_name='Nome_Disciplina')  # Field name made lowercase.
    ano_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, related_name='Ano_Ofertado')  # Field name made lowercase.
    semestre_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, db_column='Semestre_Ofertado')  # Field name made lowercase.
    id_turma = models.CharField(db_column='Id_Turma', unique=True, max_length=1)  # Field name made lowercase.
    ra_professor = models.ForeignKey(Professor, models.DO_NOTHING,  related_name='RA_Professor')  # Field name made lowercase.
    turno = models.CharField(db_column='Turno', max_length=15)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['nome_disciplina']

    def __str__(self):
        return str(self.nome_disciplina)

class Cursoturma(models.Model):
    sigla_curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Sigla_Curso')  # Field name made lowercase.
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Disciplina')  # Field name made lowercase.
    ano_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, related_name='Ano_Ofertado_Curso_Turma')  # Field name made lowercase.
    semestre_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, db_column='Semestre_Ofertado')  # Field name made lowercase.
    id_turma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='Id_Turma')  # Field name made lowercase.


class Questao(models.Model):
    nome_discplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Discplina')  # Field name made lowercase.
    ano_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, related_name='Ano_Ofertado_Questao')  # Field name made lowercase.
    semestre_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, db_column='Semestre_Ofertado')  # Field name made lowercase.
    id_turma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='Id_Turma')  # Field name made lowercase.
    numeroquestao = models.IntegerField(db_column='NumeroQuestao', unique=True)  # Field name made lowercase.
    datalimiteentrega = models.CharField(db_column='DataLimiteEntrega', max_length=10)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase. This field type is a guess.
    data = models.CharField(db_column='Data', max_length=10)  # Field name made lowercase.
       


class Arquivosquestao(models.Model):
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Disciplina')  # Field name made lowercase.
    ano_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, related_name='Ano_Ofertado_Arquivo_Questao')  # Field name made lowercase.
    semestre_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, db_column='Semestre_Ofertado')  # Field name made lowercase.
    id_turma = models.ForeignKey(Turma, models.DO_NOTHING, db_column='Id_Turma')  # Field name made lowercase.
    numero_questao = models.ForeignKey(Questao, models.DO_NOTHING, db_column='Numero_Questao')  # Field name made lowercase.
    arquivoquestao = models.CharField(db_column='ArquivoQuestao', unique=True, max_length=500, blank=True, null=True)  # Field name made lowercase.


class Resposta(models.Model):
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Disciplina')  # Field name made lowercase.
    ano_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, related_name='Ano_Ofertado_Resposta')  # Field name made lowercase.
    id_turma = models.ForeignKey('Turma', models.DO_NOTHING, db_column='Id_Turma')  # Field name made lowercase.
    numero_questao = models.ForeignKey(Questao, models.DO_NOTHING, db_column='Numero_Questao')  # Field name made lowercase.
    semestre_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, db_column='Semestre_Ofertado')  # Field name made lowercase.
    ra_aluno = models.IntegerField(db_column='RA_Aluno', unique=True)  # Field name made lowercase.
    dataavaliacao = models.CharField(db_column='DataAvaliacao', max_length=10)  # Field name made lowercase.
    nota = models.DecimalField(db_column='Nota', max_digits=4, decimal_places=2)  # Field name made lowercase.
    avaliacao = models.TextField(db_column='Avaliacao')  # Field name made lowercase. This field type is a guess.
    descricao = models.TextField(db_column='Descricao')  # Field name made lowercase. This field type is a guess.
    datadeenvio = models.CharField(db_column='DataDeEnvio', max_length=10)  # Field name made lowercase.



class Arquivosrespostas(models.Model):
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Disciplina')  # Field name made lowercase.
    ano_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, related_name='Ano_Ofertado_Arquivo_Resposta')  # Field name made lowercase.
    semestre_ofertado = models.ForeignKey('Disciplinaofertada', models.DO_NOTHING, db_column='Semestre_Ofertado')  # Field name made lowercase.
    id_turma = models.ForeignKey(Turma, models.DO_NOTHING, db_column='Id_Turma')  # Field name made lowercase.
    numero_questao = models.ForeignKey(Questao, models.DO_NOTHING, db_column='Numero_Questao')  # Field name made lowercase.
    ra_aluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='RA_Aluno')  # Field name made lowercase.
    arquivoresposta = models.CharField(db_column='ArquivoResposta', unique=True, max_length=500)  # Field name made lowercase.


class Matricula(models.Model):
    ra_aluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='RA_Aluno')  # Field name made lowercase.
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Disciplina')  # Field name made lowercase.
    ano_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, related_name='Ano_Ofertado_Matricula')  # Field name made lowercase.
    semestre_ofertado = models.ForeignKey(Disciplinaofertada, models.DO_NOTHING, db_column='Semestre_Ofertado')  # Field name made lowercase.
    id_turma = models.ForeignKey(Turma, models.DO_NOTHING, db_column='Id_Turma')  # Field name made lowercase.

    class Meta:
        verbose_name = 'Matricula'
        verbose_name_plural = 'Matriculas'
        ordering = ['ra_aluno'] 

    def __str__(self):
        return str(self.ra_aluno)

class Cadastro_Boletim(models.Model):
    ra_aluno = models.ForeignKey(Aluno, models.DO_NOTHING, related_name='Nome')
    curso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Curso')   # Field name made lowercase.
    nome_disciplina = models.ForeignKey(Disciplina, models.DO_NOTHING, db_column='Nome_Discplina')
    MB1 = models.SmallIntegerField("MB1",blank=True, null=True)  # Field name made lowercase.
    SUB1 = models.SmallIntegerField("SUB1",blank=True, null=True)
    MB2 = models.SmallIntegerField("MB2",blank=True, null=True)
    SUB2 = models.SmallIntegerField("sub2",blank=True, null=True)
    regular = models.BooleanField("Ativo?",default=True)

    def __str__(self):
        return str(self.ra_aluno)
    class Meta:
        verbose_name = 'Boletim'
        verbose_name_plural = 'Boletins'
        ordering = ['curso']     

class Questionario(models.Model):   

    acertos = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'core_questionario'
