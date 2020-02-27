import requests
import json
from bs4 import BeautifulSoup #HTML sayfasını parse etmek için gereken kütüphane
from time import sleep 

ziraatSikayetURL = "https://sikayetvar.com/ziraat-bankasi?page="
baseURL = "http://sikayetvar.com"
numberOfPages = 3 #Kaç sayfalık şikayet alınacağı burada belirlenir

complaints = {}
totalComplaintCount = 0
for page in range(numberOfPages):
    print(f"Sayfa {page + 1} taranıyor")
    r = requests.post(url=(ziraatSikayetURL + str(page)))
    parsedPage = BeautifulSoup(r.text, "lxml")
    complaintTitles = parsedPage.body.find_all("a", attrs={"class": "complaint-link-for-ads"})
    for i in range(len(complaintTitles)): # sikayetvarUrl'deki yorumlar sadece özet niteliğindedir, yorumların tamamına erişmek için yorumun adresini, complaint-lik-for-ads sınıfına sahip bütün <a> etiketlerinin href özelliğinin değerinden elde ediyoruz.
        
        complaintURL = baseURL + str(complaintTitles[i].attrs["href"]) # Şikayetin bulunduğu 
        r2 = requests.post(complaintURL) # Şikayetin tamamını içeren sayfanın içeriği için request
        parsedCommentPage = BeautifulSoup(r2.text, "lxml") # Bu sayfanın metnini BeautifulSoup nesnesine dönüştürüyoruz

        complainerNameTag = parsedCommentPage.find("span", {"class" : "user"}) # Şikayetçinin adını barındıran html etiketi
        complainerName = complainerNameTag.find("span").get_text() # Şikayetçinin adının bulunduğu etiketin içerisindeki metin elde edilir
        fullComplaintTag = parsedCommentPage.find("div", {"class" : "description"}) # Şikayet yorumunun tamamı içinde bulunduran html etiketi
        fullComplaint = fullComplaintTag.find("p").get_text() # Şikayet metninin tümü

        complaints[complainerName] = fullComplaint
        #print(f"{i+1} numaralı şikayet alındı")
    totalComplaintCount += len(complaintTitles)
    print(f"{page + 1} numaralı sayfadan {len(complaintTitles)} adet yorum alındı")
    print(f"Toplam yorum sayısı {totalComplaintCount} oldu")
    sleep(2) #Bir sayfada bulunan bütün yorumları çektikten sonra bir request sınırına takılmama ümidiyle script 2 saniye boyunca uykuya dalacak
    print("2 saniyeliğine uykuya dalıp sıradaki sayfaya geçilecek")
    print("-----------------------------------------")
print("Bütün sayfalar tamamlandı, dosya yazım işlemine başlandı")

with open("complaints2.json", "w", encoding="utf-8") as jsonFile: # Kullanıcı adları ve şikayetler complaints.json adlı dosyaya yazdırılır.
    #json.dump(complaints, jsonFile, ensure_ascii=False).encode("utf8")
    json.dump(complaints, jsonFile)
    print("Dosya yazım işlemi başarıyla tamamlandı")