import unittest
from PythonMn import greedy_justify, dp_justify, Mongol1

# Танд байгаа кодыг your_file_name.py гэж нэрлэсэн гэж үзэв.
# Хэрэв өөр нэртэй бол үүнийг өөрчлөөрэй!


class TestTextJustifyAlgorithms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hyph = Mongol1()  # Монгол хэлний hyphenation
        cls.width = 20

    # --------------------------------------------------
    # 1. Үндсэн функц ажиллаж байгаа эсэх
    # --------------------------------------------------
    def test_basic_output_type(self):
        text = "Монгол хэлний үгийг зөв таслана"
        greedy_result = greedy_justify(text, self.width, self.hyph)
        dp_result = dp_justify(text, self.width)

        self.assertIsInstance(greedy_result, list)
        self.assertIsInstance(dp_result, list)

    # --------------------------------------------------
    # 2. Хоёр алгоритм мөр урт хэтрүүлэхгүй байх ёстой
    # --------------------------------------------------
    def test_line_length_not_exceed_width(self):
        text = "Монгол хэл дээр мөрийг зөв таслах ёстой текст"
        greedy_result = greedy_justify(text, self.width, self.hyph)
        dp_result = dp_justify(text, self.width)

        for line in greedy_result:
            self.assertLessEqual(len(line), self.width)

        for line in dp_result:
            self.assertLessEqual(len(line), self.width)

    # --------------------------------------------------
    # 3. DP алгоритм Greedy-аас бага/тэнцүү badness-тай эсэх
    # --------------------------------------------------
    def test_dp_better_or_equal(self):
        text = "Энэ бол текстийг зөв мөр таслах хоёр өөр алгоритмын харьцуулалт юм."
        greedy_result = greedy_justify(text, self.width, self.hyph)
        dp_result = dp_justify(text, self.width)

        def badness(lines):
            b = 0
            for ln in lines[:-1]:  # Сүүлийн мөрт badness авдаггүй
                b += (self.width - len(ln)) ** 2
            return b

        greedy_score = badness(greedy_result)
        dp_score = badness(dp_result)

        self.assertLessEqual(dp_score, greedy_score)

    # --------------------------------------------------
    # 4. Hyphenation зөв ажиллаж байгаа эсэх
    # --------------------------------------------------
    def test_hyphenation_cut(self):
        word = "хөгжүүлэх"
        cuts = self.hyph.hyphenate(word)

        self.assertGreater(len(cuts), 0)
        for pos in cuts:
            self.assertTrue(0 < pos < len(word))

    # --------------------------------------------------
    # 5. Цөөн үгтэй текст дээр Greedy ба DP адил үр дүнтэй
    # --------------------------------------------------
    def test_short_text_same(self):
        text = "Сайн байна уу"
        greedy_result = greedy_justify(text, self.width, self.hyph)
        dp_result = dp_justify(text, self.width)

        self.assertEqual(len(greedy_result), len(dp_result))

    # --------------------------------------------------
    # 6. Маш урт үг дээр таслалт хийгдэх эсэх
    # --------------------------------------------------
    def test_hyphenation_bugood(self):
        word = "бөгөөд"
        width = 3

        result = greedy_justify(word, width, self.hyph)

        # 1. "-" заавал байх
        self.assertTrue(any("-" in line for line in result))

        # 2. Нийлүүлэхэд буцаад анхны үг болох ёстой
        rejoined = "".join(line.replace("-", "") for line in result)
        self.assertEqual(rejoined, word)

        # 3. Тасалсан байрлал зөв байх
        valid_cuts = self.hyph.hyphenate(word)

        for line in result:
            if "-" in line:
                cut_pos = len(line.split("-")[0])
                self.assertIn(cut_pos, valid_cuts)


if __name__ == "__main__":
    unittest.main()
