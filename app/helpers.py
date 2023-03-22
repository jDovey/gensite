from flask import render_template
from math import log10
import re


def check(n):
    if str(n) == str(n)[0] * len(str(n)):
        return True
    else:
        return False

def mask(number_group, number):
    # to be able to mask a number I need to be able to select everything other than the match!
    mask_pattern = r'\d((?:' + number_group + ')*)$'
    masked = re.sub(mask_pattern, r'*\1', number)
    # to be able to put spaces in, must get match of pattern and put space before and after pattern
    matches = re.finditer(number_group, masked)
    i = 0
    for match in matches:
        masked = masked[:match.start()+i] + "-" + masked[match.start()+i:match.end()+i] + "-" + masked[match.end()+i:]
        i += 2

    return masked


def repeats(number):
    answer = {
        "repeats":0,
        "pattern":"",
        "masked":"",
        "value":0
    }
    patternrepeat = r".*?(\1)"
    # iterate through length of group
    # length of group should be able to repeat at least once, hence len by 2, 11//2 = 5
    for i in range(len(number)//2, 0, -1):
        patternlen = r"(\d{" + str(i + 1) + r"})"
        # iterate through amount of repeats
        # gives maximum possible repeats in number depending on len of group
        for j in range(len(number)//i, 0, -1):
            pattern = patternlen + (patternrepeat * j)
            # 3DigitEnd pattern = r'(\d{3}$)'
            # finds Xdigitgroups amount of groups depends on amount of ".*?"
            matches = re.search(pattern, number)
            # '(\d{3}).*?(\1).*?(\1)' - produces matches when there are 3 repeats, can be changed by adding or removing ".*?"
            if matches:
                number_group = matches.group(1)
                repeat_amount = len(matches.groups())
                
                

                # if no match has been added to answer dict yet, populate with current match
                if len(answer["pattern"]) == 0:
                    answer["repeats"] = repeat_amount
                    answer["pattern"] = number_group
                    answer["masked"] = mask(number_group, number)
                    answer["value"] = repeat_amount * log10(len(number_group))

                # compare to current highest value repeat
                # log of substring allows the no. repeats to be valued higher than
                # the length of the pattern
                if (repeat_amount * log10(len(number_group))) > (answer["repeats"] * log10(len(answer["pattern"]))):
                    answer["repeats"] = repeat_amount
                    answer["pattern"] = number_group
                    answer["masked"] = mask(number_group, number)
                    answer["value"] = repeat_amount * log10(len(number_group))


    return answer


def pairs(number):
    answer = {
        "pattern":"",
        "masked":""
    }

    pairs = re.search(r'(\d)\1(?!\1)(\d)\2(?!\1|\2)(\d)\3', number)
    trios = re.search(r'(\d)\1\1(?!\1)(\d)\2\2', number)

    if pairs:
        pairs_pattern = pairs.group()
        pairs_masked = mask(pairs_pattern, number)
        answer["pattern"] = "pairs"
        answer["masked"] = pairs_masked
        return answer
    elif trios:
        trios_pattern = trios.group()
        trios_masked = mask(trios_pattern, number)
        answer["pattern"] = "trios"
        answer["masked"] = trios_masked
        return answer
        

# need to have a function for each pattern:
# 2orMore3digitgroups 07440359359 done
# 3DigitEnd e.g. 07448778777 TODO
# 3orMore2digitgroups e.g. 07448747478 done
# 4Digit e.g. 07388417777 TODO
# pairs e.g 07405228844 done
# trios e.g. 07123555666 done

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code



                # First idea to solve the issue:
                # Keeping in to see progession of problem solving
                #answer = repeats(number)
                #if bool(answer["pattern"]):
                #    masked = answer["masked"]
                #    # check if digits in repeat are the same e.g. 777
                #    if check(answer["pattern"]):
                #        c = "Same"
                #    else:
                #        c = "Unique"
                #    digit = str(len(answer["pattern"])) + "digit"
                #    pattern = str(answer["repeats"]) + c + digit + "Repeats"
                #    # create list for current number to output to csv
                #    outlist = [number, masked, pattern]
                #    print(outlist)
                #    writer.writerow(outlist)
                #    # continue iterates to next row in reader
                #    continue
                #answer = pairs(number)
                #if bool(answer):
                #    pattern = answer["pattern"]
                #    masked = answer["masked"]
                #    outlist = [number, masked, pattern]
                #    print(outlist)
                #    writer.writerow(outlist)
                #    continue
                #    
                #pattern = "No match!"
                #masked = number
                #outlist = [number, masked, pattern]
                #print(outlist)
                #writer.writerow(outlist)