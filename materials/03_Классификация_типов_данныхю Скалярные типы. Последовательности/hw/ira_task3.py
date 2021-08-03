
text =(input('Enter your text:'))
a = text.replace("Черт", "####").replace("черт", "####").replace("чЕрт", "####").replace("черТ", "####").replace("ЧЕРТ", "####")
print(a)
