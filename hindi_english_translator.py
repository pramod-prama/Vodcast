#!/usr/bin/env python3
"""
Hindi to English Translator
A Python script that translates Hindi text to English using Google Translate API
"""

from googletrans import Translator
import sys
import argparse

class HindiEnglishTranslator:
    def __init__(self):
        """Initialize the translator"""
        self.translator = Translator()
    
    def translate_text(self, hindi_text):
        """
        Translate Hindi text to English
        
        Args:
            hindi_text (str): Hindi text to translate
            
        Returns:
            str: Translated English text
        """
        try:
            # Detect if the input is actually Hindi
            detected = self.translator.detect(hindi_text)
            
            if detected.lang == 'hi':
                # Translate from Hindi to English
                result = self.translator.translate(hindi_text, src='hi', dest='en')
                return result.text
            else:
                # If not Hindi, still attempt translation but warn user
                result = self.translator.translate(hindi_text, dest='en')
                print(f"Warning: Detected language is '{detected.lang}', not Hindi")
                return result.text
                
        except Exception as e:
            return f"Translation error: {str(e)}"
    
    def translate_file(self, input_file, output_file=None):
        """
        Translate text from a file
        
        Args:
            input_file (str): Path to input file with Hindi text
            output_file (str): Path to output file for English translation
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                hindi_content = f.read()
            
            translated = self.translate_text(hindi_content)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(translated)
                print(f"Translation saved to {output_file}")
            else:
                print("Translated text:")
                print(translated)
                
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found")
        except Exception as e:
            print(f"Error processing file: {str(e)}")
    
    def interactive_mode(self):
        """Run interactive translation mode"""
        print("Hindi to English Translator")
        print("Type 'quit' to exit")
        print("-" * 30)
        
        while True:
            hindi_input = input("\nEnter Hindi text: ").strip()
            
            if hindi_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if hindi_input:
                english_output = self.translate_text(hindi_input)
                print(f"English: {english_output}")
            else:
                print("Please enter some text to translate")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Translate Hindi text to English')
    parser.add_argument('--text', '-t', help='Hindi text to translate')
    parser.add_argument('--file', '-f', help='Input file with Hindi text')
    parser.add_argument('--output', '-o', help='Output file for translation')
    parser.add_argument('--interactive', '-i', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    translator = HindiEnglishTranslator()
    
    if args.interactive:
        translator.interactive_mode()
    elif args.text:
        result = translator.translate_text(args.text)
        print(f"Translation: {result}")
    elif args.file:
        translator.translate_file(args.file, args.output)
    else:
        # No arguments provided, run interactive mode
        translator.interactive_mode()

# Example usage functions
def example_usage():
    """Demonstrate different ways to use the translator"""
    translator = HindiEnglishTranslator()
    
    # Example 1: Simple text translation
    hindi_text = "नमस्ते, आप कैसे हैं?"
    english_text = translator.translate_text(hindi_text)
    print(f"Hindi: {hindi_text}")
    print(f"English: {english_text}")
    
    # Example 2: Multiple sentences
    hindi_paragraph = """
    भारत एक विविधताओं से भरा देश है। 
    यहाँ कई भाषाएँ बोली जाती हैं।
    हमारी संस्कृति बहुत समृद्ध है।
    """
    
    english_paragraph = translator.translate_text(hindi_paragraph)
    print(f"\nHindi Paragraph:\n{hindi_paragraph}")
    print(f"English Translation:\n{english_paragraph}")

if __name__ == "__main__":
    # Check if googletrans is installed
    try:
        from googletrans import Translator
    except ImportError:
        print("Error: googletrans library not found!")
        print("Install it using: pip install googletrans==4.0.0rc1")
        sys.exit(1)
    
    main()