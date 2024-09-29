alphapet= ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']




# def encrypt(orginal_text, shift_amount):
#     cipher_text = "" 

#     for letter in orginal_text:
#         shift_position = alphapet.index(letter) +shift_amount
#         shift_position %= len(alphapet)
#         cipher_text +=alphapet[shift_position]

#     print(f"Here is the encode result :{cipher_text}")   



def ceaser(orginal_text, shift_amount , encode_or_decode):
    output_text = "" 

    if encode_or_decode =="decode":
            shift_amount *= -1

    for letter in orginal_text:
            
            if letter not in alphapet:
                 output_text+=letter
            else:
                shift_position = alphapet.index(letter) + shift_amount
                shift_position %= len(alphapet)
                output_text += alphapet[shift_position]
    print(f"Here is the {encode_or_decode}d result :{output_text}")   

should_continue = True

while should_continue:
      
    direction = input("type'encode' to encrypt, type'decode' to decrypt:\n") .lower()
    text = input("Type youre message : \n") .lower()
    shift = int(input("type the shift number : \n "))
      
    ceaser(orginal_text=text,shift_amount=shift,encode_or_decode=direction)

    restart = input("Type 'yes' if you want to go agin . Othewise, type 'no'. \n").lower()
    if restart =="no":
      should_continue = False
      print("Goodbye")