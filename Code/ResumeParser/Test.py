



def main():
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process

    t = "sad sdasndl sadlksad"
    text = " sad"

    score = fuzz.ratio(t, text.lower())
    print score


if __name__ == '__main__':
    main()
