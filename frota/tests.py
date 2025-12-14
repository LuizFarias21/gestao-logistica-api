
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Motorista

class MotoristaAPITests(APITestCase):

    def setUp(self):
        # Cria um motorista de teste
        self.motorista = Motorista.objects.create(
            nome="Teste Rota", 
            cpf="11111111111", 
            cnh="1111111111", 
            telefone="900000000"
        )
        self.url = f'/api/motoristas/{self.motorista.id}/'

    # --- TESTE DA REGRA DE EXCLUSÃO ---
    def test_nao_pode_excluir_motorista_em_rota(self):
        """
        Garante que o sistema impede a exclusão de motoristas com status 'em_rota'.
        (Regra 4 de Negócio)
        """
        # 1. Coloca o motorista em rota
        self.motorista.status = 'em_rota'
        self.motorista.save()

        # 2. Tenta deletar via API
        response = self.client.delete(self.url)

        # 3. Verifica o resultado
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Verifica se ele ainda existe no banco
        self.assertTrue(Motorista.objects.filter(id=self.motorista.id).exists())


    def test_pode_excluir_motorista_disponivel(self):
        """
        Garante que a exclusão é permitida se o status for 'disponivel'.
        """
        # Status padrão já é 'disponivel' (na função setUp)

        # Tenta deletar via API
        response = self.client.delete(self.url)

        # Verifica o resultado
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verifica se ele foi removido do banco
        self.assertFalse(Motorista.objects.filter(id=self.motorista.id).exists())