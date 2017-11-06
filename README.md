# HGVCT
İNSAN GENOMUNA AİT YENİ NESİL DİZİLEME VERİLERİNİN ANALİZİ İÇİN WEB TABANLI BİYOİNFORMATİK ARAÇ

Bu araç yeni nesil dizileme insan verilerinden varyant çağırma analiz hattı oluşturmak amacıyla geliştirilmiştir. 
Yazılımın aşağıdaki araçlar kullanılarak geliştirilmiştir. Çalıştırabilmek için bu araçların yazılımın çalıştıracağı bilgisayarda kurulu olması gerekmektedir.


Python; versiyon 3.6.3

Django; versiyon 1.10.6

---

BWA; versiyon 0.7.15

Samtools; versiyon 1.4.1

BCFtools; versiyon 1.4.1

Vcfutils.pl

SnpSift; versiyon 4.3

SnpEff; versiyon 4.3

----------------------------------------------
Bunların yanı sıra yazılımın çalışması için analiz hattı sırasında gerekli olan veritabanlarının belirtilen yerlerde olması gerekmektedir.

media/genome >> Hg38 insan genomu (BWA için gerekli)

media/snpEff/data/hg38 >> GRCh38.76 insan genomu (SnpEff için gerekli)

media/snpEff/db/GRCH38/clinvar >> clinvar varyasyon verisi (vcf formatında) (Anotasyon için gerekli)

media/snpEff/db/GRCH38/dbSnp >> dbSNP varyasyon verisi (vcf formatında) (Anotasyon için gerekli)

Bu verilerin nereden elde edileceği ya da nasıl kurulacağı ilgili dizinlerdeki readme.txt dosyaları içerisinde daha detaylı anlatılmıştır.
