class MaxHeap:
    """
    A Max Heap Data Structure.
    ABT's operations: insert, extract_root
    Functions: heapify, build, sort
    """
    @classmethod
    def heapify(cls, arr, n, i, com_func):
        l = 2 * i + 1 # left child
        r = 2 * i + 2 # right child
        largest = i
        left = l < n
        right = r < n

        # check if children are greater than parent
        if left and com_func(arr[l], arr[largest]):
            largest = l

        if right and com_func(arr[r], arr[largest]):
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i] # swap parent with largest child
            cls.heapify(arr, n, largest, com_func) # check a new parent

    @classmethod
    def build(cls, array, com_func=lambda x, y: x > y):
        for i in range(len(array) // 2, -1, -1):
            cls.heapify(array, len(array), i, com_func)

    @classmethod
    def sort(cls, array, com_func=lambda x, y: x > y):
        cls.build(array, com_func)
        for i in range(len(array) - 1, -1, -1):
            array[0], array[i] = array[i], array[0]
            cls.heapify(array, i, 0, com_func)

    @classmethod
    def insert(cls, key, arr, com_func=lambda x, y: x > y):
        arr.append(key)
        i = (len(arr) - 2) // 2
        while i >= 0 and com_func(key, arr[i]):
            cls.heapify(arr, len(arr), i, com_func)
            i = (i - 1) // 2

    @classmethod
    def extract_root(cls, arr, com_func=lambda x, y: x > y):
        arr[0], arr[-1] = arr[-1], arr[0]
        root = arr.pop()
        cls.heapify(arr, len(arr), 0, com_func)
        return root

    @classmethod
    def display(cls, arr):
        try:
            lines, _, _, _ = cls._display_aux(arr, 0)
            for line in lines:
                print(line)
        except IndexError:
            print("-")

    @classmethod
    def _display_aux(cls, arr, i=0):
        n = len(arr)
        l = 2 * i + 1 # left child
        r = 2 * i + 2 # right child
        left = l < n
        right = r < n
        # No child.
        if not right and not left:
            line = f"{arr[i]}"
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if not right:
            lines, n, p, x = cls._display_aux(arr, l)
            s = f"{arr[i]}"
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if not left:
            lines, n, p, x = cls._display_aux(arr, r)
            s = f"{arr[i]}"
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2
        # Two children.
        left, n, p, x = cls._display_aux(arr, l)
        right, m, q, y = cls._display_aux(arr, r)
        s = f"{arr[i]}"
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class MinHeap(MaxHeap):
    """
    A Min Heap Data Structure.
    ABT's operations: insert, extract_root
    Functions: heapify, build, sort
    """
    @classmethod
    def build(cls, array, com_func=lambda x, y: x < y):
        super().build(array, com_func)

    @classmethod
    def sort(cls, array, com_func=lambda x, y: x < y):
        super().sort(array, com_func)

    @classmethod
    def insert(cls, x, arr, com_func=lambda x, y: x < y):
        super().insert(x, arr, com_func)

    @classmethod
    def extract_root(cls, arr, com_func=lambda x, y: x < y):
        return super().extract_root(arr, com_func)

