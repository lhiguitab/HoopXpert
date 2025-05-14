from django.core.management.base import BaseCommand
from workout.models import RecoveryExercise  # Ajusta el nombre de tu app si es diferente
import csv
import os

class Command(BaseCommand):
    help = "Import recovery exercises from a CSV file."

    def handle(self, *args, **kwargs):
        file_path = 'workout/management/commands/recovery_exercises.csv'  # Ajusta si lo guardas en otra ruta

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                try:
                    exercise_name = row['exercise_name'].strip()
                    category = row['category'].strip()
                    duration = row['duration'].strip()
                    equipment_needed = row['equipment_needed'].strip()

                    obj, created = RecoveryExercise.objects.update_or_create(
                        exercise_name=exercise_name,
                        category=category,
                        defaults={
                            'duration': duration,
                            'equipment_needed': equipment_needed,
                        }
                    )
                    count += 1

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Skipped a row due to error: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} recovery exercises."))
