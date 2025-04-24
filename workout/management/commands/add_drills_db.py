from django.core.management.base import BaseCommand
from workout.models import BasketballDrill
import os
import csv

class Command(BaseCommand):
    help = 'Load basketball drills from basketball_drills.csv into the BasketballDrill model'
    
    def handle(self, *args, **kwargs):
        # Ruta al archivo CSV
        csv_file_path = 'workout/management/commands/basketball_drills.csv'
        
        # Verifica si el archivo existe
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'Archivo {csv_file_path} no encontrado'))
            return
        
        # Cargar datos del archivo CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            drills_db = list(csv_reader)
        
        # Imprimir información de diagnóstico
        self.stdout.write(f"Total de ejercicios en el CSV: {len(drills_db)}")
        
        # Contador para saber cuántos se agregaron o actualizaron
        added = 0
        updated = 0
        errors = 0
        
        # Recorremos cada ejercicio en el CSV
        for drill in drills_db:
            # Obtener el ID y nombre del ejercicio
            exercise_id = int(drill.get('ExerciseID', 0))
            exercise_name = drill.get('ExerciseName', '').strip()
            
            if not exercise_id or not exercise_name:
                self.stdout.write(self.style.WARNING(f"Ejercicio sin ID o nombre: {drill}"))
                continue
                
            try:
                # Buscar el ejercicio por ID (no por nombre)
                exist = BasketballDrill.objects.filter(id=exercise_id).first()
                
                if not exist:
                    # Crear nuevo ejercicio
                    BasketballDrill.objects.create(
                        id=exercise_id,
                        exercise_name=exercise_name,
                        position=drill.get('Position', 'All').strip(),
                        focus_skill=drill.get('FocusSkill', '').strip(),
                        duration_min=int(drill.get('DurationMin', 0))
                    )
                    added += 1
                else:
                    # Actualizar ejercicio existente
                    exist.exercise_name = exercise_name
                    exist.position = drill.get('Position', 'All').strip()
                    exist.focus_skill = drill.get('FocusSkill', '').strip()
                    exist.duration_min = int(drill.get('DurationMin', 0))
                    exist.save()
                    updated += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error con ejercicio ID {exercise_id} '{exercise_name}': {e}"))
                errors += 1
                
        self.stdout.write(self.style.SUCCESS(f'Se agregaron {added} ejercicios, se actualizaron {updated} ejercicios, y hubo {errors} errores.'))