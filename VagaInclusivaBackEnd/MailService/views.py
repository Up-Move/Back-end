from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import random
import string

def generate_random_code(length=6):
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

code = generate_random_code()

def send_email_view(request):
    if request.method == 'POST':
        body_json = json.loads(request.body.decode())
        email = body_json["email"]
        print(email)
        message = Mail(
            from_email='tccmailvagainclusiva@gmail.com',
            to_emails=body_json["email"],
            subject='Token de Validação',
            html_content=f'<strong>CODE: {code}</strong>')
        
        try:
            sg = SendGridAPIClient(config('SENDGRID_API_KEY'))
            response = sg.send(message)
            return HttpResponse(f"Email sent with status code: {response.status_code}")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    else:
        return HttpResponse("This view only accepts POST requests.")
    

def validate_code(code_sent_by_user, valide_code):
    if (code_sent_by_user == valide_code):
        return True
    return False

def change_password(request):
    if request.method == 'POST':
        body_json = json.loads(request.body.decode())
        code_sent_by_user = body_json["token"]
        print("code: " + code)
        print("code_sent_by_user: " + code_sent_by_user)
        if (validate_code(code_sent_by_user=code_sent_by_user, valide_code=code)):
            return HttpResponse("You can now change the password")
        return HttpResponseBadRequest("Codes not match")
    else:
        return HttpResponse("This view only accepts POST requests.")
    
# Trocar Senha
User = get_user_model()

def atualizar_senha(request):
    if request.method == 'POST':
        body_json = json.loads(request.body.decode())
        email = body_json["email"]
        nova_senha = body_json["nova_senha"]
        print(f"Email:{email} Senha:{nova_senha}")

        try:
            user = User.objects.get(email=email)
            user.set_password(nova_senha)
            user.save()
            return JsonResponse({'message': 'Senha atualizada com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Esta visualização aceita apenas solicitações POST'}, status=400)
    
# Trocar Email
def atualizar_email(request):
    if request.method == 'POST':
        body_json = json.loads(request.body.decode())
        email_cadastrado = body_json["email_cadastrado"]
        email_novo = body_json["email_novo"]
        print(f"Email Cadastrado:{email_cadastrado} Email Novo:{email_novo}")

        try:
            user = User.objects.get(email=email_cadastrado)
            user.email = email_novo
            user.save()
            return JsonResponse({'message': 'Email atualizado com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Esta visualização aceita apenas solicitações POST'}, status=400)
    
# Deletar Conta
def deletar_conta(request):
    if request.method == 'POST':
        body_json = json.loads(request.body.decode())
        email_cadastrado = body_json["email_cadastrado"]
        print(f"Email Cadastrado:{email_cadastrado}")

        try:
            user = User.objects.get(email=email_cadastrado)
            user.delete()
            return JsonResponse({'message': 'Conta Deletada com Sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Esta visualização aceita apenas solicitações POST'}, status=400)


# 1. Enviar e-mail com o código
# 2. Receber o código que o usuário colocou
# 3. Validar se os códigos batem
# 4. Liberar acesso para trocar a senha
