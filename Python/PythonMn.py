import pyphen
import math
import time

class Mongol1:
    def __init__(self):
        self.dic = pyphen.Pyphen(filename='hyph_mn_MN.dic')

    def hyphenate(self, word):
        inserted = self.dic.inserted(word)
        cuts = [i for i, c in enumerate(inserted) if c == "-"]
        return cuts


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

def greedy(text, width, hyph):
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
                    result.append(justify_line(line_words, width))
                    line_words = [right]
                    current_len = len(right)
                    placed = True
                    break

            if not placed:
                result.append(justify_line(line_words, width))
                line_words = [w]
                current_len = len(w)

    if line_words:
        result.append(justify_line(line_words, width))
    return result

def dp(text, width):
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
        lines.append(justify_line(words[i:j], width))
        i = j

    return lines

def compare_and_print(text, width, hy):
    print("\nГүйцэтгэлийн харьцуулалт")

    t1 = time.perf_counter()
    greedy_out = greedy(text, width, hy)
    t2 = time.perf_counter()
    greedy_ms = (t2 - t1) * 1000

    t3 = time.perf_counter()
    dp_out = dp(text, width)
    t4 = time.perf_counter()
    dp_ms = (t4 - t3) * 1000

    print(f"Greedy: {greedy_ms:.4f} ms")
    print(f"DP: {dp_ms:.4f} ms")

    print("\n Greedy;")
    for line in greedy_out:
        print(line)

    print("\nDP;")
    for line in dp_out:
        print(line)

if __name__ == "__main__":
    hy = Mongol1()

    print("Текстээ оруулна уу:")
    text = input("> ")

    width = int(input("Мөрийн өргөн: "))

    compare_and_print(text, width, hy)
