#!/usr/bin/env python3

import argparse
import sys

from datetime import datetime
from dateutil.relativedelta import relativedelta


class meeting_event():
    """Holds a date and a description"""

    def __init__(self, date, descr, section = None, para = None, offset_months = None, offset_weeks = None, offset_days = None):

        self.date = date
        self.description = descr
        self.section = section
        self.paragraph = para

        if offset_months:
            self.date = self.date + relativedelta(months = int(offset_months))

        if offset_weeks:
            self.date = self.date + relativedelta(weeks = int(offset_weeks))

        if offset_days:
            self.date = self.date + relativedelta(days = int(offset_days))


    def __lt__(self, other):
        return self.date < other.date


    def __gt__(self, other):
        return self.date > other.date


    def __repr__(self):
        return str(self.date)


    def __str__(self):

        date = datetime.strftime(self.date, '%Y-%m-%d')

        if (self.section and self.paragraph):
            return f'{date} {self.section} kap. {self.paragraph}§ {self.description}'

        else:
            return f'{date} {self.description}'


    def get_date(self):

        return self.date


class lbac_meet:
    """Hold dates related to annual meeting"""

    def __init__(self, date, do_check = True):

        if date.month > 4 and do_check:
            raise ValueError('The date may not exceed beyond last of April.')



        self.meeting = meeting_event(date, 'Årsmöte')
        self.events = [self.meeting]


        # 3 kap 1§ stycke 2
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Kallelse till årsmötet och förslag till föredragningslista.',
                                     section = 3,
                                     para = 1,
                                     offset_weeks = -4
                                     ))

        # 3 kap 1§ stycke 3
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Verksamhetsberättelse, årsredovisning/årsbokslut, revisorernas berättelser, '
                                     'verksamhetsplan med budget samt styrelsens förslag och inkomna motioner med styrelsens yttrande.',
                                     section = 3,
                                     para = 1,
                                     offset_weeks = -1
                                     ))

        # 3 kap 2§ stycke 2
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Förslag från medlem (motion) ska vara styrelsen tillhanda senast tre veckor före årsmötet.',
                                     section = 3,
                                     para = 2,
                                     offset_weeks = -3
                                     ))


        # 3 kap 4§ stycke 2 punkt 3
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Sista dag för beviljat medlemskap.',
                                     section = 3,
                                     para = 4,
                                     offset_months = -2
                                     ))

        # 3 kap 4§ stycke 2 punkt 3
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Sista dag för medlemsavgift.',
                                     section = 3,
                                     para = 2,
                                     offset_months = -1
                                     ))

        # 4 kap 2§ stycke 2
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Valberedningen ska senast två månader före årsmötet tillfråga dem vilkas mandattid utgår '
                                     'vid mötets slut, om de vill kandidera för nästa mandattid. Därefter ska valberedningen '
                                     'informera medlemmarna om eventuella avsägelser.',
                                     section = 4,
                                     para = 2,
                                     offset_months = -2
                                     ))

        # 4 kap 2§ stycke 3
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Senast en vecka före årsmötet ska valberedningen meddela röstberättigade medlemmar sitt '
                                     'förslag, samt meddela namnen på de personer som i övrigt har föreslagits inför '
                                     'valberedningen.',
                                     section = 4,
                                     para = 2,
                                     offset_weeks = -1
                                     ))

        # 5 kap 1§ stycke 3
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Föreningens räkenskaper för det senaste verksamhets- och räkenskapsåret ska vara '
                                     'revisorerna tillhanda senast en månad före årsmötet.',
                                     section = 5,
                                     para = 1,
                                     offset_months = -1
                                     ))

        # 5 kap 1§ stycke 4
        self.add_event(meeting_event(date = self.get_date(),
                                     descr = 'Revisorerna ska granska styrelsens förvaltning och räkenskaper för det senaste '
                                     'verksamhets- och räkenskapsåret samt till styrelsen överlämna revisionsberättelse senast '
                                     '14 dagar före årsmötet.',
                                     section = 5,
                                     para = 1,
                                     offset_days = -14
                                     ))


    def __str__(self):

        s = ''

        for i in sorted(self.events, key = lambda x: x.date, reverse = False):
            s += i.__str__() + '\n'

        return s



    def add_event(self, item):

        self.events.append(item)


    def get_date(self):

        return self.meeting.get_date()


def parse_args():
    """Parse arguments provided to program"""

    parser = argparse.ArgumentParser(
        prog='Calendar deadline generator',
        description='Generates deadline dates for annual general meeting',
        epilog='Yes')

    parser.add_argument('--date',
                        action='store',
                        dest='date',
                        help='Date for the annual general meeting',
                        required=True
                        )

    parser.add_argument('--skip-date-check',
                        action='store_true',
                        dest='date_check',
                        default=False,
                        help='Ignore checking date validity',
                        required=False
                        )

    args = parser.parse_args()

    try:
        real_date = datetime.strptime(args.date, '%Y-%m-%d')
        args.date = real_date

    except ValueError as e:
        print(f'{e}: date needs to be in format yyyy-mm-dd and be a valid date.\n', file=sys.stderr)
        sys.exit(1)

    return args


def main():
    """Main routine"""
    args = parse_args()

    meeting = lbac_meet(args.date, not args.date_check)

    print(meeting)

if __name__ == '__main__':
    main()
