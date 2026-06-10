import os
import subprocess
import difflib
from collections import defaultdict
from pathlib import Path
from repositories.submission_repository import SubmissionRepository
from models import Submission, Similarity
from dtos.submission_dto import SubmissionDTO, TempSubmissionDTO
from database import get_db

class SubmissionService:
    def __init__(self):
        self.repository = SubmissionRepository()

    def select_file(self) -> TempSubmissionDTO | None:
        """Abre o Zenity e retorna um DTO com nome, caminho e conteúdo do arquivo."""
        try:
            resultado = subprocess.run(
                [
                    "zenity", "--file-selection", "--title=Selecione o arquivo de código",
                    "--file-filter=Códigos Python | *.py", "--file-filter=C/C++ e Java | *.c *.cpp *.h *.java",
                    "--file-filter=Todos os arquivos | *"
                ],
                capture_output=True, text=True
            )
            
            if resultado.returncode != 0:
                return None
                
            file_path_str = resultado.stdout.strip()
            source_path = Path(file_path_str)
            
            if not source_path.exists():
                return None
            
            # --- NOVA LÓGICA DE LEITURA ---
            file_content = ""
            try:
                # Tenta ler o arquivo como texto UTF-8
                with open(source_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except UnicodeDecodeError:
                # Se der erro de Decode, é porque não é um arquivo de texto (ex: .zip, .exe, imagem)
                file_content = "Não foi possível visualizar. Este é um arquivo binário ou compactado."
            except Exception as e:
                file_content = f"Erro ao tentar ler o arquivo: {str(e)}"
            # ------------------------------

            return TempSubmissionDTO(
                file_name=source_path.name, 
                file_path=str(source_path),
                content=file_content  # <--- Passando o conteúdo para o DTO
            )
            
        except FileNotFoundError:
            print("Erro: Zenity não encontrado.")
            return None

    def create_submission(self, evaluation_id: int, file_name: str, file_path: str, content: str, score: float, feedback: str) -> SubmissionDTO:
        # A validação se o arquivo existe pode ser mantida por segurança
        if not os.path.exists(file_path):
            raise ValueError(f"O ficheiro não foi encontrado no sistema: {file_path}")

        submission = Submission(
            evaluation_id=evaluation_id,
            file_name=file_name,
            file_path=file_path,
            content=content,
            score=score,
            feedback=feedback
        )

        with get_db() as db:
            self.repository.create(db, submission)
            return SubmissionDTO.from_entity(submission)

    def get_submission_by_id(self, submission_id: int) -> SubmissionDTO | None:
        with get_db() as db:
            submission = self.repository.get_by_id(db, submission_id)
            if not submission:
                return None
            return SubmissionDTO.from_entity(submission)

    def list_submissions_by_evaluation(self, evaluation_id: int) -> list[SubmissionDTO]:
        with get_db() as db:
            submissions = self.repository.list_by_evaluation_id(db, evaluation_id)
            return [SubmissionDTO.from_entity(s) for s in submissions]

    def delete_submission(self, submission_id: int) -> bool:
        with get_db() as db:
            submission = self.repository.get_by_id(db, submission_id)
            if not submission:
                return False
            return self.repository.delete(db, submission)
        
    def update_score(self, submission_id: int, score: float) -> bool:
        if not 0 <= score <= 10:
            return False
        
        with get_db() as db:
            submission = self.repository.get_by_id(db, submission_id)
            if not submission:
                raise ValueError(f"Submission com ID {submission_id} não existe no banco de dados.")
            
            submission.score = score
            db.commit()
            return True

    def calculate_and_save_similarities(self, evaluation_id: int, threshold: float = 0.75):
        """
        Cruza os códigos de todos os alunos de uma avaliação e salva os 
        casos de plágio no banco de dados. O(N²).
        """
        with get_db() as db:
            # Puxa todos os arquivos físicos diretamente do banco (já com o 'content')
            subs = db.query(Submission).filter(Submission.evaluation_id == evaluation_id).all()
            
            for i, sub_a in enumerate(subs):
                if not sub_a.content: continue

                for j, sub_b in enumerate(subs):
                    if i == j or not sub_b.content: continue

                    # Ignora quebras de linha e espaços durante a comparação
                    # Isso pega alunos que tentam disfarçar mudando a indentação
                    matcher = difflib.SequenceMatcher(lambda x: x in " \t\n", sub_a.content, sub_b.content)
                    taxa = matcher.ratio()

                    # Se ultrapassou o limite, cria o registro de alerta!
                    if taxa >= threshold:
                        alerta = Similarity(
                            source_id=sub_a.id,
                            target_id=sub_b.id,
                            match_ratio=taxa
                        )
                        db.add(alerta)
            
            db.commit()

    def get_all_similarities_by_evaluation(self, evaluation_id: int) -> dict[int, list[tuple[float, str]]]:
        """
        Retorna um dicionário mapeando o ID de uma submissão para sua lista de similaridades.
        Resolve o problema N+1 fazendo apenas uma ida ao banco de dados.
        """
        with get_db() as db:
            # 1. Descobre todos os IDs das submissões desta avaliação
            subs = db.query(Submission.id).filter(Submission.evaluation_id == evaluation_id).all()
            sub_ids = [sub.id for sub in subs] # Extrai apenas os números para uma lista

            # Se a avaliação não tem submissões, retorna um dicionário vazio
            if not sub_ids:
                return {}

            # 2. Busca todas as similaridades de uma vez só usando a cláusula IN (WHERE source_id IN (...))
            # O joinedload faria o SQLAlchemy trazer a tabela alvo automaticamente, 
            # mas como criamos a "relationship", acessar o .target_submission.file_name faz isso sob demanda.
            sims = db.query(Similarity).filter(Similarity.source_id.in_(sub_ids)).all()

            # 3. Organiza os dados em memória usando um defaultdict
            # O defaultdict(list) cria uma lista vazia automaticamente caso a chave (source_id) ainda não exista
            resultado = defaultdict(list)
            
            for s in sims:
                resultado[s.source_id].append((s.match_ratio, s.target_submission.file_name))
            
            # Retorna convertendo para um dicionário padrão do Python
            return dict(resultado)