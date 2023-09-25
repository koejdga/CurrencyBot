import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang="uk")


def number_and_noun(num: float, input_word: float):
    words = input_word.split(" ")
    result = str(num)

    for word in words:
        result += " "
        word = morph.parse(word)[0]

        try:
            if num == 1:
                result += word.normal_form
            elif round(num) in (2, 3, 4) or (num > 1 and num < 2):
                result += word.inflect({"plur"}).word
            else:
                result += word.inflect({"plur", "gent"}).word
        except:
            result = f'{number_and_noun(num, "грошова одиниця")} ({input_word})'

    return result


def isfloat(num: str):
    num = num.replace(",", ".")
    try:
        float(num)
        return True
    except ValueError:
        return False
