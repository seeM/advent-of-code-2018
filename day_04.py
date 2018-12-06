"""
Notes:
------
Build a dataframe with columns:
    - day_of_month
    - guard_id
    - minute_of_midnight
    - minutes_slept
Guard with most minutes slept is:
    dataframe -> groupby(guard_id) -> sum(minutes_slept) -> argmax()
Minute most slept by this guard is:
    dataframe -> filter(guard_id) -> groupby(minute_of_midnight) \
              -> sum(minutes_slept) -> argmax()
"""
import pandas as pd
import re
from collections import Counter, defaultdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, NamedTuple, Tuple, Optional


class RecordType(Enum):
    SHIFT = 'begin_shift'
    SLEEP = 'sleep'
    AWAKE = 'awake'

    @classmethod
    def from_message(cls, message: str) -> 'RecordType':
        try:
            return {'falls asleep': RecordType.SLEEP,
                    'wakes up': RecordType.AWAKE}[message]
        except KeyError:
            return RecordType.SHIFT


class Record(NamedTuple):
    timestamp: datetime
    type: RecordType
    guard_id: Optional[int]


def ffill_guard_id(records: List[Record]) -> List[Record]:
    """ Forward fill guard IDs."""
    filled: List[Record] = []
    guard_id: Optional[int] = None
    for record in records:
        if record.type is RecordType.SHIFT:
            guard_id = record.guard_id
            filled.append(record)
        else:
            filled_record = Record(record.timestamp, record.type, guard_id)
            filled.append(filled_record)
    return filled


def parse_records(lines: List[str]) -> List[Record]:
    # Pattern for parsing each record into timestamp and message
    msg_pattern = re.compile(
        # Timestamp: [YYYY-MM-DD HH:MM]
        r'^\[([0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2})\]'
        # Message
        r' (.+)$')

    # Pattern for parsing shift start messages to extract Guard ID
    guard_id_pattern = re.compile(r'^Guard \#([0-9]+) .+$')

    records: List[Record] = []
    for line in lines:
        line = line.strip()

        timestamp, message = re.match(msg_pattern, line).groups()

        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
        record_type = RecordType.from_message(message)

        if record_type is RecordType.SHIFT:
            guard_id = int(re.match(guard_id_pattern, message).groups()[0])
        else:
            guard_id = None

        records.append(Record(timestamp, record_type, guard_id))

    records = sorted(records, key=lambda x: x.timestamp)
    records = ffill_guard_id(records)

    return records


def build_records_dataframe(records: List[Record]) -> pd.DataFrame:
    df = []
    for record in records:
        month = record.timestamp.month
        day = record.timestamp.day
        minute = record.timestamp.minute
        guard_id = record.guard_id

        if record.type is RecordType.SHIFT:
            continue

        elif record.type is RecordType.SLEEP:
            start_minute = minute

        elif record.type is RecordType.AWAKE:
            end_minute = minute
            for minute_of_midnight in range(start_minute, end_minute):
                df.append((month, day, guard_id, minute_of_midnight, 1))

    df = pd.DataFrame(df, columns=['month',
                                   'day',
                                   'guard_id',
                                   'minute_of_midnight',
                                   'minutes_slept'])
    return df


def guard_most_asleep(df: pd.DataFrame) -> int:
    return df.groupby('guard_id')['minutes_slept'].sum().idxmax()

def minute_most_asleep(df: pd.DataFrame, guard_id: int) -> int:
    return df.loc[df['guard_id'] == guard_id] \
             .groupby('minute_of_midnight')['minutes_slept'] \
             .sum().idxmax()

def guard_most_frequent_minute_asleep(df: pd.DataFrame) -> Tuple[int, int]:
    pivoted = df.pivot_table(index='guard_id',
                             columns='minute_of_midnight',
                             values='minutes_slept',
                             aggfunc='sum')
    max_ = pivoted.max().max()
    masked = pivoted[pivoted == max_]
    test = masked.idxmax().dropna()
    minute = test.index[0]
    guard_id = test.iloc[0]
    return (guard_id, minute)


test_lines = """[1518-11-01 00:00] Guard #10 begins shift
                [1518-11-01 00:05] falls asleep
                [1518-11-01 00:25] wakes up
                [1518-11-01 00:30] falls asleep
                [1518-11-01 00:55] wakes up
                [1518-11-01 23:58] Guard #99 begins shift
                [1518-11-02 00:40] falls asleep
                [1518-11-02 00:50] wakes up
                [1518-11-03 00:05] Guard #10 begins shift
                [1518-11-03 00:24] falls asleep
                [1518-11-03 00:29] wakes up
                [1518-11-04 00:02] Guard #99 begins shift
                [1518-11-04 00:36] falls asleep
                [1518-11-04 00:46] wakes up
                [1518-11-05 00:03] Guard #99 begins shift
                [1518-11-05 00:45] falls asleep
                [1518-11-05 00:55] wakes up""".split('\n')
test_records = parse_records(test_lines)
test_df = build_records_dataframe(test_records)
assert guard_most_asleep(test_df) == 10
assert minute_most_asleep(test_df, 10) == 24
assert guard_most_frequent_minute_asleep(test_df) == (99, 45)


if __name__ == '__main__':
    with open('data/day_04.txt') as file:
        records = parse_records(file.readlines())
    df = build_records_dataframe(records)
    guard_most_asleep_ = guard_most_asleep(df)
    minute_most_slept_ = minute_most_asleep(df, guard_most_asleep_)

    print('Guard most asleep:', guard_most_asleep_)
    print('Minute most slept:', minute_most_slept_)
    print('Part 1:', guard_most_asleep_ * minute_most_slept_)

    guard, minute = guard_most_frequent_minute_asleep(df)
    print('Guard:', guard, 'most frequently asleep at minute:', minute)
    print('Part 2:', guard * minute)
