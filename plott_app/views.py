import sys
import logging
import pandas

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from subprocess import run, PIPE


def index(request):
    return HttpResponse("Helloo!")

def button(request):
    return render(request, 'plot.html')


def filternal(request): # if user enters file
    data = {}
    if "GET" == request.method:
        return render(request, "graphd.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("views.tests"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("views.tests"))

        file_data = csv_file.read().decode("utf-8-sig")
        print(file_data)
        lines = file_data.split("\n")
        lines = [x.replace("\r", "") for x in lines]
        while ("" in lines):
            lines.remove("")

        clmn_names = lines[0].split(",")

        c = len(clmn_names)
        t = [0] * c
        names = lines[0]
        lines.remove(names)
        print(clmn_names)


        g = len(lines)
        data = [[0] * (g) for i in range(c)]

        for i in range(c):
            t[i] = clmn_names[i]


        for i in range(g):
            fields = lines[i].split(",")
            for x in range(c):
                data[x][i] = fields[x]

        return render(request, 'mid.html', {'data0':data[0], 'data00':data[1], 'dataA':t})

        try:
            int(data[1][0])
            return render(request, 'graphd.html', {'data1': t, 'data2': data[0], 'data3': data[1]})
        except:
            return render(request, 'graphd.html', {'data1': t, 'data2': data[1], 'data3': data[0]})

        print(data[0])
        print(data[1])
        cts = request.POST["cars"]
        print(cts)

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return render(request, 'graphd.html', {'data1': t, 'data2': data[0], 'data3': data[1]})


def tests(request):
    data = {}
    if "GET" == request.method:
        return render(request, "graphd.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("views.tests"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("views.tests"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")

        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["name"] = fields[0]
            data_dict["start_date_time"] = fields[1]
            data_dict["end_date_time"] = fields[2]
            data_dict["notes"] = fields[3]
            try:
                form = EventsForm(data_dict)
                if form.is_valid():
                    form.save()
                else:
                    logging.getLogger("error_logger").error(form.errors.as_json())
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("views.tests"))