from django.db import models
# max_length=100 --- limitador de caracteres 100
class Motorista(models.Model):
   STATUS_CHOICES = (
        ('disponivel', 'Disponível'), # Valor armazenado no banco, Nome exibido
        ('em_rota', 'Em Rota'),
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    )
   nome = models.CharField(max_length=100, help_text='Insira o nome seu completo!')
   cpf = models.CharField(max_length=11, unique=True, help_text='Insira o CPF com 11 Dígitos, sem pontos ou traços!')
   cnh = models.CharField(max_length=9, unique=True, help_text='Insira a CNH com 9 Digitos, sem pontos ou traços!')
   telefone = models.CharField(max_length=15, help_text='Ex: +55 (11) 98765-4321 ou 11987654321')   
   status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='disponivel')
   data_cadastro = models.DateTimeField(help_text= 'Data de Cadastro' ,
        auto_now_add=True,
        editable=False # Opcional: Impede que o campo seja editado no Admin
    )