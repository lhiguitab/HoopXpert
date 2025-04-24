from django.core.management.base import BaseCommand
from workout.models import RealGameDrill
import csv
import os

class Command(BaseCommand):
    help = "Import real game drills from CSV"

    def handle(self, *args, **kwargs):
        file_path = 'workout/management/commands/real_game_drills.csv'

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                try:
                    title = row['title'].strip()
                    situation_type = row['situation_type'].strip()
                    video_link = row['video_link'].strip()
                    duration_min = int(row['duration_min'])

                    obj, created = RealGameDrill.objects.update_or_create(
                        title=title,
                        situation_type=situation_type,
                        defaults={
                            'video_link': video_link,
                            'duration_min': duration_min,
                        }
                    )
                    count += 1

                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Skipped a row due to error: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} drills."))
