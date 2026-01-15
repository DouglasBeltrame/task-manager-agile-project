"""
Sistema de Gerenciamento de Tarefas - TechFlow Solutions
Versão: 1.0
Autor: [Douglas da Costa Beltrame]
"""

class Task:
    def __init__(self, id, title, description, status="A Fazer", priority="Média"):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.created_at = "2024-01-15"
    
    def update_status(self, new_status):
        """Atualiza o status da tarefa"""
        valid_status = ["A Fazer", "Em Progresso", "Concluído"]
        if new_status in valid_status:
            self.status = new_status
            return True
        return False
    
    def to_dict(self):
        """Converte tarefa para dicionário"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at
        }


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def create_task(self, title, description, priority="Média"):
        """Cria uma nova tarefa"""
        task = Task(self.next_id, title, description, priority=priority)
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def read_tasks(self, status_filter=None):
        """Lê todas as tarefas ou filtra por status"""
        if status_filter:
            return [task for task in self.tasks if task.status == status_filter]
        return self.tasks
    
    def update_task(self, task_id, **kwargs):
        """Atualiza uma tarefa existente"""
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                return task
        return None
    
    def delete_task(self, task_id):
        """Remove uma tarefa"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                return self.tasks.pop(i)
        return None
    
    def get_task_by_id(self, task_id):
        """Busca tarefa por ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_statistics(self):
        """Retorna estatísticas do projeto"""
        total = len(self.tasks)
        todo = len([t for t in self.tasks if t.status == "A Fazer"])
        in_progress = len([t for t in self.tasks if t.status == "Em Progresso"])
        done = len([t for t in self.tasks if t.status == "Concluído"])
        
        return {
            "total_tasks": total,
            "to_do": todo,
            "in_progress": in_progress,
            "done": done,
            "progress": (done / total * 100) if total > 0 else 0
        }


def main_menu():
    """Menu principal do sistema"""
    manager = TaskManager()
    
    # Adiciona algumas tarefas iniciais
    manager.create_task("Configurar repositório", "Criar estrutura inicial do projeto no GitHub")
    manager.create_task("Implementar CRUD", "Desenvolver operações Create, Read, Update, Delete")
    manager.create_task("Configurar testes", "Implementar testes automatizados com pytest", "Alta")
    manager.create_task("Configurar CI/CD", "Configurar GitHub Actions para pipeline", "Alta")
    
    while True:
        print("\n" + "="*50)
        print("SISTEMA DE GERENCIAMENTO DE TAREFAS - TECHFLOW SOLUTIONS")
        print("="*50)
        print("\nMenu Principal:")
        print("1. Criar nova tarefa")
        print("2. Visualizar todas as tarefas")
        print("3. Visualizar tarefas por status")
        print("4. Atualizar tarefa")
        print("5. Excluir tarefa")
        print("6. Ver estatísticas")
        print("7. Sair")
        
        choice = input("\nEscolha uma opção (1-7): ")
        
        if choice == "1":
            print("\n--- Criar Nova Tarefa ---")
            title = input("Título: ")
            description = input("Descrição: ")
            priority = input("Prioridade (Baixa/Média/Alta) [Média]: ") or "Média"
            task = manager.create_task(title, description, priority)
            print(f"✅ Tarefa '{task.title}' criada com ID {task.id}")
        
        elif choice == "2":
            print("\n--- Todas as Tarefas ---")
            tasks = manager.read_tasks()
            for task in tasks:
                print(f"ID: {task.id} | {task.title} | Status: {task.status} | Prioridade: {task.priority}")
        
        elif choice == "3":
            print("\n--- Filtrar por Status ---")
            print("1. A Fazer")
            print("2. Em Progresso")
            print("3. Concluído")
            status_choice = input("Escolha o status: ")
            
            status_map = {"1": "A Fazer", "2": "Em Progresso", "3": "Concluído"}
            if status_choice in status_map:
                tasks = manager.read_tasks(status_map[status_choice])
                for task in tasks:
                    print(f"ID: {task.id} | {task.title} | Prioridade: {task.priority}")
        
        elif choice == "4":
            print("\n--- Atualizar Tarefa ---")
            task_id = int(input("ID da tarefa: "))
            task = manager.get_task_by_id(task_id)
            
            if task:
                print(f"\nTarefa atual: {task.title}")
                print("1. Atualizar título")
                print("2. Atualizar descrição")
                print("3. Atualizar status")
                print("4. Atualizar prioridade")
                
                update_choice = input("O que deseja atualizar? ")
                
                if update_choice == "1":
                    new_title = input("Novo título: ")
                    manager.update_task(task_id, title=new_title)
                elif update_choice == "2":
                    new_desc = input("Nova descrição: ")
                    manager.update_task(task_id, description=new_desc)
                elif update_choice == "3":
                    print("Status disponíveis: A Fazer, Em Progresso, Concluído")
                    new_status = input("Novo status: ")
                    if task.update_status(new_status):
                        print("✅ Status atualizado!")
                    else:
                        print("❌ Status inválido!")
                elif update_choice == "4":
                    new_priority = input("Nova prioridade (Baixa/Média/Alta): ")
                    manager.update_task(task_id, priority=new_priority)
            else:
                print("❌ Tarefa não encontrada!")
        
        elif choice == "5":
            print("\n--- Excluir Tarefa ---")
            task_id = int(input("ID da tarefa a excluir: "))
            task = manager.delete_task(task_id)
            if task:
                print(f"✅ Tarefa '{task.title}' excluída!")
            else:
                print("❌ Tarefa não encontrada!")
        
        elif choice == "6":
            print("\n--- Estatísticas do Projeto ---")
            stats = manager.get_statistics()
            print(f"Total de tarefas: {stats['total_tasks']}")
            print(f"A Fazer: {stats['to_do']}")
            print(f"Em Progresso: {stats['in_progress']}")
            print(f"Concluído: {stats['done']}")
            print(f"Progresso geral: {stats['progress']:.1f}%")
        
        elif choice == "7":
            print("\nObrigado por usar o sistema!")
            break
        
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    main_menu()