import os
from repositories.submission_repository import SubmissionRepository
from models import Submission
from dtos.submission_dto import SubmissionDTO, TempSubmissionDTO
import shutil
import tempfile
from pathlib import Path
import subprocess
from database import get_db

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
        self.staging = EvaluationStagingArea(self.upload_dir)

    def select_and_save_file(self) -> TempSubmissionDTO | None:
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
            return self.staging.add_file(file_path_str)
            
        except FileNotFoundError:
            print("Erro: Zenity não encontrado.")
            return None

    def remove_from_staging(self, file_name: str):
        self.staging.remove_file(file_name)
        
    def commit_staging(self, evaluation_id: int):
        self.staging.commit(evaluation_id)
        
    def cleanup_staging(self):
        self.staging.cleanup()

    def create_submission(self, evaluation_id: int, file_name: str, file_path: str, score: float, feedback: str) -> SubmissionDTO:
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