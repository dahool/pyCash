# -*- coding: utf-8 -*-
"""Copyright (c) 2010,2011 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from cash.models import Loan
from django.db import IntegrityError, connection

class Command(BaseCommand):
    help = 'Update loans status.'
    
    def handle(self, *args, **options):
        cursor = connection.cursor()
        up = 0
        for loan in Loan.objects.all():
            total = loan.amount
            cursor.execute("SELECT sum(amount) as sum FROM payment WHERE loan_id = %s", [loan.id])
            row = cursor.fetchone()
            if row[0]!=None:
                total -= row[0]
            loan.remain = total
            loan.save()
            if total == 0:
                up += 1
        
        self.stdout.write('Full paid %d loans.\n' % up)