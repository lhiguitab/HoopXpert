from django.core.management.base import BaseCommand
from workout.models import Exercise
import os
import csv

class Command(BaseCommand):
    help = 'Load exercises from exercise_db.csv (delimited by ;) into the Exercise model'

    def handle(self, *args, **kwargs):
        # Ruta al archivo CSV en lugar de JSON
        csv_file_path = 'workout/management/commands/exercise_database.csv'
        
        # Verifica si el archivo existe
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'File {csv_file_path} not found'))
            return
        
        # Cargar datos del archivo CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            exercise_db = list(csv_reader)

        # Contador para saber cuántos se agregaron o actualizaron
        added = 0
        updated = 0
        
        # Recorremos cada ejercicio en el CSV convertido a diccionario
        for exercise in exercise_db:
            # Busca si ya existe uno con el mismo nombre
            exercise_name = exercise.get('Exercise Name', '').strip()
            if not exercise_name:
                continue  # Salta si no tiene nombre

            exist = Exercise.objects.filter(exercise_name=exercise_name).first()

            if not exist:
                try:
                    Exercise.objects.create(
                        exercise_name=exercise_name,
                        short_youtube_demonstration=exercise.get('Short YouTube Demonstration', '').strip(),
                        in_depth_youtube_explanation=exercise.get('In-Depth YouTube Explanation', '').strip(),
                        difficulty_level=exercise.get('Difficulty Level', '').strip(),
                        target_muscle_group=exercise.get('Target Muscle Group', '').strip(),
                        prime_mover_muscle=exercise.get('Prime Mover Muscle', '').strip(),
                        secondary_muscle=exercise.get('Secondary Muscle', '').strip(),
                        tertiary_muscle=exercise.get('Tertiary Muscle', '').strip(),
                        primary_equipment=exercise.get('Primary Equipment', '').strip(),
                        primary_items=int(exercise.get('# Primary Items', 0)),
                        secondary_equipment=exercise.get('Secondary Equipment', '').strip(),
                        secondary_items=int(exercise.get('# Secondary Items', 0)),
                        posture=exercise.get('Posture', '').strip(),
                        single_or_double_arm=exercise.get('Single or Double Arm', '').strip(),
                        continuous_or_alternating_arms=exercise.get('Continuous or Alternating Arms', '').strip(),
                        grip=exercise.get('Grip', '').strip(),
                        load_position_ending=exercise.get('Load Position (Ending)', '').strip(),
                        continuous_or_alternating_legs=exercise.get('Continuous or Alternating Legs', '').strip(),
                        foot_elevation=exercise.get('Foot Elevation', '').strip(),
                        combination_exercises=exercise.get('Combination Exercises', '').strip(),
                        movement_pattern_1=exercise.get('Movement Pattern #1', '').strip(),
                        movement_pattern_2=exercise.get('Movement Pattern #2', '').strip(),
                        movement_pattern_3=exercise.get('Movement Pattern #3', '').strip(),
                        plane_of_motion_1=exercise.get('Plane Of Motion #1', '').strip(),
                        plane_of_motion_2=exercise.get('Plane Of Motion #2', '').strip(),
                        plane_of_motion_3=exercise.get('Plane Of Motion #3', '').strip(),
                        body_region=exercise.get('Body Region', '').strip(),
                        force_type=exercise.get('Force Type', '').strip(),
                        mechanics=exercise.get('Mechanics', '').strip(),
                        laterality=exercise.get('Laterality', '').strip(),
                        primary_exercise_classification=exercise.get('Primary Exercise Classification', '').strip(),
                    )
                    added += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error adding exercise {exercise_name}: {e}"))
            else:
                try:
                    exist.short_youtube_demonstration = exercise.get('Short YouTube Demonstration', '').strip()
                    exist.in_depth_youtube_explanation = exercise.get('In-Depth YouTube Explanation', '').strip()
                    exist.difficulty_level = exercise.get('Difficulty Level', '').strip()
                    exist.target_muscle_group = exercise.get('Target Muscle Group', '').strip()
                    exist.prime_mover_muscle = exercise.get('Prime Mover Muscle', '').strip()
                    exist.secondary_muscle = exercise.get('Secondary Muscle', '').strip()
                    exist.tertiary_muscle = exercise.get('Tertiary Muscle', '').strip()
                    exist.primary_equipment = exercise.get('Primary Equipment', '').strip()
                    exist.primary_items = int(exercise.get('# Primary Items', 0))
                    exist.secondary_equipment = exercise.get('Secondary Equipment', '').strip()
                    exist.secondary_items = int(exercise.get('# Secondary Items', 0))
                    exist.posture = exercise.get('Posture', '').strip()
                    exist.single_or_double_arm = exercise.get('Single or Double Arm', '').strip()
                    exist.continuous_or_alternating_arms = exercise.get('Continuous or Alternating Arms', '').strip()
                    exist.grip = exercise.get('Grip', '').strip()
                    exist.load_position_ending = exercise.get('Load Position (Ending)', '').strip()
                    exist.continuous_or_alternating_legs = exercise.get('Continuous or Alternating Legs', '').strip()
                    exist.foot_elevation = exercise.get('Foot Elevation', '').strip()
                    exist.combination_exercises = exercise.get('Combination Exercises', '').strip()
                    exist.movement_pattern_1 = exercise.get('Movement Pattern #1', '').strip()
                    exist.movement_pattern_2 = exercise.get('Movement Pattern #2', '').strip()
                    exist.movement_pattern_3 = exercise.get('Movement Pattern #3', '').strip()
                    exist.plane_of_motion_1 = exercise.get('Plane Of Motion #1', '').strip()
                    exist.plane_of_motion_2 = exercise.get('Plane Of Motion #2', '').strip()
                    exist.plane_of_motion_3 = exercise.get('Plane Of Motion #3', '').strip()
                    exist.body_region = exercise.get('Body Region', '').strip()
                    exist.force_type = exercise.get('Force Type', '').strip()
                    exist.mechanics = exercise.get('Mechanics', '').strip()
                    exist.laterality = exercise.get('Laterality', '').strip()
                    exist.primary_exercise_classification = exercise.get('Primary Exercise Classification', '').strip()
                    
                    exist.save()
                    updated += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error updating exercise {exercise_name}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'Successfully added {added} exercises and updated {updated} exercises in the database'))
