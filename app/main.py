from flask import Flask, flash, redirect, render_template, request, send_from_directory
import os
import csv
from os.path import join, dirname, realpath
from app.helpers import check, mask, repeats, pairs, apology


app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        # input form for file upload
        uploaded_file = request.files['csvfile']
        if uploaded_file.filename == '':
            return apology("Invalid file!", 403)

        if not os.path.isdir('static'):
            os.mkdir('static')
        filepath = os.path.join('static', 'input.csv')
        uploaded_file.save(filepath)

        # need to use a csv file to get inputs
        # iterate through csv file of numbers and for each number check if it is repeat or pair
        outfile = open("app/static/outfile.csv", 'w')
        header = ['number', 'masked_number', 'pattern']
        writer = csv.writer(outfile)
        writer.writerow(header)

        # need to use a csv file to get inputs
        with open("static/input.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                number = str(row)
                # format as phone number (takes it out of the array [])
                number = str(number[2:len(number)-2])
                # iterate through csv file of numbers and for each number check if it is repeat or pair
                # now need to get the output and append this to a new csv file
                # columns will be number, masked, pattern or value
                RepAnswer = repeats(number)
                print(RepAnswer["value"])
                PairAnswer = pairs(number)
                if bool(RepAnswer["pattern"]) and bool(PairAnswer):
                    if RepAnswer["value"] > 1:
                        # return the repanswer
                        masked = RepAnswer["masked"]
                        # check if digits in repeat are the same e.g. 777
                        if check(RepAnswer["pattern"]):
                            c = "Same"
                        else:
                            c = "Unique"
                        digit = str(len(RepAnswer["pattern"])) + "digit"
                        pattern = str(RepAnswer["repeats"]) + c + digit + "Repeats"
                        # create list for current number to output to csv
                        outlist = [number, masked, pattern]
                        print(outlist)
                        writer.writerow(outlist)
                        # continue iterates to next row in reader
                        continue
                    else:
                        pattern = PairAnswer["pattern"]
                        masked = PairAnswer["masked"]
                        outlist = [number, masked, pattern]
                        print(outlist)
                        writer.writerow(outlist)
                        continue

                if bool(RepAnswer["pattern"]):
                    masked = RepAnswer["masked"]
                    # check if digits in repeat are the same e.g. 777
                    if check(RepAnswer["pattern"]):
                        c = "Same"
                    else:
                        c = "Unique"
                    digit = str(len(RepAnswer["pattern"])) + "digit"
                    pattern = str(RepAnswer["repeats"]) + c + digit + "Repeats"
                    # create list for current number to output to csv
                    outlist = [number, masked, pattern]
                    print(outlist)
                    writer.writerow(outlist)
                    # continue iterates to next row in reader
                    continue
                if bool(PairAnswer):
                    pattern = PairAnswer["pattern"]
                    masked = PairAnswer["masked"]
                    outlist = [number, masked, pattern]
                    print(outlist)
                    writer.writerow(outlist)
                    continue

                pattern = "No match!"
                masked = number
                outlist = [number, masked, pattern]
                print(outlist)
                writer.writerow(outlist)

    return render_template("download.html")


@app.route('/static/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    return send_from_directory(directory=uploads, filename=filename)

@app.route("/check", methods=["GET", "POST"])
def checknum():
    if request.method == "GET":
        return render_template("check.html")
    
    if request.method == "POST":
        number = request.form.get("number")

        answer = repeats(number)
        if bool(answer["pattern"]):
            masked = answer["masked"]
            # check if digits in repeat are the same e.g. 777
            if check(answer["pattern"]):
                c = "Same"
            else:
                c = "Unique"
            digit = str(len(answer["pattern"])) + "digit"
            pattern = str(answer["repeats"]) + c + digit + "Repeats"
            # create list for current number to output to csv
            outlist = [number, masked, pattern]
            print(outlist[1])
            return render_template("check.html", number=outlist)

        answer = pairs(number)
        if bool(answer):
            pattern = answer["pattern"]
            masked = answer["masked"]
            outlist = [number, masked, pattern]
            print(outlist[1])
            return render_template("check.html", number=outlist)
            

        pattern = "No match!"
        masked = number
        outlist = [number, masked, pattern]
        print(outlist[1])
        return render_template("check.html", number=outlist)

