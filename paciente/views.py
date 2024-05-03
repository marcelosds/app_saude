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


def enviar_email(request, id_data_aberta):
    # Enviar e-mail com informações dos valores
    user_email = request.user.email
    
    paciente = Consulta(paciente=request.user)
    data_consulta = DatasAbertas.objects.get(id=id_data_aberta)
    
    lista = DadosMedico.objects.values_list('email_medico', flat=True)
    lista_de_emails = list(lista)
    email_medico = lista_de_emails[0]
    
    '''objeto = DadosMedico.objects.get(id_user=id)
    texto_do_email = objeto.email'''
    
    print(email_medico)
   
       
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
           
           Valor: R$ 150,00


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


def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)
        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )
        horario_agendado.save()

        # TODO: Sugestão Tornar atomico
        data_aberta.agendado = True
        data_aberta.save()
        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        enviar_email(request, id_data_aberta)  #Envia email para o médico
        
        messages.add_message(request, constants.SUCCESS, "Email enviado com sucesso!.")
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

        