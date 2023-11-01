import requests
from bs4 import BeautifulSoup

#f_name = "link.txt"
#f = open(f_name, "r")
#t_str = f.readlines()
#f.close()
t_str = ["https://www.aliexpress.com/"]
t_t = len(t_str)
t_i = 0
f_name = "product.txt"
f = open(f_name, "w")
while t_i < t_t:
    l = t_str[t_i]
    t_i += 1
    #f_name = "all/p-"+str(t_i)+".html"
    f_name = "main.html"
    f1 = open(f_name, "w")
    print("running phase_____ "+str(t_i)+"/"+str(t_t))
    if len(l) < 20:
        continue
    link = l[0:len(l)-1]
    req = requests.get(link)
    fsoup = BeautifulSoup(req.content, "html.parser")
    f1.write(str(fsoup))
    f1.close()
    #https://www.aliexpress.com/item/1005005209142677.html?spm=a2g0o.home.moretolove.1.650c2145xLMHPP&gps-id=pcJustForYou&scm=1007.13562.333647.0&scm_id=1007.13562.333647.0&scm-url=1007.13562.333647.0&pvid=d6ba59ce-ac84-4a03-8762-065f84f540cc&_t=gps-id:pcJustForYou,scm-url:1007.13562.333647.0,pvid:d6ba59ce-ac84-4a03-8762-065f84f540cc,tpp_buckets:668%232846%238110%231995&pdp_npi=4%40dis%21BDT%211744.90%21478.08%21%21%2115.84%21%21%402103200616988700938098778e9fa7%2112000032182654678%21rec%21BD%21%21AB
    soup = fsoup.find_all("a")
    for a in soup:
        if len(a.get("href")) > 52:
            if a.get("href")[0:32] == "https://www.aliexpress.com/item/":
                f.write(a.get("href")[0:53])
                f.write("\n")
f.close()