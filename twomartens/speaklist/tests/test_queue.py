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

from twomartens.speaklist.queue import Queue, FirstSpeakerPriority, FITSoftPriority


class TestQueue(TestCase):
    """Tests the Queue."""
    def setUp(self) -> None:
        """Sets up the test case."""
        priorities = [
            FirstSpeakerPriority(),
            FITSoftPriority()
        ]
        self._queue = Queue(priorities)
    
    def test_initialization(self):
        self.assertEqual(0, len(self._queue))
        self.assertTrue(self._queue.is_prioritized())
    
    def test_prioritize(self):
        self._queue.prioritize()
        self.assertTrue(self._queue.is_prioritized())
    
    def test_insert(self):
        new_speaker = [
            'Speaker 1',
            'speaker 1',
            False
        ]
        self._queue.insert(len(self._queue), new_speaker)
        self.assertTrue('Speaker 1' in self._queue)
