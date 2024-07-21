import csv
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class Exercice:
    def __init__(self, date: str, niveau: int, allonge: bool, assis: bool, session_id: str, formatted_date: datetime):
        self.date = date
        self.niveau = niveau
        self.allonge = allonge
        self.assis = assis
        self.session_id = session_id
        self.formatted_date = formatted_date
        self.serie = 0
        self.vie = 0

def parse_date(date_str: str) -> Optional[datetime]:
    formats = ['%d/%m/%Y', '%d.%m.%Y']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None

def count_series(exercices: List[Exercice]) -> None:
    if not exercices:
        return

    vie_max = 2
    vie = vie_max
    serie = 0
    streak = 0
    
    exercices = [ex for ex in exercices if ex.formatted_date is not None]

    exercices.sort(key=lambda ex: ex.formatted_date)

    previous_date = None
    date_sessions = {}

    for exercice in exercices:
        total_assis = 0
        total_allonge = 0

        if exercice.assis:
            total_assis += exercice.niveau * 5
        if exercice.allonge:
            total_allonge += exercice.niveau * 5

        if previous_date is None:
            previous_date = exercice.formatted_date

        days_diff = (exercice.formatted_date - previous_date).days

        if days_diff > 1:
            missed_days = days_diff - 1
            exercice.vie -= 1
            if exercice.vie < 0:
                exercice.vie = 0
                serie = 0
                streak = 0

        if exercice.formatted_date not in date_sessions:
            if (total_assis >= 10 and total_allonge >= 10):
                if days_diff == 1:
                    streak += 1
                    serie += 1
                    if streak % 5 == 0:
                        vie = min(vie + 1, vie_max)
                else:
                    streak = 1
                    serie = 1
                date_sessions[exercice.formatted_date] = serie
                previous_date = exercice.formatted_date
            else:
                date_sessions[exercice.formatted_date] = serie

        exercice.serie = date_sessions[exercice.formatted_date]
        exercice.vie = vie

        previous_date = exercice.formatted_date

def read_csv(input_csv: str, output_csv: str) -> List[Exercice]:
    exercices_dict: Dict[str, List[Exercice]] = {}

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = row['Date']
            niveau = int(row['Niveau']) if row['Niveau'] else 0
            allonge = row['Allonge'].lower() in ['true', '1', 'yes']
            assis = row['Assis'].lower() in ['true', '1', 'yes']
            session_id = row['SessionID']
            formatted_date = parse_date(row['formattedDate']) if row['formattedDate'] else None

            exercice = Exercice(date=date, niveau=niveau, allonge=allonge, assis=assis, session_id=session_id, formatted_date=formatted_date)
            if session_id not in exercices_dict:
                exercices_dict[session_id] = []
            exercices_dict[session_id].append(exercice)

        for key, grouped_exercices in exercices_dict.items():
            count_series(grouped_exercices)

    exercices = [ex for ex_list in exercices_dict.values() for ex in ex_list]
    write_csv(output_csv, exercices)

def write_csv(output_csv: str, exercices: List[Exercice]) -> None:
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Date', 'Niveau', 'Allonge', 'Assis', 'SessionID', 'formatted_date', 'Serie', 'Vie']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for exercice in exercices:
            writer.writerow({
                'Date': exercice.date,
                'Niveau': exercice.niveau,
                'Allonge': exercice.allonge,
                'Assis': exercice.assis,
                'SessionID': exercice.session_id,
                'formatted_date': exercice.formatted_date.strftime('%d/%m/%Y') if exercice.formatted_date else '',
                'Serie': exercice.serie,
            })

def main():

    
    input_csv = './input/Enregistrement.csv'
    output_csv = './output/output' + datetime.now().strftime('%Y-%m-%d-%H_%M_%S') + ".csv"


    parser = argparse.ArgumentParser(description='Process some CSV files.')

    # Ajoutez des arguments pour les fichiers d'entrée et de sortie
    parser.add_argument('input_csv', type=str, help='Path to the input CSV file')
    parser.add_argument('output_csv', type=str, help='Path to the output CSV file')

    # Parsez les arguments
    args = parser.parse_args()

    # Appelez la fonction read_csv avec les arguments fournis
    read_csv(args.input_csv, args.output_csv)

if __name__ == "__main__":
    main()