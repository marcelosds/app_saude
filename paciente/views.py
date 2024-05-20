import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import request
from django.shortcuts import redirect, render
from medico.models import DadosMedico, Especialidades, DatasAbertas, is_medico
from datetime import datetime
from .models import Consulta, Documento
from django.contrib import messages
from django.contrib.messages import constants


def home(request): 
    if request.method == "GET":
        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')
        medicos = DadosMedico.objects.all()
        
        
        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)
        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)
       
        especialidades = Especialidades.objects.all()
        return render(request, 'home.html',
                      {'medicos': medicos, 'especialidades': especialidades, 'is_medico': is_medico(request.user)})


def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(
            agendado=False)
 
        return render(request, 'escolher_horario.html',
                    {'medico': medico, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)})


# Enviar e-mail com informações da consulta      
def enviar_email(request, id_data_aberta):
    
    user_email = request.user.email

    paciente = Consulta(paciente=request.user)
    data_consulta = DatasAbertas.objects.get(id=id_data_aberta)
     # Obtendo o e-mail do médico baseado na DataAberta escolhida
    id_medico = data_consulta.user.id  # Presumindo que user é a FK para o médico em DatasAbertas
    email_medico = DadosMedico.objects.filter(user_id=id_medico).values_list('email_medico', flat=True).first()
    val_consulta = DadosMedico.objects.filter(user_id=id_medico).values_list('valor_consulta', flat=True).first()

    sender_email = 'mstitecnologiadopresente@gmail.com'
    sender_password = 'mbbkrnnpmedxkvmq'
    receiver_email = user_email
    mail_medico = email_medico
    subject = 'Agendamento de Consulta Médica'
    message = f'''
    Prezado(a)

        Seguem informações de agendamento de consulta.
        
        Paciente: {paciente}
        
        Data da consulta: {data_consulta}
        
        Valor: R$ {val_consulta}


    Atenciosamente: Equipe Minha Saúde'''

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['CC'] = mail_medico
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [receiver_email, mail_medico], msg.as_string())
        
        
    except smtplib.SMTPException:
        messages.add_message(request, constants.ERROR, "Ocorreu um erro ao enviar o e-mail.")   
        
        
         

def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        
        try:
            data_aberta = DatasAbertas.objects.get(id=id_data_aberta)
            horario_agendado = Consulta(
                paciente=request.user,
                data_aberta=data_aberta
            )
            horario_agendado.save()
            data_aberta.agendado = True
            data_aberta.save()

            enviar_email(request, id_data_aberta)

            messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')
        except DatasAbertas.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Horário não encontrado.')
        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Ocorreu um erro ao agendar o horário: {e}')

        return redirect('/pacientes/minhas_consultas/')
    
  
  

def minhas_consultas(request):
    
    if request.method == "GET":
        #TODO: desenvolver filtros
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
 
        
        return render(request, 'minhas_consultas.html',
                      {'minhas_consultas': minhas_consultas, 'is_medico': is_medico(request.user)})


def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        documentos = Documento.objects.filter(consulta=consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        
        return render(request, 'consulta.html', 
                      {'consulta': consulta, 'documentos': documentos, 'dado_medico': dado_medico,
                       'is_medico': is_medico(request.user)})
        
        
def avaliacao(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        #consulta.status = 'V'
        #consulta.save()
        
        return render(request, 'avaliacao.html', {'consulta': consulta})
    
    
def avaliar(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        consulta.status = 'V'
        consulta.save()
        
        return render(request, 'avaliacao.html', {'consulta': consulta})    
    