#Starting presets
Xres = 256
Yres = 256
Xmin = -2.0
Xmax = 0.47
Ymin = -1.12
Ymax = 1.12
colours = 72
renders = 1
frames = 60
def renderImage():
    global renders
    while True:
        try:
            renderName = "render" + str(renders) + ".ppm"
            #Creates ppm image hooray
            with open(renderName, "x") as file:
                imageHeader = "P3\n" + str(Xres) + " " + str(Yres) + "\n255\n"
                file.write(imageHeader)
                val = ""
                #For each pixel...
                for k in range(Yres):
                    for i in range(Xres):
                        x = 0
                        y = 0
                        #image space to mandel space
                        x0 = Xmin+(Xmax-Xmin)*(i/Xres)
                        y0 = Ymin+(Ymax-Ymin)*(k/Yres)
                        #limit at infinity? 256 is a random big number
                        for iteration in range(256):
                            #Sum of absolutes below sqrt5 is also a random big number. Live.
                            if x**2 + y**2 <= 4:
                                x, y = x**2 - y**2 + x0, 2*x*y + y0
                            else:
                                #For with break is faster than while with an increment funnily enough
                                break
                        #areas which took an odd amount of time to exceed 5 are white. modulo patterns? Cool!
                        val = str(int((abs((iteration%colours)-colours/2)/colours)*255)) + " " + str(int((abs(((iteration+85)%colours)-colours/2)/colours)*255)) + " " + str(int((abs(((iteration+171)%colours)-colours/2)/colours)*255)) + "\n"  
                        #WriteOut thanks.
                        file.write(val)
        except FileExistsError:
            renders += 1
        else:
            with open("history.txt", "w") as file:
                metaInfo = renderName + "\n" + str(Xmin) + "<X<" + str(Xmax) + "\n" + str(Ymax) + "<Y<" + str(Ymin) + "\ncolours: " + str(colours) + "\nresolution: " + str(Xres) + "*" + str(Yres) + "\n\n"
                file.writelines(metaInfo)
            break
#def rgb2hsv(r,g,b): will be made later
#main loop
while True:
    userInput = input("Welcome to Python Mandlebrot Explorer CLI. (Z) to render image, (X) to set X bounds, (Y) to set Y bounds, (M) to magnify image, (R) to set resolution, (C) to set number of colours. Anything else to exit.")
    userInput = userInput.casefold()
    if userInput == "x":
        print("Current bounds are:\n", Xmin, "<X<", Xmax, "\n", Ymax, "<Y<", Ymin)
        try:
            valueInput = float(input("X lower bound, NaN to ignore: "))
        except ValueError:
            print("NaN")
        else:
            Xmin = valueInput
        while True:
            try:
                valueInput = float(input("X upper bound, NaN to ignore: "))
            except ValueError:
                print("NaN")
                break
            else:
                if Xmin >= valueInput:
                    print("Input out of range!")
                else:
                    Xmax = valueInput
                    break
    elif userInput == "y":
        print("Current bounds are:\n", Xmin, "<X<", Xmax, "\n", Ymax, "<Y<", Ymin)
        try:
            valueInput = float(input("Y lower bound, NaN to ignore: "))
        except ValueError:
            print("NaN")
        else:
            Ymax = valueInput
        while True:
            try:
                valueInput = float(input("Y upper bound: "))
            except ValueError:
                print("NaN")
                break
            else:
                if Ymax >= valueInput:
                    print("Input out of range!")
                else:
                    Ymin = valueInput
                    break
    elif userInput == "m":
        print("Current bounds are:\n", Xmin, "<X<", Xmax, "\n", Ymax, "<Y<", Ymin)
        while True:
            try:
                zoom = float(input("Magnification multiplier: "))
            except ValueError:
                print("Invalid input!")
            else:
                Xmin = Xmin+((Xmax-Xmin)/2)*(1-0.5**(zoom-1))
                Xmax = Xmax-((Xmax-Xmin)/2)*(1-0.5**(zoom-1))
                Ymin = Ymin+((Ymax-Ymin)/2)*(1-0.5**(zoom-1))
                Ymax = Ymax-((Ymax-Ymin)/2)*(1-0.5**(zoom-1))
                break
    elif userInput == "r":
        print("Current resolution is:\n", Xres, "*", Yres)
        while True:
            try:
                Xres = int(input("X resolution: "))
            except ValueError:
                print("Invalid input!")
            else:
                if Xres < 1:
                    print("Input out of range!")
                else:
                    break
        while True:
            try:
                Yres = int(input("Y resolution: "))
            except ValueError:
                print("Invalid input!")
            else:
                if Yres < 1:
                    print("Input out of range!")
                else:
                    break
    elif userInput == "c":
        print("Current number of colours are:\n", colours)
        while True:
            try:    
                colours = int(input("Number of colours: "))
            except ValueError:
                print("Invalid input!")
            else:
                if colours < 1:
                    print("Input out of range!")
                else:
                    break
    elif userInput == "z":
        valueInput = input("Create Animation (Y/N)? NaN to ignore: ")
        valueInput.casefold()
        if valueInput == "n":
            renderImage()
        elif valueInput == "y":
            while True:
                try:
                    frames = int(input("Render how many frames: "))
                except ValueError:
                    print("Invalid input!")
                else:
                    break
            while True:
                try:
                    zoom = float(input("Magnification multiplier per frame: "))
                except ValueError:
                    print("Invalid input!")
                else:
                    break
            for i in range(frames):
                renderImage()
                Xmin = Xmin+((Xmax-Xmin)/2)*(1-0.5**(zoom-1))
                Xmax = Xmax-((Xmax-Xmin)/2)*(1-0.5**(zoom-1))
                Ymin = Ymin+((Ymax-Ymin)/2)*(1-0.5**(zoom-1))
                Ymax = Ymax-((Ymax-Ymin)/2)*(1-0.5**(zoom-1))
        else:
            print("NaN")
    else:
        print("Goodbye!")
        exit()
