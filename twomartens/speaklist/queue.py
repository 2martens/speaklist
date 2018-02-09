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

"""speaklist.queue: provides the queue class"""
from typing import List, Tuple


class Queue:
    """Implements a priority queue with multiple priorities considered."""
    
    def __init__(self) -> None:
        self._speakers = []
    
    def add(self, speaker: Tuple[str, bool]) -> None:
        pass
    
    def add_list(self, speakers: List[Tuple[str, bool]]) -> None:
        pass
    
    def get_next(self) -> str:
        pass
    
    def get_all(self) -> List[str]:
        pass
