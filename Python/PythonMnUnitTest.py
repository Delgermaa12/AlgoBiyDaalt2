import unittest
from PythonMn import greedy, dp, Mongol1


class TestTextJustifyAlgorithms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hyph = Mongol1()
        cls.width = 20
    def test_basic_output_type(self):
        text = "Монгол хэлний үгийг зөв таслана"
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        self.assertIsInstance(greedy_result, list)
        self.assertIsInstance(dp_result, list)

    def test_line_length_not_exceed_width(self):
        text = "Монгол хэл дээр мөрийг зөв таслах ёстой текст"
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        for line in greedy_result:
            self.assertLessEqual(len(line), self.width)

        for line in dp_result:
            self.assertLessEqual(len(line), self.width)

    def test_dp_better_or_equal(self):
        text = "Энэ бол текстийг зөв мөр таслах хоёр өөр алгоритмын харьцуулалт юм."
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        def badness(lines):
            b = 0
            for ln in lines[:-1]:
                b += (self.width - len(ln)) ** 2
            return b

        greedy_score = badness(greedy_result)
        dp_score = badness(dp_result)

        self.assertLessEqual(dp_score, greedy_score)

    def test_hyphenation_cut(self):
        word = "хөгжүүлэх"
        cuts = self.hyph.hyphenate(word)

        self.assertGreater(len(cuts), 0)
        for pos in cuts:
            self.assertTrue(0 < pos < len(word))

    def test_short_text_same(self):
        text = "Сайн байна уу"
        greedy_result = greedy(text, self.width, self.hyph)
        dp_result = dp(text, self.width)

        self.assertEqual(len(greedy_result), len(dp_result))

    def test_hyphenation_bugood(self):
        word = "бөгөөд"
        width = 3

        result = greedy(word, width, self.hyph)

        self.assertTrue(any("-" in line for line in result))

        rejoined = "".join(line.replace("-", "") for line in result)
        self.assertEqual(rejoined, word)

        valid_cuts = self.hyph.hyphenate(word)

        for line in result:
            if "-" in line:
                cut_pos = len(line.split("-")[0])
                self.assertIn(cut_pos, valid_cuts)


if __name__ == "__main__":
    unittest.main()
