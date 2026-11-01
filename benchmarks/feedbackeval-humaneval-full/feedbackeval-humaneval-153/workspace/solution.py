def Strongest_Extension(class_name, extensions):
    def get_strength(extension):
        CAP = sum(1 for letter in extension if letter.isupper())
        SM = sum(1 for letter in extension if letter.islower())
        return CAP - SM

    strongest = max(extensions, key=lambda x: (get_strength(x), extensions.index(x)))
    return f"{class_name}.{strongest}"

# Testing the function
print(Strongest_Extension('my_class', ['AA', 'Be', 'CC']))  # Output: "my_class.AA"
