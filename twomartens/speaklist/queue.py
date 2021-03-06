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
from collections import Iterator, MutableSequence, deque, Counter
from typing import List, Union, Any, Dict


def sort_data(sorted_indices: List[int], data: List[Any]) -> List[Any]:
    """Sorts the data using given indices.

    :param sorted_indices: sorted indices
    :param data: data
    :return: sorted data
    """
    new_data = []
    for index in sorted_indices:
        new_data.append(data[index])
    return new_data


class Queue(MutableSequence):
    """Implements a priority queue with multiple priorities considered."""
    
    def __init__(self, priorities: List['Priority']) -> None:
        """
        Initializes the priority queue.
        
        :param priorities: list of Priorities to consider
        """
        self._speakers = deque()  # type: deque
        self._priorityData = deque()  # type: deque
        self._priorities = priorities
    
    def is_prioritized(self) -> bool:
        """Checks if the queue is properly prioritized.
        
        :return: True if the queue is prioritized
        """
        i = 0
        for priority in self._priorities:
            priority_data = []
            for data in self._priorityData:
                priority_data.append(data[i])
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
                priority_data.append(data[i])
            i += 1
            sorted_indices = priority.sort(priority_data)
            new_priority_data = []
            new_speakers = []
            for index in sorted_indices:
                new_priority_data.append(self._priorityData[index])
                new_speakers.append(self._speakers[index])
            self._priorityData = new_priority_data
            self._speakers = new_speakers
    
    def insert(self, index: int, value: list) -> None:
        """
        Inserts a new speaker at specified index (without enforcing proper prioritization).
        
        :param index: position on speak list
        :param value: list of name and priority data
        """
        priority_data = []
        i = 1
        for priority in self._priorities:
            if not priority.is_valid_insert(self._get_priority_data()[priority], value[i]):
                raise ValueError
            priority_data.append(value[i])
            i += 1
        self._speakers.insert(index, value[0])
        self._priorityData.insert(index, priority_data)
    
    def append(self, value: List[Any]) -> None:
        """
        Appends a new speaker at the end of the queue (without enforcing prioritization).
        
        :param value: list of name and priority data
        """
        priority_data = []
        i = 1
        for priority in self._priorities:
            if not priority.is_valid_insert(self._get_priority_data()[priority], value[i]):
                raise ValueError
            priority_data.append(value[i])
            i += 1
        self._speakers.append(value[0])
        self._priorityData.append(priority_data)
    
    def pop(self, index=0) -> str:
        """
        Pops the next speaker from the queue.
        
        :param index: not used by this implementation
        :return: name of the next speaker
        """
        speaker = self._speakers.popleft()
        self._priorityData.popleft()
        return speaker
    
    def _get_priority_data(self) -> Dict['Priority', List[Any]]:
        i = 0
        priority_data = {}
        for priority in self._priorities:
            __priority_data = []
            for data in self._priorityData:
                __priority_data.append(data[i])
            i += 1
            priority_data[priority] = __priority_data
        return priority_data
    
    def __iter__(self) -> Iterator:
        return iter(self._speakers)
    
    def __len__(self) -> int:
        return len(self._speakers)
    
    def __contains__(self, item: str) -> bool:
        return item in self._speakers
    
    def __getitem__(self, index: Union[int, slice]) -> str:
        return self._speakers.__getitem__(index)
    
    def __setitem__(self, key: Union[int, slice], value: list) -> None:
        priority_data = []
        i = 1
        for priority in self._priorities:
            if not priority.is_valid_insert(self._get_priority_data()[priority], value[i]):
                raise ValueError
            priority_data += value[i]
            i += 1
        self._speakers.__setitem__(key, value[0])
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
    
    @abstractmethod
    def is_valid_insert(self, queue: List[Any], item: Any) -> bool:
        """Given a list with priority data and the priority data of the new item it returns if the new item is allowed.
        
        :param queue: list with priority data for this priority
        :param item: priority data of new item
        :return: True if new item is allowed
        """
        raise NotImplementedError


class FirstSpeakerPriority(Priority):
    """Defines the first speaker priority."""
    
    def is_valid_list(self, queue: List[str]) -> bool:
        length = len(queue)
        if length < 3:
            return True
        
        max_counter = Counter(queue)
        current_counter = {}
        
        for speaker in queue:
            if speaker not in current_counter:
                current_counter[speaker] = 1
            else:
                for potential_speaker in max_counter:
                    if potential_speaker == speaker:
                        continue
                    if potential_speaker not in current_counter:
                        return False
                current_counter[speaker] += 1
        
        return True

    def sort(self, queue: List[str]) -> List[int]:
        pass

    def gettype(self) -> type:
        return type(str)
    
    def is_valid_insert(self, queue: List[Any], item: Any) -> bool:
        return True


class FITSoftPriority(Priority):
    """Defines a soft FIT priority."""

    def is_valid_list(self, queue: List[bool]) -> bool:
        length = len(queue)
        if length < 3:
            return True
        
        number_of_FIT = queue.count(True)
        counter = 0
        for value in queue:
            if number_of_FIT == 0:
                return counter == 0
            if number_of_FIT > 0 and counter < -1:
                return False
            if value:
                if counter < 0:
                    counter += 1
                number_of_FIT -= 1
            else:
                counter -= 1
        return counter == 0

    def sort(self, queue: List[bool]) -> List[int]:
        indices = []
        true_indices = deque()
        false_indices = deque()
        index = 0
        for value in queue:
            indices.append(index)
            if value:
                true_indices.append(index)
            else:
                false_indices.append(index)
            index += 1
        
        if self.is_valid_list(queue):
            return indices
            
        indices = []
        number_of_FIT = len(true_indices)
        step = 0
        while number_of_FIT > 0:
            if step % 2 == 0:
                # step 1: take FIT person
                index = true_indices.popleft()
                indices.append(index)
                number_of_FIT -= 1
            else:
                try:
                    index = false_indices.popleft()
                    indices.append(index)
                except IndexError:
                    break
            step += 1
        if number_of_FIT > 0:
            indices.extend(true_indices)
        else:
            indices.extend(false_indices)
        
        return indices

    def gettype(self) -> type:
        return type(bool)
    
    def is_valid_insert(self, queue: List[bool], item: bool) -> bool:
        return True
