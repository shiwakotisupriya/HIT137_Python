"""
Group Name: SYDN 52
Group Members:
Supriya Shiwakoti - s399239
Anil Bhusal - s399244
Sabin Gautam - s399243
Sanjaya Thapa - s399408
"""

def characterEncript(character, shift1, shift2):
    # Character encription using a shift rule
    if character.islower():
        if 'a' <= character <= 'm':
            shift = shift1 * shift2
            new_pos = (ord(character) - ord('a') + shift) % 26
            return chr(ord('a') + new_pos), 'half_lower'
        else:
            shift = shift1 + shift2
            new_pos = (ord(character) - ord('a') - shift) % 26
            return chr(ord('a') + new_pos), 'secondhalf_lower'
    elif character.isupper():
        if 'A' <= character <= 'M':
            shift = shift1
            new_pos = (ord(character) - ord('A') - shift) % 26
            return chr(ord('A') + new_pos), 'half_upper'
        else:
            shift = shift2 ** 2
            new_pos = (ord(character) - ord('A') + shift) % 26
            return chr(ord('A') + new_pos), 'secondhalf_upper'
    else:
        return character, 'unchanged'

def characterDecript(character, rule, shift1, shift2):
    # Decription by reversing a encription that is based on the applied rule
    shifts = {
        'half_lower': (shift1 * shift2, 'a', -1),
        'secondhalf_lower': (shift1 + shift2, 'a', 1),
        'half_upper': (shift1, 'A', 1),
        'secondhalf_upper': (shift2 ** 2, 'A', -1)
    }
    
    if rule in shifts:
        shift, base, direction = shifts[rule]
        new_pos = (ord(character) - ord(base) + direction * shift) % 26
        return chr(ord(base) + new_pos)
    return character

def file_encription(fileInput, fileOutput, filerules, shift1, shift2):
    # Encripts the file by applying the shift rule and saves it  
    try:
        with open(fileInput, 'r', encoding='utf-8') as f:
            content = f.read()
        
        encrypted_chars, rules = [], []
        for char in content:
            encrypted_char, rule = characterEncript(char, shift1, shift2)
            encrypted_chars.append(encrypted_char)
            rules.append(rule)
        
        with open(fileOutput, 'w', encoding='utf-8') as f:
            f.write(''.join(encrypted_chars))
        with open(filerules, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rules))
        
        print(f"Encryption is complete and output has been saved to '{fileOutput}'.")
        return True
    except FileNotFoundError:
        print(f"Error: Input file '{fileInput}' not found.")
        return False
    except Exception as e:
        print(f"Encryption error: {e}")
        return False

def fileDecription(fileInput, filerules, fileOutput, shift1, shift2):
    # Decripts and saves the file contents by reading the encription rule file saved
    try:
        with open(fileInput, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(filerules, 'r', encoding='utf-8') as f:
            rules = f.read().split('\n')
        
        if len(content) != len(rules):
            print(f"Error: Content and rules length mismatch.")
            return False
        
        decrypted_chars = [characterDecript(char, rule, shift1, shift2) 
                          for char, rule in zip(content, rules)]
        
        with open(fileOutput, 'w', encoding='utf-8') as f:
            f.write(''.join(decrypted_chars))
        
        print(f"Decryption completed. Output saved to '{fileOutput}'.")
        return True
    except FileNotFoundError:
        print(f"Error: Required file not found.")
        return False
    except Exception as e:
        print(f"Decryption error: {e}")
        return False

def verify_decryption(original_file, decrypted_file):
    # Verifies decription to make sure the original file matchs the decripted file
    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            original = f.read()
        with open(decrypted_file, 'r', encoding='utf-8') as f:
            decrypted = f.read()
        
        if original == decrypted:
            print(f"Verification successful: Files match ({len(original)} characters).")
            return True
        else:
            print(f"Verification failed: Files do not match.")
            return False
    except Exception as e:
        print(f"Verification error: {e}")
        return False

def main():
    # main function to call all other function
    print("Text File Encryption System")
    print("-" * 40)
    
    try:
        shift1 = int(input("Enter shift1 value: "))
        shift2 = int(input("Enter shift2 value: "))
    except ValueError:
        print("Error: Invalid input. Please enter integers.")
        return
    
    print(f"\nProcessing with shift1={shift1}, shift2={shift2}")
    
    if not file_encription("raw_text.txt", "encript_file.txt", "encryption_rules.txt", shift1, shift2):
        return
    if not fileDecription("encript_file.txt", "encryption_rules.txt", "decript_file.txt", shift1, shift2):
        return
    verify_decryption("raw_text.txt", "decript_file.txt")

if __name__ == "__main__":
    main()