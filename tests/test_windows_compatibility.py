import unittest
import platform

class TestWindowsCompatibility(unittest.TestCase):
    @unittest.skipIf(platform.system() != "Windows", "Windows specific test")
    def test_import_languages_on_windows(self):
        """Test that languages can be imported correctly on Windows."""
        import tree_sitter_language_pack
           
        # Essayer de charger quelques langages courants
        languages_to_test = ['python', 'javascript', 'typescript', 'java']
           
        for lang in languages_to_test:
           try:
               language = tree_sitter_language_pack.get_language(lang)
               self.assertIsNotNone(language, f"The language {lang} could not be loaded")
               
               parser = tree_sitter_language_pack.get_parser(lang)
               self.assertIsNotNone(parser, f"The parser for {lang} could not be created")
           except Exception as e:
               self.fail(f"Error loading language {lang}: {str(e)}")

if __name__ == "__main__":
   unittest.main()