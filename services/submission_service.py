import os
import subprocess
from pathlib import Path
from repositories.submission_repository import SubmissionRepository
from models import Submission
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

    def create_submission(self, evaluation_id: int, file_name: str, file_path: str, score: float, feedback: str) -> SubmissionDTO:
        # A validação se o arquivo existe pode ser mantida por segurança
        if not os.path.exists(file_path):
            raise ValueError(f"O ficheiro não foi encontrado no sistema: {file_path}")

        submission = Submission(
            evaluation_id=evaluation_id,
            file_name=file_name,
            file_path=file_path,
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