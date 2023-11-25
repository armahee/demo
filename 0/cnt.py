f_name = "emails.txt"
f = open(f_name,"r")
lines = f.readlines()
cnt = 0
itr = 0
line = []
pline = []
for i in lines:
    if i not in line:
        line.append(i)
        if itr >= 0:
            cnt += 1
            if itr == 0:
                print("start",i)
    elif itr >= 0:
        # if "info" not in i and "gmail" not in i and "hotmail" not in i and "yahoo" not in i:
        if i not in pline:
            pline.append(i)
            print(itr+2,i)
    itr += 1
print(cnt)