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

from unittest import TestCase

from speaklist.queue import Queue


class TestQueue(TestCase):
    """Tests the Queue.
    
    For now only quotation of women, inter and trans people is taken care of."""
    def setUp(self):
        self._queue = Queue()
        self._speakers = [
            ("Anton", False),
            ("Malte", False),
            ("Jim", False),
            ("Anna", True),
            ("Sophia", True),
            ("Christina", True),
            ("Anna", True),
            ("Sophia", True),
            ("Jim", False),
            ("Corinna", True),
            ("Malte", False),
        ]
        self._speakersSorted = [
            "Anna",
            "Anton",
            "Sophia",
            "Malte",
            "Christina",
            "Jim",
            "Anna",
            "Sophia",
            "Jim",
            "Corinna",
            "Malte",
        ]
        
    def test_add_list(self):
        # empty list, add list, list is sorted correctly
        self._queue.add_list(self._speakers)
        self.assertEqual(self._speakersSorted, self._queue.get_all())
    
    def test_get_next(self):
        # empty list, add list, get first speaker, get second speaker
        self._queue.add_list(self._speakers)
        self.assertEqual(self._speakersSorted[0], self._queue.get_next())
        self.assertEqual(self._speakersSorted[1], self._queue.get_next())
    
    def test_get_all(self):
        # empty list, add list, list is sorted correctly (copy of add_list test)
        self._queue.add_list(self._speakers)
        self.assertEqual(self._speakersSorted, self._queue.get_all())

    def test_add(self):
        # empty list, add list, get sorted list, add new speaker, check that new speaker is in list
        self._queue.add_list(self._speakers)
        sorted_speakers = self._queue.get_all()
        new_speaker = ("Oxford", True)
        self._queue.add(new_speaker)
        sorted_speakers.append(new_speaker[0])
        self.assertEqual(sorted_speakers, self._queue.get_all())
