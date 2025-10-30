"""
Management command to create monthly competitions.
This can be run manually or via a cron job on the 1st of each month.

Usage:
    python manage.py create_competitions
    python manage.py create_competitions --year 2025 --month 10
    python manage.py create_competitions --months 3  # Create next 3 months
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from tracker.models import Competition
from datetime import date
from dateutil.relativedelta import relativedelta


class Command(BaseCommand):
    help = 'Create monthly pushup competitions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            help='Year for the competition (default: current year)',
        )
        parser.add_argument(
            '--month',
            type=int,
            help='Month for the competition (default: current month)',
        )
        parser.add_argument(
            '--months',
            type=int,
            default=1,
            help='Number of months to create (default: 1)',
        )
        parser.add_argument(
            '--update-status',
            action='store_true',
            help='Update status of all existing competitions',
        )

    def handle(self, *args, **options):
        # Handle status update if requested
        if options['update_status']:
            self.stdout.write('Updating status of all competitions...')
            competitions = Competition.objects.all()
            for comp in competitions:
                old_status = comp.status
                comp.update_status()
                if old_status != comp.status:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Updated {comp.name}: {old_status} → {comp.status}'
                        )
                    )
            self.stdout.write(self.style.SUCCESS('Status update complete!'))
            return

        # Get starting date
        if options['year'] and options['month']:
            current_date = date(options['year'], options['month'], 1)
        else:
            current_date = date.today().replace(day=1)

        # Create competitions for specified number of months
        months_to_create = options['months']
        created_count = 0
        existing_count = 0

        for i in range(months_to_create):
            competition_date = current_date + relativedelta(months=i)
            year = competition_date.year
            month = competition_date.month

            # Try to create competition
            competition = Competition.create_monthly_competition(year, month)
            
            # Check if it was newly created
            if competition.created_at.date() == date.today():
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created: {competition.name} ({competition.status})'
                    )
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'• Already exists: {competition.name} ({competition.status})'
                    )
                )

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(f'  - Created: {created_count}')
        self.stdout.write(f'  - Already existed: {existing_count}')
        
        # Show current competition
        current_comp = Competition.get_current_competition()
        if current_comp:
            self.stdout.write('')
            self.stdout.write(
                self.style.SUCCESS(
                    f'Current competition: {current_comp.name} '
                    f'({current_comp.days_remaining} days remaining)'
                )
            )

