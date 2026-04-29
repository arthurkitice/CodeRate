import os
from sqlalchemy.orm import Session
from repositories.submission_repository import SubmissionRepository
from models import Submission
from dtos.submission_dto import SubmissionDTO, TempSubmissionDTO
import shutil
import os
import tempfile
from pathlib import Path
import subprocess

class EvaluationStagingArea:
    def __init__(self, final_upload_dir: Path):
        self.final_upload_dir = final_upload_dir
        self.temp_dir_obj = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir_obj.name)
        self.drafts: list[TempSubmissionDTO] = []

    def add_file(self, original_file_path: str) -> TempSubmissionDTO | None:
        source_path = Path(original_file_path)
        if not source_path.exists():
            return None
            
        dest_path = self.temp_path / source_path.name
        shutil.copy2(source_path, dest_path)
        
        draft = TempSubmissionDTO(file_name=source_path.name, file_path=str(dest_path))
        self.drafts.append(draft)
        return draft

    def remove_file(self, file_name: str):
        for draft in self.drafts:
            if draft.file_name == file_name:
                Path(draft.file_path).unlink(missing_ok=True)
                self.drafts.remove(draft)
                break

    def commit(self, evaluation_id: int):
        final_folder = self.final_upload_dir / f"evaluation_{evaluation_id}"
        final_folder.mkdir(parents=True, exist_ok=True)
        for draft in self.drafts:
            final_path = final_folder / draft.file_name
            if Path(draft.file_path).exists():
                shutil.move(str(draft.file_path), str(final_path))
        self.cleanup()

    def cleanup(self):
        self.drafts.clear()
        self.temp_dir_obj.cleanup()

class SubmissionService:
    def __init__(self):
        self.repository = SubmissionRepository()
        self.upload_dir = Path("uploads/submissions")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.app = None
        
        # O Service instancia a área de rascunho quando ele nasce
        self.staging = EvaluationStagingArea(self.upload_dir)

    def select_and_save_file(self) -> TempSubmissionDTO | None:
        """Abre o Zenity e já manda o arquivo para a pasta temporária /tmp."""
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
            
            # Delega a cópia para a área de estágio e retorna o DTO pronto
            return self.staging.add_file(file_path_str)
            
        except FileNotFoundError:
            print("Erro: Zenity não encontrado.")
            return None

    # --- PONTES PARA A VIEW COMUNICAR COM O RASCUNHO ---
    
    def remove_from_staging(self, file_name: str):
        self.staging.remove_file(file_name)
        
    def commit_staging(self, evaluation_id: int):
        self.staging.commit(evaluation_id)
        
    def cleanup_staging(self):
        self.staging.cleanup()

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