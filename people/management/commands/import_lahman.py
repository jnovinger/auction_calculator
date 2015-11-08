import csv
from datetime import date

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from people.models import Person


class Command(BaseCommand):
    help = 'Imports data from Lahman database files'

    @property
    def name(self):
        return self.__module__.split('.')[-1]

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)
        parser.add_argument(
            '-t', '--type',
            type=str,
            choices=('mysql', 'rdb', 'csv'),
            default='csv',
            help="Specify which type of file to import"
        )

    def handle(self, *args, **options):
        file_type = options['type']
        assert file_type == 'csv', "{} only handles csv files at this point".format(self.name)  # noqa

        readers = self.csv_iter(options['file'])
        for reader in readers:
            self.handle_csv(reader)

    def handle_csv(self, reader):
        people = (self.person_from_row(row) for row in reader)
        failures = []
        for entry in people:
            lahmanID = entry.pop('lahmanID')
            try:
                Person.objects.update_or_create(lahmanID=lahmanID,
                                                defaults=entry)
            except IntegrityError:
                failures.append(entry.update({'lahmanID': lahmanID}))

        return any(failures), failures

    def person_from_row(self, row, save=False):
        # playerID,birthYear,birthMonth,birthDay,
        # birthCountry,birthState,birthCity,
        # deathYear,deathMonth,deathDay,
        # deathCountry,deathState,deathCity,
        # nameFirst,nameLast,nameGiven,weight,height,bats,throws,
        # debut,finalGame,retroID,bbrefID
        person = {
            'lahmanID': row['playerID'],
            'given_name': row['nameFirst'],
            'family_name': row['nameLast'],
            'retroID': row['retroID'],
            'bbrefID': row['bbrefID'],
        }

        # gah, this kinda sucks, but store lahmanID as a unique
        # placeholder for unknown ID fields
        for key in ('lahman40ID', 'lahman45ID', 'holtzID', 'mlbamID'):
            person[key] = row['playerID']

        if all(row[f] for f in ('birthYear', 'birthMonth', 'birthDay')):
            person['birth'] = date(year=int(row['birthYear']),
                                   month=int(row['birthMonth']),
                                   day=int(row['birthDay']))

        if all(row[f] for f in ('deathYear', 'deathMonth', 'deathDay')):
            person['death'] = date(year=int(row['deathYear']),
                                   month=int(row['deathMonth']),
                                   day=int(row['deathDay']))

        for lahman_key, db_key in (('debut', 'debut'),
                                   ('finalGame', 'final_game')):
            if row[lahman_key]:
                try:
                    month, day, year = row[lahman_key].split('/')
                    value = date(year=int(year), month=int(month), day=int(day))
                    person[db_key] = value
                except ValueError:
                    pass

        field_maps = (
            ('birthCountry', 'birth_country'),
            ('birthState', 'birth_state'),
            ('birthCity', 'birth_city'),
            ('deathCountry', 'death_country'),
            ('deathState', 'death_state'),
            ('deathCity', 'death_city'),
        )
        for lahman, db in field_maps:
            if row[lahman]:
                person[db] = row[lahman]

        return person

    def csv_iter(self, files):
        for file_ in files:
            assert file_.endswith('Master.csv'), "Only Master.csv handled at this point"  # noqa
            with open(file_, 'rb') as lahman:
                yield csv.DictReader(lahman)
