from django.views.generic import FormView
from .models import Servico, Funcionario, Recurso
from .forms import ContatoForm
from django.urls import reverse_lazy
from django.contrib import messages


class IndexView(FormView):
    template_name = 'index.html'
    form_class = ContatoForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        recursos = list(Recurso.objects.order_by('?')[:6])

        # context['servicos'] = Servico.objects.all() (a opção abaixo traz por ordem aleatória)
        context['servicos'] = Servico.objects.order_by('?').all()
        context['recursos_left'] = recursos[:3]
        context['recursos_right'] = recursos[3:6]
        context['funcionarios'] = Funcionario.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'E-mail enviado com Sucesso!')
        return super(IndexView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar Email!')
        return super(IndexView, self).form_invalid(form, *args, **kwargs)
