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
from abc import abstractmethod
from collections import Iterator, MutableSequence
from typing import List, Tuple, Union, Any


class Queue(MutableSequence):
    """Implements a priority queue with multiple priorities considered."""
    
    def __init__(self, priorities: List['Priority']) -> None:
        """
        Initializes the priority queue.
        
        :param priorities: list of Priorities to consider
        """
        self._speakers = []  # type: List[str]
        self._priorityData = []  # type: List[list]
        self._priorities = priorities
    
    def is_prioritized(self) -> bool:
        """Checks if the queue is properly prioritized.
        
        :return: True if the queue is prioritized
        """
        i = 0
        for priority in self._priorities:
            priority_data = []
            for data in self._priorityData:
                priority_data += data[i]
            i += 1
            if not priority.is_valid_list(priority_data):
                return False
        
        return True
    
    def prioritize(self) -> None:
        """Inplace prioritization of queue."""
        i = 0
        for priority in self._priorities:
            priority_data = []
            for data in self._priorityData:
                priority_data += data[i]
            i += 1
            sorted_indices = priority.sort(priority_data)
            new_priority_data = []
            new_speakers = []
            for index in sorted_indices:
                new_priority_data += self._priorityData[index]
                new_speakers += self._speakers[index]
            self._priorityData = new_priority_data
            self._speakers = new_speakers
    
    def insert(self, index: int, value: list) -> None:
        """
        Inserts a new speaker at specified index (without enforcing proper prioritization).
        
        :param index: position on speak list
        :param value: list of name and priority data
        """
        self._speakers.insert(index, value[0])
        priority_data = []
        i = 1
        for _ in self._priorities:
            priority_data += value[i]
            i += 1
        self._priorityData.insert(index, priority_data)
    
    def __iter__(self) -> Iterator:
        return iter(self._speakers)
    
    def __len__(self) -> int:
        return len(self._speakers)
    
    def __contains__(self, item: str) -> bool:
        return item in self._speakers
    
    def __getitem__(self, index: Union[int, slice]) -> str:
        return self._speakers.__getitem__(index)
    
    def __setitem__(self, key: Union[int, slice], value: list) -> None:
        self._speakers.__setitem__(key, value[0])
        priority_data = []
        i = 1
        for _ in self._priorities:
            priority_data += value[i]
            i += 1
        self._priorityData.__setitem__(key, priority_data)
    
    def __delitem__(self, key: Union[int, slice]) -> None:
        self._speakers.__delitem__(key)
        self._priorityData.__delitem__(key)


class Priority:
    """Defines an abstract class for priorities for the queue."""
    
    @abstractmethod
    def is_valid_list(self, queue: List[Any]) -> bool:
        """Checks if given list is valid.
        
        :param queue: list with priority data for this priority
        :return: True if the given list is valid
        """
        raise NotImplementedError
    
    @abstractmethod
    def sort(self, queue: List[Any]) -> List[int]:
        """Given a list with priority data the method returns the sorted list of keys.
        
        :param queue: list with priority data for this priority
        :return: sorted list of keys
        """
        raise NotImplementedError
    
    @abstractmethod
    def gettype(self) -> type:
        """Returns the type for the priority data of this priority.
        
        :return: any type
        """
        raise NotImplementedError


class FirstSpeakerPriority(Priority):
    """Defines the first speaker priority."""

    def is_valid_list(self, queue: List[str]) -> bool:
        pass

    def sort(self, queue: List[str]) -> List[int]:
        pass

    def gettype(self) -> type:
        return type(str)


class FITSoftPriority(Priority):
    """Defines a soft FIT priority."""

    def is_valid_list(self, queue: List[bool]) -> bool:
        pass

    def sort(self, queue: List[bool]) -> List[int]:
        pass

    def gettype(self) -> type:
        return type(bool)
