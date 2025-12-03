import pyphen
import math
import time

# -----------------------
# HYPHENATOR USING PYPHEN
# -----------------------
class SimpleHyphenator:
    def __init__(self):
        # Mongolian hyphenation
        self.dic = pyphen.Pyphen(lang='mn_MN')

    def hyphenate(self, word):
        """Return cut positions (integers) where word can be hyphenated."""
        inserted = self.dic.inserted(word)  # Inserts '-' where it can be broken
        cuts = [i for i, c in enumerate(inserted) if c == "-"]
        return cuts

# -----------------------
# ALIGNMENT FUNCTIONS
# -----------------------
def left_align(line, width):
    return line

def right_align(line, width):
    return " " * (width - len(line)) + line

def center_align(line, width):
    pad = (width - len(line)) // 2
    return " " * pad + line

def justify_line(words, width):
    if len(words) == 1:
        return words[0]

    total_chars = sum(len(w) for w in words)
    spaces_needed = width - total_chars
    gaps = len(words) - 1

    base = spaces_needed // gaps
    extra = spaces_needed % gaps

    line = ""
    for i, w in enumerate(words):
        line += w
        if i < gaps:
            line += " " * (base + (1 if i < extra else 0))

    return line

# -----------------------
# GREEDY JUSTIFICATION
# -----------------------
def greedy_justify(text, width, hyph):
    words = text.split()
    result = []
    line_words = []
    current_len = 0

    for w in words:
        if current_len + len(w) + len(line_words) <= width:
            line_words.append(w)
            current_len += len(w)
        else:
            cuts = hyph.hyphenate(w)
            placed = False

            for c in reversed(cuts):
                left = w[:c] + "-"
                right = w[c:]

                if current_len + len(left) + len(line_words) <= width:
                    line_words.append(left)
                    result.append(" ".join(line_words))
                    line_words = [right]
                    current_len = len(right)
                    placed = True
                    break

            if not placed:
                result.append(" ".join(line_words))
                line_words = [w]
                current_len = len(w)

    if line_words:
        result.append(" ".join(line_words))
    return result

# -----------------------
# DP JUSTIFICATION
# -----------------------
def dp_justify(text, width):
    words = text.split()
    n = len(words)

    def badness(i, j):
        line_words = words[i:j]
        total_chars = sum(len(w) for w in line_words)
        spaces = j - i - 1
        length = total_chars + spaces
        if length > width:
            return math.inf
        return (width - length) ** 2

    dp = [math.inf] * (n + 1)
    nxt = [0] * (n + 1)
    dp[n] = 0

    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            cost = badness(i, j)
            if cost == math.inf:
                break
            if dp[j] + cost < dp[i]:
                dp[i] = dp[j] + cost
                nxt[i] = j

    lines = []
    i = 0
    while i < n:
        j = nxt[i]
        lines.append(" ".join(words[i:j]))
        i = j

    return lines

# -----------------------
# PERFORMANCE COMPARISON
# -----------------------
def compare_performance(text, width, hy):
    print("\nГүйцэтгэлийн харьцуулалт:\n")

    t1 = time.perf_counter()
    greedy_out = greedy_justify(text, width, hy)
    t2 = time.perf_counter()

    t3 = time.perf_counter()
    dp_out = dp_justify(text, width)
    t4 = time.perf_counter()

    greedy_ms = (t2 - t1) * 1000
    dp_ms = (t4 - t3) * 1000

    print(f"Greedy: {greedy_ms:.4f} ms")
    print(f"DP: {dp_ms:.4f} ms")

    return greedy_out, dp_out

# -----------------------
# MAIN PROGRAM
# -----------------------
if __name__ == "__main__":
    hy = SimpleHyphenator()

    print("Текстээ оруулна уу:")
    text = input("> ")

    width = int(input("Мөрийн өргөн: "))

    print("\n== Байршил сонгоно уу ==")
    print("1) Зүүн (Left)")
    print("2) Төв (Center)")
    print("3) Баруун (Right)")
    print("4) Greedy Justify")
    print("5) DP Justify")
    print("6) Performance Compare (Greedy vs DP)")
    mode = int(input("> "))

    lines = greedy_justify(text, width, hy)
    if mode == 5:
        lines = dp_justify(text, width)
    elif mode == 6:
        greedy_out, dp_out = compare_performance(text, width, hy)
        print("\n--- GREEDY JUSTIFIED ---")
        for line in greedy_out:
            print(justify_line(line.split(), width))
        print("\n--- DP JUSTIFIED ---")
        for line in dp_out:
            print(justify_line(line.split(), width))
        exit()

    print("\n== Үр дүн ==")
    for line in lines:
        if mode == 1:
            print(left_align(line, width))
        elif mode == 2:
            print(center_align(line, width))
        elif mode == 3:
            print(right_align(line, width))
        else:
            print(justify_line(line.split(), width))
