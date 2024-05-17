from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

class HandleTypeErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, TypeError) and "expected a number but got <SimpleLazyObject:" in str(exception):
            # Aqui você redireciona para a página de login ou qualquer outra página.
            # Você também pode retornar uma resposta JSON ou qualquer outra resposta que desejar.
            # Exemplo: redirecionar para login:
            return HttpResponseRedirect(reverse('login'))
            # Ou, se desejar retornar uma resposta JSON:
            # return JsonResponse({'error': 'Authentication required'}, status=401)

        # Caso contrário, simplesmente propague a exceção para o próximo middleware/processador de exceção
        return None