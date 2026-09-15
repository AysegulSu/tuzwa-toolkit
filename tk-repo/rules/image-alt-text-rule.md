# Media Alt Text — Q16

```
Q16 — Media alt text: (Add alt text / Skip alt text)
```

Ürünün **tüm media'sına** (IMAGE — GIF dahil, VIDEO, EXTERNAL_VIDEO, MODEL_3D) ve
`descriptionHtml` içindeki `<img>` etiketlerine, **ürünün başlığından türetilmiş** alt
text yazılır. Başlıklar kesinleştikten sonra, Phase 1'de offline üretilir, Phase 2'de
push edilir. Q6 başlıkları yeniden yazmıyorsa mevcut başlık kaynaktır.

## Kalıp

Başlığı virgülden bloklara ayır. Blok 1 = ana keyword bloğu.

| Sıra | Alt text |
|---|---|
| 1 | tam başlık (125 karaktere, kelime sınırında kırpılmış) |
| 2–3 | ana blok + farklı bir özellik bloğu |
| 4+ | aynı kalıp dönüşümlü + `– image 4` / `– video 5` / `– 3D model 7` |

Açıklama içi görseller numaralandırmayı media'nın devamından alır.

```
media 1: Rechargeable Table Lamps, Cordless Lamp Dimmable with Aluminium Dome, …
media 2: Rechargeable Table Lamps, Cordless Lamp Dimmable with Aluminium Dome
media 3: Rechargeable Table Lamps, Touch Dimming Bedside Lamp
media 4: Rechargeable Table Lamps, Cordless Lamp Dimmable with Aluminium Dome – image 4
```

## Kurallar

- En fazla 125 karakter.
- Hiçbir media boş kalmaz.
- Benzersiz: ne ürün içinde ne batch içinde iki aynı alt text. İki ürün çakışırsa numara
  eklenmez, ürünün kendi ayırt edici bloğu öne alınır.
- Her run'da hepsi baştan üretilir, üzerine yazılır.
- Marka, fiyat, promosyon, dosya adı, format, "image of" yok. Başlıkta olmayan özellik
  eklenmez.

## Push

```graphql
media(first: 250) { edges { node { id alt mediaContentType } } }
```

```graphql
mutation($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) { userErrors { field message } }
}
```

`fileUpdate` dört media tipinin gid'ini de kabul eder. Batch başına tek çağrı. Açıklama
içi alt'lar `descriptionHtml` ile normal `productUpdate`'te gider.

Push öncesi eski alt değerleri `backup-alt-<batch tag>.md` dosyasına yazılır
(media başına bir satır; hepsi boşsa tek satır not yeter).

## Doğrulama (Phase 4)

Canlıdan çek, Python'da kontrol et, sadece sayıları yazdır: 0 boş, 0 tekrar, en uzun ≤125,
media sayısı ve sırası değişmemiş.
