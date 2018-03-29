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
from collections import Iterator, MutableSequence
from typing import List, Tuple, Union


class Queue(MutableSequence):
    """Implements a priority queue with multiple priorities considered."""
    
    def __init__(self) -> None:
        self._speakers = []
    
    def add(self, speaker: Tuple[str, bool]) -> None:
        pass
    
    def add_list(self, speakers: List[Tuple[str, bool]]) -> None:
        pass
    
    def insert(self, index: int, value: str) -> None:
        """
        Inserts a new speaker at specified index.
        
        :param index: position on speak list
        :param value: name of speaker
        """
        self._speakers.insert(index, value)
    
    def __iter__(self) -> Iterator:
        return iter(self._speakers)
    
    def __len__(self) -> int:
        return len(self._speakers)
    
    def __contains__(self, item: str) -> bool:
        return item in self._speakers
    
    def __getitem__(self, index: int) -> str:
        return self._speakers[index]
    
    def __setitem__(self, key: Union[int, slice], value: str) -> None:
        self._speakers.__setitem__(key, value)
    
    def __delitem__(self, key: Union[int, slice]) -> None:
        self._speakers.__delitem__(key)
