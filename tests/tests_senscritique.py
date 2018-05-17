import unittest

import senscritique


class TestSensCritiqueMethods(unittest.TestCase):

    def test_get_user_example(self):
        example_user_name = 'عمرالعرفاوي'

        return example_user_name

    def test_print_data(self):
        data = senscritique.parse_and_cache(user_name=self.test_get_user_example(), data_type='collection')
        senscritique.print_data(data)
        self.assertGreater(len(data), 0)

    def test_parse_with_wrong_arguments(self):
        data = senscritique.parse(user_name='wok', data_type='wrong_argument')

        self.assertEqual(len(data), 0)

    def test_parse_and_cache(self):
        # Download
        downloaded_data = senscritique.parse_and_cache(user_name=self.test_get_user_example(), data_type='collection')
        # Load from cache
        loaded_data = senscritique.parse_and_cache(user_name=self.test_get_user_example(), data_type='collection')

        self.assertDictEqual(downloaded_data, loaded_data)


if __name__ == '__main__':
    unittest.main()
