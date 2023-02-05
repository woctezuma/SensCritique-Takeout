import unittest

import senscritique


class TestSensCritiqueMethods(unittest.TestCase):
    @classmethod
    def test_get_user_example(cls):
        example_user_name = 'Pipo'

        return example_user_name

    def test_parse_with_wrong_arguments(self):
        data = senscritique.parse(user_name='wok', data_type='wrong_argument')

        self.assertEqual(len(data), 0)

    def test_parse_and_cache(self):
        # Download
        downloaded_data = senscritique.parse_and_cache(
            user_name=self.test_get_user_example(),
            data_type='collection',
        )
        # Load from cache
        loaded_data = senscritique.parse_and_cache(
            user_name=self.test_get_user_example(),
            data_type='collection',
        )

        self.assertDictEqual(downloaded_data, loaded_data)

    def test_parse_collection(self):
        data = senscritique.parse(
            user_name=self.test_get_user_example(),
            data_type='collection',
            verbose=True,
        )
        senscritique.print_data(data)
        self.assertEqual(len(data), 6)

    def test_parse_critiques(self):
        data = senscritique.parse(
            user_name='MrMez',
            data_type='critiques',
            verbose=True,
        )
        senscritique.print_data(data)
        self.assertEqual(len(data), 2)

    def test_parse_listes(self):
        data = senscritique.parse(user_name='Pop-Dan', data_type='listes', verbose=True)
        senscritique.print_data(data)
        self.assertEqual(len(data), 33)


if __name__ == '__main__':
    unittest.main()
