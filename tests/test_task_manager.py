"""
Testes automatizados para o Sistema de Gerenciamento de Tarefas
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.task_manager import Task, TaskManager


class TestTask:
    def test_task_creation(self):
        """Testa criação de tarefa"""
        task = Task(1, "Teste", "Descrição teste")
        assert task.id == 1
        assert task.title == "Teste"
        assert task.status == "A Fazer"
    
    def test_status_update_valid(self):
        """Testa atualização válida de status"""
        task = Task(1, "Teste", "Descrição")
        result = task.update_status("Em Progresso")
        assert result is True
        assert task.status == "Em Progresso"
    
    def test_status_update_invalid(self):
        """Testa atualização inválida de status"""
        task = Task(1, "Teste", "Descrição")
        result = task.update_status("Status Inválido")
        assert result is False
        assert task.status == "A Fazer"


class TestTaskManager:
    def setup_method(self):
        """Prepara ambiente para cada teste"""
        self.manager = TaskManager()
    
    def test_create_task(self):
        """Testa criação de tarefa no gerenciador"""
        task = self.manager.create_task("Tarefa 1", "Descrição 1")
        assert task.id == 1
        assert len(self.manager.tasks) == 1
    
    def test_read_tasks(self):
        """Testa leitura de tarefas"""
        self.manager.create_task("Tarefa 1", "Descrição 1")
        self.manager.create_task("Tarefa 2", "Descrição 2")
        
        tasks = self.manager.read_tasks()
        assert len(tasks) == 2
    
    def test_read_filtered_tasks(self):
        """Testa leitura de tarefas com filtro"""
        task1 = self.manager.create_task("Tarefa 1", "Descrição 1")
        task2 = self.manager.create_task("Tarefa 2", "Descrição 2")
        task1.update_status("Concluído")
        
        todo_tasks = self.manager.read_tasks("A Fazer")
        done_tasks = self.manager.read_tasks("Concluído")
        
        assert len(todo_tasks) == 1
        assert len(done_tasks) == 1
    
    def test_update_task(self):
        """Testa atualização de tarefa"""
        task = self.manager.create_task("Tarefa 1", "Descrição 1")
        updated = self.manager.update_task(1, title="Novo Título")
        
        assert updated.title == "Novo Título"
    
    def test_delete_task(self):
        """Testa exclusão de tarefa"""
        self.manager.create_task("Tarefa 1", "Descrição 1")
        deleted = self.manager.delete_task(1)
        
        assert deleted is not None
        assert len(self.manager.tasks) == 0
    
    def test_get_statistics(self):
        """Testa geração de estatísticas"""
        self.manager.create_task("T1", "D1")
        self.manager.create_task("T2", "D2")
        self.manager.tasks[0].update_status("Concluído")
        
        stats = self.manager.get_statistics()
        
        assert stats["total_tasks"] == 2
        assert stats["done"] == 1
        assert stats["progress"] == 50.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])