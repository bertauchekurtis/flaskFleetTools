file = open("Book1.csv")
content = file.readlines()
file.close()
out_file = open("typeData.csv", "w")
out_file.write("Name,Family,Price,Capacity,Max Range,Fuel Burn,Lifespan,Speed,Runway,\n")

for x in (content[i:i + 10] for i in range(0, len(content), 10)):
    string = ""
    for y in x[:-1]:
        m = y.strip("\n")
        string += m + ","
    out_file.write(string + '\n')
    print(string)
out_file.close()



