import os
from sqlalchemy.orm import Session
from repositories.submission_repository import SubmissionRepository
from models import Submission
from dtos.submission_dto import SubmissionDTO
import shutil
import os
from pathlib import Path
import subprocess

class SubmissionService:
    def __init__(self):
        self.repository = SubmissionRepository()
        self.upload_dir = Path("uploads/submissions")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.app = None
    
    def select_and_save_file(self, evaluation_id: int) -> tuple[str | None, str | None]:
        """
        Abre o seletor 100% nativo do Pop!_OS/Linux chamando o Zenity.
        """
        try:
            # Invoca o programa C nativo do Linux isolado do CustomTkinter
            resultado = subprocess.run(
                [
                    "zenity", 
                    "--file-selection", 
                    "--title=Selecione o arquivo de código",
                    "--file-filter=Códigos Python | *.py",
                    "--file-filter=Códigos JavaScript | *.js",
                    "--file-filter=C/C++ e Java | *.c *.cpp *.h *.java",
                    "--file-filter=Compactados | *.zip *.rar",
                    "--file-filter=Todos os arquivos | *"
                ],
                capture_output=True, 
                text=True
            )
            
            # O código de retorno 0 significa sucesso. Diferente de 0 significa que o usuário fechou ou cancelou.
            if resultado.returncode != 0:
                return None, None
                
            # O caminho do arquivo vem com uma quebra de linha no final (\n), o strip() limpa isso.
            file_path_str = resultado.stdout.strip()
            
        except FileNotFoundError:
            print("Erro: Zenity não encontrado. No Pop!_OS/Ubuntu, instale com: sudo apt install zenity")
            return None, None

        # O usuário selecionou o arquivo com sucesso, agora é só fazer a cópia
        file_path = Path(file_path_str)
        dest_folder = self.upload_dir / f"evaluation_{evaluation_id}"
        
        # Cria a pasta caso a avaliação seja nova
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_path = dest_folder / file_path.name
        
        shutil.copy2(file_path, dest_path)
        
        return file_path.name, str(dest_path)

    def create_submission(self, db: Session, evaluation_id: int, file_name: str, file_path: str, score: float, feedback: str) -> SubmissionDTO:
        # Validação de integridade: Garante que o ficheiro realmente existe no computador
        if not os.path.exists(file_path):
            raise ValueError(f"O ficheiro não foi encontrado no sistema: {file_path}")

        submission = Submission(
            evaluation_id=evaluation_id,
            file_name=file_name,
            file_path=file_path,
            score=score,
            feedback=feedback
        )

        self.repository.create(db, submission)

        return SubmissionDTO.from_entity(submission)

    def get_submission_by_id(self, db: Session, submission_id: int) -> SubmissionDTO | None:
        submission = self.repository.get_by_id(db, submission_id)

        if not submission:
            return None
        
        return SubmissionDTO(
            id=submission.id,
            evaluation_id=submission.evaluation_id,
            file_name=submission.file_name,
            file_path=submission.file_path,
            date=submission.date,
            score=submission.score,
            feedback=submission.feedback
        )

    def list_submissions_by_evaluation(self, db: Session, evaluation_id: int) -> list[SubmissionDTO]:
        submissions = self.repository.list_by_evaluation_id(db, evaluation_id)
        return [
            SubmissionDTO(
                id=s.id,
                evaluation_id=s.evaluation_id,
                file_name=s.file_name,
                file_path=s.file_path,
                date=s.date,
                score=s.score,
                feedback=s.feedback
            ) for s in submissions
        ]

    def delete_submission(self, db: Session, submission_id: int) -> bool:
        submission = self.repository.get_by_id(db, submission_id)

        if not submission:
            return False
        
        return self.repository.delete(db, submission)