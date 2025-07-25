class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

# Manual min-heap insert
def insert_min_heap(heap, node):
    heap.append(node)
    i = len(heap) - 1
    while i > 0:
        parent = (i - 1) // 2
        if heap[parent].freq > heap[i].freq:
            heap[parent], heap[i] = heap[i], heap[parent]
            i = parent
        else:
            break

# Manual min-heap extract min
def extract_min(heap):
    if len(heap) == 0:
        return None
    min_node = heap[0]
    last_node = heap.pop()
    if heap:
        heap[0] = last_node
        min_heapify(heap, 0)
    return min_node

def min_heapify(heap, i):
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < len(heap) and heap[left].freq < heap[smallest].freq:
        smallest = left
    if right < len(heap) and heap[right].freq < heap[smallest].freq:
        smallest = right
    if smallest != i:
        heap[i], heap[smallest] = heap[smallest], heap[i]
        min_heapify(heap, smallest)

def build_huffman_tree(char_freq):
    heap = []
    for char, freq in char_freq:
        insert_min_heap(heap, Node(char, freq))

    while len(heap) > 1:
        left = extract_min(heap)
        right = extract_min(heap)
        new_node = Node(None, left.freq + right.freq)
        new_node.left = left
        new_node.right = right
        insert_min_heap(heap, new_node)

    return heap[0] if heap else None

def generate_codes(node, current_code, codes):
    if node is None:
        return
    if node.char is not None:
        codes[node.char] = current_code
        return
    generate_codes(node.left, current_code + '0', codes)
    generate_codes(node.right, current_code + '1', codes)

def decode_huffman(encoded_str, root):
    result = ""
    current = root
    for bit in encoded_str:
        if bit == '0':
            current = current.left
        else:
            current = current.right
        if current.char is not None:
            result += current.char
            current = root
    return result

# Input Handling
text = input("Enter a string for Huffman Coding: ").strip()
if not text:
    print("Empty input. Exiting.")
    exit()

# Frequency map
frequency = {}
for char in text:
    frequency[char] = frequency.get(char, 0) + 1

char_freq = list(frequency.items())

# Build Huffman Tree and Generate Codes
root = build_huffman_tree(char_freq)
codes = {}
generate_codes(root, "", codes)

# Display Codes
print("\nHuffman Codes:")
for char in sorted(codes):
    print(f"{repr(char)}: {codes[char]}")

# Encode the string
encoded = ''.join(codes[c] for c in text)
print("\nEncoded String:", encoded)

# Decode it back
decoded = decode_huffman(encoded, root)
print("\nDecoded String:", decoded)

# Validation
if decoded == text:
    print("\nDecoding is correct. Compression successful.")
else:
    print("\nDecoding failed.")
