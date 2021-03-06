# -*- coding: utf-8 -*-

#   Copyright 2018 Jim Martens
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from typing import List
from unittest import TestCase

from twomartens.speaklist.queue import Queue, FirstSpeakerPriority, FITSoftPriority, sort_data


class TestQueue(TestCase):
    """Tests the Queue."""
    def setUp(self) -> None:
        """Sets up the test case."""
        priorities = [
            FirstSpeakerPriority(),
            FITSoftPriority()
        ]
        self._queue = Queue(priorities)
    
    def test_initialization(self) -> None:
        self.assertEqual(0, len(self._queue))
        self.assertTrue(self._queue.is_prioritized())
    
    def test_prioritize(self) -> None:
        self._queue.prioritize()
        self.assertTrue(self._queue.is_prioritized())
    
    def test_insert(self) -> None:
        new_speaker = [
            'Speaker 1',
            'speaker 1',
            False
        ]
        self._queue.insert(len(self._queue), new_speaker)
        self.assertTrue('Speaker 1' in self._queue)


class TestFirstSpeakerPriority(TestCase):
    """Tests the FirstSpeakerPriority."""
    def setUp(self) -> None:
        """Sets up the test case."""
        self._priority = FirstSpeakerPriority()
    
    def test_type(self) -> None:
        self.assertEqual(type(str), self._priority.gettype())
    
    def test_is_valid_list(self) -> None:
        # always assuming that list only contains speakers to come
        # case 1: empty list
        self.assertTrue(self._priority.is_valid_list([]))
        # case 2: one person on list
        self.assertTrue(self._priority.is_valid_list(['anyone']))
        # case 3: two persons on list
        self.assertTrue(self._priority.is_valid_list(['anyone', 'anyone2']))
        self.assertTrue(self._priority.is_valid_list(['anyone', 'anyone']))
        # case 4: one person speaks twice, another person once, correctly ordered
        self.assertTrue(self._priority.is_valid_list(['anyone1', 'anyone2', 'anyone1']))
        self.assertTrue(self._priority.is_valid_list(['anyone2', 'anyone1', 'anyone1']))
        # case 5: one person speaks twice, another person once, wrongly ordered
        self.assertFalse(self._priority.is_valid_list(['anyone1', 'anyone1', 'anyone2']))
        # case 6: everyone speaks once
        self.assertTrue(self._priority.is_valid_list(['anyone1', 'anyone2', 'anyone3', 'alpha']))
        # case 7: 3 people speaking, first part correct, second wrong
        self.assertFalse(self._priority.is_valid_list(['anyone1', 'anyone2', 'anyone1', 'alpha']))
        # case 8: 3 people speaking, all OK
        self.assertTrue(self._priority.is_valid_list(['anyone1', 'anyone2', 'alpha', 'anyone1']))
        
    def test_sort(self) -> None:
        # always assuming that list only contains speakers to come
        # case 1: empty list
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([]), [])
            )
        )
        # case 2: one person on list
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone']), ['anyone'])
            )
        )
        # case 3: two persons on list
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone', 'anyone2']), ['anyone', 'anyone2'])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone', 'anyone']), ['anyone', 'anyone'])
            )
        )
        # case 4: one person speaks twice, another person once, correctly ordered
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone1', 'anyone2', 'anyone1']), ['anyone1', 'anyone2', 'anyone1'])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone2', 'anyone1', 'anyone1']), ['anyone2', 'anyone1', 'anyone1'])
            )
        )
        # case 5: one person speaks twice, another person once, wrongly ordered
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone1', 'anyone1', 'anyone2']), ['anyone1', 'anyone1', 'anyone2'])
            )
        )
        # case 6: everyone speaks once
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone1', 'anyone2', 'anyone3', 'alpha']),
                          ['anyone1', 'anyone2', 'anyone3', 'alpha'])
            )
        )
        # case 7: 3 people speaking, first part correct, second wrong
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone1', 'anyone2', 'anyone1', 'alpha']),
                          ['anyone1', 'anyone2', 'anyone1', 'alpha'])
            )
        )
        # case 8: 3 people speaking, all OK
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort(['anyone1', 'anyone2', 'alpha', 'anyone1']),
                          ['anyone1', 'anyone2', 'alpha', 'anyone1'])
            )
        )


class TestFITSoftPriority(TestCase):
    """Tests the FITSoftPriority."""
    def setUp(self) -> None:
        """Sets up the test case."""
        self._priority = FITSoftPriority()
    
    def test_type(self):
        self.assertEqual(type(bool), self._priority.gettype())
    
    def test_is_valid_list(self):
        # always assuming that list only contains speakers to come
        # case 1: empty list
        self.assertTrue(self._priority.is_valid_list([]))
        # case 2: one person on list, for soft FIT priority always OK
        self.assertTrue(self._priority.is_valid_list([False]))
        self.assertTrue(self._priority.is_valid_list([True]))
        # case 3: only non FIT people on list
        self.assertTrue(self._priority.is_valid_list([False, False, False]))
        # case 4: two people on list and FIT person in second place
        self.assertTrue(self._priority.is_valid_list([False, True]))
        # case 5: FIT person on list but not in right location
        self.assertFalse(self._priority.is_valid_list([False, False, True]))
        self.assertFalse(self._priority.is_valid_list([False, False, False, False, True]))
        # case 6: FIT person on list and in right location
        self.assertTrue(self._priority.is_valid_list([True, False, False]))
        self.assertTrue(self._priority.is_valid_list([False, True, False]))
        # case 7: more than one FIT person, first one OK, others not
        self.assertFalse(self._priority.is_valid_list([False, True, False, False, True]))
        self.assertFalse(self._priority.is_valid_list([True, False, False, False, True]))
        self.assertFalse(self._priority.is_valid_list([True, False, False, True, False]))
        # case 8: more than one FIT person, all OK
        self.assertTrue(self._priority.is_valid_list([False, True, False, True, False]))
        self.assertTrue(self._priority.is_valid_list([True, False, True, False, True]))
        self.assertTrue(self._priority.is_valid_list([True, True, True, False, True]))
        self.assertTrue(self._priority.is_valid_list([False, True, True, True, False]))
    
    def test_sort(self):
        # always assuming that list only contains speakers to come
        # case 1: empty list
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([]), [])
            )
        )
        # case 2: one person on list, for soft FIT priority always OK
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False]), [False])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([True]), [True])
            )
        )
        # case 3: only non FIT people on list
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False, False, False]), [False, False, False])
            )
        )
        # case 4: two people on list and FIT person in second place
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False, True]), [False, True])
            )
        )
        # case 5: FIT person on list but not in right location
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False, False, True]), [False, False, True])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False, False, False, False, True]),
                                [False, False, False, False, True])
            )
        )
        # case 6: FIT person on list and in right location
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([True, False, False]), [True, False, False])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False, True, False]), [False, True, False])
            )
        )
        # case 7: more than one FIT person, first one OK, others not
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False, True, False, False, True]),
                                [False, True, False, False, True])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([True, False, False, False, True]),
                                [True, False, False, False, True])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([True, False, False, True, False]),
                                [True, False, False, True, False])
            )
        )
        # case 8: more than one FIT person, all OK
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False, True, False, True, False]),
                                [False, True, False, True, False])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([True, False, True, False, True]),
                                [True, False, True, False, True])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([True, True, True, False, True]),
                                [True, True, True, False, True])
            )
        )
        self.assertTrue(
            self._priority.is_valid_list(
                sort_data(self._priority.sort([False, True, True, True, False]),
                                [False, True, True, True, False])
            )
        )
