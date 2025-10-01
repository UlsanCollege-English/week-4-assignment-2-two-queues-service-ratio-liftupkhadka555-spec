from collections import deque

class Gate:
    def __init__(self):
        # Pattern: 1 fastpass, then 3 regulars
        self._pattern = ["fastpass", "regular", "regular", "regular"]
        self._idx = 0   # always start with fastpass
        self._fast = deque()
        self._reg = deque()

    def arrive(self, line, person_id):
        """Enqueue into the chosen line."""
        if line == "fastpass":
            self._fast.append(person_id)
        elif line == "regular":
            self._reg.append(person_id)
        else:
            raise ValueError("Unknown line type")

    def serve(self):
        """
        Return the next person according to the repeating pattern.
        Skip empty lines but still move the cycle pointer correctly.
        Raise IndexError only if BOTH queues are empty.
        """
        if not self._fast and not self._reg:
            raise IndexError("Both lines are empty")

        # Keep looping until we find someone to serve
        while True:
            line_to_serve = self._pattern[self._idx]

            if line_to_serve == "fastpass" and self._fast:
                person = self._fast.popleft()
                self._idx = (self._idx + 1) % len(self._pattern)
                return person

            if line_to_serve == "regular" and self._reg:
                person = self._reg.popleft()
                self._idx = (self._idx + 1) % len(self._pattern)
                return person

            # Current slot empty → just move pointer to next
            self._idx = (self._idx + 1) % len(self._pattern)

    def peek_next_line(self):
        """
        Predict which line will serve next without dequeuing anyone.
        """
        if not self._fast and not self._reg:
            return None

        temp_idx = self._idx
        # Check up to two full cycles to safely predict
        for _ in range(len(self._pattern) * 2):
            line = self._pattern[temp_idx]
            if line == "fastpass" and self._fast:
                return "fastpass"
            if line == "regular" and self._reg:
                return "regular"
            temp_idx = (temp_idx + 1) % len(self._pattern)

        return None
