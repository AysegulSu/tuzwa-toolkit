# KURAL: CTA-üstü benefit yapısı (ürüne özel, metafield tabanlı)

Kuruldu ve canlıda doğrulandı: 2026-09-02. İlk ürün: gid://shopify/Product/15869045899550 (Digital Picture Frame 5 Inch Acrylic).

## BENEFIT DİLİ (kullanıcı kararı 2026-09-02 — EN ÖNEMLİ KURAL)
Benefitler SPEC DEĞİL, müşterinin problemine çözüm sunan CONVERSION odaklı fayda cümleleridir. Ürün özelliği kanıttır, benefit sonuçtur:
- ❌ "40mm drivers, deep bass" → ✓ "Rich sound, all-day comfort"
- ❌ "IP65 weatherproof" → ✓ "Stays outside all year"
- ❌ "500GB capacity" → ✓ "Room for every photo & file"
- ❌ "96 warm white LEDs" → ✓ "Instant cozy evenings"
- ❌ "1200mAh battery" → ✓ "Up to 4 hours cordless"
- ❌ "Sizes XS to 3XL", "7 colors, 5 sizes" → beden/renk varyant bilgisidir, benefit değil (blr-batch12'de 8 satır bu yüzden yeniden yazıldı; diğerleri: "4000mAh rechargeable battery", "1X to 10X magnification", "IPX5 sweat and rain ready", "4 sizes, 6-12mm")
- ✓ İyi örnekler: "No WiFi or app needed", "Wake up with curls", "Never buy ink again", "Stop searching - it beeps", "Fixed in 20 minutes", "Warm without the bulk"
Formül: müşterinin derdi/istediği sonuç + (gerekirse) sayısal kanıt. Yine de açıklamadaki GERÇEK özelliklere dayanmalı, uydurma iddia yok. ~30 karakter altı, İngilizce.

## HANGİ 3 BENEFIT (kullanıcı kararı 2026-09-04, blr-batch12 sonrası)
3 satır yalnızca satın alma kararını belirleyen, müşterinin bir derdini çözen benefit'lere ayrılır — açıklama bullet'ları
için description-format-rule.md §2'deki "Which five benefits" filtresinin aynısı, 3 slot ve ~30 karakterle. Her satır
"şu an yaşadığın dert → artık yok" mantığında; özellik tarifi, ikincil özellik, paket adedi, estetik ve kategori-tanımı
CTA'ya giremez. Açıklama bullet'larındaki en güçlü 3 sorun CTA'ya taşınır. Wedge pillow, aynı fact'ler:
- ❌ `Removable washable cover` / `Stays put, non-slip base` / `Two handy side pockets` (özellik tarifi; cep satın alma nedeni değil)
- ✓ `Reflux won't wake you` / `Quieter nights, less snoring` / `Never slides down the bed`
Safety Notes geçerli (2026-09-21): kaynağın kendi yazdığı sağlık faydası yazılır; kaynakta olmayan uydurulmaz, hastalık tedavi iddiası (heals / treats / cures) yazılmaz.
**Sıra (eklendi 2026-09-06, kullanıcı kararı):** üç satır önem sırasıyla yazılır — müşterinin EN BÜYÜK derdi (satın alma nedeni)
ilk satırda, kalan ikisi azalan sırada. Mobilde çoğu ziyaretçi yalnızca ilk satırı okur; ilk satır zayıfsa blok işe yaramaz.
Test: satırların yerini değiştirince ilk satır güçleniyorsa sıra yanlıştır.

### Gerçek örnekler — blr-batch26 (2026-09-06, kullanıcının canlı kontrolünden sonra eklendi)
Aşağıdaki ❌ satırların hepsi cta_check'ten geçip mağazaya ulaştı ve elle düzeltildi; ortak hata, bir özelliği/adedi saymak ya da
kitleyi tarif etmek — hiçbiri "şu an yaşadığın dert → artık yok" demiyor. ✓ satırlar aynı ürünün aynı kaynak fact'lerinden.
- Red light mask: ❌ `Seven colors, one remote` (adet + aksesuar) → ✓ `Eye pads shield your eyes`
- Water flosser: ❌ `Gentle mode for sensitive gums` (mod tarifi) → ✓ `Gentle on sensitive gums`; ❌ `Up to 3 weeks per charge` tek başına spec okunuyorsa → ✓ `Weeks between charges`
- Electric toothbrush: ❌ `Six modes for every need` (adet) → ✓ `Gentle on sensitive teeth`
- Wall light: ❌ `Works with a remote control` (özellik) → ✓ `Switch on from across the room`
- Owl decoy: ❌ `Looks and sounds like a predator` (ürünün ne yaptığı) → ✓ `Keeps pests out of your garden`
- Plush dog: ❌ `Lifelike fur and details` (estetik) → ✓ `No pet-care hassles`
- Weighted plush / puppy toy: ❌ `Great for any age`, `Great gift for any age` (kitle, dert değil) → ✓ `Comfort that fits in your bag`, `Soft plush you can cuddle`
Test cümlesi: satırı "Artık … yok / … zorunda değilsin" diye okuyabiliyor musun? Okuyamıyorsan özellik tarifidir.
Metin en fazla 30 karakter — cta_check.py ölçer (2026-09-06'dan beri); göz kararı sayılmaz.

### Gerçek örnek — anti-snoring device (2026-09-07, kullanıcının canlı kontrolünden sonra eklendi)
Üç satırın üçü de cta_check'ten, 6c okumasından ve bağımsız CTA reader'dan geçip mağazaya ulaştı. Hiçbiri yasak bir
kalıba çarpmıyor (mAh yok, beden yok, "Adjustable" yok) — kaçmalarının nedeni bu: düz İngilizce özellik cümlesi, regex'in
aradığı hiçbir kelimeyi içermiyor ve reviewer "emin değilim" deyip geçiyor. Ama üçü de spec sayfasında olabilecek
satırlar; horlayan bir müşterinin derdi (kendi uykusu, partnerinin uykusu, maske/kayış rahatsızlığı) hiçbirinde yok.
- ❌ `8 hrs battery per charge` — "per charge" istisnası sonuç cümlesi içindir (`Sleeps 8 hrs on one charge` ✓); sayı + birim +
  battery tek başına spec'tir, "per charge" yazması onu benefit yapmaz.
- ❌ `One-click on and off` — ürünün nasıl çalıştığı; müşterinin derdi değil.
- ❌ `Nose piece detaches to clean` — "detaches / includes / comes with / features / built-in" öznesi ürün olan fiillerdir;
  bunlarla başlayan satır neredeyse her zaman özellik tarifidir.
- ✓ Aynı fact'lerden: `Quiet nights for both of you` / `No mask, no straps, no noise` / `Sleeps 8 hrs on one charge`
  (sıra: partnerin uykusu = en büyük dert → konfor → şarj).
İkinci test (birinciyi tamamlar): "Bu satır ürün kutusunun arkasında ya da spec tablosunda durabilir mi?" Durabiliyorsa
CTA'ya giremez — "Artık … yok" testinden geçse bile.

## GATE (eklendi 2026-09-04, blr-batch21)
Bu bolumun kurali artik scriptle zorunlu: `cta_check.py NN...`, `gate.py`nin son adimi olarak calisir ve
spec dilini FAIL verir — beden/renk varyanti, paket adedi, ham birim (mAh, IPX6, Bluetooth 5.3, 6.6 lb, 50 metres),
"Adjustable X", ciplak nitelik zinciri ("Cordless, battery powered") ve kategori etiketi/disclaimer.
Sonuca bagli sayisal kanit FAIL degildir ("2-7 days per charge", "Up to 60 days per charge") — kural zaten bunu istiyor.
Ikon icin de uyari verir (cordless -> battery, timer -> clock, wifi/app -> wifi, video/music -> media).
Neden eklendi: bu bolum 2026-09-02den beri yaziliydi ama hicbir sey kontrol etmiyordu; gate sadece `icon|metin` ve
34 karakteri dogruluyordu. blr-batch21de 48/50 urunun CTA satiri spec diliyle yazilip canliya cikti ve kullanici yakaladi.
Regresyon testi: 21 bilinen-kotu satirin 21i yakalandi, 17 bilinen-iyi satirda 0 yanlis alarm.

## Q11 — CTA Benefits (backend batch brief'ine ek soru)
**Q11 — CTA benefits: (Write CTA benefits / Skip)**

Brief'te yoksa veya "Skip" ise metafield'a dokunulmaz. "Write CTA benefits" ise kapsamdaki her ürün için:

1. **Phase 1:** Ürün açıklamasından 3 benefit çıkar — yukarıdaki BENEFIT DİLİ kuralıyla, problem-çözüm odaklı. Icon key: `wifi`, `clock`, `battery`, `media`; uymuyorsa `check` (çember içinde tik render olur).
2. **Phase 2:** metafieldsSet ile, 25'lik gruplar, tek mutation. Payload:
   `{ownerId, namespace: "custom", key: "cta_benefits", type: "list.single_line_text_field", value: "[\"wifi|...\", \"check|...\"]"}`
   Sadece userErrors iste. Üzerine yazar (re-run güvenli).
3. **Phase 4:** Spot-check: 3 öğe, `icon_key|Metin` formatı, benefit dili spec değil.
4. Temaya DOKUNULMAZ — blok kurulu, metafield'ı olan üründe otomatik görünür.
5. "Shipping Protection" gibi hizmet/sigorta ürünleri ATLANIR.

## Yapı (kesinleşmiş kullanıcı tercihleri)
- CTA'nın (Add to cart) üstünde, ürüne özel **3 benefit**, **alt alta** (dikey flex), ikonlu.
- Sıralama: fiyat → benefitler → taksit yazısı → Add to cart (script taşıyor).
- Boşluk: 3. benefit ile taksit yazısı arası desktop 18px, mobil 14px. İkon rengi #1a7f4b.
- **Fallback ikon: çizgi stil ÇEMBER + TİK** (`check` ve bilinmeyen tüm key'ler).

## Teknik
- Metafield: `custom.cta_benefits`, tip `list.single_line_text_field`, satır formatı `icon_key|Metin`.
- **Tema (Tuzwa, 2026-09-12 itibarıyla): `Xtra -- NEW`** (MAIN, gid://shopify/OnlineStoreTheme/161796391136).
  Tema okumaları Shopify bağlayıcısı (MCP) üzerinden yapılır: script yolunun kullandığı custom app'in (`Claude Backend`)
  `read_themes` izni yok, `tuzwa.com` da container'dan kapalı (403 CONNECT). **CTA metafield'ını render eden Custom
  Liquid bloğu Tuzwa'nın temasında KURULU ve çalışıyor**: `templates/product.json` içinde blok id
  `custom_liquid_NkVEtn`, tip `custom_liquid`; Liquid'i `product.metafields.custom.cta_benefits.value` okuyor,
  `icon|Metin` satırlarını döngüye alıp `<div class="cta-benefits">` render ediyor ve blok template'in blok sırasında
  yer alıyor. 2026-09-12'de bağlayıcı üzerinden doğrulandı; kullanıcı da vitrinde göründüğünü teyit etti. Yani
  "temaya dokunulmaz, blok kurulu" kuralı Tuzwa'da da geçerli: metafield yazılır, sayfada render olur.
- GEÇMİŞ — önceki mağazanın teması (yalnızca kayıt için), Worfa, 2026-09-10: **Vault** (MAIN,
  gid://shopify/OnlineStoreTheme/174734606372), main-product'ta Custom Liquid bloğu, default product template.
  Metafield boşsa render yok. Kullanıcı Liquid bloğunu Worfa/Vault'a kendisi eklemişti ve canlıda görünüyordu
  (kullanıcı teyidi 2026-09-10).
- GEÇMİŞ — daha önceki mağazaların teması (yalnızca kayıt için): Vepine ve **2026-09-07 öncesi Tuzwa mağazası** (bugünkü
  Tuzwa mağazası değil, farklı bir mağaza) döneminde Xtra || FIXED (MAIN,
  gid://shopify/OnlineStoreTheme/204864586014), blok id custom_liquid_apEFqN.
- MCP canlı temaya yazamaz; blok değişikliklerini kullanıcı tema düzenleyiciden yapıştırır. Bloğun güncel tam kodu bu dosyanın önceki sürümünde ve konuşma geçmişinde mevcut; kritik parçalar: dikey flex CSS, installments-taşıma scripti, çember+tik else-SVG.

## Uygulama durumu
- ddl1-batch1 (49) + test ürünü: yazıldı (eski spec-ağırlıklı dille; conversion diline GÜNCELLENECEK/güncellendi — run log'lara bak)
- ddl1-batch2 (49, Shipping Protection atlandı): yazıldı (aynı not)
- ddl1-batch3 (50): yazıldı (aynı not)
- ddl1-batch4/5: conversion diliyle yazılıyor
- blr-batch11 (**2026-09-07 öncesi Tuzwa mağazası** — bugünkü Tuzwa değil, 50, 2026-09-03): conversion diliyle
  yazıldı, canlıda 50/50 doğrulandı
- **DDL2-Batch1 (Worfa, 50, 2026-09-10): conversion diliyle yazıldı, 50/50 metafield doğrulandı (verify 901 check, 0 failure);
  Worfa/Vault temasında Custom Liquid bloğu kullanıcı tarafından eklenmiş, canlıda render ediliyor (kullanıcı teyidi).**
